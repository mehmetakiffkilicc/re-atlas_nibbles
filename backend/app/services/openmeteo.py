"""Open-Meteo API client with SQLite cache and DEMO_MODE support."""
from __future__ import annotations
import json
import sqlite3
import urllib.request
import urllib.parse
from pathlib import Path

from app.config import DEMO_MODE, CACHE_DIR, DATA_DIR
from app.services.cache import get_cached, set_cached

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

ARCHIVE_PARAMS = {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "hourly": "windspeed_10m,windspeed_80m,shortwave_radiation,direct_normal_irradiance,temperature_2m",
    "timezone": "Europe/Istanbul",
    "wind_speed_unit": "ms",
}

FORECAST_PARAMS = {
    "hourly": "windspeed_10m,windspeed_80m,shortwave_radiation,direct_normal_irradiance,temperature_2m,cloudcover",
    "timezone": "Europe/Istanbul",
    "wind_speed_unit": "ms",
}

_demo_cache: dict | None = None
_weather_db: sqlite3.Connection | None = None


def _load_demo_cache():
    global _demo_cache
    if _demo_cache is not None:
        return
    path = CACHE_DIR / "demo_weather.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            _demo_cache = json.load(f)
    else:
        _demo_cache = {}


def _get_weather_db() -> sqlite3.Connection:
    global _weather_db
    if _weather_db is None:
        db_path = CACHE_DIR / "weather_yearly.sqlite"
        if db_path.exists():
            _weather_db = sqlite3.connect(db_path, check_same_thread=False)
    return _weather_db


def _nearest_demo_key(lat: float, lon: float) -> str | None:
    _load_demo_cache()
    best_key = None
    best_dist = float("inf")
    for key in _demo_cache:
        try:
            klat, klon = map(float, key.split(","))
            d = abs(klat - lat) + abs(klon - lon)
            if d < best_dist:
                best_dist = d
                best_key = key
        except ValueError:
            continue
    return best_key if best_dist < 1.0 else None


def _fetch_url(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read())


def _compute_summary_from_raw(raw: dict) -> dict:
    hourly = raw.get("hourly", {})
    wind_80 = [v for v in hourly.get("windspeed_80m", []) if v is not None]
    ghi = [v for v in hourly.get("shortwave_radiation", []) if v is not None]
    temp = [v for v in hourly.get("temperature_2m", []) if v is not None]
    avg_wind_50m = round(sum(wind_80) / len(wind_80), 2) if wind_80 else 5.0
    # Extrapolate 80m → 100m (power law α=0.143)
    avg_wind_100m = round(avg_wind_50m * (100 / 80) ** 0.143, 2) if avg_wind_50m > 0 else None
    return {
        "avg_wind_speed_50m": avg_wind_50m,
        "avg_wind_speed_100m": avg_wind_100m,
        "ghi_annual_kwh_m2": round(sum(ghi) / 1000.0, 1) if ghi else 1400.0,
        "avg_temperature_c": round(sum(temp) / len(temp), 1) if temp else 13.0,
        "data_year": 2024,
    }


def _synthetic_summary(lat: float) -> dict:
    ghi = max(1100.0, 1950.0 - abs(lat - 36) * 30)
    wind_50m = max(3.0, 6.5 - abs(lat - 38) * 0.1)
    wind_100m = round(wind_50m * (100 / 50) ** 0.143, 2)
    return {
        "avg_wind_speed_50m": round(wind_50m, 2),
        "avg_wind_speed_100m": wind_100m,
        "ghi_annual_kwh_m2": round(ghi, 1),
        "avg_temperature_c": round(max(5.0, 18.0 - abs(lat - 37) * 0.5), 1),
        "data_year": 2024,
    }


