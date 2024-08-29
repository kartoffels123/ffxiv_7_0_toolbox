import csv
import pathlib
import shutil
from concurrent.futures import ThreadPoolExecutor

# Define the source and target directories
source_dir = pathlib.Path("people")
target_dir = pathlib.Path("BC1")

def copy_file(file):
    # Create the target file path
    target_file = target_dir / file.relative_to(source_dir)
    # Create any missing parent directories
    target_file.parent.mkdir(parents=True, exist_ok=True)
    # Copy the file
    shutil.copy2(file, target_file)

# Function to read the CSV file and get the file paths
def get_file_paths_from_csv(csv_file):
    file_paths = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file_paths.append(pathlib.Path(row['filename']))
    return file_paths

# Get the list of files from the CSV
csv_file = 'documentation\csv_scratch\human_textures\BC1.csv'  # replace with your CSV file path
files = get_file_paths_from_csv(csv_file)

# Use ThreadPoolExecutor to copy files in parallel
with ThreadPoolExecutor() as executor:
    executor.map(copy_file, files)

print("Files copied successfully!")
