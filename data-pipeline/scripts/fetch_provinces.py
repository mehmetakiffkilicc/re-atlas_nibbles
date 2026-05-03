"""Downloads Turkey province boundaries and simplifies them."""
import json
import sys
from pathlib import Path
import urllib.request

ROOT = Path(__file__).parent.parent.parent
OUTPUT_RAW = ROOT / "backend" / "data" / "provinces_raw.geojson"
OUTPUT = ROOT / "backend" / "data" / "provinces.geojson"

SOURCES = [
    "https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-provinces.json",
    "https://raw.githubusercontent.com/sadikturan/tr-geojson/master/geo/tr-provinces.json",
]


def download(url: str, dest: Path) -> bool:
    try:
        print(f"  Trying {url}")
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f"  Failed: {e}")
        return False


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    downloaded = False
    for url in SOURCES:
        if download(url, OUTPUT_RAW):
            downloaded = True
            break

    if not downloaded:
        print("All sources failed — creating minimal fallback GeoJSON")
        _create_fallback()
        return

    with open(OUTPUT_RAW, encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])
    print(f"Downloaded {len(features)} province features")

    sys.path.insert(0, str(Path(__file__).parent))
    from simplify_geojson import simplify
    simplify(str(OUTPUT_RAW), str(OUTPUT), percentage=10)


def _create_fallback():
    """Minimal GeoJSON with bounding boxes for 5 demo provinces."""
    provinces = [
        {"id": "16", "name": "Bursa", "bbox": [28.0, 39.8, 30.0, 40.5]},
        {"id": "35", "name": "İzmir", "bbox": [26.2, 37.5, 28.2, 39.0]},
        {"id": "06", "name": "Ankara", "bbox": [31.5, 39.3, 33.5, 40.5]},
        {"id": "42", "name": "Konya", "bbox": [31.0, 37.2, 34.5, 38.5]},
        {"id": "38", "name": "Kayseri", "bbox": [35.0, 38.2, 36.5, 39.2]},
    ]
    features = []
    for p in provinces:
        w, s, e, n = p["bbox"]
        features.append({
            "type": "Feature",
            "properties": {"id": p["id"], "name": p["name"]},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[w, s], [e, s], [e, n], [w, n], [w, s]]]
            }
        })
    geojson = {"type": "FeatureCollection", "features": features}
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)
    print(f"Fallback provinces.geojson created with {len(features)} features")


if __name__ == "__main__":
    main()
