import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from pathlib import Path

class SpotifyClient:
    def __init__(self, client_id, client_secret):
        credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

    def get_genre_and_artist(self, song_title):
        results = self.sp.search(q='track:' + song_title, type='track')
        items = results['tracks']['items']
        if not items:
            return None, "Kein Song gefunden."

        track = items[0]
        artist_id = track['artists'][0]['id']
        
        artist = self.sp.artist(artist_id)
        genres = artist['genres']
        artist_name = artist['name']
        
        return artist_name, genres

if __name__ == "__main__":
    dotenv_path = Path('.env')
    load_dotenv(dotenv_path=dotenv_path)
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    spotify_client = SpotifyClient(client_id, client_secret)

    song_title = "Shape of You"
    artist_name, genres = spotify_client.get_genre_and_artist(song_title)
    if artist_name:
        print(f"Künstler: {artist_name}, Genres: {', '.join(genres)}")
    else:
        print(genres)
