from fastapi import APIRouter, Response, status, HTTPException
from ..proxy import NGINXConfig
from .. import processing

router = APIRouter(
    prefix=f"{NGINXConfig.uri}/tests"
)

@router.get("/postcode/{postcode}")
def test_postcode(postcode: str, response: Response):
    """Return testing data for a postcode"""
    info = processing.Tests()
    out = info.postcode(postcode)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Postcode '{postcode}' not found")

    response.status_code = 200
    return out

@router.get("/lga/{lga}")
def test_lga(lga: str, response: Response):
    """Return testing data for an lga"""
    info = processing.Tests()
    out = info.lga(lga)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"lga '{lga}' not found")

    response.status_code = 200
    return out

@router.get("/lhd/{lhd}")
def tests_lhd(lhd: str, response: Response):
    """Return testing data for an lhd"""
    info = processing.Tests()
    out = info.lhd(lhd)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"lhd '{lhd}' not found")

    response.status_code = 200
    return out

@router.get("/{location_type}")
def return_locations(location_type: str, response: Response):
    """Return the list of available postcodes, lgas, and lhd the user can request data for"""
    info = processing.CaseLocation()
    out =  info.list_locations(location_type)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Invalid location type. Use one of 'lga, postcode, or lhd'")

    response.status_code = 200
    return out
