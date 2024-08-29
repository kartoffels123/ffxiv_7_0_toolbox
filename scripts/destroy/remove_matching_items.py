from pathlib import Path

def remove_matching_items(list_file, g_dir, r_dir):
    # Read the list of matching items
    with open(list_file, 'r') as f:
        matching_items = f.read().splitlines()
    
    g_path = Path(g_dir)
    r_path = Path(r_dir)
    
    for item in matching_items:
        g_item_path = g_path / item
        r_item_path = r_path / item
        
        # Remove the item from the 7-0_id_G directory
        if g_item_path.exists():
            g_item_path.unlink()
            print(f"Removed: {g_item_path}")
        
        # Remove the item from the 7-0_id_R directory
        if r_item_path.exists():
            r_item_path.unlink()
            print(f"Removed: {r_item_path}")

# Define the paths and the list file
list_file = "solid_color_matches.txt"
g_directory = "7-0_id_G"
r_directory = "7-0_id_R"

# Run the function
remove_matching_items(list_file, g_directory, r_directory)
