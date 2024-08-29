import csv
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor

# Load the CSV data into a dictionary
def load_csv_data(csv_file):
    csv_data = {}
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            filename = row['filename'].replace('\\', '/')
            csv_data[filename] = row['format']
    return csv_data

# Copy file to the appropriate directory
def copy_file(file, csv_data, base_path):
    file_path = Path(file)
    relative_path = file_path.relative_to(base_path)
    
    # Ensure the path uses forward slashes for comparison
    relative_path_str = str(relative_path).replace('\\', '/')
    
    if relative_path_str in csv_data:
        format_dir = csv_data[relative_path_str]
        dest_path = Path(format_dir) / relative_path
    else:
        dest_path = Path('UNCOMPRESSED') / relative_path
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(file_path, dest_path)
    print(f"Copied {file_path} to {dest_path}")

def process_files(master_list_file, csv_data_file, base_path):
    # Load CSV data
    csv_data = load_csv_data(csv_data_file)
    
    # Read master list and process each file
    with open(master_list_file, mode='r') as file:
        master_files = [line.strip() for line in file.readlines()]
    
    # Use ThreadPoolExecutor to copy files in parallel
    with ThreadPoolExecutor() as executor:
        for master_file in master_files:
            executor.submit(copy_file, master_file, csv_data, base_path)

if __name__ == "__main__":
    master_list_file = 'human_dds_master_list.txt'
    csv_data_file = 'human_dds_info.csv'
    base_path = Path('')  # Adjust if necessary
    
    process_files(master_list_file, csv_data_file, base_path)
