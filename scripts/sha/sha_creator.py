import hashlib
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def calculate_file_hash(file_path, hash_algorithm='md5'):
    hash_func = hashlib.new(hash_algorithm)
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
    except Exception as e:
        return file_path, None  # In case of an error, return None as hash
    return file_path, hash_func.hexdigest()

def generate_hash_csv(directory_path, output_csv, hash_algorithm='sha256', max_workers=4):
    base_path = Path(directory_path).resolve()
    file_paths = list(base_path.rglob('*'))  # Recursive glob to find all files
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(calculate_file_hash, file_path, hash_algorithm): file_path for file_path in file_paths if file_path.is_file()}
        
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['file_path', 'hash'])
            
            for future in as_completed(future_to_file):
                file_path, file_hash = future.result()
                if file_hash:  # Only write if the hash was calculated successfully
                    writer.writerow([file_path.relative_to(base_path), file_hash])

# Example usage
directory_path = '7-0_tex_24-08-03'
output_csv = 'file_hashes_7-0_tex_24-08-03.csv'
generate_hash_csv(directory_path, output_csv)
