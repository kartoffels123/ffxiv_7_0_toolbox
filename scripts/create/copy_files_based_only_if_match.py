from pathlib import Path
import shutil

def sort_files(source_dir):
    source_dir = Path(source_dir)
    
    # Create destination directories if they don't exist
    for folder in ['characterlegacy_shpk_s', 'characterlegacy_shpk_n', 'characterlegacy_shpk_d', 'characterlegacy_shpk_id', 'characterlegacy_shpk_m']:
        Path(folder).mkdir(parents=True, exist_ok=True)

    for file_path in source_dir.rglob('*'):
        if file_path.suffix.lower() in ('.dds', '.tga'):
            stem_parts = file_path.stem.split('_')
            if len(stem_parts) > 1:
                suffix = stem_parts[-1]
                if suffix == 's':
                    dest_folder = 'characterlegacy_shpk_s'
                elif suffix == 'n':
                    dest_folder = 'characterlegacy_shpk_n'
                elif suffix == 'd':
                    dest_folder = 'characterlegacy_shpk_d'
                elif suffix == 'id':
                    dest_folder = 'characterlegacy_shpk_id'
                elif suffix == 'm':
                    dest_folder = 'characterlegacy_shpk_m'
                else:
                    continue  # Skip files that don't match any criteria
                
                relative_path = file_path.relative_to(source_dir)
                dest_path = Path(dest_folder) / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(file_path, dest_path)
                print(f"Copied {file_path} to {dest_path}")

# Usage
source_directory = Path('characterlegacy_shpk')
sort_files(source_directory)
