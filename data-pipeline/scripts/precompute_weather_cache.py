"""
Precomputes annual weather data for all 81 Turkish provinces.
Data sources (priority order):
  1. NASA POWER API — WS50M, WS100M, ALLSKY_SFC_SW_DWN (climatology, most accurate)
  2. Open-Meteo Archive API — fallback for wind/solar
  3. Synthetic physics-based estimate — last resort

Stores in SQLite cache. Also generates demo_weather.json for offline demo mode.
"""
import json
import sqlite3
import time
import urllib.request
import urllib.parse
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent.parent
STATIC_DIR = Path(__file__).parent.parent / "static"
CACHE_DIR = ROOT / "backend" / "data" / "cache"

# Open-Meteo Archive
OPENMETEO_URL = "https://archive-api.open-meteo.com/v1/archive"
OPENMETEO_PARAMS = {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "hourly": "windspeed_10m,windspeed_80m,shortwave_radiation,temperature_2m",
    "timezone": "Europe/Istanbul",
    "wind_speed_unit": "ms",
    "models": "best_match",
}

# NASA POWER Climatology (20-year avg, 2001-2020 — more stable than single year)
# Supported parameters: WS2M, WS10M, WS50M, ALLSKY_SFC_SW_DWN
# WS80M/WS100M not available — extrapolate from WS50M with power law
# Note: 'header' param is NOT supported — omit it to avoid 422 errors
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"
NASA_POWER_PARAMS = {
    "parameters": "WS50M,ALLSKY_SFC_SW_DWN",
    "community": "RE",
    "longitude": None,  # filled per request
    "latitude": None,   # filled per request
    "format": "JSON",
}

