import os
import subprocess

import config  # Import the configuration file to access FOLDER_PATHS
from logging_utils import setup_logger

mtp_logger = setup_logger("mtp_sync.log", "INFO")


def check_mtp_connection():
    """
    Check if an MTP device is connected via USB.
    """
    try:
        result = subprocess.run(["mtp-detect"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Found device" in result.stdout:
            mtp_logger.info("MTP device detected.")
            return True
        else:
            mtp_logger.error("No MTP device found. Please connect your phone via USB.")
            return False
    except FileNotFoundError:
        mtp_logger.error("mtp-detect not found. Please install mtp-tools.")
        return False


def list_storage():
    """
    List storage devices on the connected MTP device.
    """
    try:
        result = subprocess.run(["mtp-files"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            mtp_logger.info("Storage devices detected:\n" + result.stdout)
            return result.stdout
        else:
            mtp_logger.error("Failed to list storage. Ensure the device is connected and unlocked.")
            return None
    except FileNotFoundError:
        mtp_logger.error("mtp-files not found. Please install mtp-tools.")
        return None


def find_download_folder():
    """
    Locate the 'Download' folder on the connected MTP device.
    """
    try:
        result = subprocess.run(["mtp-folders"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            mtp_logger.info("Folder structure detected:\n" + result.stdout)
            # Search for the 'Download' folder in the folder structure
            for line in result.stdout.split("\n"):
                if "Download" in line:
                    folder_id = line.split()[0]  # Extract folder ID
                    mtp_logger.info(f"Found 'Download' folder with ID: {folder_id}")
                    return folder_id
            mtp_logger.error("'Download' folder not found on the device.")
            return None
        else:
            mtp_logger.error("Failed to fetch folder structure. Ensure the device is connected and unlocked.")
            return None
    except FileNotFoundError:
        mtp_logger.error("mtp-folders not found. Please install mtp-tools.")
        return None


def download_files_from_phone(folder_id, local_path):
    """
    Download files from the specified folder on the phone to a local directory.
    """
    try:
        os.makedirs(local_path, exist_ok=True)
        result = subprocess.run(["mtp-getfile", folder_id, local_path], stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            mtp_logger.info(f"Files from folder ID {folder_id} downloaded to {local_path}.")
        else:
            mtp_logger.error(f"Failed to download files. Error: {result.stderr}")
    except Exception as e:
        mtp_logger.error(f"An error occurred while downloading files: {e}")


def sync_phone_to_local():
    """
    Automates the syncing of the phone's 'Download' folder to the local system.
    Uses the FOLDER_PATHS["phone"] path from the config module.
    """
    local_path = config.FOLDER_PATHS["phone"]  # Get the phone folder path from config
    if check_mtp_connection():
        folder_id = find_download_folder()
        if folder_id:
            download_files_from_phone(folder_id, local_path)
        else:
            mtp_logger.error("Unable to locate 'Download' folder. Sync aborted.")
    else:
        mtp_logger.error("No MTP device connected. Sync aborted.")
