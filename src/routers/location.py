from fastapi import APIRouter, Response, status, HTTPException
import redis
import json
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

    if f"location_{postcode}" in r:
        return json.loads(r[f"location_{postcode}"])

    info = processing.CaseLocation()
    out = info.postcode(postcode)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Postcode '{postcode}' not found")

    r[f"location_{postcode}"] = json.dumps(out)
    return out


@router.get("/lga/{lga}")
def return_lga_overtime(lga, response: Response):
    """Return the daily cases data for an lga"""
    response.status_code = 200

    if f"location_{lga}" in r:
        return json.loads(r[f"location_{lga}"])

    info = processing.CaseLocation()
    out = info.lga(lga)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"LGA '{lga}' not found")

    r[f"location_{lga}"] = json.dumps(out)
    return out

@router.get("/lhd/{lhd}")
def return_lhd_overtime(lhd, response: Response):
    """Return the daily cases data for an lhd"""
    response.status_code = 200

    if f"location_{lhd}" in r:
        return json.loads(r[f"location_{lhd}"])

    info = processing.CaseLocation()
    out = info.lhd(lhd)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"LHD '{lhd}' not found")

    r[f"location_{lhd}"] = json.dumps(out)
    return out

@router.get("/{location_type}")
def return_locations(location_type: str, response: Response):
    """Return the list of available postcodes, lgas, and lhd the user can request data for"""
    response.status_code = 200

    if f"location_{location_type}" in r:
        return json.loads(r[f"location_{location_type}"])

    info = processing.CaseLocation()
    out =  info.list_locations(location_type)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Invalid location type. Use one of 'lga, postcode, or lhd'")

    r[f"location_{location_type}"] = json.dumps(out)
    return out
