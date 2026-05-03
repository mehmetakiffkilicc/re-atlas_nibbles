"""Downloads Turkey district boundaries and simplifies them."""
import json
import sys
from pathlib import Path
import urllib.request

ROOT = Path(__file__).parent.parent.parent
OUTPUT_RAW = ROOT / "backend" / "data" / "districts_raw.geojson"
OUTPUT = ROOT / "backend" / "data" / "districts.geojson"

SOURCES = [
    "https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-districts.json",
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
        print("Districts source failed — creating empty GeoJSON")
        geojson = {"type": "FeatureCollection", "features": []}
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(geojson, f)
        return

    with open(OUTPUT_RAW, encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])
    print(f"Downloaded {len(features)} district features")

    sys.path.insert(0, str(Path(__file__).parent))
    from simplify_geojson import simplify
    simplify(str(OUTPUT_RAW), str(OUTPUT), percentage=10)


if __name__ == "__main__":
    main()
