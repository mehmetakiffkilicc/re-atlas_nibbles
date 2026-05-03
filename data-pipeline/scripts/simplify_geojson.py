"""GeoJSON simplification: tries mapshaper first, falls back to shapely."""
import subprocess
import sys
import json
from pathlib import Path


def simplify_with_mapshaper(input_path: str, output_path: str, percentage: int = 10) -> bool:
    try:
        result = subprocess.run(
            ["mapshaper", input_path, "-simplify", f"{percentage}%", "-o", output_path],
            capture_output=True, text=True, timeout=120
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def simplify_with_shapely(input_path: str, output_path: str, tolerance: float = 0.01) -> bool:
    try:
        from shapely.geometry import shape, mapping
        from shapely.validation import make_valid
    except ImportError:
        print("shapely not installed — skipping simplification")
        import shutil
        shutil.copy(input_path, output_path)
        return True

    with open(input_path, encoding="utf-8") as f:
        geojson = json.load(f)

    for feature in geojson.get("features", []):
        geom = feature.get("geometry")
        if geom:
            try:
                s = make_valid(shape(geom))
                simplified = s.simplify(tolerance, preserve_topology=True)
                feature["geometry"] = mapping(simplified)
            except Exception:
                pass

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)
    return True


def simplify(input_path: str, output_path: str, percentage: int = 10) -> None:
    print(f"Simplifying {input_path} → {output_path} ({percentage}%)")
    if simplify_with_mapshaper(input_path, output_path, percentage):
        print("  Used mapshaper")
    else:
        print("  mapshaper not found — using shapely fallback")
        simplify_with_shapely(input_path, output_path, tolerance=0.01)

    size_kb = Path(output_path).stat().st_size / 1024
    print(f"  Output size: {size_kb:.1f} KB")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python simplify_geojson.py <input> <output> [percentage]")
        sys.exit(1)
    pct = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    simplify(sys.argv[1], sys.argv[2], pct)
