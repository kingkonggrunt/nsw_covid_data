import json
import gc
from fastapi import APIRouter, Response, status, HTTPException
import redis
from ..proxy import NGINXConfig
from .. import processing
from src.cache.redis import RedisDictionary

r = RedisDictionary(redis.Redis, db=5)

router = APIRouter(
    prefix=f"{NGINXConfig.uri}/tests"
)

@router.get("/postcode/{postcode}")
def test_postcode(postcode: str, response: Response):
    """Return testing data for a postcode"""
    response.status_code = 200

    cache_key = f"tests_{postcode}"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.Tests()
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
def test_lga(lga: str, response: Response):
    """Return testing data for an lga"""
    response.status_code = 200

    cache_key = f"tests_{lga}"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.Tests()
    out = info.lga(lga)

    if not out:

        del info
        del out
        gc.collect()

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"lga '{lga}' not found")

    r[cache_key] = json.dumps(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])

@router.get("/lhd/{lhd}")
def tests_lhd(lhd: str, response: Response):
    """Return testing data for an lhd"""
    response.status_code = 200

    cache_key = f"tests_{lhd}"
    if cache_key in r:
        return json.loads(r[cache_key])

    info = processing.Tests()
    out = info.lhd(lhd)

    if not out:

        del info
        del out
        gc.collect()

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"lhd '{lhd}' not found")

    r[cache_key] = json.dumps(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])

@router.get("/{location_type}")
def return_locations(location_type: str, response: Response):
    """Return the list of available postcodes, lgas, and lhd the user can request data for"""
    response.status_code = 200

    cache_key = f"tests_{location_type}"
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

    r[cache_key] = json.loads(out)

    del info
    del out
    gc.collect()

    return json.loads(r[cache_key])
