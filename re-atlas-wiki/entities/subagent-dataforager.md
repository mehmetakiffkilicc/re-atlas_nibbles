---
title: "Subagent: DataForager"
tags: [entity, subagent, multi-agent, veri]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Subagent: DataForager

Statik veri toplama ve GeoJSON temizleme subagentı. **Veri toplar, skor hesaplamaz.**

## Sorumluluk

- `data-pipeline/scripts/` altındaki scriptleri çalıştırır
- İl/ilçe sınırları GeoJSON (cihadturhan/tr-geojson)
- OSM Overpass landuse (orman/tarım/yerleşim)
- OSM Overpass power (trafo + iletim hatları)
- Open-Meteo hava verisi önbelleği
- Mapshaper ile GeoJSON simplifikasyonu

## Başlangıç Saati

0. saat (SchemaSmith ile paralel)

## Kritik Kontrol

3. saatte veri tamamlanmazsa → Marmara + Ege'ye daralt (16 il)

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[concepts/multi-agent-strateji]]
- [[entities/sqlite-cache]]
- [[entities/open-meteo-service]]
