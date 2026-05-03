---
title: "Veri Pipeline"
tags: [concept, veri, pipeline, osm, geojson]
source: sources/docs/2026-05-02-hackathon-plani.md
date: 2026-05-02
status: active
---

# Veri Pipeline

RE-ATLAS'ın statik veri katmanlarını hazırlayan pipeline. [[entities/subagent-dataforager]] tarafından yürütülür.

## 6 Veri Katmanı

| Katman | Kaynak | Öncelik | Boyut Hedefi |
|---|---|---|---|
| İl/ilçe GeoJSON | cihadturhan/tr-geojson veya GADM | ZORUNLU | İl <500KB, ilçe <2MB |
| OSM landuse | Overpass API (7 bölge bbox) | ZORUNLU | <5MB |
| OSM power (trafo+hat) | Overpass API | YÜKSEK | Trafo <500KB, hat <2MB |
| AFAD fay hatları | MTA / OSM geological=fault | OPSİYONEL | ~1MB |
| YEKA bölgeleri | Manuel (10 nokta) | OPSİYONEL | <1KB |
| Open-Meteo cache | archive-api.open-meteo.com | ZORUNLU | ~28MB SQLite |

## OSM Landuse Parçalama Stratejisi

Tüm Türkiye landuse sorgusu 100+ MB döndürebilir. Çözüm: **7 coğrafi bölge bbox** ile ayrı ayrı sorgu:

```python
REGIONS = {
    "marmara":    {"south": 39.5, "west": 26.0, "north": 42.1, "east": 30.5},
    "ege":        {"south": 36.5, "west": 25.5, "north": 39.8, "east": 30.0},
    "akdeniz":    {"south": 36.0, "west": 29.5, "north": 38.0, "east": 36.5},
    "ic_anadolu": {"south": 37.5, "west": 30.0, "north": 41.0, "east": 36.5},
    "karadeniz":  {"south": 40.0, "west": 30.5, "north": 42.1, "east": 41.5},
    "dogu":       {"south": 37.0, "west": 36.5, "north": 42.0, "east": 44.8},
    "guneydogu":  {"south": 36.5, "west": 36.0, "north": 38.5, "east": 44.8},
}
```

## Open-Meteo Cache Schema (SQLite)

```sql
CREATE TABLE weather_cache (
    province_id TEXT,
    timestamp TEXT,
    wind_speed_10m REAL, wind_speed_100m REAL,
    wind_direction_10m REAL, wind_direction_100m REAL,
    ghi REAL, dni REAL,
    temperature REAL, cloud_cover REAL, humidity REAL,
    PRIMARY KEY (province_id, timestamp)
);
```

81 il × 8760 saat = ~710.000 satır, ~28MB.

## GeoJSON Optimizasyonu (Mapshaper)

```bash
# İl sınırları
mapshaper provinces_raw.geojson -simplify dp 10% -o provinces.geojson

# OSM landuse (tip filtresi + basitleştirme)
mapshaper landuse_raw.geojson \
  -filter '["forest","farmland","residential","industrial"].includes(landuse)' \
  -simplify 5% -o landuse.geojson
```

## Fallback: 3. Saat Kontrolü

Tüm Türkiye OSM verisi 3. saatte hazır değilse → **Marmara + Ege (16 il)** yeterlidir. Yatırım yoğunluğu zaten bu bölgelerde.

## Sources

- [[sources/docs/2026-05-02-hackathon-plani.md]]
- [[sources/docs/2026-05-02-master-prompt.md]]

## Related

- [[entities/subagent-dataforager]]
- [[entities/sqlite-cache]]
- [[entities/open-meteo-service]]
- [[decisions/karar-veri-darbogazı-fallback]]
- [[concepts/skor-motoru]]
