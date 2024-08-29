import os
from PIL import Image
import subprocess

def process_dds_file(dds_path, output_dir):
    # Open the DDS image
    image = Image.open(dds_path)

    # Discard the alpha channel if it exists
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Resize the image by half using the box filter
    new_size = (image.width // 2, image.height // 2)
    resized_image = image.resize(new_size, Image.BOX)

    # Create the output directory if it doesn't exist
    item_dir = os.path.dirname(dds_path)
    relative_dir = os.path.relpath(item_dir, start=input_dir)
    output_path = os.path.join(output_dir, relative_dir)
    os.makedirs(output_path, exist_ok=True)

    # Save the resized image temporarily as a TGA file
    temp_tga_path = os.path.join(output_path, os.path.splitext(os.path.basename(dds_path))[0] + ".tga")
    resized_image.save(temp_tga_path, format="TGA")

    # Convert the TGA file to BC7_UNORM format using texconv
    subprocess.run(["texconv", "-f", "BC7_UNORM", "-y", "-o", output_path, temp_tga_path])

    # Remove the temporary TGA file
    os.remove(temp_tga_path)

# Input and output directories
input_dir = "kart chara textures equipment 2x expanded n reusable"
output_dir = "output_bc7_unorm"

# Walk through the input directory and process each DDS file
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.dds'):
            dds_path = os.path.join(root, file)
            process_dds_file(dds_path, output_dir)
