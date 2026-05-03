"""Economic feasibility scoring: CAPEX, payback years, LCOE."""

# Turkey 2024 reference values
CAPEX_SOLAR_TL_PER_KWP = 15_000.0
CAPEX_WIND_TL_PER_KW = 45_000.0
OPEX_RATIO = 0.02          # annual OPEX as fraction of CAPEX
ELECTRICITY_PRICE_TL_KWH = 2.50
RATED_POWER_KW = 2_000.0   # standard 2 MW wind turbine / ~2 MW solar farm
SOLAR_PANEL_AREA_M2_PER_KWP = 6.5

PAYBACK_BEST_YEARS = 3.0
PAYBACK_WORST_YEARS = 15.0


def estimate_annual_production_kwh(
    energy_type: str,
    avg_wind_speed_50m: float,
    ghi_annual_kwh_m2: float,
    capacity_factor: float | None = None,
) -> float:
    """Estimate annual energy production in kWh for a standard installation."""
    if energy_type == "wind":
        cf = capacity_factor or _wind_cf(avg_wind_speed_50m)
        return RATED_POWER_KW * cf * 8760
    elif energy_type == "solar":
        cf = capacity_factor or _solar_cf(ghi_annual_kwh_m2)
        return RATED_POWER_KW * cf * 8760
    else:  # hybrid: 50/50 split
        cf_wind = _wind_cf(avg_wind_speed_50m)
        cf_solar = _solar_cf(ghi_annual_kwh_m2)
        wind_prod = RATED_POWER_KW * cf_wind * 8760
        solar_prod = RATED_POWER_KW * cf_solar * 8760
        return (wind_prod + solar_prod) / 2


def _wind_cf(avg_wind_50m: float) -> float:
    """Approximate capacity factor from mean wind speed."""
    if avg_wind_50m < 4:
        return 0.10
    if avg_wind_50m > 9:
        return 0.45
    return 0.10 + 0.35 * (avg_wind_50m - 4) / 5


def _solar_cf(ghi_annual_kwh_m2: float) -> float:
    """Approximate capacity factor from annual GHI."""
    # 1900 kWh/m²/yr → CF ~0.22; 1200 → CF ~0.14
    if ghi_annual_kwh_m2 <= 1200:
        return 0.14
    if ghi_annual_kwh_m2 >= 1900:
        return 0.22
    return 0.14 + 0.08 * (ghi_annual_kwh_m2 - 1200) / 700


def estimate_capex_tl(energy_type: str, rated_kw: float = RATED_POWER_KW) -> float:
    if energy_type == "solar":
        return rated_kw * CAPEX_SOLAR_TL_PER_KWP
    elif energy_type == "wind":
        return rated_kw * CAPEX_WIND_TL_PER_KW
    else:
        return rated_kw * (CAPEX_SOLAR_TL_PER_KWP + CAPEX_WIND_TL_PER_KW) / 2


def estimate_payback_years(
    annual_production_kwh: float,
    capex_tl: float,
    electricity_price: float = ELECTRICITY_PRICE_TL_KWH,
    opex_ratio: float = OPEX_RATIO,
) -> float:
    annual_revenue = annual_production_kwh * electricity_price
    annual_opex = capex_tl * opex_ratio
    net_annual = annual_revenue - annual_opex
    if net_annual <= 0:
        return 99.0
    return capex_tl / net_annual


def estimate_lcoe(
    capex_tl: float,
    annual_production_kwh: float,
    lifetime_years: int = 25,
    opex_ratio: float = OPEX_RATIO,
) -> float:
    if annual_production_kwh <= 0:
        return 99.0
    total_opex = capex_tl * opex_ratio * lifetime_years
    total_production = annual_production_kwh * lifetime_years
    return (capex_tl + total_opex) / total_production


def economic_score(payback_years: float) -> float:
    """Normalize payback period [3, 15] years → [1.0, 0.0]."""
    if payback_years <= PAYBACK_BEST_YEARS:
        return 1.0
    if payback_years >= PAYBACK_WORST_YEARS:
        return 0.0
    return 1.0 - (payback_years - PAYBACK_BEST_YEARS) / (PAYBACK_WORST_YEARS - PAYBACK_BEST_YEARS)


def build_financial_summary(
    energy_type: str,
    avg_wind_speed_50m: float,
    ghi_annual_kwh_m2: float,
) -> dict:
    capex = estimate_capex_tl(energy_type)
    annual_prod = estimate_annual_production_kwh(energy_type, avg_wind_speed_50m, ghi_annual_kwh_m2)
    payback = estimate_payback_years(annual_prod, capex)
    lcoe = estimate_lcoe(capex, annual_prod)

    cf_wind = _wind_cf(avg_wind_speed_50m)
    cf_solar = _solar_cf(ghi_annual_kwh_m2)
    if energy_type == "wind":
        cf = cf_wind
    elif energy_type == "solar":
        cf = cf_solar
    else:
        cf = (cf_wind + cf_solar) / 2

    return {
        "capex_tl": round(capex),
        "annual_production_kwh": round(annual_prod),
        "payback_years": round(payback, 1),
        "lcoe_tl_per_kwh": round(lcoe, 3),
        "capacity_factor": round(cf, 3),
        "disclaimer": "Ön değerlendirme amaçlıdır. Yatırım kararı için saha ölçümü gereklidir.",
    }
