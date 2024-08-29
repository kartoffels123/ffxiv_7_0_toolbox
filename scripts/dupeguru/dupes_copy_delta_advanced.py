import pandas as pd
from pathlib import Path
import shutil

# Read the CSV file
csv_file = 'compare_6-3_RGB_to_7-0_RGB_DMS.csv'
df = pd.read_csv(csv_file)

# Filter the DataFrame based on the "Match %" criteria
filtered_df = df[df['Match %'] >= 98]

# Create a directory for results if it doesn't exist
results_dir = Path('results')
results_dir.mkdir(exist_ok=True)

# Group the filtered DataFrame by 'Group ID'
grouped_df = filtered_df.groupby('Group ID')

# Iterate over each group
for group_id, group_df in grouped_df:
    # Get the first entry of the group
    first_entry = group_df.iloc[0]
    
    # Extract the filename and folder from the first entry
    filename = first_entry['Filename']
    folder = first_entry['Folder']
    if "7-0" in folder:
        print("7-0 item, skipping " + filename)
        continue
    # Skip files ending with "_n"
    # if filename.endswith('_n.tex'):
    #     continue
    
    # Construct the full path of the first entry
    source_path = Path(folder) / filename
    
    # Check if the file exists
    if not source_path.exists():
        print(f"File not found: {source_path}")
        continue
    
    # Iterate over the remaining entries in the group
    for index, row in group_df.iloc[1:].iterrows():
        # Extract the destination folder and filename from the remaining entries
        destination_folder = row['Folder']
        destination_filename = row['Filename']
        
        # Construct the destination path
        destination_path = Path(destination_folder) / destination_filename
        results_path = Path(results_dir)/ destination_path
        
        # Create parent directories for the destination path
        results_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Copy the file from the source to the destination
            shutil.copy2(source_path, results_path)
            print(f"Copied: {source_path} to {results_path}")
        except FileNotFoundError:
            continue
            # print(f"File not found: {source_path}")

print("Files copied successfully.")