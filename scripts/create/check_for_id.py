from pathlib import Path

def find_files(pattern, directory, output_file):
    # Create a Path object for the directory
    directory_path = Path(directory)
    
    # Check if the directory exists
    if not directory_path.exists():
        print(f"The directory {directory} does not exist.")
        return

    # Find all files matching the pattern in the nested directory structure
    matching_files = list(directory_path.rglob(pattern))
    
    # Write the matching file paths to the output file
    with open(output_file, 'w') as file:
        for matching_file in matching_files:
            file.write(str(matching_file) + '\n')
    
    print(f"Found {len(matching_files)} files matching the pattern '{pattern}' and saved to {output_file}.")

# Define the pattern, directory, and output file
pattern = "*_id.tex"
directory = "equipment"
output_file = "matching_files.txt"

# Call the function to find files and write to the output file
find_files(pattern, directory, output_file)
