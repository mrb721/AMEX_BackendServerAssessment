# Backendify - Minhazur Bhuiyan Implementation

This FastAPI app aims to handle requests using 2 specified endpoints, which are detailed in Problem-Statement.md


# Design
- The "/status" and root("/") endpoints simply returned an HTTP OK - 200 Message
- The "/company/" endpoint is responsible for most of the design considerations. The BakcendifyCache class and the backendAddressesByCountry dict were created to store previously queried information and startup input, respectively.

- BackendifyCache: This object stores a dict that maps a tuple containing (companyId, country_iso) to a value that stores company information. The company_id and country_iso pairing is pehraps the most reasonably unique combination that could be used, in case a company was present across multiple countries, and therefore, within multiple backends. Our API would check the cache for this information, verify it is less than 24 hours old, and return it if so. Different iterations of this class implemented multiprocessing managers, as well as asyncio or threading module locks in order to handle concurrency. One major issue when scaling this app is ensuring the "cache" or database writes and reads are as updated and consistent as possible. Unfortunately, using a manager almost always resulted in OOM/Docker error 137, while the locks did not seem to improve the production reports. 

- backendAddressesByCountry: A simple dictionary that only needs to store startup arguments that maps country_iso against the url for its backend. 

# Issues:

- The biggest issue with this build is its memory usage. In Production, it will crash with around a 10%-50% success rate, depending on the run, based on feedback from the SRE team. Perhaps the biggest contributor to the Docker container running into OOM issues is the volume and rate of requests. There are plenty of solutions for this issue, many of which were attempted, but were not viable within the constraints of this project. Though, I am confident there are just as many solutions that do work within the same constraints. 

- Libraries such as fastapi-limiter and SlowAPI offer the ability to set rate limiting that either results in an error once the rate is exceeded, or allows for delays in handling requests. Unfortunately, fastapi-limiter requires a Redis instance, while SlowAPI has some quirks regarding specified parameters and return types for our endpoints. FastAPI's BackgroundTasks and Depends capabilities were also leveraged, but ultimately could not serve their intended purpose.  

- Additionally, modules from httpx and asyncio were also used to establish client sessions, set locks within critical processes, and  allow for retries and delays between requests. Although these were implemented in various forms, performace was negatively impacted. In these setups, 500 errors were also even more common.

- The Docker image used, python:3.11-slim, could also potentially be less suited for running an application like this. Perhaps having more granular control over the Docker Image would allow for more flexibility and better performance that isn't bogged down by potentially unnecessary Python installs taking up space. 

- FastAPI/Uvicorn allows for the use of multiple worker processes in parallel, however this would need to be under the supervision of a manager process to ensure data, like the BackendifyCache instance, is shared, as opposed to having multiple instances created. Unofrtunately, memory issues were present in all configurations involving both multiple workers and a manager. 

# Retrospective
- Perhaps maintaining another dictionary/"cache" to store extra requests would have improved performance. Let's say we only take in 50 requests at a time, and all others are "cached" until we move on to the next segment of 50. Even here, concurrency might still be an issue. Though, storing these requests in a dictionary would have stopped users from making a barrage of requests. The mapping could have been ("unique-user-trait", "endpoint" : request). The user trait could have been a token, sessionID, ip address, etc. 
- I would use Pydantic to enforce types across the app (which could have eased my own validation work)
- For BakcendifyCache, I would also implement a running process that clears all data older than 24 hours. 
- Perhaps using a debian image and only installing the necessary Python modules might have yielded *slightly* better performance?
- Having access to a Redis instance would have made it possible to implement the fast-api rate limiter (though perhaps other methods could be used)
- I would implement locks earlier, and a bit more often, to perhaps have them run in parallel through asyncio. This was vaguely attempted, but again, performance (and somehow accuracy) was compromised. 
- Ideally, I would have liked to have a rate limiter, a manager for the Backendify cache, multiple workers, and locks to supplement the awaitables in my application, for it to scale even further.  
- Overoptimization attempts - at one point, I would serialize the backend data values in BackendifyCache to strings since dicts take up far more memory, but still needed them at one level because the performance tradeoffs were important for supplying quick responses. 
