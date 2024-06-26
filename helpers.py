import os
import re
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, Tk

# Create hidden tkinter window for using the file dialog method
root = Tk()
root.withdraw()


# Regards the file system
def remove_illegal_characters(string: str) -> str:
    """Return a copy of the string with characters removed that are not allowed in file/folder names."""
    return re.sub(r'[\\/:*?"<>|]', '', string)

def save_log(log_messages: list[str], output_path: str) -> None:
    """Save the log messages to a log.txt file in the output path."""

    log_file_path = os.path.join(output_path, 'log.txt')
    with open(log_file_path, 'w') as log_file:
        complete_log = ""

        for message in log_messages:
            complete_log = complete_log + "\n" + message.encode('charmap', 'replace').decode('charmap')

        log_file.write(complete_log)

def create_playlist_folder(playlist_name: str, output_path: str) -> str:
    """Create a folder for the playlist with the current date and time in the output path."""

    now = datetime.now().strftime("%d-%m-%Y %H;%M;%S")
    playlist_name = remove_illegal_characters(playlist_name)
    folder_path = os.path.join(output_path, f"{playlist_name} ({now})")

    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# Regards the console and/or user inputs

def clear_console():
    # Function to clear console screen
    os.system('cls')

def get_yes_or_no_input(prompt: str) -> bool:
    """Prompt the user for a yes or no response."""
    while True:
        response = input(prompt + ' (y/n) ').strip().lower()

        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print(f"Your response \"{response}\" was not recognized, please respond again.")

def get_output_path() -> str:
    """Prompt the user for an output directory, defaulting to the Music folder."""

    default_path = str(Path.home() / "Music")
    if get_yes_or_no_input("Would you like to pick a destination for your download? Otherwise, it will go to Music."):
        return filedialog.askdirectory(title="Select destination folder") or default_path
    return default_path