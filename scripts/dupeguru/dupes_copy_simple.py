import pandas as pd
from pathlib import Path
import shutil

# Read the CSV file
csv_file = 'C:\\Users\\kartoffel\\PycharmProjects\\ffxiv_dawntrail\\documentation\\csv_comparisons\\common textures\\duplicates_modified.csv'
df = pd.read_csv(csv_file)

# Get the first entry for each Group ID
first_entries = df.groupby('Group ID').first().reset_index()

# Create a directory for results if it doesn't exist
results_dir = Path('results')
results_dir.mkdir(exist_ok=True)

# Iterate over the first entries
for index, row in first_entries.iterrows():
    filename = row['Filename']
    folder = row['Folder']
    
    # Construct the full path
    full_path = Path(folder) / filename
    
    # Construct the destination path within the results directory
    destination_path = results_dir / full_path.relative_to(full_path.anchor)
    
    # Create parent directories for the destination path
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy the file to the results directory
    shutil.copy2(full_path, destination_path)

print("Files copied successfully.")
