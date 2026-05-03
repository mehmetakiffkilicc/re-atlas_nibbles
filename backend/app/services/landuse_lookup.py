from app.scoring.landuse import landuse_score


def get_landuse(lat: float, lon: float) -> dict:
    score, landuse_type = landuse_score(lat, lon)
    return {"score": score, "landuse_type": landuse_type}
