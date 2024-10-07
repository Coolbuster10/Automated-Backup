import os
import shutil
from datetime import datetime

# List of source directories to back up
SOURCE_DIRS = [
    r"C:\path\to\first\folder",
    r"C:\path\to\second\folder",
    r"C:\path\to\third\folder"
]

# Destination directory (Samba share or external backup location)
BACKUP_DIR = r"Z:\backup"

# Log file path
LOG_FILE = r"C:\path\to\backup.log"

# Function to log messages
def log_message(message):
    with open(LOG_FILE, 'a') as log:
        log.write(f"{datetime.now()}: {message}\n")

# Function to calculate total size of the folder
def get_total_size(directory):
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Function to back up folders with progress percentage
def backup_folder(source, destination):
    # Get the folder name and create the corresponding directory in the backup location
    folder_name = os.path.basename(source)
    dest_folder = os.path.join(destination, folder_name)

    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    # Calculate the total size of the source folder
    total_size = get_total_size(source)
    copied_size = 0  # Track the amount of data copied so far

    # Walk through the source folder and copy each file
    for dirpath, _, filenames in os.walk(source):
        for filename in filenames:
            src_file = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(dirpath, source)
            dest_path = os.path.join(dest_folder, relative_path)

            # Ensure the destination subdirectory exists
            os.makedirs(dest_path, exist_ok=True)

            # Copy the file to the destination
            dest_file = os.path.join(dest_path, filename)
            shutil.copy2(src_file, dest_file)

            # Update the copied size
            copied_size += os.path.getsize(src_file)

            # Calculate and display the progress percentage
            progress = (copied_size / total_size) * 100
            print(f"Backing up {filename}... {progress:.2f}% completed", end='\r')

    print(f"\nBackup completed for {folder_name}.")
    log_message(f"Backup completed successfully for {folder_name}")

# Main backup function
def perform_backup():
    try:
        # Check if the backup directory exists
        if not os.path.exists(BACKUP_DIR):
            raise Exception(f"Backup directory {BACKUP_DIR} not found. Is the Samba share mounted?")
        
        # Loop through each source directory and perform the backup
        for source_dir in SOURCE_DIRS:
            if os.path.exists(source_dir):
                print(f"Starting backup for {source_dir}")
                backup_folder(source_dir, BACKUP_DIR)
            else:
                print(f"Source directory {source_dir} does not exist. Skipping...")
                log_message(f"Source directory {source_dir} does not exist. Skipping...")
    
    except Exception as e:
        log_message(f"Backup failed: {str(e)}")
        print(f"Error: {str(e)}")

# Run the backup process
if __name__ == "__main__":
    perform_backup()
