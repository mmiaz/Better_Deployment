import aiohttp
from aiohttp import FormData
import asyncio
import async_timeout
from flask import Flask
import flask
import datetime
from flask_api import FlaskAPI, status
import argparse
import logging
from flask import jsonify 


# ---------------------------------------------------------------------------------
# 1. Initializing app
logging.info("Initializing Flask app and asyncio event loop")
loop = asyncio.get_event_loop()
app = Flask(__name__)



# ---------------------------------------------------------------------------------
# 2. Async calls
def process_result(results):
    results = [i['data'] for i in results]
    pred_dict = {}
    for result in results:
        for tag_category, meta in result.items():
            pred_dict[tag_category] = meta
    return pred_dict


async def fetch(session, url, file_name):
    data = FormData()
    data.add_field('imagefile',
                   open(file_name, 'rb'),
                   filename=file_name,
                   content_type="image/jpg")
    async with session.post(url, data=data) as response:
        return await response.json()


async def main(file_name):
    ports = [5040,5020,8080,8000]
    #file_name = 'xxxxxxx.jpg'
    tasks = []
    async with aiohttp.ClientSession() as session: #, async_timeout.timeout(10)
        for port in ports:
            url = "http://0.0.0.0:{}/xxxx_api".format(port)
            tasks.append(fetch(session, url, file_name))
        results = await asyncio.gather(*tasks)
        results = process_result(results)

        data = {
            "status": "Success",
            "message": "Prediction success",
            "data": results,
        }
    return data



# ---------------------------------------------------------------------------------
# 3. API. collate Attribute prediction API
@app.route("/async_api", methods=["POST"])
def async_attr_api():
    try:
        img_file = flask.request.files["imagefile"]
        # perform multiple async requests concurrently
        responses = loop.run_until_complete(main(img_file.filename))
        return jsonify(responses), status.HTTP_200_OK

    except Exception as e:
        responses = {
            "status": "Failed",
            "message": str(e),
            "data": dict(),
        }
        return jsonify(responses), status.HTTP_400_BAD_REQUEST
    


if __name__ == "__main__":
    app.run(debug=config.APP_DEBUG, 
            host=config.APP_HOST)


