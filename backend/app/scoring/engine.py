"""Central scoring engine: orchestrates all component scores → ScoreResponse."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "contracts"))

from schemas import (
    ScoreResponse, ScoreBreakdown, ScoreExplanation,
    FinancialSummary, Substation, YekaZone, WeatherSummary,
)
from .physics import wind_resource_score, solar_resource_score, hybrid_resource_score
from .landuse import landuse_score
from .grid_proximity import grid_proximity_score
from .risk import combined_risk_score
from .yeka import yeka_bonus
from .economic import economic_score, build_financial_summary
from .explainer import generate_explanation
from .weights import get_weights


def calculate_score(
    lat: float,
    lon: float,
    energy_type: str,
    weather: WeatherSummary,
    weights_profile: str = "investor",
    province_name: str | None = None,
    province_avg_score: float | None = None,
) -> ScoreResponse:
    w = get_weights(weights_profile)

    # 1. Resource potential — prefer 100m wind data (NASA POWER) when available
    wind_100m = getattr(weather, "avg_wind_speed_100m", None)
    if energy_type == "wind":
        if wind_100m is not None:
            resource = wind_resource_score(wind_100m, hub_height_m=100)
        else:
            resource = wind_resource_score(weather.avg_wind_speed_50m, hub_height_m=50)
    elif energy_type == "solar":
        resource = solar_resource_score(weather.ghi_annual_kwh_m2)
    else:
        resource = hybrid_resource_score(
            weather.avg_wind_speed_50m,
            weather.ghi_annual_kwh_m2,
            avg_wind_speed_100m=wind_100m,
        )

    # 2. Land use
    lu_score, lu_type = landuse_score(lat, lon)

    # 3. Grid proximity
    grid, grid_dist_km, nearest_sub_dict = grid_proximity_score(lat, lon)

    # 4. Risk
    risk = combined_risk_score(lat, lon)

    # 5. Economic
    financials_dict = build_financial_summary(energy_type, weather.avg_wind_speed_50m, weather.ghi_annual_kwh_m2)
    eco = economic_score(financials_dict["payback_years"])

    # Weighted sum
    raw_score = (
        w["resource"] * resource
        + w["landuse"] * lu_score
        + w["grid"] * grid
        + w["risk"] * risk
        + w["economic"] * eco
    )

    # YEKA bonus (additive, capped at 1.0)
    bonus, yeka_info_dict = yeka_bonus(lat, lon)
    final_score = min(1.0, raw_score + bonus) * 100

    breakdown = ScoreBreakdown(
        resource_potential=round(resource, 4),
        land_use=round(lu_score, 4),
        grid_proximity=round(grid, 4),
        risk_factor=round(risk, 4),
        economic_feasibility=round(eco, 4),
    )

    explanation_dict = generate_explanation(
        energy_type=energy_type,
        breakdown=breakdown.model_dump(),
        nearest_sub=nearest_sub_dict,
        yeka_info=yeka_info_dict,
        landuse_type=lu_type,
        financials=financials_dict,
    )
    explanation = ScoreExplanation(**explanation_dict)

    nearest_sub = Substation(**nearest_sub_dict) if nearest_sub_dict else None
    yeka_zone = YekaZone(**yeka_info_dict) if yeka_info_dict and yeka_info_dict.get("bonus", 0) > 0 else None
    financials = FinancialSummary(**financials_dict)

    return ScoreResponse(
        lat=lat,
        lon=lon,
        energy_type=energy_type,
        score=round(final_score, 1),
        breakdown=breakdown,
        explanation=explanation,
        nearest_substation=nearest_sub,
        yeka_zone=yeka_zone,
        financials=financials,
        province_name=province_name,
        province_avg_score=province_avg_score,
    )
