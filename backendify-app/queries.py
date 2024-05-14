import requests
# from constants import NUM_ATTEMPTS
import utils
from models import Response
from backendify_cache import backendifyCache, backendAddressesByCountry
# from aiohttp import ClientSession, ClientTimeout, ClientError


async def getData(companyKey, url):
    appResponse = Response()

    data = await queryBackend(companyKey, url)  

    companyId = companyKey[0]  
    country_iso = companyKey[1]
    if country_iso and url and companyId:
        # check if response is valid
        if data and data != {} and data['status_code'] == 200:
            now = utils.timeNow()
            if data['saved-content-type'] == 'application/x-company-v1':
                name = data['cn']  if data['cn']  else "Company Name not provided"
                active_until  = utils.convertStringToRFCDatetime(data['closed_on'])
                active = now <= active_until if active_until else True
                appResponse = Response(companyId, name, active, active_until)
            elif data['saved-content-type'] == 'application/x-company-v2':
                name = data['company_name']  if data['company_name'] else "Company Name not provided"
                active_until = utils.convertStringToDatetime(data['dissolved_on'])
                active = now <= active_until if active_until else True
                appResponse = Response(companyId, name , active, active_until)
  
    return appResponse.__dict__

async def queryBackend(companyKey, url):
    backend = {}
    companyId = companyKey[0]  
    country_iso = companyKey[1]

    # try finding company in our cache
    if backendifyCache.isDataValid(companyId):
        backend =  getCachedBackendByCompany(companyKey)
    else:
        fullURL = utils.formatURL(url, companyId)

        if not fullURL:
            return backend
        
        # otherwise, we GET it
        response =   requests.get(fullURL)

        if companyId and response and response.status_code == 200:
            # if we get a successful response, it is added to the saved responses
            backend =  addBackendToList(country_iso, companyId, response)

    # return our response, regardless of success, this will be accounted for in getData()
    return backend

def addBackendToList(country_iso, companyId, response):
    storeData = {}
    if companyId and response:
        headers =  response.headers
        storeData = response.json()
        storeData['status_code'] = response.status_code
        storeData['saved-content-type'] = headers['content-type']
        storeData['stored-time'] = utils.convertDatetimeToString(utils.timeNow()) 
        companyKey = (companyId, country_iso)
        backendifyCache.add(companyKey, storeData)  

    return storeData

def getCachedBackendByCompany(companyKey):
    return backendifyCache.get(companyKey)

def getSavedBackendAddresses():
    return backendAddressesByCountry