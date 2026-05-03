"""Tests for ForecastSage modules."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "contracts"))

from schemas import ForecastPoint
from app.forecast.maintenance_window import find_maintenance_window


def _make_points(values: list[float], wind_ms: float = 5.0) -> list[ForecastPoint]:
    from datetime import datetime, timedelta
    base = datetime(2026, 5, 3, 0, 0)
    return [
        ForecastPoint(
            timestamp=(base + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            expected_kw=v,
            lower_kw=v * 0.85,
            upper_kw=v * 1.15,
            wind_speed_ms=wind_ms,
        )
        for i, v in enumerate(values)
    ]


class TestMaintenanceWindow:
    def test_finds_zero_production_window(self):
        values = [500.0] * 14 + [0.0, 0.0, 0.0] + [500.0] * 31
        points = _make_points(values)
        mw = find_maintenance_window(points)
        assert mw is not None
        assert mw.start_hour_offset == 14
        assert mw.avg_production_kw == 0.0

    def test_skips_high_wind(self):
        values = [0.0] * 3 + [500.0] * 45
        high_wind_points = _make_points(values, wind_ms=20.0)
        mw = find_maintenance_window(high_wind_points)
        # Should skip the zero-production window due to high wind → find next best
        # (next best is first 500 kW window, but all remaining have same wind so no window found)
        # With all high wind: no valid window
        assert mw is None

    def test_returns_none_for_insufficient_points(self):
        points = _make_points([100.0, 200.0])
        mw = find_maintenance_window(points, duration_hours=3)
        assert mw is None

    def test_description_is_string(self):
        points = _make_points([100.0] * 48)
        mw = find_maintenance_window(points)
        assert mw is not None
        assert isinstance(mw.description, str)
        assert len(mw.description) > 10

    def test_band_consistency(self):
        points = _make_points([400.0] * 48)
        for p in points:
            assert p.lower_kw <= p.expected_kw <= p.upper_kw


class TestPhysicsForecast:
    def test_returns_48_points(self):
        from app.forecast.physics_forecast import generate_forecast
        result = generate_forecast(40.213, 28.366, hours=48, energy_type="wind")
        assert len(result.points) == 48

    def test_uncertainty_band_consistent(self):
        from app.forecast.physics_forecast import generate_forecast
        result = generate_forecast(38.733, 35.485, hours=24, energy_type="solar")
        for p in result.points:
            assert p.lower_kw <= p.expected_kw, f"lower > expected at {p.timestamp}"
            assert p.expected_kw <= p.upper_kw, f"expected > upper at {p.timestamp}"

    def test_hybrid_forecast_nonnegative(self):
        from app.forecast.physics_forecast import generate_forecast
        result = generate_forecast(38.737, 33.371, hours=48, energy_type="hybrid")
        for p in result.points:
            assert p.expected_kw >= 0
            assert p.lower_kw >= 0
