"""Fetches Turkish power substations and transmission lines from OSM Overpass API."""
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2

ROOT = Path(__file__).parent.parent.parent
DATA_DIR = ROOT / "backend" / "data"

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

SUBSTATION_QUERY = """
[out:json][timeout:120];
area["ISO3166-1"="TR"][admin_level=2]->.turkey;
(
  node["power"="substation"](area.turkey);
  way["power"="substation"](area.turkey);
  relation["power"="substation"](area.turkey);
);
out center;
"""

TRANSMISSION_QUERY = """
[out:json][timeout:120];
area["ISO3166-1"="TR"][admin_level=2]->.turkey;
(
  way["power"="line"]["voltage"~"154000|380000|400000"](area.turkey);
);
out geom;
"""


def overpass_query(query: str) -> dict:
    data = urllib.parse.urlencode({"data": query}).encode()
    req = urllib.request.Request(OVERPASS_URL, data=data)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "RE-Atlas/1.0 (hackathon project; contact: re-atlas@example.com)")
    with urllib.request.urlopen(req, timeout=150) as resp:
        return json.loads(resp.read())


def element_to_point(el: dict) -> dict | None:
    if el["type"] == "node":
        lat, lon = el.get("lat"), el.get("lon")
    elif "center" in el:
        lat, lon = el["center"]["lat"], el["center"]["lon"]
    else:
        return None

    tags = el.get("tags", {})
    voltage_raw = tags.get("voltage", "")
    try:
        voltage_kv = float(voltage_raw.split(";")[0]) / 1000
    except (ValueError, AttributeError):
        voltage_kv = None

    return {
        "type": "Feature",
        "properties": {
            "osm_id": el["id"],
            "name": tags.get("name"),
            "voltage_kv": voltage_kv,
            "operator": tags.get("operator"),
        },
        "geometry": {"type": "Point", "coordinates": [lon, lat]}
    }


def line_to_feature(el: dict) -> dict | None:
    geom = el.get("geometry", [])
    if len(geom) < 2:
        return None
    coords = [[g["lon"], g["lat"]] for g in geom]
    tags = el.get("tags", {})
    voltage_raw = tags.get("voltage", "")
    try:
        voltage_kv = float(voltage_raw.split(";")[0]) / 1000
    except (ValueError, AttributeError):
        voltage_kv = None
    return {
        "type": "Feature",
        "properties": {
            "osm_id": el["id"],
            "voltage_kv": voltage_kv,
            "operator": tags.get("operator"),
        },
        "geometry": {"type": "LineString", "coordinates": coords}
    }


def fetch_substations():
    print("Fetching substations...")
    try:
        result = overpass_query(SUBSTATION_QUERY)
        features = [f for el in result.get("elements", []) if (f := element_to_point(el))]
        print(f"  {len(features)} substations found")
    except Exception as e:
        print(f"  Substation query failed: {e} — using demo fallback")
        features = _demo_substations()

    geojson = {"type": "FeatureCollection", "features": features}
    out = DATA_DIR / "substations.geojson"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)
    print(f"  Saved to {out} ({out.stat().st_size // 1024} KB)")


def fetch_transmission():
    print("Fetching transmission lines...")
    try:
        result = overpass_query(TRANSMISSION_QUERY)
        features = [f for el in result.get("elements", []) if (f := line_to_feature(el))]
        print(f"  {len(features)} transmission line segments found")
    except Exception as e:
        print(f"  Transmission query failed: {e} — using empty fallback")
        features = []

    geojson = {"type": "FeatureCollection", "features": features}
    out = DATA_DIR / "transmission_lines.geojson"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)
    print(f"  Saved to {out}")


def _demo_substations() -> list:
    """Hardcoded substations near demo coordinates for offline testing."""
    return [
        {"type": "Feature", "properties": {"name": "Karacabey TM", "voltage_kv": 154, "operator": "TEİAŞ"}, "geometry": {"type": "Point", "coordinates": [28.37, 40.22]}},
        {"type": "Feature", "properties": {"name": "Kayseri TM", "voltage_kv": 380, "operator": "TEİAŞ"}, "geometry": {"type": "Point", "coordinates": [35.49, 38.74]}},
        {"type": "Feature", "properties": {"name": "Konya TM", "voltage_kv": 154, "operator": "TEİAŞ"}, "geometry": {"type": "Point", "coordinates": [32.48, 37.87]}},
        {"type": "Feature", "properties": {"name": "İzmir TM", "voltage_kv": 380, "operator": "TEİAŞ"}, "geometry": {"type": "Point", "coordinates": [27.13, 38.42]}},
        {"type": "Feature", "properties": {"name": "Bursa TM", "voltage_kv": 154, "operator": "TEİAŞ"}, "geometry": {"type": "Point", "coordinates": [29.07, 40.18]}},
        {"type": "Feature", "properties": {"name": "Ankara TM", "voltage_kv": 380, "operator": "TEİAŞ"}, "geometry": {"type": "Point", "coordinates": [32.86, 39.93]}},
        {"type": "Feature", "properties": {"name": "Çatalca TM", "voltage_kv": 154, "operator": "TEİAŞ"}, "geometry": {"type": "Point", "coordinates": [28.45, 41.15]}},
        {"type": "Feature", "properties": {"name": "Tuz Gölü TM", "voltage_kv": 154, "operator": "TEİAŞ"}, "geometry": {"type": "Point", "coordinates": [33.37, 38.73]}},
    ]


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    fetch_substations()
    time.sleep(2)
    fetch_transmission()
