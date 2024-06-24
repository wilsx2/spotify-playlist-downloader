# Spotify Playlist Downloader

This project allows you to download songs from a Spotify playlist as audio files from YouTube. The project consists of several scripts that interact with the Spotify and YouTube APIs to retrieve song information and download audio streams.

## Project Structure

- `spotify_utils.py`: Handles Spotify API interactions.
- `youtube_utils.py`: Handles YouTube searching and audio stream retrieval.
- `helpers.py`: Contains other utility functions used in main.
- `main.py`: Manages the flow of the program, integrates all functionalities, and handles user interactions.

## Prerequisites

- Python 3.7 or later
- pip (Python package installer)

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/wilsx2/spotify-playlist-downloader.git
    cd spotify-playlist-downloader
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Edit the `.env` file in the root directory of the project and add your Spotify client ID and client secret from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard). Your `.env` file should look like this:

    ```
    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIPY_REDIRECT_URI=http://localhost:3000
    ```

## How to Run

1. **Run the main script:**

    ```sh
    python main.py
    ```

2. **Follow the prompts:**

    - Provide the Spotify playlist URL when prompted.
    - Choose the download destination (default is the Music folder).

3. **Wait for the download to complete:**

    - The program will download the songs using multiprocessing to speed up the process.
    - A log file will be saved in the download folder with the results of each download.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
