"""High-resolution grid endpoint: fetches real-time Open-Meteo data for zoomed-in views."""
import asyncio
import time
from typing import Literal
import httpx
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from app.scoring.physics import wind_resource_score, solar_resource_score, hybrid_resource_score

router = APIRouter()

# Simple TTL cache keyed by (bbox_rounded, zoom, type)
_cache: dict[tuple, tuple[float, list]] = {}  # key → (timestamp, cells)
_CACHE_TTL = 600  # 10 minutes


def _cache_key(min_lat: float, min_lon: float, max_lat: float, max_lon: float,
               zoom: int, type: str) -> tuple:
    # Round bbox to 2 decimal places for cache grouping (~1km grid)
    return (round(min_lat, 2), round(min_lon, 2), round(max_lat, 2), round(max_lon, 2), zoom, type)


def _cache_get(key: tuple) -> list | None:
    if key in _cache:
        ts, data = _cache[key]
        if time.time() - ts < _CACHE_TTL:
            return data
        del _cache[key]
    return None


def _cache_set(key: tuple, data: list) -> None:
    _cache[key] = (time.time(), data)

# Grid spacing by zoom level (degrees)
_SPACING: list[tuple[int, float]] = [
    (14, 0.010),   # ~1.1 km
    (12, 0.020),   # ~2.2 km
    (10, 0.040),   # ~4.4 km
    (8,  0.080),   # ~8.9 km
]

# Open-Meteo forecast endpoint — supports comma-separated lat/lon for batch
_OM_URL = "https://api.open-meteo.com/v1/forecast"
_BATCH_SIZE = 50    # conservative max per request to avoid Open-Meteo timeouts

# Calibrated to Turkey's real NASA POWER values (same as grid.db normalization)
WIND_MIN, WIND_MAX = 3.0, 8.0      # m/s at 100m hub height
SOLAR_MIN, SOLAR_MAX = 1200, 1900  # kWh/m²/year


def _spacing_for_zoom(zoom: int) -> float:
    for min_zoom, spacing in _SPACING:
        if zoom >= min_zoom:
            return spacing
    return 0.10


def _wind_score_100m(ws10: float) -> float:
    """10m wind → 100m hub via power law → normalized 0-100."""
    ws100 = ws10 * (100 / 10) ** 0.143
    # Use Turkey-calibrated range instead of global physics.py thresholds
    raw = max(0.0, min(1.0, (ws100 - WIND_MIN) / (WIND_MAX - WIND_MIN)))
    return round(raw * 100, 1)


def _solar_score_instant(ghi_w_m2: float) -> float:
    """Instantaneous GHI (W/m²) → annual proxy → normalized 0-100.

    Conversion: assume 5 peak sun hours/day average for Turkey.
    annual_kWh_m2 ≈ ghi_W_m2 * 5h * 365d / 1000
    """
    annual = ghi_w_m2 * 5 * 365 / 1000
    raw = max(0.0, min(1.0, (annual - SOLAR_MIN) / (SOLAR_MAX - SOLAR_MIN)))
    return round(raw * 100, 1)


async def _fetch_batch(lats: list[float], lons: list[float], variables: str) -> list[dict]:
    """Fetch one batch from Open-Meteo with retry on 429/5xx."""
    params = {
        "latitude":  ",".join(f"{v:.4f}" for v in lats),
        "longitude": ",".join(f"{v:.4f}" for v in lons),
        "current":   variables,
        "timezone":  "Europe/Istanbul",
    }
    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(_OM_URL, params=params)
                if resp.status_code == 429:
                    await asyncio.sleep(1.0 * (attempt + 1))
                    continue
                resp.raise_for_status()
                data = resp.json()
                # Single point returns dict; multiple points returns list
                if isinstance(data, dict):
                    return [data]
                return data
        except httpx.TimeoutException:
            await asyncio.sleep(0.5 * (attempt + 1))
    raise RuntimeError("Open-Meteo request failed after 3 attempts")


class HiResCell(BaseModel):
    lat: float
    lon: float
    score: float
    cell_km: float


class HiResResponse(BaseModel):
    cells: list[HiResCell]
    cell_km: float
    total: int


@router.get("/grid/hires", response_model=HiResResponse)
async def get_hires_grid(
    min_lat: float = Query(...),
    min_lon: float = Query(...),
    max_lat: float = Query(...),
    max_lon: float = Query(...),
    zoom: int = Query(..., ge=8),
    type: Literal["solar", "wind", "hybrid"] = Query(default="solar"),
):
    # Check cache first
    ck = _cache_key(min_lat, min_lon, max_lat, max_lon, zoom, type)
    cached = _cache_get(ck)
    if cached is not None:
        km = cached[0].cell_km if cached else 4.4
        return HiResResponse(cells=cached, cell_km=km, total=len(cached))

    bbox_area = (max_lat - min_lat) * (max_lon - min_lon)
    if bbox_area > 40.0:
        raise HTTPException(400, "Bbox too large for high-res mode. Zoom in first.")

    spacing = _spacing_for_zoom(zoom)
    cell_km = round(spacing * 111, 1)

    # Generate sample grid points
    points: list[tuple[float, float]] = []
    lat = min_lat
    while lat <= max_lat + 1e-9:
        lon = min_lon
        while lon <= max_lon + 1e-9:
            points.append((round(lat, 5), round(lon, 5)))
            lon += spacing
        lat += spacing

    # Cap points — auto-increase spacing instead of rejecting
    if len(points) > 400:
        # Subsample to at most 400 by increasing spacing multiplier
        factor = max(2, int((len(points) / 400) ** 0.5))
        points = [p for i, p in enumerate(points)
                  if (round((p[0] - min_lat) / spacing) % factor == 0
                      and round((p[1] - min_lon) / spacing) % factor == 0)]

    # Select Open-Meteo variables based on energy type
    if type == "solar":
        variables = "shortwave_radiation"
    elif type == "wind":
        variables = "wind_speed_10m"
    else:
        variables = "wind_speed_10m,shortwave_radiation"

    # Sequential batch fetch — avoids Open-Meteo rate limits from parallel requests
    all_results: list[dict] = []
    batches = [points[i:i + _BATCH_SIZE] for i in range(0, len(points), _BATCH_SIZE)]
    try:
        for batch in batches:
            results = await _fetch_batch(
                [p[0] for p in batch],
                [p[1] for p in batch],
                variables,
            )
            all_results.extend(results)
            # Small delay between batches to respect rate limits
            if len(batches) > 1:
                await asyncio.sleep(0.15)
    except Exception as e:
        raise HTTPException(502, f"Open-Meteo API error: {e}")

    # Build scored cells
    cells: list[HiResCell] = []
    for i, (lat, lon) in enumerate(points):
        if i >= len(all_results):
            break
        current = all_results[i].get("current", {})
        ws10 = current.get("wind_speed_10m", 0.0) or 0.0
        ghi  = current.get("shortwave_radiation", 0.0) or 0.0

        if type == "wind":
            score = _wind_score_100m(ws10)
        elif type == "solar":
            score = _solar_score_instant(ghi)
        else:
            w = _wind_score_100m(ws10)
            s = _solar_score_instant(ghi)
            score = round(0.5 * w + 0.5 * s, 1)

        cells.append(HiResCell(lat=lat, lon=lon, score=score, cell_km=cell_km))

    _cache_set(ck, cells)
    return HiResResponse(cells=cells, cell_km=cell_km, total=len(cells))
