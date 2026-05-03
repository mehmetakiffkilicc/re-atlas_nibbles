from fastapi import APIRouter, Query
from typing import Literal

from app.routers.provinces import get_province_scores

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "contracts"))
from schemas import ProvinceScore

router = APIRouter()


@router.get("/top", response_model=list[ProvinceScore])
def get_top(
    type: Literal["solar", "wind", "hybrid"] = Query(default="solar"),
    n: int = Query(default=5, ge=1, le=81),
):
    scores = get_province_scores(type)
    sorted_scores = sorted(scores, key=lambda s: s.score, reverse=True)
    return sorted_scores[:n]
