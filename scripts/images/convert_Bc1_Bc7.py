import os
from PIL import Image, ImageChops
import subprocess
import numpy as np

def process_tga_file(tga_path, output_dirs, alpha_threshold=250):
    # Open the TGA image
    image = Image.open(tga_path)

    # Discard the alpha channel if it exists and is above the threshold
    is_rgba = False
    if image.mode == 'RGBA':
        alpha = np.array(image.getchannel('A'))
        if np.all(alpha >= alpha_threshold):
            image = image.convert('RGB')
            is_rgba = False
        else:
            is_rgba = True
    else:
        is_rgba = False

    # Select the appropriate output directory based on the image type
    if is_rgba:
        output_dir = output_dirs['BC7']
        texconv_format = "BC7_UNORM"
        texconv_command = ["texconv", "-f", texconv_format, "-y", "-bc", "q", "-sepalpha", "-o", output_dir, tga_path]
    else:
        output_dir = output_dirs['BC1']
        texconv_format = "BC1_UNORM"
        texconv_command = ["texconv", "-f", texconv_format, "-y", "-o", output_dir, tga_path]

    # Create the output directory if it doesn't exist
    relative_path = os.path.relpath(tga_path, input_dir)
    output_path = os.path.join(output_dir, os.path.dirname(relative_path))
    os.makedirs(output_path, exist_ok=True)

    # Update the output directory in the texconv command to ensure correct output path
    texconv_command[-2] = output_path

    # Convert the TGA file to the appropriate format using texconv
    subprocess.run(texconv_command)

# Input and output directories
input_dir = "characterlegacy_shpk_d"
output_dirs = {
    'BC1': "characterlegacy_shpk_d_BC1",
    'BC7': "characterlegacy_shpk_d_BC7"
}

# Walk through the input directory and process each TGA file
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.tga'):
            tga_path = os.path.join(root, file)
            process_tga_file(tga_path, output_dirs, alpha_threshold=250)
