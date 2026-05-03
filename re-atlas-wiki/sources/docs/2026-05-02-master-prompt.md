---
title: "Claude Code Master Prompt — Orkestrasyon Sistemi"
tags: [source, multi-agent, claude-code, subagent]
source: raw/docs/master-prompt.md
date: 2026-05-02
status: active
---

# Claude Code Master Prompt — Orkestrasyon Sistemi

Claude Code'da 1 orkestratör + 6 subagent yapısının tam prompt tanımı. Her subagent için sistem promptu, çıktı dosyaları, yetki sınırları ve kapatma kriterleri içerir.

## Amaç

Hackathon sürecinde farklı Claude Code oturumlarında çalışacak subagentların tam spesifikasyonu. Her subagent bu promptla başlatılır.

## Anahtar Noktalar

- **Orkestratör (Architect)**: Subagentları sırayla başlatır, tip uyumsuzluğunda müdahale eder, 12. saat freeze'i zorlar, koda yorum İngilizce/kullanıcıya Türkçe
- **SchemaSmith prompt özeti**: `contracts/` klasöründe sadece tip yazar. Kritik tipler: ScoreRequest/Response, Coordinate, EnergyType, ProvinceScore, ForecastPoint, LandUseType, Substation, YekaZone, MaintenanceWindow, ScoreBreakdown, FinancialSummary, FilterState, WeatherSummary, CompareRequest/Response
- **DataForager prompt özeti**: 6 veri katmanını toplar. OSM landuse için 7 bölge bbox parçalama stratejisi. YEKA bölgeleri manuel 10 nokta. SQLite cache schema tanımlı.
- **ScoreSmith prompt özeti**: Tüm skor bileşenleri Python kodu düzeyinde: solar/wind_resource_score, LANDUSE_SCORES dict, grid_proximity_score, seismic_risk_score, yeka_bonus, economic_score, LCOE, explainer. R-tree spatial index zorunlu.
- **APIWeaver prompt özeti**: FastAPI endpoint'leri, CORS (localhost:5173), cache stratejisi (1 saatlik TTL), demo modu
- **MapForge prompt özeti**: React+Leaflet UI, tasarım sistemi CSS değişkenleri, layout ASCII, detay panel 8 bileşen, tutarlılık cümlesi ZORUNLU, Lighthouse >80
- **ForecastSage prompt özeti**: physics_forecast.py birincil, prophet_wrapper.py opsiyonel, maintenance_window.py. LSTM kesinlikle yasak.

## Subagent Başlatma Şablonu

```
Sen [SUBAGENT_ADI] subagent'isin. Kapsam dışına çıkmak YASAKTIR.
Çalışma klasörün: [KLASÖR]
Bağımlılıkların: [LİSTE]
Çıktı dosyaların: [LİSTE]
Kapatma kriterin: [KRİTER]
Master plan: hackathon-proje-plani.md
```

## YEKA Bölgeleri (Manuel Girilecek 10 Nokta)

| Ad | Tip | Kapasite | Koordinat | Durum |
|---|---|---|---|---|
| Karapınar YEKA-GES | solar | 1000 MW | 37.72, 33.55 | active |
| Kıyıköy YEKA-RES | wind | 500 MW | 41.63, 28.10 | active |
| Saros YEKA-RES | wind | 450 MW | 40.60, 26.60 | active |
| Akhisar YEKA-RES | wind | 600 MW | 38.92, 27.84 | active |
| Niğde-Bor YEKA-GES | solar | 500 MW | 37.89, 34.56 | planned |
| Şanlıurfa YEKA-GES | solar | 500 MW | 37.16, 38.79 | active |
| Hatay YEKA-RES | wind | 400 MW | 36.40, 36.17 | active |
| Konya Kulu YEKA-GES | solar | 500 MW | 39.09, 33.08 | planned |
| Balıkesir YEKA-RES | wind | 550 MW | 39.65, 28.00 | active |
| Muğla YEKA-RES | wind | 350 MW | 37.22, 28.36 | active |

## Açık Konular

- Subagentların bağımlılık sırasına uyulması kritik (SchemaSmith hepsinden önce bitmeli)
- Her API anahtarı `.env` dosyasından okunmalı, koda gömülmemeli

## Sources

- [[raw/docs/master-prompt.md]]

## Related

- [[sources/docs/2026-05-02-project-context]]
- [[sources/docs/2026-05-02-hackathon-plani]]
- [[concepts/multi-agent-strateji]]
- [[entities/subagent-schemasmith]]
- [[entities/subagent-dataforager]]
- [[entities/subagent-scoresmith]]
- [[entities/subagent-apiweaver]]
- [[entities/subagent-mapforge]]
- [[entities/subagent-forecastsage]]
- [[concepts/yeka-bolgeleri]]
