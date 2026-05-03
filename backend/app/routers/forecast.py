from fastapi import APIRouter, Query
from typing import Literal

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "contracts"))
from schemas import ForecastResponse, ForecastPoint

router = APIRouter()


@router.get("/forecast", response_model=ForecastResponse)
def get_forecast(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    type: Literal["solar", "wind", "hybrid"] = Query(default="hybrid"),
    hours: int = Query(default=48, ge=1, le=168),
):
    # Try the real ForecastSage implementation
    try:
        from app.forecast.physics_forecast import generate_forecast
        return generate_forecast(lat, lon, hours, type)
    except ImportError:
        pass
    except Exception:
        pass

    # Stub: synthetic forecast until ForecastSage delivers
    return _stub_forecast(lat, lon, type, hours)


def _stub_forecast(lat: float, lon: float, energy_type: str, hours: int) -> ForecastResponse:
    import math
    from datetime import datetime, timedelta

    base = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    points = []
    for h in range(hours):
        t = base + timedelta(hours=h)
        hour_of_day = t.hour
        if energy_type == "wind":
            expected = max(0.0, 400 + 200 * math.sin(math.pi * hour_of_day / 12))
        elif energy_type == "solar":
            expected = max(0.0, 600 * math.sin(math.pi * (hour_of_day - 6) / 12)) if 6 <= hour_of_day <= 18 else 0.0
        else:
            wind_part = max(0.0, 200 + 100 * math.sin(math.pi * hour_of_day / 12))
            solar_part = max(0.0, 300 * math.sin(math.pi * (hour_of_day - 6) / 12)) if 6 <= hour_of_day <= 18 else 0.0
            expected = wind_part + solar_part

        points.append(ForecastPoint(
            timestamp=t.strftime("%Y-%m-%dT%H:%M:%SZ"),
            expected_kw=round(expected, 1),
            lower_kw=round(expected * 0.85, 1),
            upper_kw=round(expected * 1.15, 1),
        ))

    return ForecastResponse(lat=lat, lon=lon, energy_type=energy_type, points=points)
