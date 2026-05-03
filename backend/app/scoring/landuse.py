"""Landuse score lookup with grid-based spatial index for fast nearest-neighbor search."""
from __future__ import annotations
import json
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent.parent / "data"

LANDUSE_SCORES: dict[str, float] = {
    "forest": 0.0,
    "nature_reserve": 0.0,
    "protected_area": 0.0,
    "military": 0.1,
    "residential": 0.1,
    "commercial": 0.2,
    "retail": 0.2,
    "cemetery": 0.2,
    "farmland": 0.3,
    "orchard": 0.3,
    "vineyard": 0.3,
    "allotments": 0.4,
    "grass": 0.6,
    "village_green": 0.6,
    "meadow": 0.7,
    "greenfield": 0.7,
    "construction": 0.5,
    "brownfield": 0.6,
    "industrial": 0.8,
    "quarry": 0.7,
    "landfill": 0.6,
    "barren": 1.0,
    "unknown": 0.5,
}

# Grid cell size in degrees (~5.5 km at Turkey's latitude)
GRID_RES = 0.05

_grid: dict[tuple[int, int], list[tuple[float, float, float, str]]] | None = None  # cell → [(lat, lon, score, type)]
_loaded = False


def _cell(lat: float, lon: float) -> tuple[int, int]:
    return (int(lat / GRID_RES), int(lon / GRID_RES))


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def _load_landuse():
    global _grid, _loaded
    if _loaded:
        return
    _loaded = True

    path = DATA_DIR / "landuse.geojson"
    if not path.exists():
        _grid = {}
        return

    print(f"Loading landuse index from {path} ({path.stat().st_size // 1024 // 1024} MB)...")
    grid: dict[tuple[int, int], list] = defaultdict(list)

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    for feat in data.get("features", []):
        geom = feat.get("geometry", {})
        props = feat.get("properties", {})
        if geom.get("type") == "Point":
            lon, lat = geom["coordinates"][:2]
            lt = props.get("landuse_type", "unknown")
            score = props.get("score", LANDUSE_SCORES.get(lt, 0.5))
            grid[_cell(lat, lon)].append((lat, lon, score, lt))

    _grid = dict(grid)
    total = sum(len(v) for v in _grid.values())
    print(f"Landuse index ready: {total:,} points in {len(_grid):,} cells")


def landuse_score(lat: float, lon: float) -> tuple[float, str]:
    """Find nearest landuse point using grid index. Returns (score, landuse_type)."""
    _load_landuse()

    if not _grid:
        return 0.5, "unknown"

    # Try shapely STRtree first for maximum accuracy
    try:
        return _landuse_score_shapely(lat, lon)
    except Exception:
        pass

    # Grid-based search: expand radius until we find candidates
    ci, cj = _cell(lat, lon)
    best_dist = float("inf")
    best_score, best_type = 0.5, "unknown"

    for radius in range(0, 5):
        candidates_found = 0
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                if abs(di) != radius and abs(dj) != radius:
                    continue  # only the ring at this radius
                cell_pts = _grid.get((ci + di, cj + dj), [])
                for plat, plon, pscore, ptype in cell_pts:
                    d = _haversine_km(lat, lon, plat, plon)
                    if d < best_dist:
                        best_dist = d
                        best_score = pscore
                        best_type = ptype
                    candidates_found += 1

        # If we found candidates and have a good match, stop expanding
        if candidates_found > 0 and best_dist < (radius + 1) * GRID_RES * 111:
            break

    return best_score, best_type


def _landuse_score_shapely(lat: float, lon: float) -> tuple[float, str]:
    from shapely.geometry import Point
    from shapely.strtree import STRtree

    if not hasattr(_landuse_score_shapely, "_tree"):
        all_pts = []
        for cell_pts in _grid.values():
            all_pts.extend(cell_pts)
        pts_geom = [Point(p[1], p[0]) for p in all_pts]  # (lon, lat)
        _landuse_score_shapely._tree = STRtree(pts_geom)
        _landuse_score_shapely._data = all_pts

    query_pt = Point(lon, lat)
    nearest_idx = _landuse_score_shapely._tree.nearest(query_pt)
    p = _landuse_score_shapely._data[nearest_idx]
    return p[2], p[3]


def invalidate_cache():
    global _grid, _loaded
    _grid = None
    _loaded = False
    if hasattr(_landuse_score_shapely, "_tree"):
        del _landuse_score_shapely._tree
        del _landuse_score_shapely._data
