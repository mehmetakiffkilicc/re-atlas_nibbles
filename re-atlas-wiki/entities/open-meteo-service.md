---
title: "Open-Meteo Servisi"
tags: [entity, external-api, veri]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Open-Meteo Servisi

Ücretsiz hava durumu API'si. RE-ATLAS'ta canlı hava verisi ve tarihsel veri kaynağı olarak kullanılır.

## Kullanım Alanları

- 81 il merkezi için son 1 yılın saatlik hava verisi (SQLite cache'e yazılır)
- Koordinat bazlı canlı 48 saatlik tahmin
- GHI (Global Horizontal Irradiance) ve rüzgar hızı verileri

## Risk

- Rate limit: 25 saat boyunca yeterliliği belirsiz → demo modunda local JSON fallback zorunlu
- Veri tamlığı: Türkiye'deki tüm ilçe merkezleri için tutarlı veri olup olmadığı kontrol edilmeli

## Bağımlılıklar

- [[entities/sqlite-cache]] — verinin önbelleğe alınması
- [[concepts/demo-mode]] — API çökerse fallback

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/backend-api]]
- [[concepts/physics-based-forecast]]
