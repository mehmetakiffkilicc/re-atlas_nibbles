---
title: "SQLite Cache"
tags: [entity, backend, veri-tabani]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# SQLite Cache

Hava verisi ve statik coğrafi verilerin önbelleğe alındığı SQLite veritabanı.

## İçerik

- `weather_yearly.sqlite` — 81 il merkezi için son 1 yılın saatlik hava verisi
- `demo_weather.json` — Demo modu için local JSON fallback

## Konum

```
backend/data/cache/
├── weather_yearly.sqlite
└── demo_weather.json
```

## Amaç

- Open-Meteo API rate limit riskini azaltmak
- Demo gecesi internet kesilirse uygulamanın çalışmaya devam etmesi
- Veri pipeline'ının bir kez çalıştırılıp sonuçların tekrar kullanılması

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/open-meteo-service]]
- [[entities/backend-api]]
- [[concepts/demo-mode]]
