from fastapi import FastApi
from src import data

app = FastAPI()

data = data.CovidData()

@app.get("/")
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

@app.get("/age/total")
def age_total():
    df = data.load_csv("Cases_AgeRange.csv", parse_dates=['notification_date'])
    out = df.groupby(["age_group"]).sum().to_dict(orient="dict")['confirmed_cases_count']
    return out

@app.get()
