from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


EnergyType = Literal["solar", "wind", "hybrid"]

LandUseType = Literal[
    "forest", "protected", "residential", "farmland",
    "meadow", "industrial", "barren", "water", "unknown"
]


class Coordinate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"lat": 40.213, "lon": 28.366}})

    lat: float = Field(..., ge=-90, le=90, description="Enlem")
    lon: float = Field(..., ge=-180, le=180, description="Boylam")


class ScoreRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "lat": 40.213, "lon": 28.366, "energy_type": "wind", "weights": "investor"
    }})

    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    energy_type: EnergyType = Field(default="hybrid")
    weights: Literal["investor", "individual"] = Field(default="investor")


class ScoreBreakdown(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "resource_potential": 0.82, "land_use": 0.70, "grid_proximity": 0.95,
        "risk_factor": 0.85, "economic_feasibility": 0.65
    }})

    resource_potential: float = Field(..., ge=0, le=1)
    land_use: float = Field(..., ge=0, le=1)
    grid_proximity: float = Field(..., ge=0, le=1)
    risk_factor: float = Field(..., ge=0, le=1)
    economic_feasibility: float = Field(..., ge=0, le=1)


class Substation(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "name": "Karacabey TM", "voltage_kv": 154, "distance_km": 3.2,
        "lat": 40.215, "lon": 28.370
    }})

    name: Optional[str] = None
    voltage_kv: Optional[float] = None
    distance_km: float = Field(..., ge=0)
    lat: float
    lon: float


class YekaZone(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "name": "Karapınar YEKA", "radius_km": 50, "lat": 37.72, "lon": 33.55,
        "distance_km": 12.3, "bonus": 0.10
    }})

    name: str
    radius_km: float
    lat: float
    lon: float
    distance_km: float
    bonus: float = Field(..., ge=0, le=0.10)


class MaintenanceWindow(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "start_hour_offset": 14, "end_hour_offset": 17,
        "avg_production_kw": 42.5, "description": "Yarın 14:00-17:00 arası bakım için uygun pencere."
    }})

    start_hour_offset: int = Field(..., ge=0, le=47, description="Şu andan kaç saat sonra başlar")
    end_hour_offset: int = Field(..., ge=1, le=48)
    avg_production_kw: float = Field(..., ge=0)
    description: str


class FinancialSummary(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "capex_tl": 90_000_000, "annual_production_kwh": 5_256_000,
        "payback_years": 8.5, "lcoe_tl_per_kwh": 0.82,
        "capacity_factor": 0.30, "disclaimer": "Ön değerlendirme amaçlıdır."
    }})

    capex_tl: float
    annual_production_kwh: float
    payback_years: float
    lcoe_tl_per_kwh: float
    capacity_factor: float
    disclaimer: str = "Ön değerlendirme amaçlıdır. Yatırım kararı için saha ölçümü gereklidir."


class ScoreExplanation(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "summary": "Karacabey bölgesi rüzgar için yüksek potansiyel sunuyor.",
        "highlights": ["Şebekeye 3.2 km mesafe", "Tarım arazisi — uygun arazi"],
        "warnings": []
    }})

    summary: str
    highlights: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class WeatherSummary(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "avg_wind_speed_50m": 7.2, "avg_wind_speed_100m": 8.1,
        "ghi_annual_kwh_m2": 1650.0, "avg_temperature_c": 13.5, "data_year": 2024
    }})

    avg_wind_speed_50m: float = Field(..., description="50m yükseklikteki yıllık ortalama rüzgar hızı (m/s)")
    avg_wind_speed_100m: Optional[float] = Field(None, description="100m yükseklikteki yıllık ortalama rüzgar hızı (m/s) — NASA POWER WS100M")
    ghi_annual_kwh_m2: float = Field(..., description="Yıllık toplam güneş ışınımı (kWh/m²)")
    avg_temperature_c: float
    data_year: int = 2024


class ScoreResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "lat": 40.213, "lon": 28.366, "energy_type": "wind",
        "score": 84.0, "breakdown": {}, "explanation": {},
        "nearest_substation": {}, "yeka_zone": None, "financials": {}
    }})

    lat: float
    lon: float
    energy_type: EnergyType
    score: float = Field(..., ge=0, le=100)
    breakdown: ScoreBreakdown
    explanation: ScoreExplanation
    nearest_substation: Optional[Substation] = None
    yeka_zone: Optional[YekaZone] = None
    financials: Optional[FinancialSummary] = None
    province_name: Optional[str] = None
    province_avg_score: Optional[float] = None


class ProvinceScore(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "province_id": "16", "province_name": "Bursa",
        "score": 78.0, "energy_type": "wind", "centroid_lat": 40.18, "centroid_lon": 29.06
    }})

    province_id: str
    province_name: str
    score: float = Field(..., ge=0, le=100)
    energy_type: EnergyType
    centroid_lat: float
    centroid_lon: float
    geometry: Optional[dict] = Field(default=None, description="GeoJSON geometry")


class DistrictScore(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "district_id": "1601", "district_name": "Karacabey", "province_id": "16",
        "score": 84.0, "energy_type": "wind", "centroid_lat": 40.213, "centroid_lon": 28.366
    }})

    district_id: str
    district_name: str
    province_id: str
    score: float = Field(..., ge=0, le=100)
    energy_type: EnergyType
    centroid_lat: float
    centroid_lon: float
    geometry: Optional[dict] = Field(default=None, description="GeoJSON geometry")


class ForecastPoint(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "timestamp": "2026-05-03T14:00:00Z",
        "expected_kw": 850.0, "lower_kw": 722.5, "upper_kw": 977.5,
        "wind_speed_ms": 7.2, "ghi_w_m2": 0.0
    }})

    timestamp: str = Field(..., description="ISO 8601 UTC")
    expected_kw: float = Field(..., ge=0)
    lower_kw: float = Field(..., ge=0)
    upper_kw: float = Field(..., ge=0)
    wind_speed_ms: Optional[float] = None
    ghi_w_m2: Optional[float] = None


class ForecastResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "lat": 40.213, "lon": 28.366, "energy_type": "wind",
        "points": [], "maintenance_window": {}
    }})

    lat: float
    lon: float
    energy_type: EnergyType
    points: list[ForecastPoint]
    maintenance_window: Optional[MaintenanceWindow] = None


class FilterState(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "hide_forest": False, "show_yeka": False,
        "grid_max_km": None, "exclude_high_risk": False
    }})

    hide_forest: bool = False
    show_yeka: bool = False
    grid_max_km: Optional[float] = None
    exclude_high_risk: bool = False


class CompareRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "point_a": {"lat": 40.213, "lon": 28.366},
        "point_b": {"lat": 38.733, "lon": 35.485},
        "energy_type": "wind"
    }})

    point_a: Coordinate
    point_b: Coordinate
    energy_type: EnergyType = "hybrid"
    weights: Literal["investor", "individual"] = "investor"


class CompareResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {
        "score_a": {}, "score_b": {}, "winner": "a", "delta": 5.0
    }})

    score_a: ScoreResponse
    score_b: ScoreResponse
    winner: Literal["a", "b", "tie"]
    delta: float = Field(..., description="Mutlak skor farkı")
