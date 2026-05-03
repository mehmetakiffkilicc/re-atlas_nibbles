from fastapi import APIRouter, Query
from typing import Literal
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "contracts"))
from schemas import DistrictScore, WeatherSummary

from app.services.openmeteo import get_weather_summary
from app.scoring.engine import calculate_score
from app.config import DATA_DIR

router = APIRouter()

_districts_geojson: dict | None = None


def _load_districts():
    global _districts_geojson
    if _districts_geojson is not None:
        return
    path = DATA_DIR / "districts.geojson"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            _districts_geojson = json.load(f)
    else:
        _districts_geojson = {"features": []}


def _centroid(geometry: dict) -> tuple[float, float]:
    """Approximate centroid from first polygon ring."""
    try:
        coords_list = geometry.get("coordinates", [])
        if geometry.get("type") == "Polygon":
            ring = coords_list[0]
        elif geometry.get("type") == "MultiPolygon":
            ring = coords_list[0][0]
        else:
            return 39.0, 35.0
        lons = [c[0] for c in ring]
        lats = [c[1] for c in ring]
        return sum(lats) / len(lats), sum(lons) / len(lons)
    except Exception:
        return 39.0, 35.0


@router.get("/districts", response_model=list[DistrictScore])
def list_districts(
    province_id: str = Query(...),
    type: Literal["solar", "wind", "hybrid"] = Query(default="solar"),
):
    _load_districts()
    results = []
    for feat in _districts_geojson.get("features", []):
        props = feat.get("properties", {})
        # Match by province_id prefix or property
        feat_province = str(props.get("province_id", props.get("il_id", "")))
        feat_id = str(props.get("id", props.get("district_id", "")))
        if not feat_province.startswith(province_id) and not feat_id.startswith(province_id):
            continue

        lat, lon = _centroid(feat.get("geometry", {}))
        weather_dict = get_weather_summary(lat, lon)
        weather = WeatherSummary(**weather_dict)
        score_resp = calculate_score(lat, lon, type, weather)

        results.append(DistrictScore(
            district_id=feat_id or f"{province_id}_{len(results)}",
            district_name=props.get("name", props.get("district_name", f"İlçe {len(results)+1}")),
            province_id=province_id,
            score=score_resp.score,
            energy_type=type,
            centroid_lat=round(lat, 5),
            centroid_lon=round(lon, 5),
            geometry=feat.get("geometry"),
        ))

    return results
