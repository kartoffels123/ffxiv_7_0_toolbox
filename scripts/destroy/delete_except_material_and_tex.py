import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def remove_file(file_path):
    os.remove(file_path)

def clean_directory_structure(root_dir, max_workers=4):
    tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
            for filename in filenames:
                if not (filename.endswith('.tex') or filename.endswith('.mtrl')):
                    file_path = os.path.join(dirpath, filename)
                    futures.append(executor.submit(remove_file, file_path))

            # Remove empty directories
            for dirname in dirnames:
                dirpath_full = os.path.join(dirpath, dirname)
                if not os.listdir(dirpath_full):
                    tasks.append(dirpath_full)

        # Wait for file removal to complete
        for future in as_completed(futures):
            future.result()  # to raise exceptions if any

        # Remove empty directories in the main thread
        for task in tasks:
            if not os.listdir(task):
                os.rmdir(task)

if __name__ == "__main__":
    root_directory = Path('ENTIRE_GAME_DUMP_6_3_FFXIV')  # Replace with your root directory path
    clean_directory_structure(root_directory, max_workers=8)
    print("Directory cleaned, preserving only .tex and .mtrl files")
