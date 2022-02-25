from fastapi import APIRouter, Response, status, HTTPException
from ..proxy import NGINXConfig
from .. import processing

router = APIRouter(
    prefix=f"{NGINXConfig.uri}/age"
)

@router.get("/total")
def age_total():
    """Return the total covid cases for each age group"""
    info = processing.AgeGroup()
    out = info.age_group_totals()
    return out

@router.get("/{group}")
def age_group_overtime(group: str, response: Response):
    """Return the daily cases data for an age group"""
    info = processing.AgeGroup()
    out = info.age_group_overtime(group)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Age Group '{group}' not found")

    response.status_code = 200
    return out
