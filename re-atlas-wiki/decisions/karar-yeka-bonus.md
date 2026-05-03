---
title: "Karar: YEKA Bölgesi Bonus Sistemi"
tags: [decision, skor, veri]
source: sources/docs/2026-05-02-master-prompt.md
date: 2026-05-02
status: active
---

# Karar: YEKA Bölgesi Bonus Sistemi

**Karar:** YEKA bölgeleri ağırlıklı bileşen olarak değil, ana skora **eklenen bonus** olarak işlenir.

## Gerekçe

YEKA bölgesi içinde olmak yatırım için güçlü sinyal — bakanlık onaylı alan, altyapı var. Ama formüle bağımlı ağırlık olarak eklemek diğer bileşenlerle oranı bozar. Ayrı bonus daha temiz.

## Hesaplama

```python
final_score = clamp(base_score + yeka_bonus, 0, 100)
# yeka_bonus: +0.10 (içinde), +0.05 (20km içinde), 0 (dışında)
```

## Sources

- [[sources/docs/2026-05-02-master-prompt.md]]

## Related

- [[concepts/yeka-bolgeleri]]
- [[concepts/skor-motoru]]
- [[entities/subagent-scoresmith]]
