---
title: "Backend API"
tags: [entity, backend, fastapi]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Backend API

Python 3.11 + FastAPI + Pydantic v2 ile yazılan REST API. Skor motoru, tahmin ve veri endpoint'lerini sunar.

## Endpoint'ler

| Endpoint | Açıklama |
|---|---|
| `GET /api/health` | Sağlık kontrolü |
| `GET /api/score?lat={}&lon={}&type={solar\|wind\|hybrid}` | Koordinat bazlı uygunluk skoru |
| `GET /api/provinces` | 81 il GeoJSON + skor |
| `GET /api/districts?province_id={}` | İlçe GeoJSON + skor |
| `GET /api/forecast?lat={}&lon={}&hours=48` | 48 saatlik üretim tahmini |
| `GET /api/top?type={}&n=5` | En iyi N nokta |
| `GET /api/nearest-substation?lat={}&lon={}` | En yakın trafo |
| `GET /api/landuse?lat={}&lon={}` | Arazi kullanım türü |

## Klasör yapısı

```
backend/app/
├── main.py
├── routers/        ← score.py, forecast.py, provinces.py, districts.py, top.py
├── scoring/        ← engine.py, physics.py, landuse.py, grid_proximity.py, weights.py
├── forecast/       ← physics_forecast.py, prophet_wrapper.py, maintenance_window.py
└── services/       ← openmeteo.py, cache.py, landuse_lookup.py, substation_lookup.py
```

## Bağımlılıklar

- [[entities/open-meteo-service]] — hava verisi
- [[entities/sqlite-cache]] — önbellek
- [[concepts/skor-motoru]] — hesaplama mantığı
- [[concepts/physics-based-forecast]] — tahmin mantığı

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/frontend-map]]
- [[entities/subagent-apiweaver]]
- [[entities/subagent-scoresmith]]
