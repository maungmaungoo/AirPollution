from app import app
from flask import jsonify
import requests
import json
import aqi

@app.route('/')
@app.route('/index')
def index():
    return "Air Pollution Project"

@app.route('/api/v1/purpleair', methods=['GET'])
def purpleair_all_api():
    purpleair = requests.get('https://www.purpleair.com/json?show=9578|33329|26359|9618|26285|31425|51727|20389|36553|29855')
    purpleair = purpleair.json()
    purpleair = preprocessing_all(purpleair)
    return jsonify(purpleair)

@app.route('/api/v1/purpleair/<int:id>', methods=['GET'])
def purpleair_api(id):
    purpleair = requests.get(f'https://www.purpleair.com/json?show={id}')
    purpleair = purpleair.json()
    purpleair = preprocessing_one(purpleair)
    return jsonify(purpleair)

def preprocessing_all(api_json):
    result = {}
    for apis in api_json["results"]:
        if not "ParentID" in apis:
            one_res = {}
            one_res["Label"] = apis["Label"]
            one_res["Lat"] = apis["Lat"]
            one_res["Lon"] = apis["Lon"]
            one_res["PM1_0"] = apis["pm1_0_atm"]
            one_res["PM2_5"] = apis["pm2_5_atm"]
            one_res["PM10_0"] = apis["pm10_0_atm"]
            one_res["Humidity"] = apis["humidity"]
            one_res["Temperature"] = apis["temp_f"]
            one_res["Pressure"] = apis["pressure"]
            one_res["AQI"] = int(aqi.to_iaqi(aqi.POLLUTANT_PM25, str(apis["pm2_5_atm"]), algo=aqi.ALGO_EPA))
            result[apis["Label"]] = one_res
    return result

def preprocessing_one(api_json):
    result = {}
    result["Label"] = api_json["results"][0]["Label"]
    result["Lat"] = api_json["results"][0]["Lat"]
    result["Lon"] = api_json["results"][0]["Lon"]
    result["PM1_0"] = api_json["results"][0]["pm1_0_atm"]
    result["PM2_5"] = api_json["results"][0]["pm2_5_atm"]
    result["PM10_0"] = api_json["results"][0]["pm10_0_atm"]
    result["Humidity"] = api_json["results"][0]["humidity"]
    result["Temperature"] = api_json["results"][0]["temp_f"]
    result["Pressure"] = api_json["results"][0]["pressure"]
    result["AQI"] = int(aqi.to_iaqi(aqi.POLLUTANT_PM25, str(api_json["results"][0]["pm2_5_atm"]), algo=aqi.ALGO_EPA))
    return result
