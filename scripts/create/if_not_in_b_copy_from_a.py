from pathlib import Path
import shutil

def cache_file_structure(dir_path):
    file_structure = set()
    for file in Path(dir_path).rglob('*'):
        if file.is_file():
            relative_path = file.relative_to(dir_path)
            file_structure.add(relative_path)
    return file_structure

def copy_non_matching_files(output_dir, source_dir, new_output_dir):
    output_dir = Path(output_dir)
    source_dir = Path(source_dir)
    new_output_dir = Path(new_output_dir)

    output_files = cache_file_structure(output_dir)
    source_files = cache_file_structure(source_dir)

    for relative_path in source_files:
        if relative_path not in output_files:
            source_file = source_dir / relative_path
            destination = new_output_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(source_file, destination)
                print(f"Copied: {source_file} to {destination}")
            except Exception as e:
                print(f"Error copying {source_file} to {destination}: {e}")

if __name__ == "__main__":
    output_directory = "6-3"
    source_directory = "7-0"
    new_output_directory = "7-0_output"

    copy_non_matching_files(output_directory, source_directory, new_output_directory)
    print("Process completed.")
