import json
from pathlib import Path

def normalize_textures(textures):
    return sorted([tex.replace('\\', '/') for tex in textures])

def load_and_normalize_materials(json_file):
    with open(json_file, 'r') as f:
        materials = json.load(f)
    for material in materials:
        material['textures'] = normalize_textures(material['textures'])
    return materials

def merge_materials(materials_a, materials_b):
    textures_set = {tuple(material['textures']) for material in materials_b}
    merged_materials = materials_b.copy()

    for material in materials_a:
        if tuple(material['textures']) not in textures_set:
            merged_materials.append(material)
            textures_set.add(tuple(material['textures']))

    return merged_materials

def save_materials(materials, output_file):
    with open(output_file, 'w') as f:
        json.dump(materials, f, indent=4)

if __name__ == "__main__":
    textools_json = "materials_textools.json"
    game_dump_json = "materials.json"
    output_json = "merged_materials.json"
    
    materials_textools = load_and_normalize_materials(textools_json)
    materials_game_dump = load_and_normalize_materials(game_dump_json)
    
    merged_materials = merge_materials(materials_textools, materials_game_dump)
    
    save_materials(merged_materials, output_json)
    
    print(f"Materials merged and saved to {output_json}")
