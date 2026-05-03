"""
Generates grid.db with real weather data from weather_yearly.sqlite.

For each ~2.23km grid cell covering Turkey:
  1. Find the nearest province center by Euclidean distance
  2. Use that province's real wind/GHI values (NASA POWER or Open-Meteo)
  3. Add small deterministic noise to create spatial variation within provinces
  4. Scores are resource-only (0-100); other factors are computed per-query by scoring engine
"""
import sqlite3
import math
import random
from pathlib import Path

# Turkey Bounding Box
MIN_LAT, MAX_LAT = 35.8, 42.1
MIN_LON, MAX_LON = 25.6, 44.8

# Step sizes for ~2.23 km cells
STEP_LAT = 0.020
STEP_LON = 0.026

DATA_DIR = Path(__file__).parent.parent / "data"
CACHE_DIR = DATA_DIR / "cache"
DB_PATH = DATA_DIR / "grid.db"
WEATHER_DB_PATH = CACHE_DIR / "weather_yearly.sqlite"

# Normalization ranges calibrated to Turkey's actual NASA POWER values
# ws50 range across 81 provinces: 2.67–7.21 m/s → map to 0-100
# ws100 range across 81 provinces: 2.95–7.96 m/s → map to 0-100
SOLAR_MIN, SOLAR_MAX = 1200.0, 1900.0   # kWh/m²/year
WIND_MIN_100M, WIND_MAX_100M = 3.0, 8.0  # m/s at 100m (Turkey actual range)
WIND_MIN_50M, WIND_MAX_50M = 2.5, 7.5   # m/s at 50m (Turkey actual range)

NOISE_SIGMA = 4.0  # ±4 points spatial variation within a province


def normalize(val: float, lo: float, hi: float) -> float:
    return max(0.0, min(1.0, (val - lo) / (hi - lo)))


def load_province_weather() -> list[dict]:
    """Load all province weather data from SQLite cache."""
    if not WEATHER_DB_PATH.exists():
        raise FileNotFoundError(
            f"weather_yearly.sqlite not found at {WEATHER_DB_PATH}\n"
            "Run: python data-pipeline/scripts/precompute_weather_cache.py"
        )
    conn = sqlite3.connect(WEATHER_DB_PATH)
    try:
        rows = conn.execute(
            "SELECT lat, lon, avg_wind_speed_50m, avg_wind_speed_100m, ghi_annual_kwh_m2, data_source "
            "FROM weather_cache WHERE data_year=2024"
        ).fetchall()
    except sqlite3.OperationalError:
        # Older schema without 100m column
        rows_old = conn.execute(
            "SELECT lat, lon, avg_wind_speed_50m, NULL, ghi_annual_kwh_m2, 'legacy' "
            "FROM weather_cache WHERE data_year=2024"
        ).fetchall()
        rows = rows_old
    conn.close()

    provinces = []
    for lat, lon, ws50, ws100, ghi, source in rows:
        provinces.append({
            "lat": lat,
            "lon": lon,
            "ws50": ws50 or 4.0,
            "ws100": ws100,
            "ghi": ghi or 1400.0,
            "source": source or "unknown",
        })
    print(f"Loaded {len(provinces)} province weather records")
    nasa_count = sum(1 for p in provinces if p["source"] == "nasa_power")
    print(f"  NASA POWER: {nasa_count}  |  Other: {len(provinces) - nasa_count}")
    return provinces


def nearest_province(lat: float, lon: float, provinces: list[dict]) -> dict:
    """Find the nearest province center by Euclidean distance."""
    best = min(provinces, key=lambda p: (p["lat"] - lat) ** 2 + (p["lon"] - lon) ** 2)
    return best


def score_solar(ghi: float, noise: float) -> float:
    """Resource-based solar score (0-100)."""
    raw = normalize(ghi, SOLAR_MIN, SOLAR_MAX) * 100 + noise
    return round(max(10.0, min(98.0, raw)), 1)


def score_wind(ws100: float | None, ws50: float, noise: float) -> float:
    """Resource-based wind score (0-100). Prefer 100m data."""
    if ws100 is not None and ws100 > 0:
        raw = normalize(ws100, WIND_MIN_100M, WIND_MAX_100M) * 100 + noise
    else:
        raw = normalize(ws50, WIND_MIN_50M, WIND_MAX_50M) * 100 + noise
    return round(max(10.0, min(98.0, raw)), 1)


def generate_grid():
    DATA_DIR.mkdir(exist_ok=True)

    provinces = load_province_weather()
    if not provinces:
        raise ValueError("No province weather data found. Run precompute_weather_cache.py first.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS grid_cells")
    cursor.execute("""
        CREATE TABLE grid_cells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            score_solar REAL NOT NULL,
            score_wind REAL NOT NULL,
            score_hybrid REAL NOT NULL
        )
    """)

    random.seed(42)

    print(f"\nGenerating grid cells for Turkey ({MIN_LAT}–{MAX_LAT}°N, {MIN_LON}–{MAX_LON}°E)...")
    print(f"Step: {STEP_LAT}° lat × {STEP_LON}° lon (~2.23 km cells)")

    cells = []
    count = 0
    lat = MIN_LAT

    while lat <= MAX_LAT + 1e-9:
        lon = MIN_LON
        progress = (lat - MIN_LAT) / (MAX_LAT - MIN_LAT) * 100
        if count % 20000 == 0:
            print(f"  {progress:.1f}% — {count:,} cells")

        while lon <= MAX_LON + 1e-9:
            prov = nearest_province(lat, lon, provinces)
            noise = random.gauss(0, NOISE_SIGMA)

            s_solar = score_solar(prov["ghi"], noise)
            s_wind = score_wind(prov["ws100"], prov["ws50"], noise)
            s_hybrid = round(0.55 * s_solar + 0.45 * s_wind, 1)

            cells.append((round(lat, 5), round(lon, 5), s_solar, s_wind, s_hybrid))
            count += 1
            lon += STEP_LON

            if len(cells) >= 10000:
                cursor.executemany(
                    "INSERT INTO grid_cells (lat, lon, score_solar, score_wind, score_hybrid) VALUES (?,?,?,?,?)",
                    cells
                )
                cells = []

        lat += STEP_LAT

    if cells:
        cursor.executemany(
            "INSERT INTO grid_cells (lat, lon, score_solar, score_wind, score_hybrid) VALUES (?,?,?,?,?)",
            cells
        )

    conn.commit()
    print(f"\nCreating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_lat_lon ON grid_cells(lat, lon)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_lat_lon_covering "
        "ON grid_cells(lat, lon, score_solar, score_wind, score_hybrid)"
    )
    conn.commit()

    # Verify
    row_count = cursor.execute("SELECT COUNT(*) FROM grid_cells").fetchone()[0]
    stats = cursor.execute(
        "SELECT "
        "MIN(score_solar), MAX(score_solar), AVG(score_solar), "
        "MIN(score_wind), MAX(score_wind), AVG(score_wind) "
        "FROM grid_cells"
    ).fetchone()
    conn.close()

    print(f"\n{'='*60}")
    print(f"grid.db created: {row_count:,} cells at {DB_PATH}")
    print(f"Solar  — min: {stats[0]:.1f}  max: {stats[1]:.1f}  avg: {stats[2]:.1f}")
    print(f"Wind   — min: {stats[3]:.1f}  max: {stats[4]:.1f}  avg: {stats[5]:.1f}")
    print(f"{'='*60}")
    print("Data source: weather_yearly.sqlite (NASA POWER + Open-Meteo)")


if __name__ == "__main__":
    generate_grid()
