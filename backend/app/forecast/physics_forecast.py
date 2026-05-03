"""Physics-based 48-hour production forecast using Open-Meteo data."""
from __future__ import annotations
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "contracts"))
from schemas import ForecastPoint, ForecastResponse

from app.scoring.physics import wind_power_kw, solar_power_kw
from app.services.openmeteo import get_forecast_raw
from app.forecast.maintenance_window import find_maintenance_window

UNCERTAINTY_BAND = 0.15  # ±15%


def generate_forecast(
    lat: float,
    lon: float,
    hours: int = 48,
    energy_type: str = "hybrid",
) -> ForecastResponse:
    raw = get_forecast_raw(lat, lon, hours)
    hourly = raw.get("hourly", {})

    times = hourly.get("time", [])
    wind_speeds = hourly.get("windspeed_80m", [])
    ghi_values = hourly.get("shortwave_radiation", [])

    # Pad or truncate to requested hours
    n = min(hours, len(times))
    points: list[ForecastPoint] = []

    base = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

    for i in range(n):
        wind_ms = wind_speeds[i] if i < len(wind_speeds) and wind_speeds[i] is not None else 5.0
        ghi_wm2 = ghi_values[i] if i < len(ghi_values) and ghi_values[i] is not None else 0.0

        if energy_type == "wind":
            expected = wind_power_kw(wind_ms)
        elif energy_type == "solar":
            expected = solar_power_kw(ghi_wm2)
        else:  # hybrid
            expected = wind_power_kw(wind_ms) + solar_power_kw(ghi_wm2)

        lower = round(expected * (1 - UNCERTAINTY_BAND), 1)
        upper = round(expected * (1 + UNCERTAINTY_BAND), 1)

        timestamp = (base + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        if i < len(times):
            try:
                timestamp = datetime.strptime(times[i], "%Y-%m-%dT%H:%M").strftime("%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                pass

        points.append(ForecastPoint(
            timestamp=timestamp,
            expected_kw=round(expected, 1),
            lower_kw=lower,
            upper_kw=upper,
            wind_speed_ms=round(wind_ms, 1),
            ghi_w_m2=round(ghi_wm2, 1),
        ))

    maintenance = find_maintenance_window(points)

    return ForecastResponse(
        lat=lat,
        lon=lon,
        energy_type=energy_type,
        points=points,
        maintenance_window=maintenance,
    )
