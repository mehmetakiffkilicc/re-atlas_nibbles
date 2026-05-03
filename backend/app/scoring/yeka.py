"""YEKA zone bonus scoring."""
from __future__ import annotations
import json
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2

STATIC_DIR = Path(__file__).parent.parent.parent.parent / "data-pipeline" / "static"

INNER_BONUS = 0.10
OUTER_BONUS = 0.05
OUTER_RADIUS_KM = 20.0

_yeka_zones: list[dict] | None = None


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def _load_yeka():
    global _yeka_zones
    if _yeka_zones is not None:
        return
    path = STATIC_DIR / "yeka_zones.json"
    if not path.exists():
        _yeka_zones = []
        return
    with open(path, encoding="utf-8") as f:
        _yeka_zones = json.load(f)


def yeka_bonus(lat: float, lon: float) -> tuple[float, dict | None]:
    """Return (bonus_score, zone_info) for nearest YEKA zone."""
    _load_yeka()
    if not _yeka_zones:
        return 0.0, None

    best_dist = float("inf")
    best_zone = None
    for zone in _yeka_zones:
        d = _haversine_km(lat, lon, zone["lat"], zone["lon"])
        if d < best_dist:
            best_dist = d
            best_zone = zone

    if best_zone is None:
        return 0.0, None

    zone_info = {
        "name": best_zone["name"],
        "radius_km": best_zone["radius_km"],
        "lat": best_zone["lat"],
        "lon": best_zone["lon"],
        "distance_km": round(best_dist, 2),
        "bonus": 0.0,
    }

    if best_dist <= best_zone["radius_km"]:
        zone_info["bonus"] = INNER_BONUS
        return INNER_BONUS, zone_info
    elif best_dist <= best_zone["radius_km"] + OUTER_RADIUS_KM:
        zone_info["bonus"] = OUTER_BONUS
        return OUTER_BONUS, zone_info

    return 0.0, None


def invalidate_cache():
    global _yeka_zones
    _yeka_zones = None
