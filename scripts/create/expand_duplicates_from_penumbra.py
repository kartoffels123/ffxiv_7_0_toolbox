import json
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_files(metadata_file, source_dir, dest_dir):
    source_dir = Path(source_dir)
    dest_dir = Path(dest_dir)

    try:
        with open(metadata_file, 'r', encoding='utf-8-sig') as file:
            metadata = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON decode error reading {metadata_file}: {e}")
        return
    except FileNotFoundError as e:
        print(f"File not found: {metadata_file}")
        return
    except PermissionError as e:
        print(f"Permission error reading {metadata_file}: {e}")
        return
    except Exception as e:
        print(f"Unexpected error reading {metadata_file}: {e}")
        return

    files = metadata.get('Files', {})

    for key, value in files.items():
        key_path = dest_dir / key
        value_path = source_dir / value

        if not key_path.exists():
            if value_path.exists():
                try:
                    key_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(value_path, key_path)
                    print(f"Copied {value_path} to {key_path}")
                except Exception as e:
                    print(f"Error copying {value_path} to {key_path}: {e}")
            else:
                print(f"Source file {value_path} does not exist, cannot copy to {key_path}")

    source_dir = Path(source_dir)
    dest_dir = Path(dest_dir)

    try:
        with open(metadata_file, 'r') as file:
            metadata = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading {metadata_file}: {e}")
        return
    except Exception as e:
        print(f"Unexpected error reading {metadata_file}: {e}")
        return

    files = metadata.get('Files', {})

    for key, value in files.items():
        key_path = dest_dir / key
        value_path = source_dir / value

        if not key_path.exists():
            if value_path.exists():
                try:
                    key_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(value_path, key_path)
                    print(f"Copied {value_path} to {key_path}")
                except Exception as e:
                    print(f"Error copying {value_path} to {key_path}: {e}")
            else:
                print(f"Source file {value_path} does not exist, cannot copy to {key_path}")


def recurse_and_process_meta(root_dir, source_dir, dest_dir):
    root_dir = Path(root_dir)
    meta_files = list(root_dir.rglob('default_mod.json'))

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_files, meta_file, source_dir, dest_dir) for meta_file in meta_files]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing meta file: {e}")


if __name__ == "__main__":
    root_dir = 'common_textures\\kart world textures common v2-1-0-update'
    source_dir = 'common_textures\\kart world textures common\\'
    dest_dir = 'common_textures\\kart world textures common2\\'

    recurse_and_process_meta(root_dir, source_dir, dest_dir)

    print("All meta.json files processed.")
