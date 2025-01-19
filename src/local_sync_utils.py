import os
import shutil

def sync_folders(source_path, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    for root, _, files in os.walk(source_path):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, source_path)
            dest_file = os.path.join(target_path, rel_path)

            if not os.path.exists(dest_file):
                print(f"Copying {file} from {source_path} to {target_path}...")
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(src_file, dest_file)
            else:
                print(f"{file} already exists in {target_path}.")