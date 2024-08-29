import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess

def resize_image(file_path, source_dir, output_dir):
    # Create the output directory if it doesn't exist
    relative_path = file_path.relative_to(source_dir)
    output_path = output_dir / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Form the command to execute
    command = f'ImageResizer-r133.exe /load "{file_path}" /resize auto "XBR 2x <NoBlend>" /save "{output_path}"'
    print(f'processing: {file_path}')
    try:
        subprocess.run(command, check=True, shell=True)
        print(f'Successfully processed: {file_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error processing {file_path}: {e}')

def process_images(source_dir, output_dir):
    # Collect all image file paths
    image_paths = [p for p in source_dir.glob('**/*') if p.is_file() and p.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']]
    
    # Use ThreadPoolExecutor to process images in parallel
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(resize_image, file_path, source_dir, output_dir) for file_path in image_paths]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f'Error in thread: {e}')

if __name__ == '__main__':
    source_directory = Path('./2x_noblend')
    output_directory = Path('./2x_noblend_out')
    
    process_images(source_directory, output_directory)

