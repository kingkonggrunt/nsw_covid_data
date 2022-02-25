from fastapi import APIRouter, Response, status, HTTPException
from ..proxy import NGINXConfig
from .. import processing

router = APIRouter(
    prefix=f"{NGINXConfig.uri}/location"
)

@router.get("/postcode/{postcode}")
def return_postcode_overtime(postcode, response: Response):
    """Return the daily cases data for a postcode"""
    info = processing.CaseLocation()
    out = info.postcode(postcode)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Postcode '{postcode}' not found")

    response.status_code = 200
    return out


@router.get("/lga/{lga}")
def return_lga_overtime(lga, response: Response):
    """Return the daily cases data for an lga"""
    info = processing.CaseLocation()
    out = info.lga(lga)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"LGA '{lga}' not found")

    response.status_code = 200
    return out

@router.get("/lhd/{lhd}")
def return_lhd_overtime(lhd, response: Response):
    """Return the daily cases data for an lhd"""
    info = processing.CaseLocation()
    out = info.lhd(lhd)

    if not out:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"LHD '{lhd}' not found")

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
