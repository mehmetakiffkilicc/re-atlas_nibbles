---
title: "Contracts — Tip Sözleşmeleri"
tags: [entity, backend, frontend, typescript, pydantic]
source: sources/docs/2026-05-02-master-prompt.md
date: 2026-05-02
status: active
---

# Contracts — Tip Sözleşmeleri

Projenin tek tip doğruluk kaynağı. [[entities/subagent-schemasmith]] tarafından yazılır, her subagent bu sözleşmelere uyar.

## Dosyalar

- `contracts/schemas.py` — Pydantic v2 modelleri
- `contracts/schemas.ts` — TypeScript tipleri (birebir eşleşmeli)
- `contracts/README.md` — tip açıklamaları

## Kritik Tipler

| Tip | Açıklama |
|---|---|
| `ScoreRequest` | lat, lon, energy_type |
| `ScoreResponse` | score, energy_type, breakdown, explanation, financials |
| `Coordinate` | lat, lon |
| `EnergyType` | enum: solar / wind / hybrid |
| `ProvinceScore` | province_id, name, score, energy_type |
| `DistrictScore` | district_id, name, score |
| `ForecastPoint` | timestamp, expected_kw, lower_kw, upper_kw |
| `ForecastResponse` | points, maintenance_window |
| `LandUseType` | enum: forest/farmland/residential/industrial/meadow/barren/military/protected/default |
| `Substation` | name, voltage_kv, distance_km, type |
| `YekaZone` | name, type, capacity_mw, distance_km, status, radius_km |
| `MaintenanceWindow` | start_time, end_time, avg_production_kw, description |
| `ScoreBreakdown` | resource, landuse, grid_proximity, risk, economic, yeka_bonus |
| `FinancialSummary` | capex_tl, annual_production_kwh, payback_years, lcoe_tl_kwh |
| `FilterState` | show_forests, show_yeka, trafo_within_km, exclude_high_risk, energy_type |
| `WeatherSummary` | avg_wind_10m, avg_wind_100m, avg_ghi, avg_temperature |
| `CompareRequest` | point_a, point_b, energy_type |
| `CompareResponse` | score_a, score_b |

## Kural

Tip değişirse SchemaSmith günceller, hem Python hem TypeScript güncellenir. Yarısı bırakılmaz — tip uyumsuzluğu = anında dur.

## Sources

- [[sources/docs/2026-05-02-master-prompt.md]]

## Related

- [[entities/subagent-schemasmith]]
- [[entities/backend-api]]
- [[entities/frontend-map]]
