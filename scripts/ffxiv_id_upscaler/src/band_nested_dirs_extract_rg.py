import os
import subprocess
from PIL import Image

def convert_bc5_to_tga(input_path, temp_tga_path):
    texconv_path = os.path.join('src', 'texconv.exe')

    # Convert BC5_UNORM to TGA using texconv
    if not input_path.lower().endswith('.dds'):
        pass
    else:
        subprocess.run([texconv_path, "-f", "R8G8B8A8_UNORM", "-y",  "-ft", "tga", "-o", os.path.dirname(temp_tga_path), input_path], check=True)

def split_channels(temp_tga_path, output_r_path, output_g_path):
    with Image.open(temp_tga_path) as img:
        r, g, _, _ = img.split()
        r.save(output_r_path)
        g.save(output_g_path)

def process_bc5_images(input_dir, output_r_dir, output_g_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.dds'):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_r_path = os.path.join(output_r_dir, os.path.splitext(relative_path)[0] + '.png')
                output_g_path = os.path.join(output_g_dir, os.path.splitext(relative_path)[0] + '.png')
                temp_tga_path = os.path.join(os.path.dirname(input_path), os.path.splitext(file)[0] + '.tga')

                os.makedirs(os.path.dirname(output_r_path), exist_ok=True)
                os.makedirs(os.path.dirname(output_g_path), exist_ok=True)

                convert_bc5_to_tga(input_path, temp_tga_path)
                split_channels(temp_tga_path, output_r_path, output_g_path)
                
                # Remove the temporary TGA file after processing
                os.remove(temp_tga_path)

# Example usage
input_dir = "input"
output_r_dir = "R"
output_g_dir = "G"

process_bc5_images(input_dir, output_r_dir, output_g_dir)