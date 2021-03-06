import json
import gc
from fastapi import APIRouter, Response, status, HTTPException
import redis
from .. import processing
from ..proxy import NGINXConfig
from src.cache.redis import RedisDictionary



r = RedisDictionary(redis.Redis, db=5)

router = APIRouter(
    prefix=f"{NGINXConfig.uri}/location"
)

@router.get("/postcode/{postcode}")
def return_postcode_overtime(postcode, response: Response):
    """Return the daily cases data for a postcode"""
    response.status_code = 200

    cache_key = f"location_{postcode}"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.CaseLocation()
    out = info.postcode(postcode)

    if not out:

        del info
        del out
        gc.collect()

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Postcode '{postcode}' not found")

    r[cache_key] = json.dumps(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])


@router.get("/lga/{lga}")
def return_lga_overtime(lga, response: Response):
    """Return the daily cases data for an lga"""
    response.status_code = 200

    cache_key = f"location_{lga}"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.CaseLocation()
    out = info.lga(lga)

    if not out:

        del info
        del out
        gc.collect()

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"LGA '{lga}' not found")

    r[cache_key] = json.dumps(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])

@router.get("/lhd/{lhd}")
def return_lhd_overtime(lhd, response: Response):
    """Return the daily cases data for an lhd"""
    response.status_code = 200

    cache_key = f"location_{lhd}"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.CaseLocation()
    out = info.lhd(lhd)

    if not out:

        del info
        del out
        gc.collect()

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"LHD '{lhd}' not found")

    r[cache_key] = json.dumps(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])

@router.get("/{location_type}")
def return_locations(location_type: str, response: Response):
    """Return the list of available postcodes, lgas, and lhd the user can request data for"""
    response.status_code = 200

    cache_key = f"location_{location_type}"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.CaseLocation()
    out =  info.list_locations(location_type)

    if not out:

        del info
        del out
        gc.collect()

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Invalid location type. Use one of 'lga, postcode, or lhd'")

    r[cache_key] = json.dumps(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])
