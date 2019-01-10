#!/usr/bin/python3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import  MultiOutputRegressor
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import spotipy
import spotipy.util as util
from requests import get
from datetime import datetime

##### SENSING-IOT COURSEWORK 2018 #####

def algorithm():
    ### Google drive Authorization ###
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
    WeatherData = WeatherData[['datetime','wind speed', 'cloud cover', 'temperature','humidity', 'icon']]
    WeatherData = WeatherData.apply(pd.to_numeric, errors='ignore')
    WeatherData['datetime'] = pd.to_datetime(WeatherData['datetime'], infer_datetime_format=True)
    temp = (WeatherData['temperature']-32)*5/9
    WeatherData['temperature'] = temp
    WeatherData.fillna(0, inplace = True)

    #categorical_cols = WeatherData['icon']
    #WeatherData['icon'] = WeatherData['icon'].astype('category')

    combinedData = pd.merge_asof(SpotifyData.sort_values('datetime'),WeatherData, on = "datetime", direction ="nearest")

    weather = combinedData[['cloud cover','wind speed', 'temperature', 'humidity']]
    spotify = combinedData[['tempo', 'acousticness', 'livelines', 'danceability', 'speechiness',
                            'loudness', 'energy', 'instrumentalness']]

    #weather = pd.get_dummies(weather)

    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(weather.values)
    weather = pd.DataFrame(x_scaled)

    weather = np.asarray(weather, dtype=np.float64)
    spotify = np.asarray(spotify, dtype=np.float64)

    X_train, X_test = train_test_split(weather, test_size=0.25)
    Y_train, Y_test = train_test_split(spotify, test_size=0.25)

    #print(X_train.shape)
    #print(Y_train.shape)

    #print(X_train)
    #print(Y_train)

    knn =KNeighborsRegressor()
    mlp = MLPClassifier()
    rr =  RandomForestRegressor(n_estimators=10)
    regr = MultiOutputRegressor(rr)

    regr.fit(X_train, Y_train)
    #print(X_test[:][1])
    #print(X_test)

    return regr

def regression(model, data):
    m = model
    d = data
    audiodata = m.predict([[d[0], d[1], d[2], d[3]]])
    return audiodata

def createSpotify():
    ### Spotify Authorization ###
    with open('Spotify_Credentials.json') as f:
        spotifyCreds = json.load(f)

    token = util.prompt_for_user_token(
        username=spotifyCreds['Spotifyusername'],
        scope=spotifyCreds['Spotifyscope'],
        client_id=spotifyCreds['Spotifyclient_id'],
        client_secret=spotifyCreds['Spotifyclient_secret'],
        redirect_uri=spotifyCreds['Spotifyredirect_uri'])


    # Create spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)

    return spotifyObject

def spotifyRec(Tempo, Acoustic, Live, Dance, Speech, Loud, Energy, Instrumental, description):

    spotifyObject = createSpotify()

    tempo = Tempo
    acoustic = Acoustic
    live = Live
    dance = Dance
    speech = Speech
    loud = Loud
    energy = Energy
    instrumental = Instrumental
    genres = spotifyObject.recommendation_genre_seeds()
    #print(genres)
    desc = description
    rec = spotifyObject.recommendations(seed_genres=['afrobeat', 'alt-rock', 'british','chicago-house'],
                                        target_tempo = tempo, target_acousticness = acoustic,
                                        target_liveness = live, target_danceability = dance,
                                        target_speechiness = speech, target_loudness =loud,target_energy=energy,
                                        target_instrumentalness = instrumental)

    word = "This is a Spotify playlist made by the Whatever the Weather Application. Sponsored by Dark Sky and Spotify"
    trackURI = []
    user_data = spotifyObject.current_user()
    playlist = spotifyObject.user_playlist_create(user_data["id"], desc, description=word)
    playlist_id = playlist["id"]


    for i in range(len(rec['tracks'])):
        #print(rec['tracks'][i]['uri'])
        t = rec['tracks'][i]['uri']
        trackURI.append(t)
    #print(trackURI)
    p = spotifyObject.user_playlist_add_tracks(user_data['id'], playlist_id, trackURI)

    #p = playlist['id']
    #print(p)
    #t = spotifyObject.track(trackURI[0])
    #print(t)

    #thing = t['album']['images'][0]['url']

    #print(thing)
    return playlist_id

def getGenres():
    spotifyObject = createSpotify()

    genres = spotifyObject.recommendation_genre_seeds()
    genres = genres['genres']
    return genres

model = algorithm()
data = [0.2, 2.0, 10.0, 0.76]
t = regression(model, data)
t = t[0]
prediction = spotifyRec(t[0], t[1], t[2],t[3], t[4], t[5], t[6], t[7], "nah")

#getGenres()

def dark_sky_API(location):

    ### Weather Authorization ###
    with open('Weather_Credentials.json') as f:
        weatherCreds = json.load(f)

    key = weatherCreds['darksky_key']
    sheffyT = location #Latitude and longitude for sheffield terrace, london

    Dark = "https://api.darksky.net/forecast/{}/{loc[0]:},{loc[1]:}?".format(key, loc=sheffyT)
    weather = get(Dark)
    currentW = json.loads(weather.text)['currently'] #Current weather data

    #Connvert UNIX time stamp to YMDHMS
    currentTime = currentW['time']
    timedate = datetime.fromtimestamp(int(currentTime)).strftime('%Y-%m-%d %H:%M:%S')

    return [currentW['cloudCover'], currentW['windSpeed'], currentW['temperature'], currentW['humidity'], currentW['icon']]

#print(dark_sky_API((51, -0.1)))

def webSpotify(whatever):
    token = "BQCyKM8pr9mnPNIwptOtlmV2Cu4g3iahURxkBfcvGXoWXsS4Rb9V2T9dEQqg9ObaWLQGW7gk970-eSzoPkofsqwqji-_IGBChn5sDl-GUcRGWtqTjzIY8-diOxcEQzMXt6NIpOnRO-BIzih94v3iOxctgs5yrMcbP9MBvby4"