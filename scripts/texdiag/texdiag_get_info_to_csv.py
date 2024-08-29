import subprocess
from pathlib import Path
import csv
import re

def get_texdiag_info(file_path):
    try:
        result = subprocess.run(['./tools/texdiag.exe', 'info', file_path], capture_output=True, text=True)
        output = result.stdout
        # Using regular expressions to extract width, height, and format
        width_match = re.search(r'width\s*=\s*(\d+)', output)
        height_match = re.search(r'height\s*=\s*(\d+)', output)
        format_match = re.search(r'format\s*=\s*([\w_]+)', output)

        width = int(width_match.group(1)) if width_match else None
        height = int(height_match.group(1)) if height_match else None
        format = format_match.group(1) if format_match else None

        if not (width and height and format):
            print(f"Failed to parse texdiag info for {file_path}")
            print(output)

        return width, height, format

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None, None

def compare_files_and_generate_csv(output_a, csv_file):
    output_a = Path(output_a)
    csv_path = Path(csv_file)
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "dimensions", "format"])

        for file_path_a in output_a.rglob('*.dds'):
            width_a, height_a, format_a = get_texdiag_info(file_path_a)
            if width_a and height_a and format_a:
                writer.writerow([str(file_path_a), f"{width_a}x{height_a}", format_a])
                print(f"{str(file_path_a)}, {width_a}x{height_a}, {format_a}")


if __name__ == "__main__":
    # Define directories
    output_a = 'people'
    csv_file = 'results.csv'

    # Compare files and generate CSV
    compare_files_and_generate_csv(output_a, csv_file)

    print("Comparison completed and CSV generated successfully.")
