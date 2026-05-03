# RE-ATLAS Wiki — İçerik Kataloğu

Her ingest sonrası güncellenir. Query'de ilk okunan dosya budur.

---

## Kaynaklar (sources/)

### sources/docs/
- [[sources/docs/2026-05-02-project-context]] — RE-ATLAS proje bağlamı: kararlar, mimari, skor formülleri, 25 saatlik plan
- [[sources/docs/2026-05-02-hackathon-plani]] — Detaylı tasarım: Python kod örnekleri, UX detayları, acil durum planları, demo koordinatları
- [[sources/docs/2026-05-02-master-prompt]] — Claude Code orkestrasyon sistemi: 6 subagent prompt tanımı, YEKA verileri, başlatma protokolü
- [[sources/docs/2026-05-02-frontend-modernization-start]] — Frontend modernizasyon süreci başlangıcı ve Antigravity devri

---


## Varlıklar (entities/)

**Backend:**
- [[entities/backend-api]] — FastAPI REST API, tüm endpoint'ler ve yanıt süreleri
- [[entities/open-meteo-service]] — Ücretsiz hava API, rate limit riski
- [[entities/sqlite-cache]] — Hava verisi ve demo fallback önbelleği
- [[entities/contracts-schema]] — Pydantic+TypeScript tip sözleşmeleri (tek doğruluk kaynağı)
- [[entities/demo-koordinatlar]] — Önceden seçilmiş test/demo koordinatları

**Frontend:**
- [[entities/frontend-map]] — React 18 + Vite + TypeScript + Leaflet harita uygulaması
- [[entities/leaflet-map]] — Açık kaynak harita kütüphanesi (Google Maps alternatifi)

**Subagentlar:**
- [[entities/subagent-schemasmith]] — Tip sözleşmeleri, 0. saat
- [[entities/subagent-dataforager]] — Statik veri toplama + GeoJSON, 0. saat
- [[entities/subagent-scoresmith]] — Skor motoru + fizik formülleri + YEKA + ekonomik, 2. saat
- [[entities/subagent-apiweaver]] — FastAPI endpoint'leri + Open-Meteo entegrasyonu, 4. saat
- [[entities/subagent-mapforge]] — React + Leaflet UI bileşenleri, 4. saat
- [[entities/subagent-forecastsage]] — 48 saatlik tahmin + bakım penceresi, 8. saat

---

## Kavramlar (concepts/)

**Mimari:**
- [[concepts/choropleth-map]] — Çift seviye gerçek choropleth, fake heatmap yasak
- [[concepts/physics-based-forecast]] — Fizik formülleri + Prophet, LSTM neden reddedildi
- [[concepts/skor-motoru]] — Uygunluk skoru formülü, 6 bileşen, ağırlıklar
- [[concepts/veri-pipeline]] — 6 veri katmanı, OSM parçalama stratejisi, GeoJSON optimizasyonu
- [[concepts/multi-agent-strateji]] — 1 orkestratör + 6 subagent yapısı

**UX:**
- [[concepts/tasarim-sistemi]] — CSS değişkenleri, tipografi, performans hedefleri, erişilebilirlik
- [[concepts/finansal-kart]] — CAPEX/geri ödeme/LCOE, sabit varsayımlar, disclaimer

**Risk & Operasyon:**
- [[concepts/demo-mode]] — `DEMO_MODE=true` fallback mekanizması
- [[concepts/feature-freeze]] — 12. saatte kapsam dondurma
- [[concepts/yeka-bolgeleri]] — 10 YEKA noktası, bonus hesabı, frontend gösterimi

---

## Kararlar (decisions/)

- [[decisions/karar-prophet-vs-lstm]] — LSTM iptal, Prophet + fizik seçildi
- [[decisions/karar-leaflet-vs-googlemaps]] — Leaflet + OSM, Google Maps reddedildi
- [[decisions/karar-tek-mod]] — Tek kullanıcı modu (yatırımcı persona)
- [[decisions/karar-cift-seviye-choropleth]] — Çift seviye gerçek choropleth, fake heatmap yasak
- [[decisions/karar-feature-freeze-12saat]] — 12. saatte feature freeze
- [[decisions/karar-demo-modu]] — Demo modu zorunlu
- [[decisions/karar-yeka-bonus]] — YEKA bonus ana skora eklenir (ağırlıklı bileşen değil)
- [[decisions/karar-veri-darbogazı-fallback]] — 3. saatte OSM gelmezse Marmara+Ege (16 il)

---

## Sorunlar (issues/)

_(Henüz kayıtlı sorun yok — geliştirme başlamadı)_

---

## Sentezler (syntheses/)

_(Henüz sentez sayfası yok)_

---

## Arşiv (archive/)

_(Henüz arşivlenen sayfa yok)_

---

_Son güncelleme: 2026-05-02 | Toplam sayfa: 33 (3 source + 13 entity + 10 concept + 8 decision)_
