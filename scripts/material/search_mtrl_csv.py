import os
from pathlib import Path
import re
import csv
import concurrent.futures

def process_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8', errors='ignore')
            
        shpk_match = re.search(r'(\w+\.shpk)', content)
        
        if shpk_match:
            return {
                'file_path': str(file_path),
                'shpk': shpk_match.group(1)
            }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return None

def search_files(root_dir):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for path in Path(root_dir).rglob('*.mtrl'):
            futures.append(executor.submit(process_file, path))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    return results

def write_to_csv(results, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['file_path', 'shpk']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == '__main__':
    root_directory = "MATERIAL_GAME_DUMP_PRELIMINARY_DAWNTRAIL_UP_TO_6_3"
    output_file = "materials.csv"
    
    results = search_files(root_directory)
    write_to_csv(results, output_file)
    
    print(f"Search complete. Results written to {output_file}")