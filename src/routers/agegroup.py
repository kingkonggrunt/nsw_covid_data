import json
import gc
from fastapi import APIRouter, Response, status, HTTPException
import redis
from ..proxy import NGINXConfig
from .. import processing
from src.cache.redis import RedisDictionary

r = RedisDictionary(redis.Redis, db=5)

router = APIRouter(
    prefix=f"{NGINXConfig.uri}/age"
)

@router.get("/total")
def age_total(response: Response):
    """Return the total covid cases for each age group"""
    response.status_code = 200

    cache_key = "age_group_total"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.AgeGroup()
    out = info.age_group_totals()

    if not out:

        del info
        del out
        gc.collect()

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail= "Age Group data not found")

    r[cache_key] = json.dumps(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])


@router.get("/{group}")
def age_group_overtime(group: str, response: Response):
    """Return the daily cases data for an age group"""
    response.status_code = 200

    cache_key = f"age_group_{group}"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.AgeGroup()
    out = info.age_group_overtime(group)

    if not out:

        del info
        del out
        gc.collect()

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Age Group '{group}' not found")

    r[cache_key] = json.dumps(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])
