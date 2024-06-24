import multiprocessing
from tqdm import tqdm
from functools import partial

# Import functions from other scripts
from spotify_utils import get_playlist_name_and_song_list_from_spotify_url
from youtube_utils import create_search_query, get_top_url_from_youtube_search, get_highest_quality_audio_stream
from helpers import remove_illegal_characters, save_log, create_playlist_folder, clear_console, get_yes_or_no_input, get_output_path

def get_playlist_name_and_song_list_from_user_input() -> tuple[str, list[dict[str, str]]]:
    """Prompt the user for a Spotify playlist URL and return the playlist name and song list."""
    clear_console()
    input_url = input("What Spotify playlist do you want to download? (Provide URL)\n\t> ")

    try:
        playlist_name, song_list = get_playlist_name_and_song_list_from_spotify_url(input_url)
        print(f"Playlist found: \"{playlist_name}\"")
        return playlist_name, song_list
    except Exception as e:
        print(f"Error: {e}")
        if get_yes_or_no_input("Try again?"):
            return get_playlist_name_and_song_list_from_user_input()
        else:
            return None, None

def download_audio_stream(url: str, output_path: str, filename: str) -> None:
    """Download the highest quality audio stream from a YouTube video URL."""

    audio_stream = get_highest_quality_audio_stream(url)
    audio_stream.download(output_path=output_path, filename=filename)

def download_song(song_info: dict[str, str], output_path: str) -> tuple[int, str]:
    """Download a song and return a summary of the result."""

    song_description = f"{song_info['number']} {song_info['name']} - {song_info['artists']} - {song_info['album']}"
    search_query = create_search_query(song_info)

    failure_message = None
    video_url = None

    try:
        video_url = get_top_url_from_youtube_search(search_query)
    except Exception as e:
        failure_message = f"Failed to retrieve YouTube URL: {str(e)}"
    
    if video_url:
        try:
            filename = remove_illegal_characters(song_description) + ".mp4"
            download_audio_stream(video_url, output_path, filename)
        except Exception as e:
            failure_message = f"Failed to download audio stream: {str(e)}"

    result_summary = (
        f"Spotify Info: {song_description}\n"
        f"\tDownload: {'Successful' if video_url and not failure_message else failure_message}\n"
        f"\tQuery Used: {search_query}\n"
        f"\tURL Retrieved: {video_url if video_url else 'N/A'}"
    )
    return int(song_info['number']), result_summary

def main() -> None:
    """Main function to download songs from a Spotify playlist."""
    playlist_name, song_list = get_playlist_name_and_song_list_from_user_input()

    if not playlist_name:
        return

    download_path = get_output_path()
    playlist_folder = create_playlist_folder(playlist_name, download_path)

    result_summaries = [None for _ in range(len(song_list))]
    download_song_with_path = partial(download_song, output_path=playlist_folder)

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        results = pool.imap_unordered(download_song_with_path, song_list)
        progress_bar = tqdm(results, total=len(song_list), colour='#16c60c', desc="Downloading")
        for song_number, result_summary in progress_bar:
            result_summaries[song_number - 1] = result_summary

    save_log(result_summaries, playlist_folder)
    print(f"Complete! Downloaded to {playlist_folder}")

if __name__ == "__main__":
    main()