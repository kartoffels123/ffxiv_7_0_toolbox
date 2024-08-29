import os
from PIL import Image

upscale_factor = os.environ.get('UPSCALE_FACTOR', 'x2')


def merge_images(item_path, output_bands, output_alpha, output_bands_alpha_merged, out_bands_final):
    # Extract the item filename and directory structure
    item_dir = os.path.dirname(item_path)
    item_name = os.path.basename(item_path)
    item_name_without_ext = os.path.splitext(item_name)[0]

    # Create the output directories if they don't exist
    os.makedirs(os.path.join(output_bands_alpha_merged, item_dir), exist_ok=True)
    os.makedirs(os.path.join(out_bands_final, item_dir), exist_ok=True)

    # Merge the alpha channels from output_alpha into output_bands
    merged_images = []
    for i in range(8):
        band_path = os.path.join(output_bands, item_dir, f"{item_name_without_ext}_{i}.png")
        alpha_path = os.path.join(output_alpha, item_dir, f"{item_name_without_ext}_{i}.png")

        # Check if the band and alpha images exist
        if not os.path.exists(band_path) or not os.path.exists(alpha_path):
            continue  # Skip this band if either the band or alpha image is missing

        # Open the band image and alpha image
        band_image = Image.open(band_path).convert("RGBA")
        alpha_image = Image.open(alpha_path).convert("L")

        # Replace the alpha channel of the band image with the alpha image
        band_image.putalpha(alpha_image)

        # Save the merged image to output_bands_alpha_merged
        merged_path = os.path.join(output_bands_alpha_merged, item_dir, f"{item_name_without_ext}_{i}.png")
        band_image.save(merged_path)

        merged_images.append(band_image)

    # Create a new grayscale image with the same size as the merged images
    if merged_images:
        final_image = Image.new("L", merged_images[0].size)

        # Apply the merged images over each other, starting from 0
        for merged_image in merged_images:
            final_image = Image.composite(merged_image.convert("L"), final_image, merged_image.split()[-1])

        # Save the final grayscale image to out_bands_final
        final_path = os.path.join(out_bands_final, item_dir, item_name)
        final_image.save(final_path)


# Example usage
path_R = f"R_{upscale_factor}"
output_bands = f"output_bands_padded_{upscale_factor}"
output_alpha = f"output_alpha_{upscale_factor}"
output_bands_alpha_merged = f"output_bands_alpha_merged_{upscale_factor}"
out_bands_final = f"out_bands_final_{upscale_factor}"

for root, dirs, files in os.walk(path_R):
    for file in files:
        if file.endswith('.png'):
            item_path = os.path.join(root, file)
            item_rel_path = os.path.relpath(item_path, path_R)
            merge_images(item_rel_path, output_bands, output_alpha, output_bands_alpha_merged, out_bands_final)
