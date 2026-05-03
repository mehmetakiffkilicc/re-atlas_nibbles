from fastapi import APIRouter, Query, HTTPException
from typing import Literal

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "contracts"))
from schemas import ProvinceScore

router = APIRouter()

# Populated at startup by main.py
_province_scores: dict[str, list[ProvinceScore]] = {}


def set_province_scores(energy_type: str, scores: list[ProvinceScore]):
    _province_scores[energy_type] = scores


def get_province_scores(energy_type: str) -> list[ProvinceScore]:
    return _province_scores.get(energy_type, [])


@router.get("/provinces", response_model=list[ProvinceScore])
def list_provinces(
    type: Literal["solar", "wind", "hybrid"] = Query(default="solar"),
    hide_forest: bool = Query(default=False),
    exclude_high_risk: bool = Query(default=False),
    grid_max_km: float | None = Query(default=None),
):
    scores = get_province_scores(type)
    if not scores:
        raise HTTPException(status_code=503, detail="Province scores not ready yet, retry in a few seconds")
    if hide_forest:
        scores = [p for p in scores if p.score >= 35]
    if exclude_high_risk:
        scores = [p for p in scores if p.score >= 45]
    return scores
