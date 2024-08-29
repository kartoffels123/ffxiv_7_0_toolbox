import csv
from pathlib import Path
import shutil

def copy_structure_from_csv(input_dir, output_dir, csv_file):
    # Convert input_dir and output_dir to Path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Read the CSV file
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        
        for row in reader:
            name, model_path, model_type, material_paths = row
            source_dir = input_dir / Path(model_path).parent.parent.parent  # Stopping at 'obj' level
            dest_dir = output_dir / source_dir.relative_to(input_dir)
            
            if source_dir.exists() and source_dir.is_dir():
                dest_dir.mkdir(parents=True, exist_ok=True)
                for item in source_dir.rglob('*'):
                    relative_path = item.relative_to(source_dir)
                    dest_item_path = dest_dir / relative_path
                    if item.is_file():
                        dest_item_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dest_item_path)
                    elif item.is_dir():
                        dest_item_path.mkdir(parents=True, exist_ok=True)



if __name__ == "__main__":
    input_dir = "7-0"
    output_dir = "7-0_only_named"
    csv_file = "ENpcs.csv"

    copy_structure_from_csv(input_dir, output_dir, csv_file)
