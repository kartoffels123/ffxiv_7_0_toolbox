import shutil
from pathlib import Path


def read_list(file_path):
    with open(file_path, 'r') as f:
        return {line.strip() for line in f}


def get_file_name_to_path_map(file_paths):
    file_map = {}
    for file_path in file_paths:
        file_name = Path(file_path).name
        if file_name in file_map:
            file_map[file_name].append(file_path)
        else:
            file_map[file_name] = [file_path]
    return file_map


def copy_files(current_list, correct_list, base_dir):
    current_files = read_list(current_list)
    correct_files = read_list(correct_list)

    current_file_map = get_file_name_to_path_map(current_files)
    correct_file_map = get_file_name_to_path_map(correct_files)

    base_dir = Path(base_dir)
    list_b_fix_dir = base_dir / 'list_b_fix'
    list_a_only_dir = base_dir / 'list_a_only'

    for file_name, current_paths in current_file_map.items():
        if file_name in correct_file_map:
            for correct_path in correct_file_map[file_name]:
                for current_path in current_paths:
                    src = Path(current_path)
                    if src.exists():
                        dest = list_b_fix_dir / correct_path
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dest)
                        print(f"Copied {src} to {dest}")
        else:
            for current_path in current_paths:
                src = Path(current_path)
                if src.exists():
                    dest = list_a_only_dir / current_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dest)
                    print(f"Copied {src} to {dest}")


if __name__ == "__main__":
    current_list = 'list_textools_paths.txt'
    correct_list = 'list_correct_paths.txt'
    base_directory = '.'

    copy_files(current_list, correct_list, base_directory)
