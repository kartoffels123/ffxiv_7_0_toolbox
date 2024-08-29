import os
from pathlib import Path
import re
import json
import concurrent.futures

def process_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Find shpk in binary content
        shpk_match = re.search(rb'(\w+\.shpk)', content)
        
        # Find all texture paths
        texture_pattern = rb'((?:bg|bgcommon|chara|vfx)\S+\.tex)'
        texture_matches = re.findall(texture_pattern, content)
        
        if shpk_match and texture_matches:
            # Decode and split textures by null byte
            textures = [tex.decode('utf-8', errors='ignore') for tex in texture_matches]
            textures = [tex for texture in textures for tex in texture.split('\x00') if tex]
            
            return {
                'file_path': str(file_path),
                'shpk': shpk_match.group(1).decode('utf-8', errors='ignore'),
                'textures': textures
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

def write_to_json(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(results, jsonfile, indent=2)

if __name__ == '__main__':
    root_directory = "MATERIAL_GAME_DUMP_PRELIMINARY_DAWNTRAIL_UP_TO_6_3"
    output_file = "materials.json"
    
    results = search_files(root_directory)
    write_to_json(results, output_file)
    
    print(f"Search complete. Results written to {output_file}")