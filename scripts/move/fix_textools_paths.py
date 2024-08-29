import json
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

# Function to pre-scan and store paths
def pre_scan_paths(directory):
    paths = {}
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            paths[file_path.name] = file_path
    return paths

# Function to process textures using pre-scanned paths
def process_texture(expected_texture, stored_paths, changed_paths):
    filename = Path(expected_texture).name
    extensions = [".tex", ".dds", ".png", ".tga"]
    expected_texture_path = Path(expected_texture.replace("/", "\\"))

    for ext in extensions:
        search_filename = filename.rsplit(".", 1)[0] + ext
        if search_filename in stored_paths:
            file_path = stored_paths[search_filename]
            if file_path != expected_texture_path:
                fixed_file_path = fixed_paths_dir / expected_texture_path.parent / (expected_texture_path.name.rsplit(".", 1)[0] + ext)
                fixed_file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(file_path, fixed_file_path)
                print(f"Copied {file_path} to {fixed_file_path}")
                changed_paths.append((str(file_path), str(fixed_file_path)))

# Pre-scan the directory and store paths
stored_paths = pre_scan_paths("textools_game_7_0")

# Load the JSON file
with open("materials.json") as file:
    data = json.load(file)

# Create the fixed_paths directory if it doesn't exist
fixed_paths_dir = Path("fixed_paths")
fixed_paths_dir.mkdir(parents=True, exist_ok=True)

# Filter the JSON data to only include objects where "file_path" contains "\\chara\\"
filtered_data = [obj for obj in data if "\\chara\\" in obj["file_path"] or "\\bgcommon\\" in obj["file_path"]]


# Create a list to store changed paths
changed_paths = []

# Create a ThreadPoolExecutor with the maximum number of worker threads
max_workers = 32  # Adjust this value based on your system's capabilities
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    for obj in filtered_data:
        expected_textures = obj["textures"]
        futures.extend(executor.submit(process_texture, texture, stored_paths, changed_paths) for texture in expected_textures)

    total_futures = len(futures)
    completed_futures = 0
    for future in as_completed(futures):
        completed_futures += 1
        print(f"Progress: {completed_futures}/{total_futures} completed")

# Save the changed paths to a CSV file
with open('changed_paths.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Original', 'New'])
    csvwriter.writerows(changed_paths)

print("Changed paths have been saved to changed_paths.csv")
