import json
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

def load_materials(json_file):
    with open(json_file, 'r') as f:
        materials = json.load(f)
    
    # Create a dictionary to map normalized texture paths to shpk values
    materials_dict = defaultdict(list)
    for entry in materials:
        shpk = entry['shpk']
        for tex in entry['textures']:
            normalized_tex = normalize_path(tex)
            materials_dict[normalized_tex].append(shpk)
    return materials_dict

def normalize_path(path):
    return path.replace('\\', '/').replace('.dds', '.tex')

def copy_texture(input_dir, output_dir, no_material_dir, materials_dict, file_path):
    relative_path = file_path.relative_to(input_dir)
    normalized_relative_path = normalize_path(str(relative_path))
    
    if normalized_relative_path in materials_dict:
        shpk_list = materials_dict[normalized_relative_path]
        for shpk in shpk_list:
            output_path = output_dir / shpk / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, output_path)
            print(f"Copied {file_path} to {output_path}")
    else:
        no_material_path = no_material_dir / relative_path
        no_material_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, no_material_path)
        print(f"No material entry found for {relative_path}, copied to {no_material_path}")

def process_textures(input_dir, materials_json, output_dir, no_material_dir):
    materials_dict = load_materials(materials_json)
    
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    no_material_dir = Path(no_material_dir)
    
    # Collect all .dds files
    files = list(input_dir.rglob('*.dds'))

    # Process files in parallel
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file_path: copy_texture(input_dir, output_dir, no_material_dir, materials_dict, file_path), files)

if __name__ == "__main__":
    input_dir = "7-0_dim_same_type_difference"
    materials_json = "merged_materials.json"
    output_dir = "output"
    no_material_dir = "no_material_found"
    
    process_textures(input_dir, materials_json, output_dir, no_material_dir)

    print("Processing completed.")
