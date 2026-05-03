"""Finds optimal maintenance windows within a 48-hour forecast."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "contracts"))
from schemas import ForecastPoint, MaintenanceWindow

WINDOW_HOURS = 3
MAX_SAFE_WIND_MS = 13.9  # 50 km/h


def find_maintenance_window(
    points: list[ForecastPoint],
    duration_hours: int = WINDOW_HOURS,
    max_wind_ms: float = MAX_SAFE_WIND_MS,
) -> MaintenanceWindow | None:
    if len(points) < duration_hours:
        return None

    best_sum = float("inf")
    best_start = None

    for i in range(len(points) - duration_hours + 1):
        window = points[i:i + duration_hours]

        # Safety: skip windows with dangerous wind speeds
        if any(
            p.wind_speed_ms is not None and p.wind_speed_ms > max_wind_ms
            for p in window
        ):
            continue

        production_sum = sum(p.expected_kw for p in window)
        if production_sum < best_sum:
            best_sum = production_sum
            best_start = i

    if best_start is None:
        return None

    window = points[best_start:best_start + duration_hours]
    avg_prod = best_sum / duration_hours

    start_offset = best_start
    end_offset = best_start + duration_hours

    # Build human-readable description
    start_h = best_start % 24
    end_h = (best_start + duration_hours) % 24
    day_label = "Bugün" if best_start < 24 else "Yarın"
    description = (
        f"{day_label} {start_h:02d}:00–{end_h:02d}:00 arası beklenen üretim "
        f"ortalama {avg_prod:.0f} kW — bakım için uygun pencere."
    )

    return MaintenanceWindow(
        start_hour_offset=start_offset,
        end_hour_offset=end_offset,
        avg_production_kw=round(avg_prod, 1),
        description=description,
    )
