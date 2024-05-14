from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import queries
import random
import time
# from requests import Request, Response
# from slowapi.errors import RateLimitExceeded
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from models import Response
from statsd_utils import incrementCounter, getTiming

app = FastAPI()
# rateLimiter  = Limiter(key_func=get_remote_address)
# app.state.limiter = rateLimiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# app.add_middleware(SlowAPIMiddleware, delay=1)

STATUS_OK = { "message": "OK" }

# rateLimiter.limit("50/minute", key="ip", method="GET", returning="delay")(app.router.find_operation("/company", "GET"))

@app.get("/")
async def root():
    return JSONResponse(status_code=200,content=STATUS_OK)

@app.get("/status")
async def status():
    return JSONResponse(status_code=200, content=STATUS_OK)

@app.get("/company")
# @rateLimiter.limit("5/minute")
async def query(id: str = Query(None, description="Company ID"), country_iso: str = Query(None, description="Country code to look up")):
    # initialize timer
    start_time = time.time()
    # initialize data
    appResponse = None

    if id and country_iso:
        incrementCounter('metric.1')
        databases = queries.getSavedBackendAddresses()
        # check if country exists in our collection of backends
        if country_iso in databases:
            url = databases[country_iso]
            url = databases.get(country_iso,None)
            companyKey = (id, country_iso)
            appResponse = await queries.getData(companyKey, url)

    # if the country_iso hasn't been saved and/or our app response is empty, return 404
    if not appResponse or appResponse['id'] == None:
        incrementCounter('metric.2')
        raise HTTPException(status_code=404, detail="Item not found")
    
    getTiming('metric.3', start_time)  # Record timing
    return JSONResponse(status_code=200, content=appResponse)
    