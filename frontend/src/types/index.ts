// Mirror of contracts/schemas.ts — keep in sync

export type EnergyType = "solar" | "wind" | "hybrid";
export type LandUseType = "forest" | "protected" | "residential" | "farmland" | "meadow" | "industrial" | "barren" | "water" | "unknown";
export type WeightsType = "investor" | "individual";

export interface Coordinate { lat: number; lon: number; }

export interface ScoreBreakdown {
  resource_potential: number;
  land_use: number;
  grid_proximity: number;
  risk_factor: number;
  economic_feasibility: number;
}

export interface Substation {
  name?: string | null;
  voltage_kv?: number | null;
  distance_km: number;
  lat: number;
  lon: number;
}

export interface YekaZone {
  name: string;
  radius_km: number;
  lat: number;
  lon: number;
  distance_km: number;
  bonus: number;
}

export interface MaintenanceWindow {
  start_hour_offset: number;
  end_hour_offset: number;
  avg_production_kw: number;
  description: string;
}

export interface FinancialSummary {
  capex_tl: number;
  annual_production_kwh: number;
  payback_years: number;
  lcoe_tl_per_kwh: number;
  capacity_factor: number;
  disclaimer: string;
}

export interface ScoreExplanation {
  summary: string;
  highlights: string[];
  warnings: string[];
}

export interface ScoreResponse {
  lat: number;
  lon: number;
  energy_type: EnergyType;
  score: number;
  breakdown: ScoreBreakdown;
  explanation: ScoreExplanation;
  nearest_substation?: Substation | null;
  yeka_zone?: YekaZone | null;
  financials?: FinancialSummary | null;
  province_name?: string | null;
  province_avg_score?: number | null;
}

export interface ProvinceScore {
  province_id: string;
  province_name: string;
  score: number;
  energy_type: EnergyType;
  centroid_lat: number;
  centroid_lon: number;
  geometry?: object | null;
}

export interface DistrictScore {
  district_id: string;
  district_name: string;
  province_id: string;
  score: number;
  energy_type: EnergyType;
  centroid_lat: number;
  centroid_lon: number;
  geometry?: object | null;
}

export interface ForecastPoint {
  timestamp: string;
  expected_kw: number;
  lower_kw: number;
  upper_kw: number;
  wind_speed_ms?: number | null;
  ghi_w_m2?: number | null;
}

export interface ForecastResponse {
  lat: number;
  lon: number;
  energy_type: EnergyType;
  points: ForecastPoint[];
  maintenance_window?: MaintenanceWindow | null;
}

export interface FilterState {
  hide_forest: boolean;
  show_yeka: boolean;
  grid_max_km?: number | null;
  exclude_high_risk: boolean;
}

export interface CompareResponse {
  score_a: ScoreResponse;
  score_b: ScoreResponse;
  winner: "a" | "b" | "tie";
  delta: number;
}
