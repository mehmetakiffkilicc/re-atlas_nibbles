---
title: "Karar: Veri Darboğazı Fallback — Marmara+Ege"
tags: [decision, risk, veri]
source: sources/docs/2026-05-02-hackathon-plani.md
date: 2026-05-02
status: active
---

# Karar: Veri Darboğazı Fallback — Marmara+Ege

**Karar:** 3. saatte tüm Türkiye OSM landuse verisi hazır değilse, kapsam otomatik olarak Marmara + Ege bölgelerine (16 il) daraltılır.

## Gerekçe

- OSM Overpass API büyük sorguları zaman zaman yavaş yanıt verebilir
- 16 il, Türkiye'nin yenilenebilir enerji yoğunluğunu temsil eder (Ege rüzgar, Marmara şebeke yakınlığı)
- Demo akışını bozmaz, jüriye hikaye anlatımı yapılabilir

## Kontrol Kriteri

3. saat sonunda:
- ✓ İl sınırları alındı
- ✓ Open-Meteo cache hazır
- ✗ OSM landuse 30 dakikadan fazla sürüyor → Fallback tetiklenir

## Sources

- [[sources/docs/2026-05-02-hackathon-plani.md]]

## Related

- [[concepts/veri-pipeline]]
- [[entities/subagent-dataforager]]
