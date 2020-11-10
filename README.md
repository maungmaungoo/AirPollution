
# Air Pollution Myanmar

This documentation explains what you can get from our API.

## Air Pollution Data in Myanmar

All Data: [/api/v1/air](https://myanmarairpollution.herokuapp.com/api/v1/air "Get all air pollution data") ```GET```

**Result**

```json
[
  {
    "AQI": 93, //Air Quality Index
    "City": "Yangon", Located City
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

## ERROR

### 404

```json
{
  "Code": 404,
  "Message": "Not Found"
}
```

### 500

```json
{
  "Code": 500,
  "Message": "Server Error"
}
```
