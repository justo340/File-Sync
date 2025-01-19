import os


def sync_google_drive_to_local(drive, folder_id, local_path):
    print (f"this is the os path:{local_path}")
    print (f"this is the folder_id:{folder_id}")
        
        # Check if the directory exists and print if it doesn't
    if not os.path.exists(local_path):
        print(f"Folder does not exist. Creating folder: {local_path}")
        os.makedirs(local_path)
    else:
        print(f"Folder already exists: {local_path}")

        
        
    print(f"Folder ID being used: {folder_id}")

    try:
        # query fo files within the folder
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        
        

        for file in file_list:
            file_path = os.path.join(local_path, file['title'])
            if not os.path.exists(file_path):
                print(f"Downloading {file['title']} to {local_path}...")
                file.GetContentFile(file_path)
            else:
                print(f"{file['title']} already exists in {local_path}.")
    except Exception as e:
        print(f"Error syncing Google Drive to local: {e}")
    
        
def sync_local_to_google_drive(drive, local_path, folder_id):
    for root, _, files in os.walk(local_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)

            file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false and title='{file_name}'"}).GetList()
            if not file_list:
                print(f"Uploading {file_name} to Google Drive...")
                gfile = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
                gfile.SetContentFile(file_path)
                gfile.Upload()
            else:
                print(f"{file_name} already exists on Google Drive.")