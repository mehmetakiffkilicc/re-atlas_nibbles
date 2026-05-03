"""Seismic risk scoring based on distance to fault lines."""
from __future__ import annotations
import json
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2

DATA_DIR = Path(__file__).parent.parent.parent / "data"

NEAR_KM = 5.0
FAR_KM = 25.0
DEFAULT_SCORE = 0.85  # no fault data → assume moderate-low risk

_fault_points: list[tuple[float, float]] | None = None


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def _load_faults():
    global _fault_points
    if _fault_points is not None:
        return
    path = DATA_DIR / "faults.geojson"
    if not path.exists():
        _fault_points = []
        return
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    points = []
    for feat in data.get("features", []):
        geom = feat.get("geometry", {})
        coords = geom.get("coordinates", [])
        if geom.get("type") == "LineString":
            for c in coords:
                points.append((c[1], c[0]))  # (lat, lon)
        elif geom.get("type") == "MultiLineString":
            for line in coords:
                for c in line:
                    points.append((c[1], c[0]))
    _fault_points = points


def _distance_to_nearest_fault(lat: float, lon: float) -> float:
    _load_faults()
    if not _fault_points:
        return 999.0
    best = float("inf")
    for flat, flon in _fault_points:
        d = _haversine_km(lat, lon, flat, flon)
        if d < best:
            best = d
        if best < 0.5:
            break
    return best


def seismic_risk_score(lat: float, lon: float) -> float:
    """Distance to nearest fault → risk score [0,1]. Closer = lower score (higher risk)."""
    dist = _distance_to_nearest_fault(lat, lon)
    if dist >= FAR_KM:
        return 0.9
    if dist <= NEAR_KM:
        return 0.1
    return 0.1 + 0.8 * (dist - NEAR_KM) / (FAR_KM - NEAR_KM)


def combined_risk_score(lat: float, lon: float) -> float:
    return seismic_risk_score(lat, lon)


def invalidate_cache():
    global _fault_points
    _fault_points = None
