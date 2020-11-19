from app import app
from flask import jsonify
import requests
import json
import aqi
import pandas as pd

y_df = pd.read_csv('app/static/data/yangon.csv')
m_df = pd.read_csv('app/static/data/mandalay.csv')
y_df["YM"] = y_df["Year"].astype(str) +" "+ y_df["Month"].astype(str)
m_df["YM"] = m_df["Year"].astype(str) +" "+ m_df["Month"].astype(str)

@app.route('/')
@app.route('/index')
def index():
    return "Air Pollution Myanmar"

@app.route('/api/v1/air', methods=['GET'])
def purpleair_all_api():
    purpleair = requests.get('https://www.purpleair.com/json?show=9578|33329|26359|9618|26285|31425|51727|20389|36553|29855|33255|34545')
    purpleair = purpleair.json()
    purpleair = preprocessing_all(purpleair)
    air = jsonify(purpleair)
    air.headers.add("Access-Control-Allow-Origin", "*")
    return air

@app.route('/api/v1/air/<int:id>', methods=['GET'])
def purpleair_api(id):
    purpleair = requests.get(f'https://www.purpleair.com/json?show={id}')
    purpleair = purpleair.json()
    purpleair = preprocessing_one(purpleair)
    air = jsonify(purpleair)
    air.headers.add("Access-Control-Allow-Origin", "*")
    return air

def preprocessing_all(api_json):
    result = []
    count = 1;
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
            one_res["ID"] = count
            count = count + 1
            if "Mandalay" in apis["Label"]:
                one_res["City"] = "Mandalay"
            else:
                one_res["City"] = "Yangon"
            result.append(one_res)
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
    if "Mandalay" in api_json["results"][0]["Label"]:
        result["City"] = "Mandalay"
    else:
        result["City"] = "Yangon"
    result["AQI"] = int(aqi.to_iaqi(aqi.POLLUTANT_PM25, str(api_json["results"][0]["pm2_5_atm"]), algo=aqi.ALGO_EPA))
    return result

@app.route('/api/v1/yangon_weather', methods=['GET'])
def yangon_weather():
    weather = get_weather("yangon")
    weather.headers.add("Access-Control-Allow-Origin", "*")
    return weather

@app.route('/api/v1/mandalay_weather', methods=['GET'])
def mandalay_weather():
    weather = get_weather("mandalay")
    weather.headers.add("Access-Control-Allow-Origin", "*")
    return weather

def get_weather(city):
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=43c99395c0a8d27cad1592502a69fd07')
    weather = weather.json()
    result = {}
    result["Weather"] = weather["weather"][0]["main"]
    result["Description"] = weather["weather"][0]["description"]
    result["Icon"] = f"https://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png"
    return jsonify(result)

@app.route('/api/v1/pm_monthly', methods=['GET'])
def monthly_air():
    result = {}
    result["Yangon"] = get_m(y_df)
    result["Mandalay"] = get_m(m_df)

    result = jsonify(result)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result

def get_m(df):
    pm2_5 = df.groupby("YM")['PM2.5_ATM_ug/m3'].apply(list).to_dict()
    pm1_0 = df.groupby("YM")['PM1.0_ATM_ug/m3'].apply(list).to_dict()
    pm10_0 = df.groupby("YM")['PM10_ATM_ug/m3'].apply(list).to_dict()

    months = df["YM"].to_list()
    months = set(months)

    result = {}

    for month in months:
        r = {}
        p1 = sum(pm1_0[month]) / len(pm1_0[month])
        p2 = sum(pm2_5[month]) / len(pm2_5[month])
        p10 = sum(pm10_0[month]) / len(pm10_0[month])
        r["PM1.0"] = float("{:.2f}".format(p1))
        r["PM2.5"] = float("{:.2f}".format(p2))
        r["PM10.0"] = float("{:.2f}".format(p10))
        result[month] = r

    return result

@app.route('/api/v1/aqi_monthly', methods=['GET'])
def monthly_aqi():
    pass

@app.errorhandler(404)
def not_found(e):
    result = jsonify("")
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result, 404

@app.errorhandler(500)
def server_error(e):
    result = jsonify("")
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result, 500
