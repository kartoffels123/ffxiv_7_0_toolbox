from pathlib import Path

def remove_matching_files(output_dir, source_dir):
    output_dir = Path(output_dir)
    source_dir = Path(source_dir)

    for output_file in output_dir.rglob('*'):
        if output_file.is_file():
            relative_path = output_file.relative_to(output_dir).with_suffix('')
            for source_file in source_dir.rglob(f'{relative_path.stem}.*'):
                if source_file.is_file() and source_file.stem == relative_path.stem:
                    try:
                        source_file.unlink()
                        print(f"Removed: {source_file}")
                    except Exception as e:
                        print(f"Error removing {source_file}: {e}")

if __name__ == "__main__":
    output_directory = "7-0_only_check_for_low_res_TGA"
    source_directory = "7-0_only_check_for_low_res"

    remove_matching_files(output_directory, source_directory)
    print("Process completed.")
