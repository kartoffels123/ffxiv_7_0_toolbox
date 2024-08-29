from pathlib import Path

def remove_matching_items(list_file, r_dir):
    # Read the list of matching items
    with open(list_file, 'r') as f:
        matching_items = f.read().splitlines()
    
    r_path = Path(r_dir)
    
    for item in matching_items:
        r_item_path = r_path / item
        
        # Remove the item from the 7-0_id_R directory
        if r_item_path.exists():
            r_item_path.unlink()
            print(f"Removed: {r_item_path}")

# Define the paths and the list file
list_file = "RGBA.txt"
r_directory = "textures_output"

# Run the function
remove_matching_items(list_file, r_directory)
