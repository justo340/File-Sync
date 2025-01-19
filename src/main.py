if __name__ == "__main__":
    from google_drive_utils import sync_google_drive_to_local, sync_local_to_google_drive
    from local_sync_utils import sync_folders
    from logging_utils import setup_logger
    from quickstart import authenticate_google_drive
    from config import GOOGLE_DRIVE_FOLDER_ID,FOLDER_PATHS
    import importlib
    import config

    # Force reload to get the latest data from config.py
    importlib.reload(config)
    
    print('started executing the main folder..........')
    logger = setup_logger("sync.log", "INFO")

    logger.info("Starting Folder Sync Tool...")
    
    #GOOGLE_DRIVE_FOLDER_ID = config.GOOGLE_DRIVE_FOLDER_ID
    logger.info(f"Google Drive Folder ID: {config.GOOGLE_DRIVE_FOLDER_ID}")
    
    
    
    # Authenticate Google Drive and get the drive instance
    drive = authenticate_google_drive()  # This will use the credentials stored or reauthenticate if necessary


    # Sync Google Drive with local devices
    logger.info("Syncing Google Drive to laptop...")
    sync_google_drive_to_local(drive, GOOGLE_DRIVE_FOLDER_ID,FOLDER_PATHS["laptop"])
    #sync_local_to_google_drive(drive, FOLDER_PATHS["laptop"], GOOGLE_DRIVE_FOLDER_ID)


    # # Sync between local folders
    # logger.info("Syncing laptop and external drive...")
    # sync_folders(FOLDER_PATHS["laptop"], FOLDER_PATHS["external_drive"])
    # sync_folders(FOLDER_PATHS["external_drive"], FOLDER_PATHS["laptop"])

    # logger.info("Syncing laptop and phone...")
    # sync_folders(FOLDER_PATHS["laptop"], FOLDER_PATHS["phone"])
    # sync_folders(FOLDER_PATHS["phone"], FOLDER_PATHS["laptop"])

    logger.info("Folder Sync Tool completed.")
