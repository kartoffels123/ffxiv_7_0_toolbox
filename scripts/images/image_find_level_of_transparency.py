import pathlib
from PIL import Image
import concurrent.futures
from collections import defaultdict
import shutil

def categorize_transparency(image_path):
    try:
        with Image.open(image_path) as img:
            if img.mode == 'RGBA':
                alpha = img.getchannel('A')
                total_pixels = alpha.size[0] * alpha.size[1]
                transparent_pixels = sum(1 for pixel in alpha.getdata() if pixel < 255)
                transparency_percentage = (transparent_pixels / total_pixels) * 100

                if transparency_percentage < 10:
                    return image_path, 'less_than_10_percent'
                elif transparency_percentage < 25:
                    return image_path, 'less_than_25_percent'
                elif transparency_percentage < 50:
                    return image_path, 'less_than_50_percent'
                elif transparency_percentage < 75:
                    return image_path, 'less_than_75_percent'
                elif transparency_percentage < 90:
                    return image_path, 'less_than_90_percent'
                else:
                    return image_path, 'less_than_100_percent'
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
    return image_path, None

def process_images(image_paths):
    categorized_images = defaultdict(list)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(categorize_transparency, path) for path in image_paths]
        for future in concurrent.futures.as_completed(futures):
            image_path, category = future.result()
            if category:
                categorized_images[category].append(image_path)
    return categorized_images

def find_images(directory):
    return [path for path in pathlib.Path(directory).rglob('*.png')]

def copy_images(categorized_images, output_dir):
    for category, images in categorized_images.items():
        for image_path in images:
            relative_path = image_path.relative_to(input_directory)
            output_path = output_dir / category / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(image_path, output_path)

if __name__ == "__main__":
    input_directory = pathlib.Path("source")
    output_directory = pathlib.Path("output")

    image_paths = find_images(input_directory)
    categorized_images = process_images(image_paths)
    copy_images(categorized_images, output_directory)
