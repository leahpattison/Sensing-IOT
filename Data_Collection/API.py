import json
import spotipy
import spotipy.util as util
from requests import get
from datetime import datetime


def Spotify_API(your_username, scope, client_id, client_secret, redirect_uri):
    token = util.prompt_for_user_token(
        username=your_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

    # Create spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)

    # Get current playing track
    devices = spotifyObject.current_user_playing_track()

    # Connvert UNIX time stamp to YMDHMS
    time = devices['timestamp']/1E3
    timedate = datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
    print(devices)
    name = devices['item']['name'] #song name
    url = devices['item']['external_urls']['spotify'] # song url
    artist = devices['item']['album']['artists'][0]['name'] #artist name
    artist2 = devices['item']['album']['artists'][0]['uri']
    album = devices['item']['album']['name'] #album name
    duration = devices['item']['duration_ms'] #song duration
    album_image_url = devices['item']['album']['images'][0]['url'] #album image url
    trackplaying = devices['is_playing'] #T/F track is playing
    trackid = devices['item']['uri'] #Spotify track ID


    artists = spotifyObject.artist(artist2)
    genres = artists['genres']
    print(genres)
    analysis = spotifyObject.audio_features(trackid)
    return [timedate, name, artist, album, duration,album_image_url, url, trackid, genres[0],trackplaying, analysis[0]['tempo'],
            analysis[0]['acousticness'], analysis[0]['liveness'], analysis[0]['danceability'], analysis[0]['speechiness'],
            analysis[0]['loudness'], analysis[0]['energy'], analysis[0]['instrumentalness']]

def dark_sky_API(key):
    sheffyT = ("51.505", "-0.196") #Latitude and longitude for sheffield terrace, london
    Dark = "https://api.darksky.net/forecast/{}/{loc[0]:},{loc[1]:}?".format(key, loc=sheffyT)
    weather = get(Dark)
    currentW = json.loads(weather.text)['currently'] #Current weather data

    #Connvert UNIX time stamp to YMDHMS
    currentTime = currentW['time']
    timedate = datetime.fromtimestamp(int(currentTime)).strftime('%Y-%m-%d %H:%M:%S')

    return [timedate, currentW['cloudCover'], currentW['windSpeed'], currentW['temperature'], currentW['humidity'], currentW['icon'], currentW['precipIntensity']]