---
title: "RE-ATLAS Proje Bağlam Dokümanı"
tags: [source, proje-genel, mimari, kararlar]
source: raw/docs/project-context.md
date: 2026-05-02
status: active
---

# RE-ATLAS Proje Bağlam Dokümanı

Projenin tek doğruluk kaynağı. Farklı AI modelleri arasında sıfır bağlam kaybıyla geçiş için tasarlandı. Planlama aşaması tamamlandı, uygulama aşamasına geçiliyor.

## Amaç

Türkiye genelinde yenilenebilir enerji yatırım uygunluğunu haritada gösteren ve 48 saatlik üretim tahmini sunan B2B karar destek aracı.

## Ne Anlatılıyor

- Fikrin doğuşu ve çoklu model (Claude + GPT + Gemini) tartışma süreci
- Donmuş kapsam (final özellik listesi)
- Skor motoru formülleri ve ağırlıkları
- Veri katmanları ve öncelikleri
- Teknoloji yığını
- Mimari ve dosya yapısı
- Multi-agent geliştirme stratejisi (6 subagent)
- 25 saatlik çalışma planı ve ekip rolleri
- UX ve tasarım kararları
- Demo akışı (90 saniye)
- Risk yönetimi tablosu
- Açık sorular

## Anahtar Noktalar

- **Ana persona:** Enerji yatırımcısı / saha geliştirme uzmanı (B2B) — tek mod, diğer personalar demoda sözlü anlatılır
- **Çözünürlük:** Çift seviye gerçek choropleth (zoom out → 81 il, zoom in → ~973 ilçe) — fake heatmap kesinlikle yasak
- **Tahmin modeli:** Prophet + fizik formülü (LSTM 3 model tarafından oybirliğiyle reddedildi)
- **Harita:** Leaflet + OSM dark theme (Google Maps kota/maliyet riski nedeniyle reddedildi)
- **Demo güvenliği:** `DEMO_MODE=true` ile tüm veri local JSON'dan okunur
- **Feature freeze:** 12. saatte — sonrası sadece bug fix
- **Veri kaynakları (zorunlu):** Open-Meteo API, cihadturhan/tr-geojson, OSM Overpass (landuse + power)

## Kararlar

- [[decisions/karar-prophet-vs-lstm]] — LSTM iptal, Prophet + fizik formülü seçildi
- [[decisions/karar-leaflet-vs-googlemaps]] — Leaflet + OSM seçildi
- [[decisions/karar-tek-mod]] — Tek kullanıcı modu (yatırımcı), çoklu mod reddedildi
- [[decisions/karar-cift-seviye-choropleth]] — Çift seviye gerçek choropleth, fake heatmap yasak
- [[decisions/karar-feature-freeze-12saat]] — 12. saatte feature freeze
- [[decisions/karar-demo-modu]] — Demo modu zorunlu risk mitigasyonu

## Açık Konular

- Zustand mu Redux mu? (Önerilen: Zustand — subagent kararı)
- Recharts mı Chart.js mi? (Önerilen: Recharts — subagent kararı)
- TEİAŞ trafo verisinin OSM'de tamlığı (yarışma başında kontrol)
- Open-Meteo rate limit yeterliliği (25 saat boyunca)
- Mapshaper Windows'ta sorunsuz mu

## Sources

- [[raw/docs/project-context.md]]

## Related

- [[entities/backend-api]]
- [[entities/frontend-map]]
- [[entities/open-meteo-service]]
- [[entities/sqlite-cache]]
- [[entities/subagent-schemasmith]]
- [[entities/subagent-dataforager]]
- [[entities/subagent-scoresmith]]
- [[entities/subagent-apiweaver]]
- [[entities/subagent-mapforge]]
- [[entities/subagent-forecastsage]]
- [[concepts/choropleth-map]]
- [[concepts/physics-based-forecast]]
- [[concepts/skor-motoru]]
- [[concepts/demo-mode]]
- [[concepts/feature-freeze]]
- [[concepts/multi-agent-strateji]]
