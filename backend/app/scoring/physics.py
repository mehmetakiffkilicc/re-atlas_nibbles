"""Physics formulas for wind and solar power estimation."""
import math

# Wind turbine constants
CUT_IN_SPEED_MS = 3.0
CUT_OUT_SPEED_MS = 25.0
RATED_SPEED_MS = 12.0

# Solar constants
STANDARD_IRRADIANCE_W_M2 = 1000.0


def wind_power_kw(
    wind_speed_ms: float,
    rotor_diameter_m: float = 80.0,
    cp: float = 0.40,
    rho: float = 1.225,
) -> float:
    """Instantaneous wind power using Betz limit formula.

    Returns 0 outside cut-in/cut-out range.
    """
    if wind_speed_ms <= CUT_IN_SPEED_MS or wind_speed_ms >= CUT_OUT_SPEED_MS:
        return 0.0
    rotor_area = math.pi * (rotor_diameter_m / 2) ** 2
    power_w = 0.5 * rho * rotor_area * cp * wind_speed_ms ** 3
    return power_w / 1000.0


def solar_power_kw(
    ghi_w_m2: float,
    panel_area_m2: float = 50.0,
    efficiency: float = 0.18,
    performance_ratio: float = 0.80,
) -> float:
    """Instantaneous solar power from GHI irradiance."""
    if ghi_w_m2 <= 0:
        return 0.0
    power_w = ghi_w_m2 * panel_area_m2 * efficiency * performance_ratio
    return power_w / 1000.0


def capacity_factor(hourly_production_kw: list[float], rated_power_kw: float) -> float:
    """Capacity factor: actual / theoretical maximum production."""
    if not hourly_production_kw or rated_power_kw <= 0:
        return 0.0
    actual = sum(hourly_production_kw)
    theoretical = rated_power_kw * len(hourly_production_kw)
    return min(1.0, actual / theoretical)


def wind_resource_score(avg_wind_speed: float, hub_height_m: int = 100) -> float:
    """Normalize wind speed → [0, 1].

    Thresholds vary by hub height:
    - 100m (modern large turbines): 5–10 m/s
    - 50m (legacy/small turbines):  4–9  m/s
    """
    if hub_height_m >= 80:
        MIN_MS, MAX_MS = 5.0, 10.0
    else:
        MIN_MS, MAX_MS = 4.0, 9.0
    if avg_wind_speed <= MIN_MS:
        return 0.0
    if avg_wind_speed >= MAX_MS:
        return 1.0
    return (avg_wind_speed - MIN_MS) / (MAX_MS - MIN_MS)


def solar_resource_score(ghi_annual_kwh_m2: float) -> float:
    """Normalize annual GHI [1200, 1900] kWh/m² → [0, 1]."""
    MIN_GHI, MAX_GHI = 1200.0, 1900.0
    if ghi_annual_kwh_m2 <= MIN_GHI:
        return 0.0
    if ghi_annual_kwh_m2 >= MAX_GHI:
        return 1.0
    return (ghi_annual_kwh_m2 - MIN_GHI) / (MAX_GHI - MIN_GHI)


def hybrid_resource_score(
    avg_wind_speed_50m: float,
    ghi_annual_kwh_m2: float,
    avg_wind_speed_100m: float | None = None,
) -> float:
    """Hybrid resource score: equal weight of wind (best available height) and solar."""
    if avg_wind_speed_100m is not None:
        w_score = wind_resource_score(avg_wind_speed_100m, hub_height_m=100)
    else:
        w_score = wind_resource_score(avg_wind_speed_50m, hub_height_m=50)
    return 0.5 * w_score + 0.5 * solar_resource_score(ghi_annual_kwh_m2)