DEMO_COORDS = [
    (40.213, 28.366, "Karacabey"),
    (38.733, 35.485, "Kayseri"),
    (38.737, 33.371, "Tuz Gölü"),
    (41.218, 28.450, "Çatalca"),
    (40.984, 28.725, "Çamlıca"),
]

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS weather_cache (
    province_id TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    avg_wind_speed_50m REAL,
    avg_wind_speed_100m REAL,
    ghi_annual_kwh_m2 REAL,
    avg_temperature_c REAL,
    data_year INTEGER,
    data_source TEXT,
    fetched_at TEXT,
    PRIMARY KEY (province_id, data_year)
)
"""

MIGRATE_ADD_COLS = [
    "ALTER TABLE weather_cache ADD COLUMN avg_wind_speed_100m REAL",
    "ALTER TABLE weather_cache ADD COLUMN data_source TEXT",
]


def _migrate_table(conn: sqlite3.Connection):
    """Add new columns to existing table without data loss."""
    existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(weather_cache)")}
    for sql in MIGRATE_ADD_COLS:
        col = sql.split("ADD COLUMN ")[1].split()[0]
        if col not in existing_cols:
            try:
                conn.execute(sql)
                conn.commit()
                print(f"  Migrated: added column {col}")
            except Exception as e:
                print(f"  Migration skip ({col}): {e}")


def fetch_nasa_power(lat: float, lon: float) -> dict | None:
    """Fetch climatology from NASA POWER API."""
    params = NASA_POWER_PARAMS.copy()
    params["latitude"] = round(lat, 4)
    params["longitude"] = round(lon, 4)
    url = NASA_POWER_URL + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "RE-Atlas/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        # Extract annual mean from monthly climatology
        props = data.get("properties", {}).get("parameter", {})
        ws50 = props.get("WS50M", {})
        ghi = props.get("ALLSKY_SFC_SW_DWN", {})

        # NASA POWER uses "ANN" key for annual value — use it directly
        ws50_val = ws50.get("ANN")
        if ws50_val is None or ws50_val <= 0:
            return None

        # Extrapolate 50m -> 100m using power law (α=0.143, roughness class 2)
        ws100_val = round(ws50_val * (100 / 50) ** 0.143, 3)

        # NASA POWER GHI is kWh/m²/day per month — convert to annual kWh/m²
        days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_keys = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                      "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        ghi_annual = 0.0
        for m, days in zip(month_keys, days_per_month):
            v = ghi.get(m)
            if v is not None and v > 0:
                ghi_annual += v * days
        ghi_val = round(ghi_annual, 1) if ghi_annual > 0 else None

        return {
            "avg_wind_speed_50m": round(ws50_val, 3),
            "avg_wind_speed_100m": ws100_val,
            "ghi_annual_kwh_m2": ghi_val,
            "source": "nasa_power",
        }
    except Exception as e:
        print(f"    NASA POWER error: {e}")
        return None


def fetch_openmeteo(lat: float, lon: float) -> dict | None:
    """Fetch 2024 archive from Open-Meteo API."""
    params = OPENMETEO_PARAMS.copy()
    params["latitude"] = lat
    params["longitude"] = lon
    url = OPENMETEO_URL + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"    Open-Meteo error: {e}")
        return None


def compute_openmeteo_summary(data: dict) -> dict:
    hourly = data.get("hourly", {})
    wind_80 = [v for v in hourly.get("windspeed_80m", []) if v is not None]
    wind_10 = [v for v in hourly.get("windspeed_10m", []) if v is not None]
    ghi_vals = [v for v in hourly.get("shortwave_radiation", []) if v is not None]
    temp_vals = [v for v in hourly.get("temperature_2m", []) if v is not None]

    if wind_80 and sum(wind_80) > 0:
        avg_wind_50m = round(sum(wind_80) / len(wind_80), 2)
    elif wind_10:
        avg_wind_50m = round((sum(wind_10) / len(wind_10)) * (80 / 10) ** 0.143, 2)
    else:
        avg_wind_50m = 0.0

    # Extrapolate 80m -> 100m with power law (α=0.143)
    avg_wind_100m = round(avg_wind_50m * (100 / 80) ** 0.143, 2) if avg_wind_50m > 0 else None

    ghi_annual = round(sum(ghi_vals) / 1000.0, 1) if ghi_vals else 0.0
    avg_temp = round(sum(temp_vals) / len(temp_vals), 1) if temp_vals else 12.0

    return {
        "avg_wind_speed_50m": avg_wind_50m,
        "avg_wind_speed_100m": avg_wind_100m,
        "ghi_annual_kwh_m2": ghi_annual,
        "avg_temperature_c": avg_temp,
        "source": "open_meteo",
    }


def _synthetic_summary(lat: float) -> dict:
    """Physics-based estimates when all APIs are unavailable."""
    ghi = max(1100, 1950 - abs(lat - 36) * 30)
    wind_50m = max(3.0, 6.5 - abs(lat - 38) * 0.1)
    wind_100m = round(wind_50m * (100 / 50) ** 0.143, 2)
    temp = max(5.0, 18.0 - abs(lat - 37) * 0.5)
    return {
        "avg_wind_speed_50m": round(wind_50m, 2),
        "avg_wind_speed_100m": wind_100m,
        "ghi_annual_kwh_m2": round(ghi, 1),
        "avg_temperature_c": round(temp, 1),
        "source": "synthetic",
    }


def _get_summary(lat: float, lon: float, name: str) -> dict:
    """Try NASA POWER first, fallback to Open-Meteo, then synthetic."""
    print(f"    Trying NASA POWER...", end=" ", flush=True)
    nasa = fetch_nasa_power(lat, lon)
    if nasa and nasa.get("avg_wind_speed_50m") is not None:
        # NASA POWER doesn't include temperature — get from Open-Meteo or use synthetic
        temp = 12.0
        try:
            om = fetch_openmeteo(lat, lon)
            if om:
                om_summary = compute_openmeteo_summary(om)
                temp = om_summary.get("avg_temperature_c", 12.0)
                # If NASA GHI failed, use Open-Meteo GHI
                if not nasa.get("ghi_annual_kwh_m2"):
                    nasa["ghi_annual_kwh_m2"] = om_summary.get("ghi_annual_kwh_m2", 0.0)
        except Exception:
            pass
        print(f"OK (NASA POWER + Open-Meteo temp)")
        return {
            "avg_wind_speed_50m": nasa["avg_wind_speed_50m"],
            "avg_wind_speed_100m": nasa.get("avg_wind_speed_100m"),
            "ghi_annual_kwh_m2": nasa.get("ghi_annual_kwh_m2", 0.0),
            "avg_temperature_c": temp,
            "source": "nasa_power",
        }

    print(f"failed -> Open-Meteo...", end=" ", flush=True)
    time.sleep(0.5)
    om = fetch_openmeteo(lat, lon)
    if om:
        print(f"OK (Open-Meteo)")
        return compute_openmeteo_summary(om)

    print(f"failed -> synthetic fallback")
    return _synthetic_summary(lat)


def main(force_refresh: bool = False, extra_coords: list | None = None):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    db_path = CACHE_DIR / "weather_yearly.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()
    _migrate_table(conn)

    with open(STATIC_DIR / "province_centers.json", encoding="utf-8") as f:
        provinces = json.load(f)

    demo_data = {}

    print(f"\n{'='*60}")
    print(f"Processing {len(provinces)} provinces...")
    print(f"Data sources: NASA POWER (priority) -> Open-Meteo -> Synthetic")
    print(f"{'='*60}\n")

    for p in provinces:
        pid = p["id"]
        name = p["name"]
        lat, lon = p["lat"], p["lon"]

        if not force_refresh:
            row = conn.execute(
                "SELECT avg_wind_speed_100m FROM weather_cache WHERE province_id=? AND data_year=2024",
                (pid,)
            ).fetchone()
            if row is not None and row[0] is not None:
                print(f"  [{pid}] {name} — already cached (100m wind: {row[0]} m/s), skipping")
                continue
            elif row is not None:
                print(f"  [{pid}] {name} — cached but missing 100m wind, refreshing...")
            else:
                print(f"  [{pid}] {name} ({lat}, {lon})...")

        summary = _get_summary(lat, lon, name)

        conn.execute(
            """INSERT OR REPLACE INTO weather_cache
               (province_id, lat, lon, avg_wind_speed_50m, avg_wind_speed_100m,
                ghi_annual_kwh_m2, avg_temperature_c, data_year, data_source, fetched_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (pid, lat, lon,
             summary["avg_wind_speed_50m"], summary.get("avg_wind_speed_100m"),
             summary["ghi_annual_kwh_m2"], summary.get("avg_temperature_c", 12.0),
             2024, summary.get("source", "unknown"),
             datetime.utcnow().isoformat())
        )
        conn.commit()
        print(f"    wind_50m={summary['avg_wind_speed_50m']} m/s  "
              f"wind_100m={summary.get('avg_wind_speed_100m')} m/s  "
              f"GHI={summary['ghi_annual_kwh_m2']} kWh/m²  "
              f"[{summary.get('source', '?')}]")
        time.sleep(1.2)  # respectful rate limiting

    # Demo coordinates
    all_demo_coords = list(DEMO_COORDS)
    if extra_coords:
        for coord_str in extra_coords:
            lat_str, lon_str = coord_str.split(",")
            all_demo_coords.append((float(lat_str), float(lon_str), "custom"))

    print(f"\n{'='*60}")
    print("Processing demo coordinates...")
    for lat, lon, label in all_demo_coords:
        key = f"{round(lat, 3)},{round(lon, 3)}"
        print(f"  Demo: {label} ({key})...")
        summary = _get_summary(lat, lon, label)
        demo_data[key] = {"summary": summary}
        time.sleep(1.2)

    demo_path = CACHE_DIR / "demo_weather.json"
    with open(demo_path, "w", encoding="utf-8") as f:
        json.dump(demo_data, f, ensure_ascii=False, indent=2)
    print(f"\nDemo weather cache saved to {demo_path}")

    row_count = conn.execute("SELECT COUNT(*) FROM weather_cache").fetchone()[0]
    nasa_count = conn.execute(
        "SELECT COUNT(*) FROM weather_cache WHERE data_source='nasa_power'"
    ).fetchone()[0]
    print(f"\nSQLite cache: {row_count} rows total ({nasa_count} from NASA POWER) in {db_path}")
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Precompute weather cache for RE-Atlas")
    parser.add_argument("--coords", nargs="*", help="Extra lat,lon pairs e.g. 40.213,28.366")
    parser.add_argument("--force", action="store_true", help="Force re-fetch all provinces")
    args = parser.parse_args()
    main(force_refresh=args.force, extra_coords=args.coords)
