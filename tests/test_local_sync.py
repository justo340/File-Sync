from src.local_sync_utils import sync_folders
import os
import shutil

def test_sync_folders():
    source = "test_source"
    target = "test_target"

    os.makedirs(source, exist_ok=True)
    with open(os.path.join(source, "test.txt"), "w") as f:
        f.write("This is a test.")

    sync_folders(source, target)

    assert os.path.exists(os.path.join(target, "test.txt"))

    shutil.rmtree(source)
    shutil.rmtree(target)