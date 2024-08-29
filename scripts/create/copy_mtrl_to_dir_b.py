import os
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

def copy_file(src_file, dest_file):
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file, dest_file)

def process_directory(dirpath, filenames, src_root, dest_root):
    tasks = []
    for filename in filenames:
        if filename.endswith('.mtrl'):
            relative_path = Path(dirpath).relative_to(src_root)
            dest_dir = Path(dest_root) / relative_path
            src_file = Path(dirpath) / filename
            dest_file = dest_dir / filename
            tasks.append((src_file, dest_file))
    return tasks

def copy_mtrl_files(src_root, dest_root, max_workers=4):
    tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for dirpath, _, filenames in os.walk(src_root):
            task_list = process_directory(dirpath, filenames, src_root, dest_root)
            tasks.extend(task_list)

        for src_file, dest_file in tasks:
            futures.append(executor.submit(copy_file, src_file, dest_file))

        for future in as_completed(futures):
            future.result()  # to raise exceptions if any

if __name__ == "__main__":
    src_directory = Path('ENTIRE_GAME_DUMP_PRELIMINARY_DAWNTRAIL_UP_TO_6_3')  # Replace with your source directory path
    dest_directory = Path('MATERIAL_GAME_DUMP_PRELIMINARY_DAWNTRAIL_UP_TO_6_3')  # Replace with your destination directory path
    copy_mtrl_files(src_directory, dest_directory, max_workers=8)
    print("Material files copied, preserving directory structure")
