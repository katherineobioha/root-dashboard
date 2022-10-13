import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import dash_daq as daq
import requests
import calendar
from datetime import datetime

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt


def api_call():
    latInitial =  5.544230
    lonInitial =  5.760269
    city = 'Delta'
    state = 'Nigeria'
    key = '399d8f4ee537173296522eb45d2f25b6'  # put api key here
   # r = requests.get("http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}".format(city, state, key))
    r = requests.get("http://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&appid={}&units=imperial".format(latInitial, lonInitial, key))
    data = r.json()
    day = [calendar.day_name[(datetime.strptime((datetime.utcfromtimestamp(data["daily"][i]['dt']).strftime('%d-%m-%Y')),'%d-%m-%Y')).weekday()] for i
           in range(0, 5, 1)]
   # day = [calendar.day_name[(datetime.strptime(data["list"][i]['dt_txt'].split(" ")[0], '%Y-%M-%d')).weekday()] for i in range(3, 36, 8)]
    #description = [data["daily"][i]["weather"][0]['description'] for i in range(0, 5, 1)]
    description = ["http://openweathermap.org/img/wn/"+data["daily"][i]["weather"][0]['icon']+"@2x.png" for i in range(0, 5, 1)]
    temp = [data["daily"][i]['temp']['min']for i in range(0, 5, 1)]
    tempMax = [data["daily"][i]['temp']['max'] for i in range(0, 5, 1)]
    wind_speed = [data["daily"][i]['wind_speed'] for i in range(0, 5, 1)]
    humidity = [data["daily"][i]['humidity'] for i in range(0, 5, 1)]
    df = pd.DataFrame(
        data={'Day': day, ' ': description, 'Temperature Low': temp,'Temperature High': tempMax, 'Humidity': humidity, 'Wind': wind_speed})

    return df


print('Display weather')
df = api_call()
print(df)
