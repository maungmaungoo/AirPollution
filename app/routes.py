from app import app
from flask import jsonify, render_template
import requests
import json
import aqi
import pandas as pd
import joblib
from datetime import datetime

y_df = pd.read_csv('app/static/data/yangon.csv')
m_df = pd.read_csv('app/static/data/mandalay.csv')
y_df["YM"] = y_df["Year"].astype(str) +" "+ y_df["Month"].astype(str)
m_df["YM"] = m_df["Year"].astype(str) +" "+ m_df["Month"].astype(str)

@app.route('/')
@app.route('/index')
def index():
    """Index of Myanmar Air Pollution API"""
    return render_template("index.html", title="Air Pollution Myanmar")

@app.route('/api/v1/air', methods=['GET'])
def air():
    """Get air pollution data from Yangon and Mandalay regions"""
    purpleair = requests.get('https://www.purpleair.com/json?show=9578|33329|26359|9618|26285|31425|51727|20389|36553|29855|33255|34545')
    purpleair = purpleair.json()
    purpleair = preprocessing_all(purpleair)
    air = jsonify(purpleair)
    air.headers.add("Access-Control-Allow-Origin", "*")
    return air

@app.route('/api/v1/air/<int:id>', methods=['GET'])
def air_id(id):
    """Get air pollution data using location ID"""
    purpleair = requests.get(f'https://www.purpleair.com/json?show={id}')
    purpleair = purpleair.json()
    purpleair = preprocessing_one(purpleair)
    air = jsonify(purpleair)
    air.headers.add("Access-Control-Allow-Origin", "*")
    return air

def preprocessing_all(api_json):
    """Accept input json from purpleair API
    Return processed data in list format
    """
    result = []
    count = 1
    # get data from 'result' key
    for apis in api_json["results"]:
        # get data only from parent Air Quality Meters
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
            # calculate AQI using PM2.5 value
            one_res["AQI"] = int(aqi.to_iaqi(aqi.POLLUTANT_PM25, str(apis["pm2_5_atm"]), algo=aqi.ALGO_EPA))
            one_res["ID"] = count
            count = count + 1
            # separate Yangon an Mandalay
            if "Mandalay" in apis["Label"]:
                one_res["City"] = "Mandalay"
            else:
                one_res["City"] = "Yangon"
            result.append(one_res)
    return result

def preprocessing_one(api_json):
    """Accept input json from purpleair API
    Return processed data in list format
    """
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
    # separate Yangon an Mandalay
    if "Mandalay" in api_json["results"][0]["Label"]:
        result["City"] = "Mandalay"
    else:
        result["City"] = "Yangon"
    # calculate AQI using PM2.5 value
    result["AQI"] = int(aqi.to_iaqi(aqi.POLLUTANT_PM25, str(api_json["results"][0]["pm2_5_atm"]), algo=aqi.ALGO_EPA))
    return result

@app.route('/api/v1/yangon_weather', methods=['GET'])
def yangon_weather():
    """Get yangon weather condition"""
    weather = get_weather("yangon")
    weather.headers.add("Access-Control-Allow-Origin", "*")
    return weather

@app.route('/api/v1/mandalay_weather', methods=['GET'])
def mandalay_weather():
    """Get mandalay weather condition"""
    weather = get_weather("mandalay")
    weather.headers.add("Access-Control-Allow-Origin", "*")
    return weather

def get_weather(city):
    """Get Yangon weather from Openweather API"""
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=43c99395c0a8d27cad1592502a69fd07')
    weather = weather.json()
    result = {}
    # get weather condition
    result["Weather"] = weather["weather"][0]["main"]
    # get detail description of weather
    result["Description"] = weather["weather"][0]["description"]
    # get icon
    result["Icon"] = f"https://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png"
    return jsonify(result)

@app.route('/api/v1/pm_monthly', methods=['GET'])
def pm_monthly():
    """Get PM1.0, PM2.5 and PM10.0 values"""
    result = {}
    result["Yangon"] = get_monthly_pm_values(y_df)
    result["Mandalay"] = get_monthly_pm_values(m_df)

    result = jsonify(result)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result

def get_monthly_pm_values(df):
    """Get mean values of PM1.0, PM2.5 and PM10.0"""
    pm2_5 = df.groupby("YM")['PM2.5_ATM_ug/m3'].apply(list).to_dict()
    pm1_0 = df.groupby("YM")['PM1.0_ATM_ug/m3'].apply(list).to_dict()
    pm10_0 = df.groupby("YM")['PM10_ATM_ug/m3'].apply(list).to_dict()

    months = df["YM"].to_list()
    months = set(months)

    result = {}

    for month in months:
        r = {}
        # get mean value of PM1.0
        p1 = sum(pm1_0[month]) / len(pm1_0[month])
        # get mean value of PM2.5
        p2 = sum(pm2_5[month]) / len(pm2_5[month])
        # get mean value of PM10.0
        p10 = sum(pm10_0[month]) / len(pm10_0[month])
        r["PM1.0"] = float("{:.2f}".format(p1))
        r["PM2.5"] = float("{:.2f}".format(p2))
        r["PM10.0"] = float("{:.2f}".format(p10))
        result[month] = r

    return result

