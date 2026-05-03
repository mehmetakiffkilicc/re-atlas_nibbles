---
title: "Karar: Leaflet + OSM (Google Maps Reddedildi)"
tags: [decision, harita, frontend]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Karar: Leaflet + OSM (Google Maps Reddedildi)

**Karar:** Harita kütüphanesi olarak Leaflet + OpenStreetMap seçildi. Google Maps API reddedildi.

## Gerekçe

- Google Maps API: faturalandırma riski, demo gecesi kota dolar, choropleth desteği zayıf
- Leaflet + OSM: ücretsiz, API kotası yok, GeoJSON choropleth için güçlü destek
- 3 model hemfikir

## Kullanıcının İlk Tercihi

Kullanıcı başlangıçta Google Maps'i tercih etti. Claude'un uyarısıyla (kota/maliyet riski) Leaflet'e geçildi.

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/leaflet-map]]
- [[entities/frontend-map]]
- [[concepts/choropleth-map]]
