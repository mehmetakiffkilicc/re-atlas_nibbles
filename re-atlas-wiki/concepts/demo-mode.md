---
title: "Demo Modu"
tags: [concept, risk, demo, fallback]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Demo Modu

`DEMO_MODE=true` ortam değişkeniyle aktive edilen fallback mekanizması. API veya internet bağlantısı çöktüğünde tüm veriyi local JSON'dan okur.

## Neden Zorunlu

- Demo gecesi internet kesintisi riski
- Open-Meteo rate limit aşılması riski
- Jüri önünde "uygulama çalışmıyor" senaryosunu engellemek

## Nasıl Çalışır

- `backend/data/cache/demo_weather.json` önceden doldurulur
- `DEMO_MODE=true` olduğunda tüm API çağrıları bu dosyadan döner
- Kullanıcı arayüzünde hiçbir fark yoktur

## Üç Model Hemfikir Karar

Cache stratejisi ve demo modu zorunlu olarak kararlaştırıldı — tüm modeller (Claude + GPT + Gemini) bu konuda hemfikirdi.

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/sqlite-cache]]
- [[entities/open-meteo-service]]
- [[decisions/karar-demo-modu]]
