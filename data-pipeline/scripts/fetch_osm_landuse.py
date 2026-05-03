"""
Fetches Turkish landuse polygons from OSM Overpass API using 7-region strategy.
Falls back to Marmara+Ege (2 regions) if full Turkey fetch is too slow.
"""
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_DIR = ROOT / "backend" / "data"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

LANDUSE_TAGS = "forest|farmland|meadow|industrial|residential|commercial|retail|construction|cemetery|grass|village_green|allotments|orchard|vineyard|quarry|landfill|brownfield|greenfield|military|nature_reserve|protected_area"

REGIONS_FULL = [
    ("Marmara", 39.5, 26.0, 42.1, 32.0),
    ("Ege", 37.0, 25.8, 39.6, 30.5),
    ("Akdeniz", 36.0, 29.0, 38.5, 36.5),
    ("İç_Anadolu", 37.5, 29.5, 40.5, 36.5),
    ("Karadeniz", 40.5, 31.0, 42.5, 41.5),
    ("Doğu_Anadolu", 37.0, 36.5, 40.5, 44.5),
    ("Güneydoğu", 36.5, 37.0, 38.5, 42.5),
]

REGIONS_FALLBACK = [
    ("Marmara", 39.5, 26.0, 42.1, 32.0),
    ("Ege", 37.0, 25.8, 39.6, 30.5),
]

LANDUSE_SCORE_MAP = {
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
    "unknown": 0.5,
}


def make_query(region_name: str, s: float, w: float, n: float, e: float) -> str:
    return f"""
[out:json][timeout:120];
(
  way["landuse"~"{LANDUSE_TAGS}"]({s},{w},{n},{e});
  relation["landuse"~"{LANDUSE_TAGS}"]({s},{w},{n},{e});
  way["natural"="wood"]({s},{w},{n},{e});
  way["leisure"~"park|nature_reserve"]({s},{w},{n},{e});
);
out center tags;
"""


def query_overpass(query: str) -> list:
    data = urllib.parse.urlencode({"data": query}).encode()
    req = urllib.request.Request(OVERPASS_URL, data=data)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "RE-Atlas/1.0 (hackathon project; contact: re-atlas@example.com)")
    with urllib.request.urlopen(req, timeout=150) as resp:
        result = json.loads(resp.read())
    return result.get("elements", [])


def element_to_feature(el: dict) -> dict | None:
    center = el.get("center")
    if not center:
        return None
    tags = el.get("tags", {})
    landuse_type = tags.get("landuse") or tags.get("natural") or tags.get("leisure") or "unknown"
    score = LANDUSE_SCORE_MAP.get(landuse_type, 0.5)
    return {
        "type": "Feature",
        "properties": {"landuse_type": landuse_type, "score": score},
        "geometry": {"type": "Point", "coordinates": [center["lon"], center["lat"]]}
    }


def fetch_regions(regions: list) -> list:
    all_features = []
    for name, s, w, n, e in regions:
        print(f"  Fetching {name}...")
        try:
            elements = query_overpass(make_query(name, s, w, n, e))
            features = [f for el in elements if (f := element_to_feature(el))]
            print(f"    {len(features)} features")
            all_features.extend(features)
            time.sleep(3)
        except Exception as ex:
            print(f"    WARNING: {name} failed — {ex}")
    return all_features


def main(fallback: bool = False):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    regions = REGIONS_FALLBACK if fallback else REGIONS_FULL
    print(f"Fetching landuse: {'FALLBACK (Marmara+Ege)' if fallback else 'full Turkey (7 regions)'}")

    features = fetch_regions(regions)

    if not features:
        print("No features fetched — creating minimal synthetic landuse")
        features = _synthetic_fallback()

    geojson = {"type": "FeatureCollection", "features": features}
    out = DATA_DIR / "landuse.geojson"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)

    size_kb = out.stat().st_size / 1024
    print(f"Saved {len(features)} features to {out} ({size_kb:.1f} KB)")

    if size_kb < 100 and not fallback:
        print("Output too small — re-running with fallback regions")
        main(fallback=True)


def _synthetic_fallback() -> list:
    """Sparse grid of synthetic landuse points covering Turkey."""
    import random
    random.seed(42)
    features = []
    for lat in [i * 0.5 + 36.0 for i in range(13)]:
        for lon in [i * 0.5 + 26.0 for i in range(38)]:
            lt = random.choice(["farmland", "meadow", "industrial", "barren", "residential"])
            features.append({
                "type": "Feature",
                "properties": {"landuse_type": lt, "score": LANDUSE_SCORE_MAP.get(lt, 0.5)},
                "geometry": {"type": "Point", "coordinates": [lon, lat]}
            })
    return features


if __name__ == "__main__":
    import sys
    main(fallback="--fallback" in sys.argv)
