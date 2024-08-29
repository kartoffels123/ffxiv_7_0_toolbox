import os
import shutil
from pathlib import Path

def read_file_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def copy_structure(input_dir, output_dir, file_list):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    for file_path in file_list:
        if '/obj/' in file_path:
            # Cut the path at 'obj'
            truncated_path = file_path.split('/obj/')[0] + '/obj'
            
            # Construct the source directory path
            source_dir = input_dir / truncated_path
            
            if source_dir.exists() and source_dir.is_dir():
                # Construct the destination directory path
                dest_dir = output_dir / source_dir.relative_to(input_dir)
                
                # Copy the directory structure and files
                for item in source_dir.rglob('*'):
                    relative_path = item.relative_to(source_dir)
                    dest_item_path = dest_dir / relative_path
                    
                    if item.is_file():
                        dest_item_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dest_item_path)
                        print(f"Copied: {item} to {dest_item_path}")
                    elif item.is_dir():
                        dest_item_path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    input_dir = "7-0_all"
    output_dir = "Named_NPCcs"
    file_list_path = "ENpcs_ModelPath.csv"  # Path to your text file containing the file list
    
    file_list = read_file_list(file_list_path)
    copy_structure(input_dir, output_dir, file_list)