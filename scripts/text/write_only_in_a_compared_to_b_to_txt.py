import pathlib

def find_unique_files(source_dir, output_dir):
    source_files = {file.relative_to(source_dir) for file in source_dir.rglob('*') if file.is_file()}
    output_files = {file.relative_to(output_dir) for file in output_dir.rglob('*') if file.is_file()}
    
    unique_files = source_files - output_files
    return [str(file) for file in unique_files]

def write_list_to_file(file_list, output_file):
    with open(output_file, 'w') as f:
        for file in file_list:
            f.write(f"{file}\n")

if __name__ == "__main__":
    source_directory = pathlib.Path("source")
    output_directory = pathlib.Path("out")
    output_file_path = "unique_files.txt"

    unique_files = find_unique_files(source_directory, output_directory)
    write_list_to_file(unique_files, output_file_path)
    
    print(f"List of unique files written to {output_file_path}")