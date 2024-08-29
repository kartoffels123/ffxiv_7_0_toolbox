import os
from pathlib import Path
import shutil

def scan_and_copy_files(file_list_path, source_dir, dest_dir, not_found_file):
    source_dir = Path(source_dir)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    not_found_path = Path(not_found_file)

    with open(file_list_path, 'r') as file_list, open(not_found_path, 'w') as not_found:
        for line in file_list:
            relative_path = line.strip()
            source_file_path = source_dir / relative_path
            dest_file_path = dest_dir / relative_path

            if source_file_path.exists():
                dest_file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file_path, dest_file_path)
            else:
                not_found.write(f"{relative_path}\n")

if __name__ == "__main__":
    file_list_path = 'documentation\csv_comparisons\\files.txt'
    source_dir = 'kart_world_textures'
    dest_dir = 'kart_world_reusable'
    not_found_file = 'filenotfound.txt'

    scan_and_copy_files(file_list_path, source_dir, dest_dir, not_found_file)

    print("Files have been scanned and copied. Check 'filenotfound.txt' for any missing files.")
