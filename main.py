import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import filedialog

# Logging configuration for debugging
logging.basicConfig(
    filename="file_organizer_debug.log",  # Store log output in a file
    level=logging.DEBUG,  # Set to DEBUG to capture more details
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define where the files will be moved based on their extensions
DIRECTORIES = {
    "Executables": [".exe", ".msi"],
    "Images": [".jpeg", ".jpg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Documents": [".doc", ".docx", ".pdf", ".txt", ".xls", ".xlsx"],
    "Music": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Code": [".py", ".java", ".cpp", ".html", ".css", ".js"],
}

# Wait time for incomplete file operations
FILE_WAIT_TIME = 1  # Time in seconds to wait for a file to be fully written

class FileOrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.debug(f"File created: {event.src_path}")
            self.process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            logging.debug(f"File modified: {event.src_path}")
            self.process_file(event.src_path)

    def process_file(self, src_path):
        try:
            # Ensure the file is fully copied/downloaded before processing
            time.sleep(FILE_WAIT_TIME)

            if os.path.isfile(src_path):
                logging.debug(f"Processing file: {src_path}")
                self.move_file(src_path)
            else:
                logging.debug(f"File not found or not ready: {src_path}")
        except Exception as e:
            logging.error(f"Error processing file {src_path}: {e}")

    def move_file(self, src_path):
        file_ext = os.path.splitext(src_path)[1].lower()

        moved = False
        for folder_name, extensions in DIRECTORIES.items():
            if file_ext in extensions:
                self.move_to_folder(src_path, folder_name)
                moved = True
                break

        if not moved:
            # If file extension is not in our list, move to a generic "Others" folder
            self.move_to_folder(src_path, "Others")

    def move_to_folder(self, src_path, folder_name):
        try:
            dest_folder = os.path.join(user_directory, folder_name)
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            dest_path = os.path.join(dest_folder, os.path.basename(src_path))

            # Ensure no overwriting if a file with the same name exists
            if os.path.exists(dest_path):
                dest_path = self.generate_unique_name(dest_path)

            shutil.move(src_path, dest_path)
            logging.info(f"Moved {src_path} to {dest_path}")

        except Exception as e:
            logging.error(f"Error moving file {src_path} to {folder_name}: {e}")

    def generate_unique_name(self, path):
        """
        Generates a unique file name if a file with the same name already exists.
        """
        base, extension = os.path.splitext(path)
        counter = 1
        new_path = f"{base} ({counter}){extension}"

        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base} ({counter}){extension}"

        return new_path

    def process_existing_files(self):
        """
        Process all existing files in the selected folder when the script starts.
        """
        logging.info(f"Processing existing files in {user_directory}...")
        for filename in os.listdir(user_directory):
            file_path = os.path.join(user_directory, filename)
            if os.path.isfile(file_path):
                logging.debug(f"Found existing file: {file_path}")
                self.move_file(file_path)
        logging.info("Finished processing existing files.")


def select_directory():
    """
    Opens a file dialog to let the user select a directory.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title="Select the folder to organize")
    return folder_selected


if __name__ == "__main__":
    # Get the user to select a directory
    user_directory = select_directory()
    if not user_directory:
        logging.error("No directory selected. Exiting...")
        exit()

    logging.info(f"Selected directory: {user_directory}")

    # Set up observer and event handler
    event_handler = FileOrganizerHandler()

    # First process existing files
    event_handler.process_existing_files()

    observer = Observer()

    # Log starting
    logging.debug(f"Starting to monitor folder: {user_directory}")

    try:
        # Start observing the folder
        observer.schedule(event_handler, user_directory, recursive=False)
        observer.start()

        while True:
            # Keeps the script running
            time.sleep(10)

    except Exception as e:
        logging.error(f"Error in main loop: {e}")

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
