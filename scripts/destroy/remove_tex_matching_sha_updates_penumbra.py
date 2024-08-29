import pandas as pd
from pathlib import Path
import os

# Load the updated files CSV
file_path = 'updated_files.csv'
updated_files = pd.read_csv(file_path)

# Get the list of file paths to be deleted
file_paths_to_delete = updated_files['file_path'].tolist()

# Define the base directory as the current directory
base_dir = Path('.')

# Function to delete .tex files matching the list
def delete_tex_files(base_dir, file_paths):
    for tex_file in base_dir.rglob('*.tex'):
        relative_path = tex_file.relative_to(base_dir).as_posix()
        for file_path in file_paths:
            # Normalize paths
            norm_file_path = os.path.normpath(file_path).replace('\\', '/')
            norm_relative_path = os.path.normpath(relative_path).replace('\\', '/')
            
            # Check if the normalized file_path is at the end of the normalized relative_path
            if norm_relative_path.endswith(norm_file_path):
                tex_file.unlink()
                print(f"Deleted: {tex_file}")
                break

# Run the deletion function
delete_tex_files(base_dir, file_paths_to_delete)