"""Grid proximity scoring: nearest substation distance → [0, 1] score."""
from __future__ import annotations
import json
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2

DATA_DIR = Path(__file__).parent.parent.parent / "data"

NEAR_KM = 5.0
FAR_KM = 50.0

_substations: list[dict] | None = None


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def _load_substations():
    global _substations
    if _substations is not None:
        return
    path = DATA_DIR / "substations.geojson"
    if not path.exists():
        _substations = []
        return
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    _substations = []
    for feat in data.get("features", []):
        geom = feat.get("geometry", {})
        props = feat.get("properties", {})
        if geom.get("type") == "Point":
            lon, lat = geom["coordinates"][:2]
            _substations.append({
                "lat": lat, "lon": lon,
                "name": props.get("name"),
                "voltage_kv": props.get("voltage_kv"),
            })


def grid_proximity_score(lat: float, lon: float) -> tuple[float, float, dict | None]:
    """Return (score [0,1], distance_km, nearest_substation_info)."""
    _load_substations()

    if not _substations:
        return 0.3, 30.0, None

    best_dist = float("inf")
    best_sub = None
    for sub in _substations:
        d = _haversine_km(lat, lon, sub["lat"], sub["lon"])
        if d < best_dist:
            best_dist = d
            best_sub = sub

    score = _distance_to_score(best_dist)
    sub_info = {
        "name": best_sub["name"],
        "voltage_kv": best_sub["voltage_kv"],
        "distance_km": round(best_dist, 2),
        "lat": best_sub["lat"],
        "lon": best_sub["lon"],
    } if best_sub else None

    return score, round(best_dist, 2), sub_info


def _distance_to_score(distance_km: float) -> float:
    if distance_km <= NEAR_KM:
        return 1.0
    if distance_km >= FAR_KM:
        return 0.0
    return 1.0 - (distance_km - NEAR_KM) / (FAR_KM - NEAR_KM)


def invalidate_cache():
    global _substations
    _substations = None
