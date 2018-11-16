import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#problem with pip install of spotipy - installs 2.0.1 so pull from github


#Enter user name ect
#Can use a except code


your_username = '1117981227'
scope = 'user-read-private user-read-currently-playing user-read-playback-state user-read-recently-played'
client_id = 'bcfcac8b1e7748ad855ea59ba5554548'
client_secret = 'b9f0390792be4596ab54e964863bd134'
redirect_uri = 'http://google.com/'

token = util.prompt_for_user_token(
        username=your_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

#Create spotify optject with permissions
spotifyObject = spotipy.Spotify(auth=token)

# Get current device
d = spotifyObject.current_user_recently_played()
devices = spotifyObject.current_user_playing_track()

print(devices['timestamp'])
print(devices['item']['name'])
print(devices['item']['album']['artists'][0]['name'])
print(devices['item']['album']['name'])
print(devices['item']['duration_ms'])
print(devices['item']['album']['images'][0])