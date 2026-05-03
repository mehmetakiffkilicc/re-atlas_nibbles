"""Generates human-readable score explanations."""
from __future__ import annotations


def generate_explanation(
    energy_type: str,
    breakdown: dict,
    nearest_sub: dict | None,
    yeka_info: dict | None,
    landuse_type: str,
    financials: dict,
) -> dict:
    highlights = []
    warnings = []

    resource = breakdown.get("resource_potential", 0)
    grid = breakdown.get("grid_proximity", 0)
    landuse = breakdown.get("land_use", 0)
    risk = breakdown.get("risk_factor", 0)
    eco = breakdown.get("economic_feasibility", 0)

    # Resource
    if resource >= 0.75:
        label = "rüzgar" if energy_type == "wind" else ("güneş" if energy_type == "solar" else "hibrit")
        highlights.append(f"Yüksek {label} kaynağı potansiyeli ({resource:.0%})")
    elif resource < 0.40:
        warnings.append(f"Düşük kaynak potansiyeli — alternatif bölge değerlendirin")

    # Grid
    if nearest_sub:
        dist = nearest_sub.get("distance_km", 0)
        name = nearest_sub.get("name") or "yakın trafo"
        if dist <= 10:
            highlights.append(f"Şebekeye çok yakın: {name} ({dist:.1f} km)")
        elif dist > 30:
            warnings.append(f"Şebekeden uzak: en yakın trafo {dist:.1f} km ({name})")

    # Landuse
    if landuse >= 0.7:
        highlights.append(f"Uygun arazi kullanımı: {_landuse_label(landuse_type)}")
    elif landuse == 0.0:
        warnings.append(f"Arazi kısıtı: {_landuse_label(landuse_type)} — kurulum izni gerekebilir")

    # YEKA
    if yeka_info and yeka_info.get("bonus", 0) > 0:
        highlights.append(f"YEKA bölgesi avantajı: {yeka_info['name']} ({yeka_info['distance_km']:.0f} km)")

    # Risk
    if risk < 0.4:
        warnings.append("Yüksek deprem riski bölgesi — yapısal tasarıma dikkat")

    # Economic
    payback = financials.get("payback_years", 10)
    if payback <= 6:
        highlights.append(f"Hızlı geri ödeme: ~{payback:.0f} yıl")
    elif payback > 12:
        warnings.append(f"Uzun geri ödeme süresi: ~{payback:.0f} yıl")

    # Summary sentence
    total_score = (
        0.4 * resource + 0.2 * landuse + 0.3 * grid + 0.05 * risk + 0.05 * eco
    ) * 100
    if total_score >= 70:
        quality = "yüksek"
    elif total_score >= 45:
        quality = "orta"
    else:
        quality = "düşük"

    type_label = {"wind": "rüzgar", "solar": "güneş", "hybrid": "hibrit"}.get(energy_type, energy_type)
    summary = f"Bu koordinat {type_label} enerjisi için {quality} uygunluk skoru almaktadır."

    return {"summary": summary, "highlights": highlights, "warnings": warnings}


def _landuse_label(landuse_type: str) -> str:
    labels = {
        "farmland": "tarım arazisi",
        "meadow": "mera",
        "industrial": "endüstriyel alan",
        "barren": "çıplak arazi",
        "forest": "orman",
        "residential": "yerleşim alanı",
        "protected_area": "koruma altındaki alan",
        "nature_reserve": "doğal koruma alanı",
    }
    return labels.get(landuse_type, landuse_type)
