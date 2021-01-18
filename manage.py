import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import main
app = Flask(__name__)
method = 0
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/playlistgenerator", methods=['GET', 'POST'])
def playlistgenerator():
    method = 1
    if request.method == 'POST':
        req = request.form
        arty = req.get("artists")
        global playlist_name
        playlist_name = req.get("playlist_name")
        global list
        list = main.get_tracks_url(arty)
        return redirect('/signin')
    return render_template("playlistgenerator.html")





CLIENT_ID = "33d36c75c90f4c6897e6c9f62d71d3cb"
CLIENT_SECRET = "340a5398a57e4eacb0a530e921c8dca3"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='33d36c75c90f4c6897e6c9f62d71d3cb', client_secret='340a5398a57e4eacb0a530e921c8dca3'))

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


@app.route("/signin", methods= ['GET', 'POST'])
def signin():
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q", methods = ['GET', 'POST'])
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)
    main.topTen(access_token, profile_data, list, playlist_name)
    display_arr = "Check your Spotify Playlists!!"
    return render_template("signin.html", sorted_array=display_arr)



if __name__ == "__main__":
    app.run(debug=True, port=PORT)
