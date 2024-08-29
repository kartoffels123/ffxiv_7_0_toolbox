import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess

upscale_factor = os.environ.get('UPSCALE_FACTOR', 'x2')
resizer_scale = upscale_factor.replace('x', '') + 'x'

def run_island_padder():
    command = os.path.join('src', 'island-padder.exe')
    subprocess.run(command, check=True, shell=True)

def resize_bands(file_path, source_dir, output_dir):
    relative_path = Path(file_path).relative_to(source_dir)
    output_path = output_dir / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    

    image_resizer_path = os.path.join('src', 'ImageResizer-r133.exe')
    command = f'"{image_resizer_path}" /load "{file_path}" /resize auto "XBR {resizer_scale}" /save "{output_path}"'
    subprocess.run(command, check=True, shell=True)

def resize_alpha_r(file_path, source_dir, output_dir):
    relative_path = Path(file_path).relative_to(source_dir)
    output_path = output_dir / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    image_resizer_path = os.path.join('src', 'ImageResizer-r133.exe')
    command = f'"{image_resizer_path}" /load "{file_path}" /resize auto "XBR {resizer_scale} <NoBlend>" /save "{output_path}"'
    subprocess.run(command, check=True, shell=True)

def process_directory(input_dir, output_dir, process_func):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    image_paths = [p for p in input_dir.glob('**/*') if p.is_file() and p.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']]
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_func, file_path, input_dir, output_dir) for file_path in image_paths]
        for future in futures:
            future.result()

def main():
    # Step 1: Create output_bands_padded using island-padder.exe
    input_bands = "output_bands"
    output_bands_padded = "output_bands_padded"
    run_island_padder()
    
    for root, _, files in os.walk(input_bands):
        for file in files:
            input_path = os.path.join(root, file)
            relative_path = os.path.relpath(input_path, input_bands)
            output_path = os.path.join(output_bands_padded, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
    
    # Step 2: Process output_bands_padded with ImageResizer-r133.exe
    process_directory(output_bands_padded, f"output_bands_padded_{upscale_factor}", resize_bands)
    process_directory("output_alpha", f"output_alpha_{upscale_factor}", resize_alpha_r)
    process_directory("R", f"R_{upscale_factor}", resize_alpha_r)
if __name__ == "__main__":
    main()