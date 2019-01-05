#!/usr/bin/python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from API import Spotify_API, dark_sky_API
import json

##### SENSING-IOT COURSEWORK 2018 #####

### Google drive Authorization ###
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Google_Credentials.json', scope)
gc = gspread.authorize(credentials)
doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tdNvPJiN7f1mJFN0sjtZMy7s_MwcuzsVzBkgFAtgKRk/edit#gid=0')

### Spotify Authorization ###
with open('Spotify_Credentials.json') as f:
    spotifyCreds = json.load(f)

### Weather Authorization ###
with open('Weather_Credentials.json') as f:
    weatherCreds = json.load(f)

try:
    spotifydata = Spotify_API(spotifyCreds['Spotifyusername'], spotifyCreds['Spotifyscope'],
                              spotifyCreds['Spotifyclient_id'], spotifyCreds['Spotifyclient_secret'],
                              spotifyCreds['Spotifyredirect_uri'])
    print(spotifydata[-1])
    if spotifydata[-1] == False:
        print('No track playing')
    elif spotifydata[-1] == True:
        doc.worksheet('Spotify').append_row(spotifydata)
        print('Spotify data added')
except:
    print('No track playing')


try:
    weatherdata = dark_sky_API(weatherCreds['darksky_key'])
    doc.worksheet('Weather').append_row(weatherdata)
    print('Weather data added')
except:
    print('No weather data')

