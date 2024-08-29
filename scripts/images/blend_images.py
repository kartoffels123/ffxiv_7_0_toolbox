from pathlib import Path
from PIL import Image, ImageFilter, ImageDraw

def blend_middle(image_path, output_dir):
    # Open the image
    image = Image.open(image_path)
    
    # Get the image dimensions
    width, height = image.size
    
    # Calculate the width of the blend strip
    blend_width = max(10, int(width / 68.26))  # This scales 2048px to 30px, 4096px to 60px
    
    # Calculate the middle region boundaries
    left_boundary = width // 2 - blend_width // 2
    right_boundary = width // 2 + blend_width // 2
    
    # Crop the middle region
    middle_region = image.crop((left_boundary, 0, right_boundary, height))
    
    # Apply Gaussian blur to the middle region
    blurred_region = middle_region.filter(ImageFilter.GaussianBlur(radius=10))
    
    # Create a mask for the middle region with a gradient effect
    mask = Image.new("L", (blend_width, height), 0)
    draw = ImageDraw.Draw(mask)
    for i in range(blend_width // 2):
        draw.line((i, 0, i, height), fill=int(255 * (i / (blend_width // 2))))
        draw.line((blend_width - 1 - i, 0, blend_width - 1 - i, height), fill=int(255 * (i / (blend_width // 2))))
    
    # Paste the blurred region onto the original image using the mask
    image.paste(blurred_region, (left_boundary, 0), mask)
    
    # Save the blended image to the output directory
    output_path = output_dir / image_path.relative_to(input_directory)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    
    print(f"Processed: {image_path}")

def process_directory(input_dir, output_dir):
    # Iterate over the files in the input directory
    for file_path in input_dir.glob("**/*"):
        if file_path.is_file() and file_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".tga"]:
            blend_middle(file_path, output_dir)

# Directory containing the nested structure of images
input_directory = Path("BC7_TGA_MIRRORED_TEST")

# Output directory for blended images
output_directory = Path("blended")

# Process the images in the input directory
process_directory(input_directory, output_directory)
