import os
import shutil
import subprocess
from datetime import datetime

# List of source directories you want to back up
SOURCE_DIRS = [
    r"C:\Users\coolb\Documents",
    r"C:\Users\coolb\Pictures\Pictures",
    r"C:\Users\coolb\Desktop"
]

# NAS share backup directory (mapped as Z: drive)
BACKUP_DIR = r"Z:\Data\Backup"

# Function to check if the backup directory is available
def check_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        raise Exception(f"Backup directory {BACKUP_DIR} not found. Is the Samba share mounted?")

# Function to copy files with progress monitoring
def copy_files_with_progress():
    for source_dir in SOURCE_DIRS:
        # Create destination directory within the Samba share (keeping folder names)
        folder_name = os.path.basename(source_dir)
        destination_dir = os.path.join(BACKUP_DIR, folder_name)

        # Ensure the destination directory exists
        os.makedirs(destination_dir, exist_ok=True)

        # Get the total size of the source directory for progress calculation
        total_size = sum(os.path.getsize(os.path.join(root, file)) 
                         for root, _, files in os.walk(source_dir) 
                         for file in files)

        copied_size = 0  # To keep track of the size copied

        # Walk through the source directory and copy files
        for root, _, files in os.walk(source_dir):
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(destination_dir, os.path.relpath(src_file, source_dir))

                # Copy the file
                shutil.copy2(src_file, dst_file)

                # Update copied size
                copied_size += os.path.getsize(src_file)

                # Calculate and display progress
                progress_percentage = (copied_size / total_size) * 100
                print(f"Backing up {file}... {progress_percentage:.2f}% completed", end='\r')

        log_message(f"Backup completed successfully for {folder_name} on {datetime.now()}")

# Function to log messages
def log_message(message):
    log_file = r"C:\Users\coolb\Documents\backup.log"
    with open(log_file, 'a') as log:
        log.write(message + '\n')

# Main script execution
if __name__ == "__main__":
    try:
        check_backup_dir()  # Check if the Samba share is available
        copy_files_with_progress()  # Perform the backup for all directories
    except Exception as e:
        log_message(f"Backup failed: {str(e)}")
