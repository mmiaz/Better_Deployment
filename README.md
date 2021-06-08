# Better_Deployment
This is a repo saving options for better and faster api solutions:
1. FastAPI
2. aiohttp + asyncio + flask API
3. ....


## flask_api.py
As some of the modules are getting results from multiple models, we are hoping to call the same api but different ports asynchronously. The individual APIs are all Flask api, so we create this main API to call them and aggregate the result.
