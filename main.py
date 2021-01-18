import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='33d36c75c90f4c6897e6c9f62d71d3cb', client_secret='340a5398a57e4eacb0a530e921c8dca3'))

def get_artist_url(q):
    search_q = spotify.search(q,limit = 1, type='artist') #seraches for artist
    return search_q['artists']['items'][0]['external_urls']['spotify'] #gets link to artist

def get_tracks_url(input_string):
    temp_list = []
    artist_list = []
    temp_list = input_string.split(",")
    for i in temp_list:
            artist_list.append(get_artist_url(i))#appends artist url to list

    not_final_list = []
    final_list = []
    count = 0
    for art in artist_list:
        not_final_list.append(spotify.artist_top_tracks(art)) #appends artist top tracks to final_list
    for artist in not_final_list:
        for track in artist['tracks']:
            final_list.append(track['external_urls']['spotify'])
    return final_list
def topTen(access_token, profile_data, list, playlist_name):
        sp = spotipy.Spotify(access_token)
        sp.user_playlist_create(profile_data['id'], playlist_name, description="Playlist created by playlist maker")
        playlist_id = ((sp.user_playlists(profile_data['id'], limit = 50, offset = 0))['items'][0]['id'])
        sp.user_playlist_add_tracks(profile_data['id'], playlist_id, list)
def main():
    pass
main()
