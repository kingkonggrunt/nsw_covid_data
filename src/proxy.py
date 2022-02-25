class NGINXConfig:
    """Custom Class for configuring the api for NGINX deployment"""
    uri = "/covid-data"  # base uri where api will be deployed example.com/<uri>
    ## --root-path parameter in uvicorn doesn't work 2020-02-17
