
# Air Pollution Myanmar

This documentation explains what you can get from our API.

## Air Pollution Data in Myanmar

All Data: [/api/v1/air](https://myanmarairpollution.herokuapp.com/api/v1/air "Get all air pollution data") ```GET```

**Result**

```json
[
  {
    "AQI": 93, //Air Quality Index
    "City": "Yangon", //Located City
    "Humidity": "58",
    "ID": 1,
    "Label": "7 Mile Mayangone", //Location
    "Lat": 16.856831,
    "Lon": 96.146523,
    "PM10_0": "38.15", //PM10.0
    "PM1_0": "22.21", //PM1.0
    "PM2_5": "32.26", //PM2.5
    "Pressure": "1009.87",
    "Temperature": "90" //Ferinheight
  },
  {
    "AQI": 135,
    "City": "Yangon",
    "Humidity": "56",
    "ID": 2,
    "Label": "American Center Yangon",
    "Lat": 16.826124,
    "Lon": 96.139805,
    "PM10_0": "63.21",
    "PM1_0": "31.34",
    "PM2_5": "49.4",
    "Pressure": "1008.86",
    "Temperature": "90"
  },
  ...
]
```

Specific Location Data: [/api/v1/air/{location_id}](https://myanmarairpollution.herokuapp.com/api/v1/air/9578 "Get all air pollution data from ID 9578") ```GET```

**Result**

```json
{
  "AQI": 95,
  "City": "Yangon",
  "Humidity": "58",
  "Label": "7 Mile Mayangone",
  "Lat": 16.856831,
  "Lon": 96.146523,
  "PM10_0": "39.41",
  "PM1_0": "22.36",
  "PM2_5": "32.95",
  "Pressure": "1009.9",
  "Temperature": "90"
}
```

### Location IDs
|ID|Location|
|---|---|
|9578|7 Mile Mayangone|
|33329|American Center Yangon|
|26359|Beca Myanmar|
|9618|Dulwich College Yangon (Pun Hlaing)|
|26285|GEMS Condo|
|31425|UNOPS Myanmar|
|51727|WWF -Myanmar|
|20389|Yangon International School* (Thin Gan Gyun)|
|36553|Yangon-HO|
|29855|YIS Grade 4C|
|33255|Jefferson Center Mandalay|
|34545|Mandalay|

## Get Weather Data

### Yangon

API: [/api/v1/yangon_weather](https://myanmarairpollution.herokuapp.com/api/v1/yangon_weather "Get yangon weather data") ```GET```

**Result**

```json
{
  "Description": "scattered clouds",
  "Icon": "https://openweathermap.org/img/wn/03n@2x.png", //Icon link
  "Weather": "Clouds" //Weather condition
}
```

### Mandalay

API: [/api/v1/mandalay_weather](https://myanmarairpollution.herokuapp.com/api/v1/mandalay_weather "Get yangon weather data") ```GET```

**Result**

```json
{
  "Description": "clear sky",
  "Icon": "https://openweathermap.org/img/wn/01n@2x.png", //Icon link
  "Weather": "Clear" //Weather condition
}
```

## PM1.0, PM2.5 and PM10.0 mean values per month

API: [/api/v1/pm_monthly](https://myanmarairpollution.herokuapp.com/api/v1/pm_monthly "Get PM values") ```GET```

**Result**

```json
{
  "Mandalay": { //Loaction
    "2019 December": { //Month
      "PM1.0": 19.18, //Mean value of PM1.0 for a month
      "PM10.0": 33.4, //Mean value of PM10.0 for a month
      "PM2.5": 28.92 //Mean value of PM2.5 for a month
    },
    ...
  }
  "Yangon": {
    "2019 December": {
      "PM1.0": 29.41,
      "PM10.0": 51.6,
      "PM2.5": 43.8
    },
    ...
  }
}
```

## Average AQI values per month

API: [/api/v1/get_center_monthly](https://myanmarairpollution.herokuapp.com/api/v1/get_center_monthly "Get AQI values") ```GET```

**Result**

```json
{
  "19th Street": { //Location
    "2019 December": 86.37, //Each month AQI mean value
    "2019 November": 87.09,
    "2019 October": 86.37,
    "2020 April": 86.37,
    "2020 August": 58.01,
    "2020 February": 86.37,
    "2020 January": 86.37,
    "2020 July": 50.69,
    "2020 June": 86.37,
    "2020 March": 86.37,
    "2020 May": 86.37,
    "2020 October": 79.74,
    "2020 September": 65.25
  },
  ...
}
```

## AQI and Covid 19 cases

API: [/api/v1/aqi_monthly](https://myanmarairpollution.herokuapp.com/api/v1/aqi_monthly "Get AQI and Covid 19 cases") ```GET```

**Result**

```json
{
  "Mandalay": {
    "2019 December": {
      "12/1/2019": {
        "AQI": 86.37,
        "CUL": 0, //New cases
        "NEW": 0 //Cumulative cases
      },
      ...
    }
    ...
  },
  "Yangon": {
    "2019 December": {
      "12/1/2019": {
        "AQI": 97.38,
        "CUL": 0,
        "NEW": 0
      },
      ...
    },
    ...
  }
}
```