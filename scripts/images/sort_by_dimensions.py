from pathlib import Path
from PIL import Image
import shutil

def process_directory(input_dir, output_dir):
    # Iterate over the files in the input directory
    for file_path in input_dir.glob("**/*"):
        if file_path.is_file() and file_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".tga"]:
            try:
                # Open the image
                with Image.open(file_path) as img:
                    width, height = img.size
                
                # Create the output path based on dimensions
                dimension_folder = f"{width}x{height}"
                relative_path = file_path.relative_to(input_dir)
                output_path = output_dir / dimension_folder / relative_path
                
                # Ensure the output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the image to the output directory
                shutil.copy(file_path, output_path)
                
                print(f"Processed: {file_path} -> {output_path}")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

# Directory containing the nested structure of images
input_directory = Path("BC7_TGA_MIRRORED_TEST")

# Output directory for processed images
output_directory = Path("output")

# Process the images in the input directory
process_directory(input_directory, output_directory)
