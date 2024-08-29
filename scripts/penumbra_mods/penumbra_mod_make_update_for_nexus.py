import shutil
from pathlib import Path
from datetime import datetime, timedelta

def get_recent_files(source_folder, time_threshold):
    recent_files = []
    for file in source_folder.rglob('*'):
        if file.is_file():
            file_mod_time = datetime.fromtimestamp(file.stat().st_mtime)
            if file_mod_time >= time_threshold:
                recent_files.append(file)
    return recent_files

def copy_files_with_structure(files, source_folder, destination_folder):
    for file in files:
        relative_path = file.relative_to(source_folder)
        destination_path = destination_folder / relative_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, destination_path)

def main():
    source_folder = Path('Kartoffels Upscaled Equipment Textures')
    destination_folder = Path('Kartoffels Upscaled Equipment Textures_update')

    # Set the time threshold to 24 hours ago
    time_threshold = datetime.now() - timedelta(hours=24)

    # Get the list of files updated within the last 24 hours
    recent_files = get_recent_files(source_folder, time_threshold)

    # Copy the recent files preserving the folder structure
    copy_files_with_structure(recent_files, source_folder, destination_folder)

if __name__ == "__main__":
    main()
