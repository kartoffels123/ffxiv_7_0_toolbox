import os
import subprocess
from PIL import Image
import numpy as np
import shutil

def convert_bc5_to_tga(input_path, temp_tga_path):
    texconv_path = ('texconv.exe')

    # Convert BC5_UNORM to TGA using texconv
    if input_path.lower().endswith('.dds'):
        subprocess.run([texconv_path, "-f", "R8G8B8A8_UNORM", "-y", "-ft", "tga", "-o", os.path.dirname(temp_tga_path), input_path], check=True)

def is_solid_color(image_path):
    with Image.open(image_path) as img:
        img_np = np.array(img)
        if np.all(img_np == img_np[0,0]):
            return True
    return False

def process_bc5_images(input_dir, solid_color_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.dds'):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                temp_tga_path = os.path.join(os.path.dirname(input_path), os.path.splitext(file)[0] + '.tga')

                convert_bc5_to_tga(input_path, temp_tga_path)

                if is_solid_color(temp_tga_path):
                    solid_color_path = os.path.join(solid_color_dir, relative_path)
                    os.makedirs(os.path.dirname(solid_color_path), exist_ok=True)
                    print(file + " is solid color.")
                    shutil.move(input_path, solid_color_path)

                # Remove the temporary TGA file after processing
                os.remove(temp_tga_path)

# Example usage
input_dir = "dds"
solid_color_dir = "solid_color"

process_bc5_images(input_dir, solid_color_dir)
