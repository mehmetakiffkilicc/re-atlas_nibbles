"""Fetches fault lines from OSM (optional). Creates empty FeatureCollection on failure."""
import json
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_DIR = ROOT / "backend" / "data"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

QUERY = """
[out:json][timeout:120];
area["ISO3166-1"="TR"][admin_level=2]->.turkey;
(
  way["geological"="fault"](area.turkey);
  relation["geological"="fault"](area.turkey);
);
out geom;
"""


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / "faults.geojson"

    try:
        data = urllib.parse.urlencode({"data": QUERY}).encode()
        req = urllib.request.Request(OVERPASS_URL, data=data)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("User-Agent", "RE-Atlas/1.0 (hackathon project; contact: re-atlas@example.com)")
        with urllib.request.urlopen(req, timeout=150) as resp:
            result = json.loads(resp.read())

        features = []
        for el in result.get("elements", []):
            geom = el.get("geometry", [])
            if len(geom) >= 2:
                coords = [[g["lon"], g["lat"]] for g in geom]
                features.append({
                    "type": "Feature",
                    "properties": {"osm_id": el["id"]},
                    "geometry": {"type": "LineString", "coordinates": coords}
                })

        print(f"Fetched {len(features)} fault line segments")
    except Exception as e:
        print(f"Fault query failed: {e} — writing empty FeatureCollection")
        features = []

    geojson = {"type": "FeatureCollection", "features": features}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