def get_weather_summary(lat: float, lon: float):
    """Returns WeatherSummary-compatible dict. Checks SQLite → API → synthetic."""
    from app.config import DEMO_MODE

    cache_key = f"weather:{round(lat, 2)}:{round(lon, 2)}"

    # 1. DEMO_MODE: use pre-fetched demo cache
    if DEMO_MODE:
        _load_demo_cache()
        key = _nearest_demo_key(lat, lon)
        if key and "summary" in _demo_cache[key]:
            return _demo_cache[key]["summary"]
        return _synthetic_summary(lat)

    # 2. Check API response cache
    cached = get_cached(cache_key)
    if cached:
        return cached

    # 3. Check SQLite province weather cache (exact or nearest)
    db = _get_weather_db()
    if db:
        # Try to read avg_wind_speed_100m — may not exist in older schema
        try:
            row = db.execute(
                "SELECT avg_wind_speed_50m, avg_wind_speed_100m, ghi_annual_kwh_m2, avg_temperature_c, data_year "
                "FROM weather_cache ORDER BY ABS(lat-?) + ABS(lon-?) LIMIT 1",
                (lat, lon)
            ).fetchone()
        except sqlite3.OperationalError:
            row = db.execute(
                "SELECT avg_wind_speed_50m, NULL, ghi_annual_kwh_m2, avg_temperature_c, data_year "
                "FROM weather_cache ORDER BY ABS(lat-?) + ABS(lon-?) LIMIT 1",
                (lat, lon)
            ).fetchone()
        if row:
            summary = {
                "avg_wind_speed_50m": row[0],
                "avg_wind_speed_100m": row[1],
                "ghi_annual_kwh_m2": row[2],
                "avg_temperature_c": row[3],
                "data_year": row[4],
            }
            set_cached(cache_key, summary, ttl_seconds=86400)
            return summary

    # 4. Live API call
    try:
        params = ARCHIVE_PARAMS.copy()
        params["latitude"] = lat
        params["longitude"] = lon
        url = ARCHIVE_URL + "?" + urllib.parse.urlencode(params)
        raw = _fetch_url(url)
        summary = _compute_summary_from_raw(raw)
        set_cached(cache_key, summary, ttl_seconds=86400)
        return summary
    except Exception:
        return _synthetic_summary(lat)


def get_forecast_raw(lat: float, lon: float, hours: int = 48) -> dict:
    """Returns raw Open-Meteo forecast JSON."""
    from app.config import DEMO_MODE

    if DEMO_MODE:
        _load_demo_cache()
        key = _nearest_demo_key(lat, lon)
        if key and "raw" in _demo_cache.get(key, {}):
            return _demo_cache[key]["raw"]
        return _build_synthetic_forecast(lat, lon, hours)

    cache_key = f"forecast:{round(lat, 2)}:{round(lon, 2)}:{hours}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        params = FORECAST_PARAMS.copy()
        params["latitude"] = lat
        params["longitude"] = lon
        params["forecast_days"] = max(2, hours // 24 + 1)
        url = FORECAST_URL + "?" + urllib.parse.urlencode(params)
        raw = _fetch_url(url)
        set_cached(cache_key, raw, ttl_seconds=3600)
        return raw
    except Exception:
        return _build_synthetic_forecast(lat, lon, hours)


def _build_synthetic_forecast(lat: float, lon: float, hours: int) -> dict:
    """Deterministic synthetic forecast when API is unavailable."""
    import math
    from datetime import datetime, timedelta

    base = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    times, wind_80, ghi, temp = [], [], [], []

    for h in range(hours):
        t = base + timedelta(hours=h)
        times.append(t.strftime("%Y-%m-%dT%H:%M"))
        hour_of_day = t.hour
        wind = 5.5 + 2.0 * math.sin(math.pi * hour_of_day / 12)
        irr = max(0.0, 700 * math.sin(math.pi * (hour_of_day - 6) / 12)) if 6 <= hour_of_day <= 18 else 0.0
        wind_80.append(round(wind, 1))
        ghi.append(round(irr, 1))
        temp.append(round(14 + 6 * math.sin(math.pi * (hour_of_day - 6) / 12), 1))

    return {
        "hourly": {
            "time": times,
            "windspeed_80m": wind_80,
            "shortwave_radiation": ghi,
            "temperature_2m": temp,
            "cloudcover": [30] * hours,
        }
    }
