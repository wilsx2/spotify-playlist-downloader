import pytube
from pytube import YouTube
from youtubesearchpython import VideosSearch

def create_search_query(song_info: dict[str, str]) -> str:
    """Create a YouTube search query from song information."""

    return get_youtube_search_query_from_song_info(song_info)

def get_youtube_search_query_from_song_info(song_info: dict[str, str]) -> str:
    """Generate a YouTube search query from song information."""
    song_name = song_info['name']
    artist_names = song_info['artists']
    return f"{song_name} by {artist_names} Official Audio"

def get_top_url_from_youtube_search(search_query: str) -> str:
    """Retrieve the top video URL from a YouTube search query."""
    video_search = VideosSearch(search_query, limit=1)
    url = video_search.result()['result'][0]['link']
    return url

def get_highest_quality_audio_stream(url: str) -> pytube.Stream:
    """Retrieve the highest quality audio stream from a YouTube video URL."""
    yt = YouTube(url)
    audio_streams = yt.streams.filter(only_audio=True)
    return max(audio_streams, key=lambda stream: int(stream.abr[:-4]))

def get_audio_stream_from_song_info(song_info: dict[str, str]) -> pytube.Stream:
    """Get the highest quality audio stream for a song using its information."""
    search_query = get_youtube_search_query_from_song_info(song_info)
    video_url = get_top_url_from_youtube_search(search_query)
    return get_highest_quality_audio_stream(video_url)
