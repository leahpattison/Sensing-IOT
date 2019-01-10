#!/usr/bin/python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from sklearn.linear_model import LinearRegression, Perceptron
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import  MultiOutputRegressor
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import json
import spotipy
import spotipy.util as util
from requests import get
from datetime import datetime

## Google drive Authorization ###
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Google_Credentials.json', scope)
gc = gspread.authorize(credentials)
doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tdNvPJiN7f1mJFN0sjtZMy7s_MwcuzsVzBkgFAtgKRk/edit#gid=0')

SpotifyData = doc.worksheet('Spotify').get_all_values()
SpotifyData = pd.DataFrame(SpotifyData[1:], columns=SpotifyData[0])
SpotifyData = SpotifyData[['datetime', 'tempo', 'acousticness',
         'livelines', 'danceability', 'speechiness', 'loudness', 'energy', 'instrumentalness']]
SpotifyData = SpotifyData.apply(pd.to_numeric, errors='ignore')
SpotifyData['datetime'] = pd.to_datetime(SpotifyData['datetime'], infer_datetime_format=True)
#SpotifyData.index = SpotifyData['datetime']
SpotifyData.fillna(0, inplace = True)
SpotifyData = SpotifyData.drop_duplicates(subset = None, keep = 'first')

WeatherData = doc.worksheet('Weather').get_all_values()
WeatherData = pd.DataFrame(WeatherData[1:], columns = WeatherData[0])
WeatherData = WeatherData[['datetime', 'cloud cover', 'temperature','humidity', 'icon']]
WeatherData = WeatherData.apply(pd.to_numeric, errors='ignore')
WeatherData['datetime'] = pd.to_datetime(WeatherData['datetime'], infer_datetime_format=True)
temp = (WeatherData['temperature']-32)*5/9
WeatherData['temperature'] = temp
WeatherData.fillna(0, inplace = True)
categorical_cols = WeatherData['icon']
WeatherData['icon'] = WeatherData['icon'].astype('category')

combinedData = pd.merge_asof(SpotifyData.sort_values('datetime'),WeatherData, on = "datetime", direction ="nearest")

weather = combinedData[[ 'cloud cover','temperature', 'humidity','icon']]
spotify = combinedData[['tempo', 'acousticness', 'livelines', 'danceability', 'speechiness',
                        'loudness', 'energy', 'instrumentalness']]