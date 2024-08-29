import subprocess
from pathlib import Path
import csv
import re

def get_texdiag_info(file_path):
    try:
        result = subprocess.run(['texdiag.exe', 'info', file_path], capture_output=True, text=True)
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

def compare_files_and_generate_csv(output_a, output_b, csv_file, error_log):
    output_a = Path(output_a)
    output_b = Path(output_b)
    csv_path = Path(csv_file)
    error_log_path = Path(error_log)

    index = 0

    with open(csv_path, mode='w', newline='') as file, open(error_log_path, mode='w') as log_file:
        writer = csv.writer(file)
        writer.writerow(["index", "filename", "dimensions", "format"])
        log_file.write("Error Log:\n")

        for file_path_a in output_a.rglob('*.dds'):
            try:
                relative_path = file_path_a.relative_to(output_a)
                file_path_b = output_b / relative_path

                if file_path_b.exists():
                    width_a, height_a, format_a = get_texdiag_info(file_path_a)
                    width_b, height_b, format_b = get_texdiag_info(file_path_b)

                    if width_a and height_a and format_a:
                        writer.writerow([index, str(file_path_a), f"{width_a}x{height_a}", format_a])
                        print(f"{index}, {str(file_path_a)}, {width_a}x{height_a}, {format_a}")
                    if width_b and height_b and format_b:
                        writer.writerow([index, str(file_path_b), f"{width_b}x{height_b}", format_b])
                        print(f"{index}, {str(file_path_b)}, {width_b}x{height_b}, {format_b}")

                    index += 1
            except Exception as e:
                log_file.write(f"Error processing {file_path_a}: {e}\n")
                print(f"Error processing {file_path_a}: {e}")

if __name__ == "__main__":
    # Define directories
    output_a = '6-3_match'
    output_b = '7-0_match'
    csv_file = 'comparison_results.csv'
    error_log = 'error_log.txt'

    # Compare files and generate CSV
    compare_files_and_generate_csv(output_a, output_b, csv_file, error_log)

    print("Comparison completed, CSV generated, and error log created successfully.")
