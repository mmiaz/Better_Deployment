# Better_Deployment
This is a repo saving options for better and faster api solutions:
1. FastAPI
2. aiohttp + asyncio + flask API
3. ....


## flask_api.py
As some of the modules are getting results from multiple models, we are hoping to call the same api but different ports asynchronously. The individual APIs are all Flask api, so we create this main API to call them and aggregate the result.

### Usage
we need to pass local image
 
```shell
curl -X POST http://0.0.0.0:5000/async_api  -F imagefile=@xxxxxxx.jpg
```

## fastapi.py
As FastAPI offers swagger UI and embeddd asyncio functionality, we are hoping to compare performance testing of it with that of flask api.

### Usage
Make us of below command to start the service and go to route **/docs** to check documantation and test it out. We can later use Jmeter to do performance testing.
 
```shell
uvicorn main:app
uvicorn main:app --reload
```
