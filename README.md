# File-Sync


A brief description of what the project does and its purpose.

## Features

- **Google Drive Integration**: Sync local folders with Google Drive.
- **Easy Setup**: Simple authentication and folder synchronization process.
- **Configuration Management**: Automatically updates configuration files with Google Drive folder ID.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.x
- Required Python packages (listed below)
- Google Drive API credentials (`client_secret.json`)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

2. **Create a virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows:venv\Scripts\activate  

3. **Install required dependancies**
    ```bash
    pip install -r requirements.txt

4. **Obtain Google Drive API credentials**    
    Go to the Google Cloud Console.
    Create a project and enable the Google Drive API.
    Download the client_secret.json file and place it in the project directory.

## Configuration
        FOLDER_PATHS = {
        "laptop": "/path/to/local/laptop/folder",
        "external_drive": "/path/to/external/drive/folder",
        "phone": "/path/to/phone/folder",
        "google_drive": ""  # This will be automatically updated after running the script.
    }

    GOOGLE_DRIVE_FOLDER_ID = ""  # This will be automatically updated after running the script.

    LOG_FILE = "sync.log"
    LOG_LEVEL = "INFO"


## Usage

Run the quickstart.py script to authenticate with Google Drive and retrieve the folder ID:
```bash
python quickstart.py
```
The script will:

    Authenticate with your Google account.
    Search for a specified folder in your Google Drive.
    Save the Google Drive folder ID into the config.py file.

Sync local folders: After setting the folder paths and Google Drive folder ID in config.py, you can use the script to sync your local folders with Google Drive.

(If additional sync functionality is part of your project, provide usage instructions here.)

## Logging
The script generates logs based on the following settings in config.py:

    Log file: The log file is saved as sync.log.
    Log level: You can set the log level to INFO, DEBUG, or ERROR.