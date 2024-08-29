import os
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

def compare_and_move_file(file_path_a, file_path_b, dir_a, dir_b, output_a, output_b, diff_output):
    size_a = file_path_a.stat().st_size
    size_b = file_path_b.stat().st_size
    if size_a != size_b:
        relative_path = file_path_a.relative_to(dir_a)
        diff_output.write(f"{relative_path}\n")
        output_path_a = output_a / relative_path
        output_path_b = output_b / relative_path
        output_path_a.parent.mkdir(parents=True, exist_ok=True)
        output_path_b.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path_a, output_path_a)
        shutil.copy2(file_path_b, output_path_b)

def compare_and_move_files(dir_a, dir_b, output_a, output_b, diff_file, max_workers=4):
    dir_a = Path(dir_a)
    dir_b = Path(dir_b)
    output_a = Path(output_a)
    output_b = Path(output_b)

    with open(diff_file, 'w') as diff_output:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for root_a, _, files_a in os.walk(dir_a):
                for file_a in files_a:
                    file_path_a = Path(root_a) / file_a
                    relative_path = file_path_a.relative_to(dir_a)
                    file_path_b = dir_b / relative_path
                    if file_path_b.exists():
                        futures.append(executor.submit(
                            compare_and_move_file,
                            file_path_a,
                            file_path_b,
                            dir_a,
                            dir_b,
                            output_a,
                            output_b,
                            diff_output
                        ))

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Define directories
    dir_a = '6-3'
    dir_b = '7-0'
    output_a = '6-3_output'
    output_b = '7-0_output'
    diff_file = 'for_sure_different.txt'

    compare_and_move_files(dir_a, dir_b, output_a, output_b, diff_file)
    print("Process completed successfully.")