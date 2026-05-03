---
title: "Leaflet Harita Kütüphanesi"
tags: [entity, frontend, harita, external-lib]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Leaflet Harita Kütüphanesi

Açık kaynak, ücretsiz JavaScript harita kütüphanesi. RE-ATLAS'ta Google Maps'e alternatif olarak seçildi.

## Neden Leaflet

- Ücretsiz, API kotası yok
- OSM (OpenStreetMap) tile'larıyla çalışır
- Choropleth (renk kodlu bölge) gösterimi için güçlü GeoJSON desteği
- React entegrasyonu: `react-leaflet` paketi

## Harita Teması

CartoDB Dark Matter veya Stadia Maps Dark — koyu arka plan üzerinde renk kodlu bölgeler yüksek kontrast sağlar.

## Karar Geçmişi

- [[decisions/karar-leaflet-vs-googlemaps]] — Google Maps API kota ve maliyet riski nedeniyle reddedildi

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/frontend-map]]
- [[concepts/choropleth-map]]
