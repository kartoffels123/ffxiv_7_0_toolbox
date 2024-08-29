import subprocess
from pathlib import Path
import csv
import re
import shutil

def get_texdiag_info(file_path):
    try:
        result = subprocess.run(['texdiag.exe', 'info', str(file_path)], capture_output=True, text=True)
        output = result.stdout
        format_match = re.search(r'format\s*=\s*([\w_]+)', output)
        format = format_match.group(1) if format_match else "Unknown"
        return format
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return "Error"

def move_file(file_path, destination_root, format):
    relative_path = file_path.relative_to(input_dir)
    destination_path = destination_root / format / relative_path
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(destination_path))
    return destination_path

def process_directory_and_move_files(input_dir, output_root, csv_file):
    input_dir = Path(input_dir)
    output_root = Path(output_root)
    csv_path = Path(csv_file)

    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["index", "original_path", "new_path", "format"])

        for index, file_path in enumerate(input_dir.rglob('*.dds')):
            try:
                format = get_texdiag_info(file_path)
                new_path = file_path  # Default to original path

                if format in ["BC3_UNORM", "BC7_UNORM", "BC1_UNORM"]:
                    format_folder = format.split('_')[0]  # Extract BC3, BC7, or BC1
                    new_path = move_file(file_path, output_root, format_folder)

                writer.writerow([index, str(file_path.relative_to(input_dir)), str(new_path.relative_to(output_root)), format])
                print(f"{index}, {str(file_path.relative_to(input_dir))}, {str(new_path.relative_to(output_root))}, {format}")

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    input_dir = 'checks'
    output_root = 'sorted_textures'
    csv_file = 'texture_sorting_results.csv'

    process_directory_and_move_files(input_dir, output_root, csv_file)
    print("Processing completed and CSV generated successfully.")