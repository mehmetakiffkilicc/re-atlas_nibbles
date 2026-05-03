"""Score component weights for different user profiles."""

WEIGHTS_INVESTOR: dict[str, float] = {
    "resource": 0.40,
    "landuse": 0.20,
    "grid": 0.30,
    "risk": 0.05,
    "economic": 0.05,
}

WEIGHTS_INDIVIDUAL: dict[str, float] = {
    "resource": 0.30,
    "landuse": 0.10,
    "grid": 0.05,
    "risk": 0.05,
    "economic": 0.50,
}

WEIGHTS_MAP: dict[str, dict[str, float]] = {
    "investor": WEIGHTS_INVESTOR,
    "individual": WEIGHTS_INDIVIDUAL,
}


def get_weights(profile: str = "investor") -> dict[str, float]:
    return WEIGHTS_MAP.get(profile, WEIGHTS_INVESTOR)
