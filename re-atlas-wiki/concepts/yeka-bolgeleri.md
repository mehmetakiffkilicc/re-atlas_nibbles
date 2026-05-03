---
title: "YEKA Bölgeleri"
tags: [concept, veri, enerji-politikası, bonus]
source: sources/docs/2026-05-02-master-prompt.md
date: 2026-05-02
status: active
---

# YEKA Bölgeleri

Yenilenebilir Enerji Kaynak Alanları — Enerji Bakanlığı'nın tahsis ettiği özel bölgeler. RE-ATLAS'ta uygunluk skoruna bonus olarak yansıtılır.

## Skor Etkisi

- YEKA bölgesi **içindeyse** → `yeka_bonus = +0.10`
- YEKA'ya **20 km içindeyse** → `yeka_bonus = +0.05`
- **Dışındaysa** → bonus yok
- Bonus ana skor formülüne **eklenir** (ağırlıklı bileşen DEĞİL): `final_score = base_score + yeka_bonus`

## 10 Hazır YEKA Noktası (Manuel Girilecek)

| Ad | Tip | Kapasite | Koordinat | Durum |
|---|---|---|---|---|
| Karapınar YEKA-GES | solar | 1000 MW | 37.72°N, 33.55°E | active |
| Kıyıköy YEKA-RES | wind | 500 MW | 41.63°N, 28.10°E | active |
| Saros YEKA-RES | wind | 450 MW | 40.60°N, 26.60°E | active |
| Akhisar YEKA-RES | wind | 600 MW | 38.92°N, 27.84°E | active |
| Niğde-Bor YEKA-GES | solar | 500 MW | 37.89°N, 34.56°E | planned |
| Şanlıurfa YEKA-GES | solar | 500 MW | 37.16°N, 38.79°E | active |
| Hatay YEKA-RES | wind | 400 MW | 36.40°N, 36.17°E | active |
| Konya Kulu YEKA-GES | solar | 500 MW | 39.09°N, 33.08°E | planned |
| Balıkesir YEKA-RES | wind | 550 MW | 39.65°N, 28.00°E | active |
| Muğla YEKA-RES | wind | 350 MW | 37.22°N, 28.36°E | active |

## Veri Dosyası

`data-pipeline/static/yeka_zones.json` → `backend/data/yeka_zones.geojson`

## Frontend Gösterimi

Haritada yarı saydam daire overlay. Filtre panelinde "YEKA bölgelerini göster" checkbox'ı.

## Sources

- [[sources/docs/2026-05-02-master-prompt.md]]
- [[sources/docs/2026-05-02-hackathon-plani.md]]

## Related

- [[decisions/karar-yeka-bonus]]
- [[entities/subagent-dataforager]]
- [[entities/subagent-scoresmith]]
- [[concepts/skor-motoru]]
