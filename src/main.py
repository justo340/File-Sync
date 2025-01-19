# import os
import requests
import config
from mtp_sync_utils import check_mtp_connection, find_download_folder, download_files_from_phone
from google_drive_utils import sync_google_drive_to_local, sync_local_to_google_drive
from local_sync_utils import sync_folders
from quickstart import authenticate_google_drive
from config import GOOGLE_DRIVE_FOLDER_ID,FOLDER_PATHS
from logging_utils import setup_logger

# Separate logger for sync.log (main syncing process)
sync_logger = setup_logger("sync.log", "INFO")

# Separate logger for mtp_sync.log (MTP-specific logging)
mtp_logger = setup_logger("mtp_sync.log", "INFO")


def is_connected_to_internet():
    """
    Check if the system is connected to the internet.
    """
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def sync_phone():
    """
    Sync the phone's 'Download' folder to the local system.
    If connected via USB, use MTP sync.
    If USB is not available, sync via Google Drive.
    """
    local_phone_path = config.FOLDER_PATHS["phone"]
    
    # Attempt MTP-based syncing
    sync_logger.info("Checking for MTP device connection......")
    if check_mtp_connection():
        mtp_logger.info("MTP connection detected. Starting sync...")
        folder_id = find_download_folder()
        if folder_id:
            download_files_from_phone(folder_id, local_phone_path)
            mtp_logger.info("MTP sync completed successfully.")
        else:
            mtp_logger.error("Unable to locate 'Download' folder on MTP device.")
    else:
        sync_logger.warning("No MTP device detected. Falling back to Google Drive sync...")
        
        # Check for internet connection before falling
        if is_connected_to_internet():
            sync_logger.info("Internet connection detected. Falling back to Google Drive sync...")
            
            # Sync from Google Drive
            drive = authenticate_google_drive()
            sync_logger.info("Syncing Google Drive to phone folder...")
            sync_google_drive_to_local(drive, config.GOOGLE_DRIVE_FOLDER_ID, local_phone_path)
        else:
            sync_logger.error("No internet connection detected. Unable to sync via Google Drive.")

def main():
    print('started executing the main folder..........')
   
    sync_logger.info("Starting Folder Sync Tool...")
    
    
    sync_logger.info(f"Google Drive Folder ID: {config.GOOGLE_DRIVE_FOLDER_ID}")
    
    
    
    # Authenticate Google Drive and get the drive instance
    drive = authenticate_google_drive()  # This will use the credentials stored or reauthenticate if necessary


    # Sync Google Drive with local devices
    sync_logger.info("Syncing Google Drive to laptop...")
    sync_google_drive_to_local(drive, GOOGLE_DRIVE_FOLDER_ID,FOLDER_PATHS["laptop"])
    sync_local_to_google_drive(drive, FOLDER_PATHS["laptop"], GOOGLE_DRIVE_FOLDER_ID)


    # # Sync between local folders
    sync_logger.info("Syncing laptop and external drive...")
    sync_folders(FOLDER_PATHS["laptop"], FOLDER_PATHS["external_drive"])
    sync_folders(FOLDER_PATHS["external_drive"], FOLDER_PATHS["laptop"])

    # logger.info("Syncing phone with drive and usb connection to laptop..")
    sync_phone()

    sync_logger.info("Folder Sync Tool completed.")

if __name__ == "__main__":
    main()

