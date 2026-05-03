from app.scoring.grid_proximity import grid_proximity_score


def get_nearest_substation(lat: float, lon: float) -> dict | None:
    _, _, sub_info = grid_proximity_score(lat, lon)
    return sub_info
