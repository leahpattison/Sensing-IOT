#!/usr/bin/python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import json
import spotipy
import spotipy.util as util
from requests import get
from datetime import datetime


def spotifyRec(your_username, scope, client_id, client_secret, redirect_uri):
    token = util.prompt_for_user_token(
        username=your_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

    # Create spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)

    print(spotifyObject.recommendation_genre_seeds())

    print(spotifyObject.recommendations(seed_genres=['afrobeat', 'alt-rock', 'british','chicago-house'],
                                        target_tempo = 130, target_acousticness = 0.4,
                                        target_liveness = 0.2, target_danceability = 0.54,
                                        target_speechiness = 0.03, target_loudness = -4,target_energy=0.6,
                                        target_instrumentalness = 0))

    return print('lol')


### Spotify Authorization ###
with open('Spotify_Credentials.json') as f:
    spotifyCreds = json.load(f)

spotifydata = spotifyRec(spotifyCreds['Spotifyusername'], spotifyCreds['Spotifyscope'],
                              spotifyCreds['Spotifyclient_id'], spotifyCreds['Spotifyclient_secret'],
                              spotifyCreds['Spotifyredirect_uri'])

