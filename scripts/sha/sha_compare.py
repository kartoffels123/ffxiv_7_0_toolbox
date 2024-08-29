import csv
from pathlib import Path

def load_hashes_from_csv(csv_file):
    hashes = {}
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            file_path, file_hash = row
            hashes[file_path] = file_hash
    return hashes

def compare_hashes(current_csv, previous_csv):
    current_hashes = load_hashes_from_csv(current_csv)
    previous_hashes = load_hashes_from_csv(previous_csv)
    
    updated_files = []
    new_files = []
    unchanged_files = []
    
    for file_path, current_hash in current_hashes.items():
        if file_path in previous_hashes:
            if current_hash != previous_hashes[file_path]:
                updated_files.append(file_path)
            else:
                unchanged_files.append(file_path)
        else:
            new_files.append(file_path)
    
    return updated_files, new_files, unchanged_files

def write_list_to_csv(file_list, output_csv):
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file_path'])
        for file_path in file_list:
            writer.writerow([file_path])


# Example usage
current_csv = 'file_hashes_7-0_tex_24-07-13.csv'
previous_csv = 'file_hashes_7-0_tex_24-08-03.csv'

updated_files, new_files, unchanged_files = compare_hashes(current_csv, previous_csv)

write_list_to_csv(updated_files, 'updated_files.csv')
write_list_to_csv(new_files, 'new_files.csv')
write_list_to_csv(unchanged_files, 'unchanged_files.csv')
