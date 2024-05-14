# import httpx
import asyncio
# import time
from backendify_cache import backendAddressesByCountry
import uvicorn
import sys
import os
import time
import random

def main():
    start_time = time.time()

    # loop through our input arguments
    for arg in sys.argv:
        # split by '=' where applicable
        pair = arg.split('=')
        # only append arguments that follow our expected behavior
        if len(pair) == 2:
            backendAddressesByCountry[pair[0]] = pair[1]

    # run app server
    uvicorn.run("routes:app", port=9000, host='0.0.0.0')

   
if __name__ == "__main__":
    # asyncio.run(main())  # ideally asyncio would be used more, but performance was worse with different configs
    main()
   