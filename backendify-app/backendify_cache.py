
# from fastapi import Depends
import utils
# import asyncio
# import threading


# We are caching using 2 dictionaries, mimicking caches like Redis
class BackendifyCache:
    def __init__(self) -> None:
        # Schema - {compnayKey: responseData + saved custom attributes}
        # companyKey - (companyId, country_iso) 
        # important to save companyId with country in case one company is in multiple countries
        self._backendsByCompany = {}
        # maintaining a thread or asyncio lock would ideally help with concurrency issues
        # self._lock =  asyncio.Lock() # asyncio.Lock()
    
    def get(self, key, defaultVal = None):
        # async with self._lock:
        return self._backendsByCompany.get(key, defaultVal)

    def add(self, key, val):
        # async with self._lock:
        self._backendsByCompany[key] = val
       
    def remove(self, key):
        # async with self._lock:
        del self._backendsByCompany[key]
    
    def isDataValid(self, key):
        # async with self._lock:
        if key not in self._backendsByCompany:
            return False
            
        backend = self._backendsByCompany[key]
        storedTime = backend['stored-time']
        isWithinTimeLimit = utils.withinTimeLimit(utils.timeNow(), utils.convertStringToDatetime(storedTime))
        return isWithinTimeLimit




# instantiate cache
backendifyCache = BackendifyCache()

# Schema - {country_iso : backend_address}
# one country per backend, ensuring country_iso will be unique
backendAddressesByCountry = {}
