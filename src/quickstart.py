import logging
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import config


# Authentication
def authenticate_google_drive():
    # Check if token already exists (this will prevent re-authentication)
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile("client_secret.json")



    # Attempt to load the saved credentials
    gauth.LoadCredentialsFile("credentials.json")


    if gauth.credentials is None:
        # If no saved credentials, go through the authentication flow
        print("No credentials found. Initiating authentication...")
        
            
        # automatically visit the URL 
        try:    
            gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
            gauth.SaveCredentialsFile("credentials.json")  # Save the credentials for future use
            print("Authentication successful!")
        except Exception as e:
            print(f"Authentication failed: {e}")
            exit(1)

    
    else:
        # If credentials are found, use them
        print("Credentials found. Using saved credentials.")


    logging.basicConfig(level=logging.DEBUG)

    # Print the URL and manually visit it if the local webserver doesn't work
    auth_url = gauth.GetAuthUrl()
    print(f"Please visit this URL to authenticate: {auth_url}")


    # Initialize PyDrive client
    drive = GoogleDrive(gauth)
    return drive

def get_google_drive_folder_id(drive, folder_name='testFolder'):
    # Search for a folder by name
    
    file_list = drive.ListFile({'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

    # Get Folder ID
    if file_list:
        folder = file_list[0]  # Assuming the folder exists, and this is the first match
        print(f"Folder ID: {folder['id']}")
        return folder['id']
    else:
        print(f"Folder '{folder_name}' not found.")
        return None



def update_config_with_folder_id(folder_id):
    # Update GOOGLE_DRIVE_FOLDER_ID in config.py
    config.FOLDER_PATHS["google_drive"] = folder_id  # Add new path or modify existing path
        

            
    with open("src/config.py", "w") as config_file:
        # Writing updated config content
        config_file.write(f"FOLDER_PATHS = {str(config.FOLDER_PATHS)}\n")
        config_file.write(f'GOOGLE_DRIVE_FOLDER_ID = "{folder_id}"\n')
        config_file.write(f"LOG_FILE = '{config.LOG_FILE}'\n")
        config_file.write(f"LOG_LEVEL = '{config.LOG_LEVEL}'\n")
        

    print("Config file updated with Google Drive folder ID.")


if __name__ == "__main__":
    
      
        # Authenticate and get the Google Drive client
        drive = authenticate_google_drive()
        
        
        # Retrieve the folder ID for the 'important documents' folder
        folder_id = get_google_drive_folder_id(drive)

        print(f"folder_id value: {folder_id}")
        print(f"folder_id type: {type(folder_id)}")
       
        if folder_id:
            print(f"Folder ID retrieved: {folder_id}")
        
            
            # Update GOOGLE_DRIVE_FOLDER_ID in config.py
            update_config_with_folder_id(folder_id)

            # Run main.py after updating config.py
            print('starting a main.py subprocess..........')
            subprocess.run(["python", "src/main.py"])  # This will execute main.py automatically after completion
        else:
            print("Folder ID retrieval failed, exiting...")

