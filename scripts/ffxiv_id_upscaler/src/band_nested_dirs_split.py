import numpy as np
from PIL import Image
import os

def clean_img_r(img_r_array):
    # Define the valid values
    valid_values = np.array([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
                             0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF])

    # Reshape img_r_array to have an extra dimension for broadcasting
    img_r_array_reshaped = img_r_array.reshape(img_r_array.shape + (1,))

    # Compute the absolute difference between each pixel and the valid values
    diff = np.abs(img_r_array_reshaped - valid_values)

    # Find the index of the closest valid value for each pixel
    closest_index = np.argmin(diff, axis=-1)

    # Get the closest valid value for each pixel using the index
    cleaned_img_r_array = valid_values[closest_index]

    return cleaned_img_r_array

def process_images(img_r_path, img_g_path, output_alpha, output_bands):
    # Read the input images
    img_r = Image.open(img_r_path).convert('L')
    img_g = Image.open(img_g_path).convert('L')

    # Convert the images to numpy arrays
    img_r_array = np.array(img_r)
    # img_g_array = np.array(img_g)

    # Clean img_r
    cleaned_img_r_array = clean_img_r(img_r_array)

    # Save the cleaned img_r as a grayscale image
    # cleaned_img_r = Image.fromarray(cleaned_img_r_array)

    # Define the band pairs
    band_pairs = [(0x00, 0x11), (0x22, 0x33), (0x44, 0x55), (0x66, 0x77),
                  (0x88, 0x99), (0xAA, 0xBB), (0xCC, 0xDD), (0xEE, 0xFF)]

    # Process each band pair
    for i, pair in enumerate(band_pairs):
        lower, upper = pair

        # Create a mask for the current band pair
        mask = np.zeros_like(cleaned_img_r_array, dtype=np.uint8)
        mask[(cleaned_img_r_array == lower) | (cleaned_img_r_array == upper)] = 0xFF

        # Check if the mask is empty (all zeros)
        if np.all(mask == 0):
            continue  # Skip exporting this band if the mask is empty

        # Save the mask as a grayscale image
        alpha = Image.fromarray(mask)
        alpha_output_path = os.path.join(output_alpha, os.path.relpath(img_r_path, path_R).replace('.png', f'_{i}.png'))
        os.makedirs(os.path.dirname(alpha_output_path), exist_ok=True)
        alpha.save(alpha_output_path)

        # Create a new image with the alpha channel
        img_result = Image.new('RGBA', img_g.size)
        img_result.paste(img_g, (0, 0))
        img_result.putalpha(alpha)

        # Save the resulting image
        img_result_output_path = os.path.join(output_bands, os.path.relpath(img_r_path, path_R).replace('.png', f'_{i}.png'))
        os.makedirs(os.path.dirname(img_result_output_path), exist_ok=True)
        img_result.save(img_result_output_path)

# Example usage
path_G = "G"
path_R = "R"
output_alpha = "output_alpha"
output_bands = "output_bands"

for root, dirs, files in os.walk(path_G):
    for file in files:
        if file.endswith('.png'):
            img_g_path = os.path.join(root, file)
            img_r_path = os.path.join(path_R, os.path.relpath(img_g_path, path_G))
            process_images(img_r_path, img_g_path, output_alpha, output_bands)