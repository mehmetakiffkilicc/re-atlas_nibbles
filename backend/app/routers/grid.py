"""Grid endpoint: scores a bbox as a grid of cells using SQLite."""
import sqlite3
from typing import Literal
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from app.config import DATA_DIR

router = APIRouter()
DB_PATH = DATA_DIR / "grid.db"

# Must match init_grid_db.py step sizes
MIN_LAT_GRID = 35.8
MIN_LON_GRID = 25.6

_db_conn: sqlite3.Connection | None = None


def _get_conn() -> sqlite3.Connection:
    global _db_conn
    if _db_conn is None and DB_PATH.exists():
        _db_conn = sqlite3.connect(str(DB_PATH), timeout=30, check_same_thread=False)
    return _db_conn


class GridCell(BaseModel):
    lat: float
    lon: float
    score: float
    cell_km: float


class GridResponse(BaseModel):
    cells: list[GridCell]
    cell_km: float
    total: int


@router.get("/grid", response_model=GridResponse)
def get_grid(
    min_lat: float = Query(...),
    min_lon: float = Query(...),
    max_lat: float = Query(...),
    max_lon: float = Query(...),
    cell_km: float = Query(default=2.23),
    type: Literal["solar", "wind", "hybrid"] = Query(default="solar"),
):
    if not DB_PATH.exists():
        return GridResponse(cells=[], cell_km=cell_km, total=0)

    conn = _get_conn()
    if conn is None:
        raise HTTPException(500, "Grid database not available")

    try:
        col = f"score_{type}"

        # Grid native step sizes (must match init_grid_db.py)
        STEP_LAT = 0.020
        STEP_LON = 0.026

        # Estimate cell count in bbox
        bbox_lat = max(STEP_LAT, max_lat - min_lat)
        bbox_lon = max(STEP_LON, max_lon - min_lon)
        n_lat = round(bbox_lat / STEP_LAT)
        n_lon = round(bbox_lon / STEP_LON)
        total_est = n_lat * n_lon

        # Subsample factor: keep at most TARGET cells, uniformly on both axes
        # Smaller target = fewer cells = faster canvas rendering in browser
        zoom_area = (max_lat - min_lat) * (max_lon - min_lon)
        TARGET = 3_000 if zoom_area > 50 else 4_000 if zoom_area > 10 else 5_000
        k = max(1, int((total_est / TARGET) ** 0.5))

        # Subsample by taking every k-th lat band and every k-th lon band.
        # Use ROUND to normalize float coordinates to integer grid indices.
        lat_idx_expr = f"CAST(ROUND((lat - {MIN_LAT_GRID}) / {STEP_LAT}) AS INTEGER)"
        lon_idx_expr = f"CAST(ROUND((lon - {MIN_LON_GRID}) / {STEP_LON}) AS INTEGER)"

        rows = conn.execute(
            f"SELECT lat, lon, {col} as score "
            f"FROM grid_cells "
            f"WHERE lat BETWEEN ? AND ? AND lon BETWEEN ? AND ? "
            f"AND ({lat_idx_expr} % ?) = 0 "
            f"AND ({lon_idx_expr} % ?) = 0",
            (min_lat, max_lat, min_lon, max_lon, k, k),
        ).fetchall()

        cells = [GridCell(lat=r[0], lon=r[1], score=r[2], cell_km=2.23 * k) for r in rows]
        return GridResponse(cells=cells, cell_km=2.23 * k, total=len(cells))

    except Exception as e:
        print(f"Grid DB Error: {e}")
        raise HTTPException(500, f"Database error: {e}")
