"""FastAPI application entry point. Reload trigger #1"""
import json
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "contracts"))
from schemas import ProvinceScore, WeatherSummary

from app.config import DATA_DIR
from app.routers import score, provinces, districts, top, forecast, grid, hires
from app.routers.provinces import set_province_scores
from app.services.openmeteo import get_weather_summary
from app.scoring.engine import calculate_score


def _load_provinces_geojson() -> list[dict]:
    path = DATA_DIR / "provinces.geojson"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("features", [])


def _centroid(geometry: dict) -> tuple[float, float]:
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


def _precompute_province_scores():
    """Compute province scores for all energy types at startup."""
    features = _load_provinces_geojson()
    if not features:
        print("WARNING: provinces.geojson not found — run DataForager first")
        return

    print(f"Precomputing scores for {len(features)} provinces...")
    for energy_type in ["solar", "wind", "hybrid"]:
        scores = []
        for feat in features:
            props = feat.get("properties", {})
            province_id = str(props.get("id", props.get("OBJECTID", props.get("fid", ""))))
            province_name = props.get("name", props.get("NAME_1", props.get("il_adi", f"İl {province_id}")))

            lat, lon = _centroid(feat.get("geometry", {}))
            try:
                weather_dict = get_weather_summary(lat, lon)
                weather = WeatherSummary(**weather_dict)
                score_resp = calculate_score(lat, lon, energy_type, weather, province_name=province_name)
                scores.append(ProvinceScore(
                    province_id=province_id,
                    province_name=province_name,
                    score=score_resp.score,
                    energy_type=energy_type,
                    centroid_lat=round(lat, 5),
                    centroid_lon=round(lon, 5),
                    geometry=feat.get("geometry"),
                ))
            except Exception as e:
                print(f"  Score failed for {province_name}: {e}")

        set_province_scores(energy_type, scores)
        print(f"  {energy_type}: {len(scores)} provinces scored")


@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    await asyncio.to_thread(_precompute_province_scores)
    yield


app = FastAPI(
    title="RE-Atlas API",
    version="1.0.0",
    description="Renewable Energy Investment Suitability API for Turkey",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(score.router, prefix="/api", tags=["scoring"])
app.include_router(provinces.router, prefix="/api", tags=["geography"])
app.include_router(districts.router, prefix="/api", tags=["geography"])
app.include_router(top.router, prefix="/api", tags=["scoring"])
app.include_router(forecast.router, prefix="/api", tags=["forecast"])
app.include_router(grid.router, prefix="/api", tags=["grid"])
app.include_router(hires.router, prefix="/api", tags=["grid"])


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/nearest-substation")
def nearest_substation(
    lat: float,
    lon: float,
):
    from app.services.substation_lookup import get_nearest_substation
    sub = get_nearest_substation(lat, lon)
    if sub is None:
        return {"error": "No substation data available"}
    return sub


@app.get("/api/landuse")
def landuse(lat: float, lon: float):
    from app.services.landuse_lookup import get_landuse
    return get_landuse(lat, lon)
