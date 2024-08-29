import os
from pathlib import Path
import shutil

def copy_listed_files(source_dir, target_dir, list_file):
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)
    
    with open(list_file, 'r') as file:
        for line in file:
            # Remove any leading/trailing whitespace and convert to Path
            relative_path = Path(line.strip())
            source_file = source_dir / relative_path
            target_file = target_dir / relative_path
            
            # Create the target directory if it doesn't exist
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the file
            if source_file.exists():
                shutil.copy2(source_file, target_file)
                print(f"Copied: {relative_path}")
            else:
                print(f"Source file not found: {source_file}")

# Usage
source_directory = "7-0"
target_directory = "minor_changes"
list_file = "differs.txt"

copy_listed_files(source_directory, target_directory, list_file)
print("Process completed.")