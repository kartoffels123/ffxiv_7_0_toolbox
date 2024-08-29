from pathlib import Path
import shutil

# Define the file paths
source_file = Path('source.txt')
map_file = Path('map.txt')
output_file = Path('output.txt')

# Read the map file into a dictionary
map_dict = {}
with map_file.open() as f:
    for line in f:
        if '=' in line:
            key, values = line.strip().split('=')
            key = key.strip()
            values = [v.strip() for v in values.split(',')]
            map_dict[key] = values

# Read the source file into a list
with source_file.open() as f:
    source_paths = [line.strip() for line in f]

# Read the output file into a list
with output_file.open() as f:
    output_paths = [line.strip() for line in f]

# Function to find corresponding output paths
def find_matching_paths(source_path):
    for key, values in map_dict.items():
        if key in source_path:
            matching_paths = [p for p in output_paths if any(value in p for value in values)]
            return matching_paths
    return []

# Directory to copy files to
output_directory = Path('output')

# Create the output directory if it doesn't exist
output_directory.mkdir(parents=True, exist_ok=True)

# Copy the source files to the matching output paths
for source_path_str in source_paths:
    source_path = Path(source_path_str)
    matching_paths = find_matching_paths(source_path_str)
    if matching_paths:
        for match in matching_paths:
            match_path = Path(match)
            # Construct the full output path
            destination_path = output_directory / match_path
            print(destination_path)
            # Create the destination directory if it doesn't exist
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            # Copy the file
            shutil.copy(source_path, destination_path)

print("Files copied successfully based on the mapping.")
