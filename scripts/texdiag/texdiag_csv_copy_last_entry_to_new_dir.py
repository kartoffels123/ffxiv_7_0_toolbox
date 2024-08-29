import csv
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor

def copy_file(src_file, dest_file):
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file, dest_file)
    print(f"Copied {src_file} to {dest_file}")

def copy_files_from_csv(input_csv, target_folder):
    # Read the CSV file and store the second entries
    second_entries = []
    index_count = {}
    
    with open(input_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        for row in reader:
            index, filename, dimensions, format = row
            index = int(index)
            
            if index not in index_count:
                index_count[index] = 1
            else:
                index_count[index] += 1
                
                if index_count[index] == 2:
                    second_entries.append(row)

    # Create target directory if it doesn't exist
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)

    # Prepare the file copy tasks
    tasks = []
    for row in second_entries:
        _, filename, _, _ = row
        src_file = Path(filename)
        dest_file = target_folder / filename
        tasks.append((src_file, dest_file))

    # Copy files in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        executor.map(lambda args: copy_file(*args), tasks)

if __name__ == "__main__":
    input_csv = 'comparison_results_dimension_same_type_difference.csv'
    target_folder = '7-0_dim_same_type_difference'

    copy_files_from_csv(input_csv, target_folder)

    print("Files copied successfully.")
