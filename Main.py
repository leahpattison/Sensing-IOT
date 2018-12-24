import gspread
from oauth2client.service_account import ServiceAccountCredentials
from API import Spotify_API, dark_sky_API
##### SENSING-IOT COURSEWORK 2018 #####
# Script pulls current playing track data from users spotify & weather data from London, appends to googlesheet
# Spotify: spotipy library for spotify API
# Weather data: Dark Sky API
# Google sheet: Gspread API


### Google drive script ###
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Credentials.json', scope)
gc = gspread.authorize(credentials)
doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1tdNvPJiN7f1mJFN0sjtZMy7s_MwcuzsVzBkgFAtgKRk/edit#gid=0')

### Credentials for spotify API ###
#problem with pip install of spotipy - installs 2.0.1 so pull from github
Spotifyusername = '1117981227'
Spotifyscope = 'user-read-private user-read-currently-playing user-read-playback-state user-read-recently-played'
Spotifyclient_id = 'bcfcac8b1e7748ad855ea59ba5554548'
Spotifyclient_secret = 'b9f0390792be4596ab54e964863bd134'
Spotifyredirect_uri = 'http://google.com/'

### Credentials for weather API ###
darksky_key = "5809cc0ad2768d8c9dcd6ee3bc868dec"

### Spotify update ###
#Time stamp, artist name, album name, duration of song, album image url
# [time, name, artist, album, duration, album_image_url, spotify url, trackid, trackplaying]
try:
    spotifydata = Spotify_API(Spotifyusername, Spotifyscope, Spotifyclient_id, Spotifyclient_secret, Spotifyredirect_uri)
    print(spotifydata[-1])
    if spotifydata[-1] == False:
        print('No track playing')
    elif spotifydata[-1] == True:
        doc.worksheet('Spotify').append_row(spotifydata)
        print('Spotify data added')
except:
    print('No track playing')

### Dark Sky Weather API update ###
# [time, cloudcover, windspeed, temp, humidity, icon, precip]
try:
    weatherdata = dark_sky_API(darksky_key)
    doc.worksheet('Weather').append_row(weatherdata)
    print('Weather data added')
except:
    print('No weather data')

