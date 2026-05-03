---
title: "Karar: Demo Modu Zorunlu"
tags: [decision, risk, demo]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Karar: Demo Modu Zorunlu

**Karar:** `DEMO_MODE=true` ile tüm verinin local JSON'dan okunacağı bir fallback modu zorunlu olarak eklenir.

## Gerekçe

- Demo gecesi internet kesintisi gerçek bir risk
- Open-Meteo rate limit aşılabilir
- Jüri önünde uygulama çöküşünü önlemek kritik
- 3 model hemfikir: demo modu zorunlu

## Uygulama

- `backend/data/cache/demo_weather.json` önceden hazırlanır
- `DEMO_MODE=true` olduğunda tüm harici API çağrıları bu dosyadan döner
- Kullanıcı arayüzünde hiçbir fark gözükmez

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[concepts/demo-mode]]
- [[entities/sqlite-cache]]
