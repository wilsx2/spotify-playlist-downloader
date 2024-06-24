import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Load environment variables from .env file
load_dotenv()

# Read Spotify credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:3000')

# Spotify authentication
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))

def get_playlist_name(playlist_id: str) -> str:
    """Retrieve the playlist name from the Spotify API."""
    playlist_info = sp.playlist(playlist_id=playlist_id, fields='name')
    return playlist_info['name']

def get_all_playlist_tracks(playlist_id: str) -> list[dict]:
    """Retrieve all tracks from a Spotify playlist using pagination."""
    tracks = []
    results = sp.playlist_tracks(playlist_id=playlist_id)
    tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return tracks

def format_track_info(tracks: list[dict]) -> list[dict[str, str]]:
    """Format track information into a list of dictionaries."""
    formatted_song_list = []

    for index, track_info in enumerate(tracks):
        track = track_info['track']
        track_name = track['name']
        album_name = track['album']['name']
        artists = [artist['name'] for artist in track['artists']]
        artist_names = ', '.join(artists)
        track_number = str(index + 1)
        display_name = f"{track_name} - {artist_names}"

        formatted_song_list.append({
            'artists': artist_names,
            'album': album_name,
            'number': track_number,
            'name': track_name,
            'display': display_name
        })

    return formatted_song_list

def get_playlist_name_and_song_list_from_spotify_url(url: str) -> tuple[str, list[dict[str, str]]]:
    """Get the playlist name and formatted song list from a Spotify playlist URL."""
    playlist_name = get_playlist_name(url)
    tracks = get_all_playlist_tracks(url)
    formatted_song_list = format_track_info(tracks)
    return playlist_name, formatted_song_list