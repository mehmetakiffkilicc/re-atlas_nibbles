---
title: "Hackathon Proje Planı — Detaylı Tasarım"
tags: [source, proje-genel, mimari, veri, ux]
source: raw/docs/hackathon-plani.md
date: 2026-05-02
status: active
---

# Hackathon Proje Planı — Detaylı Tasarım

`PROJECT_CONTEXT.md`'nin detaylı versiyonu. Kararların arkasındaki gerekçeler, alternatiflerin değerlendirmesi, uygulama spesifikasyonları ve kod örnekleri burada.

## Amaç

Proje planı, bakım yapanlar ve jüri için kapsamlı referans. Karar Defteri (Bölüm 16) değişiklik tarihçesi tutar.

## Anahtar Noktalar

- **Skor formülü** tüm bileşenlerin Python kodu düzeyinde spesifike edilmiş (kaynak/arazi/şebeke/risk/YEKA bonus/ekonomik)
- **Tahmin modülü** iki katmanlı: Fizik tabanlı (birincil) + Prophet (opsiyonel, 12. saat kesim)
- **Veri pipeline** 6 katman: il/ilçe GeoJSON, OSM landuse (bölgesel parçalama), OSM power, AFAD fay hatları, YEKA bölgeleri, Open-Meteo cache
- **CSS değişkenleri** ve tipografi tam tanımlanmış
- **Acil durum planları** A/B/C/D: veri patlarsa, backend patlarsa, frontend patlarsa, ekip düşerse
- **Demo koordinatları** önceden seçilmiş (Karacabey/Bursa rüzgar, Kayseri güneş, Tuz Gölü hibrit)
- **Performans hedefleri**: FCP <1.5s, TTI <3s, API yanıtı <500ms, bundle <500KB gzipped
- **Test koordinatları**: Karacabey(40.213,28.366)=yüksek rüzgar, Kayseri(38.733,35.485)=yüksek güneş, Çamlıca(41.025,29.066)=düşük(yerleşim), Tuz Gölü(38.737,33.371)=hibrit, Çatalca(41.218,28.450)=düşük(orman)

## Kararlar

- [[decisions/karar-prophet-vs-lstm]]
- [[decisions/karar-leaflet-vs-googlemaps]]
- [[decisions/karar-tek-mod]]
- [[decisions/karar-cift-seviye-choropleth]]
- [[decisions/karar-feature-freeze-12saat]]
- [[decisions/karar-demo-modu]]
- [[decisions/karar-yeka-bonus]]
- [[decisions/karar-veri-darbogazı-fallback]]

## Açık Konular

- Finans kart mock değerleri gerçek veriye göre kalibre edilmeli
- AFAD fay hattı verisi OSM'de ne kadar tam (yarışma başında kontrol)
- Prophet Windows kurulumu sorunlu olabilir (fallback: sadece fizik)
- OSM Overpass rate limit için bölgesel parçalama stratejisi uygulanmalı

## Sources

- [[raw/docs/hackathon-plani.md]]

## Related

- [[sources/docs/2026-05-02-project-context]]
- [[sources/docs/2026-05-02-master-prompt]]
- [[concepts/skor-motoru]]
- [[concepts/physics-based-forecast]]
- [[concepts/veri-pipeline]]
- [[entities/backend-api]]
- [[entities/frontend-map]]
