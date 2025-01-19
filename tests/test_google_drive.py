from src.google_drive_utils import authenticate_google_drive

def test_google_drive_auth():
    drive = authenticate_google_drive()
    assert drive is not None
