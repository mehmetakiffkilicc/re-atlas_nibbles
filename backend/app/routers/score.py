from fastapi import APIRouter, Query
from typing import Literal
from math import radians, sin, cos, sqrt, atan2

from app.services.openmeteo import get_weather_summary
from app.scoring.engine import calculate_score
from app.routers.provinces import get_province_scores

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "contracts"))
from schemas import ScoreResponse, WeatherSummary

router = APIRouter()


import sqlite3
from app.config import DATA_DIR
from math import radians, sin, cos, sqrt, atan2

DB_PATH = DATA_DIR / "grid.db"

def _nearest_province(lat: float, lon: float, energy_type: str):
    """Return (province_name, avg_score) for the nearest province centroid."""
    provinces = get_province_scores(energy_type)
    if not provinces:
        return None, None
    best, best_d = None, float("inf")
    for p in provinces:
        dlat = radians(p.centroid_lat - lat)
        dlon = radians(p.centroid_lon - lon)
        a = sin(dlat / 2) ** 2 + cos(radians(lat)) * cos(radians(p.centroid_lat)) * sin(dlon / 2) ** 2
        d = 2 * atan2(sqrt(a), sqrt(1 - a))
        if d < best_d:
            best_d = d
            best = p
    return (best.province_name, best.score) if best else (None, None)

def _get_score_from_db(lat: float, lon: float, energy_type: str) -> float:
    if not DB_PATH.exists():
        return 50.0
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        col = f"score_{energy_type}"
        cursor.execute(f"SELECT {col} FROM grid_cells ORDER BY (lat - ?)*(lat - ?) + (lon - ?)*(lon - ?) LIMIT 1", (lat, lat, lon, lon))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 50.0
    except Exception:
        return 50.0

@router.get("/score", response_model=ScoreResponse)
def get_score(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    type: Literal["solar", "wind", "hybrid"] = Query(default="hybrid"),
    weights: Literal["investor", "individual"] = Query(default="investor"),
):
    db_score = _get_score_from_db(lat, lon, type)
    
    try:
        weather_dict = get_weather_summary(lat, lon)
        weather = WeatherSummary(**weather_dict)
    except Exception:
        from app.services.openmeteo import _synthetic_summary
        weather_dict = _synthetic_summary(lat)
        weather = WeatherSummary(**weather_dict)

    pname, pavg = _nearest_province(lat, lon, type)
    resp = calculate_score(lat, lon, type, weather, weights, province_name=pname, province_avg_score=pavg)
    resp.score = db_score
    return resp
