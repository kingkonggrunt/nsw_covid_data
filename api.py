from fastapi import FastAPI, Response
from src import data
from src import processing

app = FastAPI()

data = data.CovidData()

class NGINXConfig():
    """Custom Class for configuring the api for NGINX deployment"""
    uri = "/covid-data"  # base uri where api will be deployed example.com/<uri>
    ## prefix parameter in include router doesn't work 2020-02-17

@app.get(NGINXConfig.uri + "/")
def get_routes():
    return {
        "Welcome": "Routes are listed below",
        "Routes": {
            "/" : "This Route",
            "/age" : {
                "/Total" : 'Total Confirmed Cases for each age group',
                "/0-19" : 'Confirmed Cases Over Time for Age Group "0-19"',
                "/20-24" : 'Confirmed Cases Over Time for Age Group "20-24"',
                "/25-29" : 'Confirmed Cases Over Time for Age Group "25-29"',
                "/30-34" : 'Confirmed Cases Over Time for Age Group "30-34"',
                "/35-39" : 'Confirmed Cases Over Time for Age Group "35-39"',
                "/40-44" : 'Confirmed Cases Over Time for Age Group "40-44"',
                "/45-49" : 'Confirmed Cases Over Time for Age Group "45-49"',
                "/50-54" : 'Confirmed Cases Over Time for Age Group "50-54"',
                "/55-59" : 'Confirmed Cases Over Time for Age Group "55-59"',
                "/70" : 'Confirmed Cases Over Time for Age Group "70+"',
                "/None" : 'Confirmed Cases Over Time for Age Group "None"',
            },
            "/location": {
                "/postcode" : "List available postcodes",
                "/lhd" : "List available local health district codes and names",
                "/lga" : "List available local goverment area codes and names",
                "/postcode/<postcode>" : "Cases Over Time for Postcode",
                "/lhd/<code or name>" : "Cases Over Time for lhd code/name",
                "/lga/<code or name>" : "Cases Over Time for lga code/name"
            },
            "/tests": {
                "/postcode/<postcode>" : "Tests Over Time for Postcode",
                "/lhd/<code or name>" : "Tests Over Time for lhd code/name",
                "/lga/<code or name>" : "Tests Over Time for lga code/name"
            }
        }
    }

@app.get(NGINXConfig.uri + "/age/total")
def age_total():
    df = data.load_csv("Cases_AgeRange.csv", parse_dates=['notification_date'])
    out = processing.AgeGroup(df)
    out.age_group_totals()
    return out.data

@app.get(NGINXConfig.uri + "/age/{group}")
def age_group_overtime(group: str, response: Response):
    df = data.load_csv("Cases_AgeRange.csv")
    out = processing.AgeGroup(df)
    out.age_group_overtime(group)

    if not out.data:
        response.status_code = 404
        return "Invalid Age Group"

    response.status_code = 200
    return out.data


"""Location Routes

/location/postcode/{postcode}
/location/lga/{lga}
/location/lhd/{lhd}
/location/{type}
"""

@app.get(NGINXConfig.uri + "/location/postcode/{postcode}")
def return_postcode_overtime(postcode, response: Response):
    df = data.load_csv("Cases_Location.csv")
    out = processing.CaseLocation(df)
    out.postcode(postcode)

    if not out.data:
        response.status_code = 404
        return "Invalid Postcode"

    response.status_code = 200
    return out.data

@app.get(NGINXConfig.uri + "/location/lga/{lga}")
def return_lga_overtime(lga, response: Response):
    df = data.load_csv("Cases_Location.csv")
    out = processing.CaseLocation(df)
    out.lga(lga)

    if not out.data:
        response.status_code = 404
        return "Invalid LGA Code or Name"

    response.status_code = 200
    return out.data

@app.get(NGINXConfig.uri + "/location/lhd/{lhd}")
def return_lhd_overtime(lhd, response: Response):
    df = data.load_csv("Cases_Location.csv")
    out = processing.CaseLocation(df)
    out.lhd(lhd)

    if not out.data:
        response.status_code = 404
        return "Invalid LHD Code or Name"

    response.status_code = 200
    return out.data

@app.get(NGINXConfig.uri + "/location/{type}")
def return_locations(type: str):
    df = data.load_csv("Cases_Location.csv")
    out = processing.CaseLocation(df)
    out.list_locations(type)
    return out.data


"""Test Routes

/tests/postcode/{postcode}
/tests/lhd/{lhd}
/tests/lga/{lga}
"""
@app.get(NGINXConfig.uri + "/tests/postcode/{postcode}")
def test_postcode(postcode: str):
    df = data.load_csv("Tests_Location.csv")
    out = processing.Tests(df)
    out.postcode(postcode)

    if not out.data:
        response.status_code = 404
        return "Invalid Postcode"

    response.status_code = 200
    return out.data

@app.get(NGINXConfig.uri + "/tests/lga/{lga}")
def test_lga(lga: str):
    df = data.load_csv("Tests_Location.csv")
    out = processing.Tests(df)
    out.lga(lga)

    if not out.data:
        response.status_code = 404
        return "Invalid LGA Code or Name"

    response.status_code = 200
    return out.data

@app.get(NGINXConfig.uri + "/tests/lhd/{lhd}")
def tests_lhd(lhd: str):
    df = data.load_csv("Tests_Location.csv")
    out = processing.Tests(df)
    out.lhd(lhd)

    if not out.data:
        response.status_code = 404
        return "Invalid LHD Code or Name"

    response.status_code = 200
    return out.data