@app.route('/api/v1/aqi_monthly', methods=['GET'])
def aqi_monthly():
    """Get daily AQI value and Covid 19 cases for each month"""
    result = {}
    result["Yangon"] = get_monthly_aqi(y_df)
    result["Mandalay"] = get_monthly_aqi(m_df)

    result = jsonify(result)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result

def get_monthly_aqi(df):
    """Get daily AQI value and Covid 19 cases"""
    date = df.groupby(["YM","Date"])["AQI"].apply(list).to_dict()
    new = df.groupby(["YM","Date"])["New_cases"].apply(list).to_dict()
    cul = df.groupby(["YM","Date"])["Cumulative_cases"].apply(list).to_dict()

    result = {}
    tmp = {}
    for keys, values in date.items():
        date = {}
        aqi_val = {}
        # get mean value of AQI values from all location of each city
        aqi_val["AQI"] = float("{:.2f}".format(sum(values) / len(values)))
        new_cases = new[keys]
        aqi_val["NEW"] = new_cases[0]
        cumulative = cul[keys]
        aqi_val["CUL"] = cumulative[0]
        date[keys[1]] = aqi_val
        if keys[0] in result:
            result[keys[0]].update(date)
        else:
            result[keys[0]] = date
 
    return result

@app.route('/api/v1/predict', methods=['GET'])
def predict():
    """Predict tomorrow AQI value and PM2.5 value using XGBoost"""
    result = {}
    # load XGBoost model
    loaded_model = joblib.load("app/static/model.sav")
    # get current month
    month = datetime.now().month
    # get current season
    season = get_season(month)
    air = requests.get('https://www.purpleair.com/json?show=9578|33329|26359|9618|26285|31425|51727|20389|36553|29855|33255|34545')
    air = air.json()
    air = preprocessing_all(air)
    for a in air:
        r = {}
        # Yangon = 1, Mandalay = 0
        city = 1 if a["City"] == "Yangon" else 0
        temp = a["Temperature"]
        humd = a["Humidity"]
        center = 0
        # convert center name into respective value
        center = get_center(a["Label"])
        p_data = [[city, center, month, season, int(temp) , int(humd)]]
        # convert into pandas DataFrame
        p_data = pd.DataFrame(p_data, columns=['City', 'Center', 'Month', 'Season', 'Temperature_F', 'Humidity_%'])
        # predict
        aqi_p = loaded_model.predict(p_data)
        # convert into int value
        r["PM2.5"] = int(float(aqi_p.astype(str)[0]))
        # calculate AQI value
        r["AQI"] = int(aqi.to_iaqi(aqi.POLLUTANT_PM25, str(r["PM2.5"]), algo=aqi.ALGO_EPA))
        result[a["Label"]] = r

    result = jsonify(result)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result

def get_season(argument):
    # Nov - Feb = Cool season => 0
    # Mar - John = Rainy season => 2
    # July - Oct = Hot season => 1
    switcher = {
        1: 0,
        2: 0,
        3: 2,
        4: 2,
        5: 2,
        6: 2,
        7: 1,
        8: 1,
        9: 1,
        10: 1,
        11: 0,
        12: 0,
    }
    return switcher.get(argument, 3)

def get_center(argument):
    switcher = {
        "Mandalay": 0,
        "7 Miles Mayangone": 1,
        "American Center Yangon": 3,
        "Beca Myanmar": 4,
        "GEMS Condo": 5,
        "Jefferson Center Mandalay": 6,
        "Dulwich College Yangon (Pun Hlaing)": 7,
        "Yangon International School* (Thin Gan Gyun)": 8,
        "UNOPS Myanmar": 9,
        "WWF -Myanmar": 10,
        "YIS Grade 4C": 11,
        "Yangon-HO": 12,
    }
    return switcher.get(argument, 2)

@app.route("/api/v1/get_center_monthly")
def get_monthly_aqi_each_center():
    """Get Yangon and Mandalay monthly AQI mean value"""
    yangon = get_monthly_mean_aqi_each_center(y_df)
    mandalay = get_monthly_mean_aqi_each_center(m_df)
    # add yangon and mandalay dict into one
    result = {**yangon, **mandalay}
    result = jsonify(result)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result

def get_monthly_mean_aqi_each_center(df):
    """Get Yangon and Mandalay AQI for each month and calculate mean values"""
    center = df.groupby(["Center","YM"])["AQI"].apply(list).to_dict()
    result = {}
    # keys => ('Jefferson Center', '2020 September')
    # values => [79.14, 76.8, 92.53, ... ]
    for keys, values in center.items():
        r = {}
        # calculate mean value
        r[keys[1]] = float("{:.2f}".format(sum(values) / len(values)))
        if keys[0] in result:
            result[keys[0]].update(r)
        else:
            result[keys[0]] = r

    return result

@app.errorhandler(404)
def not_found(e):
    """404"""
    result = jsonify("")
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result, 404

@app.errorhandler(500)
def server_error(e):
    """500"""
    result = jsonify("")
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result, 500
