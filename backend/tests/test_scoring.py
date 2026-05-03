"""Unit tests for scoring engine components."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "contracts"))

from app.scoring.physics import (
    wind_power_kw, solar_power_kw, wind_resource_score,
    solar_resource_score, capacity_factor,
)
from app.scoring.weights import get_weights
from app.scoring.economic import economic_score, estimate_payback_years


class TestWindPower:
    def test_below_cut_in(self):
        assert wind_power_kw(0.0) == 0.0
        assert wind_power_kw(2.9) == 0.0

    def test_at_cut_in(self):
        assert wind_power_kw(3.0) == 0.0  # exactly at cut-in → 0

    def test_operating_range(self):
        p = wind_power_kw(8.0)
        assert p > 0, "Should produce power at 8 m/s"
        assert p < 5000, "Power seems too high"

    def test_above_cut_out(self):
        assert wind_power_kw(25.0) == 0.0
        assert wind_power_kw(30.0) == 0.0

    def test_power_increases_with_speed(self):
        assert wind_power_kw(6.0) < wind_power_kw(9.0)


class TestSolarPower:
    def test_zero_irradiance(self):
        assert solar_power_kw(0.0) == 0.0

    def test_standard_irradiance(self):
        p = solar_power_kw(1000.0)
        assert p > 0

    def test_proportional(self):
        assert solar_power_kw(500.0) < solar_power_kw(1000.0)


class TestResourceScores:
    def test_wind_score_boundaries(self):
        assert wind_resource_score(0.0) == 0.0
        assert wind_resource_score(4.0) == 0.0
        assert wind_resource_score(9.0) == 1.0
        assert wind_resource_score(15.0) == 1.0

    def test_wind_score_midpoint(self):
        score = wind_resource_score(6.5)
        assert 0.4 < score < 0.6

    def test_solar_score_boundaries(self):
        assert solar_resource_score(1000.0) == 0.0
        assert solar_resource_score(1200.0) == 0.0
        assert solar_resource_score(1900.0) == 1.0
        assert solar_resource_score(2200.0) == 1.0

    def test_solar_score_midpoint(self):
        score = solar_resource_score(1550.0)
        assert 0.45 < score < 0.55


class TestCapacityFactor:
    def test_empty(self):
        assert capacity_factor([], 100) == 0.0

    def test_full(self):
        assert capacity_factor([100.0] * 10, 100.0) == 1.0

    def test_half(self):
        assert capacity_factor([50.0] * 10, 100.0) == 0.5


class TestWeights:
    def test_investor_weights_sum(self):
        w = get_weights("investor")
        total = sum(w.values())
        assert abs(total - 1.0) < 1e-9

    def test_individual_weights_sum(self):
        w = get_weights("individual")
        total = sum(w.values())
        assert abs(total - 1.0) < 1e-9

    def test_unknown_profile_defaults_to_investor(self):
        w = get_weights("nonexistent")
        assert w == get_weights("investor")


class TestEconomicScore:
    def test_best_payback(self):
        assert economic_score(3.0) == 1.0
        assert economic_score(1.0) == 1.0

    def test_worst_payback(self):
        assert economic_score(15.0) == 0.0
        assert economic_score(20.0) == 0.0

    def test_mid_payback(self):
        score = economic_score(9.0)
        assert 0.4 < score < 0.6

    def test_payback_estimate_reasonable(self):
        years = estimate_payback_years(
            annual_production_kwh=5_000_000,
            capex_tl=90_000_000,
        )
        assert 5 < years < 30


class TestGridProximity:
    def test_score_range(self):
        from app.scoring.grid_proximity import _distance_to_score
        assert _distance_to_score(0) == 1.0
        assert _distance_to_score(5) == 1.0
        assert _distance_to_score(50) == 0.0
        assert _distance_to_score(100) == 0.0
        s = _distance_to_score(27.5)
        assert 0.45 < s < 0.55
