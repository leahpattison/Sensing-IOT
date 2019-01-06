#!/usr/bin/python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt


##### SENSING-IOT COURSEWORK 2018 #####

### Google drive Authorization ###
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Google_Credentials.json', scope)
gc = gspread.authorize(credentials)
doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tdNvPJiN7f1mJFN0sjtZMy7s_MwcuzsVzBkgFAtgKRk/edit#gid=0')

SpotifyData = doc.worksheet('Spotify').get_all_values()
SpotifyData = pd.DataFrame(SpotifyData[1:], columns=SpotifyData[0])
SpotifyData = SpotifyData[['datetime', 'track name', 'artist', 'track duration', 'genre', 'tempo', 'acousticness',
         'livelines', 'danceability', 'speechiness', 'loudness', 'energy', 'instrumentalness']]
SpotifyData = SpotifyData.apply(pd.to_numeric, errors='ignore')
SpotifyData['datetime'] = pd.to_datetime(SpotifyData['datetime'], infer_datetime_format=True)
SpotifyData.index = SpotifyData['datetime']

WeatherData = doc.worksheet('Weather').get_all_values()
WeatherData = pd.DataFrame(WeatherData[1:], columns = WeatherData[0])
WeatherData = WeatherData[['datetime', 'cloud cover', 'temperature', 'icon']]
WeatherData = WeatherData.apply(pd.to_numeric, errors='ignore')
WeatherData['datetime'] = pd.to_datetime(WeatherData['datetime'], infer_datetime_format=True)
WeatherData.index = WeatherData['datetime']
temp = (WeatherData['temperature']-32)*5/9
WeatherData['temperature'] = temp


WeatherData['temperature'].plot(label='temperature')
plt.legend()
plt.show()
