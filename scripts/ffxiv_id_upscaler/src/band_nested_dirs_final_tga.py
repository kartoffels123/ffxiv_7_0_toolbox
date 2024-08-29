import os
from PIL import Image

upscale_factor = os.environ.get('UPSCALE_FACTOR', 'x2')


def merge_channels(cleaned_r_path, bands_final_path, output_tga):
    # Extract the item filename and directory structure
    item_dir = os.path.dirname(cleaned_r_path)
    item_name = os.path.basename(cleaned_r_path)
    item_name_without_ext = os.path.splitext(item_name)[0]

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.join(output_tga, item_dir), exist_ok=True)

    # Open the cleaned_r image and bands_final image
    cleaned_r_image = Image.open(cleaned_r_path).convert("L")
    bands_final_image = Image.open(bands_final_path).convert("L")

    # Create a new RGB image with the same size as the input images
    merged_image = Image.new("RGB", cleaned_r_image.size)

    # Get the individual bands of the merged image
    r_band, g_band, b_band = merged_image.split()

    # Copy the cleaned_r image to the red channel
    r_band = cleaned_r_image.copy()

    # Copy the bands_final image to the green channel
    g_band = bands_final_image.copy()

    # Create a pure black image for the blue channel
    b_band = Image.new("L", cleaned_r_image.size, 0)

    # Merge the channels back into the merged image
    merged_image = Image.merge("RGB", (r_band, g_band, b_band))

    # Save the merged image as TGA
    tga_path = os.path.join(output_tga, item_dir, f"{item_name_without_ext}.tga")
    merged_image.save(tga_path, format="TGA")


# Example usage
output_cleaned_r = f"R_{upscale_factor}"
output_bands_final = f"out_bands_final_{upscale_factor}"
output_tga = "output_tga"  # or output_tga = "output_tga"

for root, dirs, files in os.walk(output_cleaned_r):
    for file in files:
        if file.endswith('.png'):
            cleaned_r_path = os.path.join(root, file)
            cleaned_r_rel_path = os.path.relpath(cleaned_r_path, output_cleaned_r)
            bands_final_path = os.path.join(output_bands_final, cleaned_r_rel_path)
            merge_channels(cleaned_r_path, bands_final_path, output_tga)
