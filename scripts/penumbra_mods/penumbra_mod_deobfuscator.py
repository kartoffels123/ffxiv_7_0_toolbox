import json
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Function to sanitize directory names
def sanitize_name(name):
    return name.replace('/', '_').replace('\\', '_')

# Function to process each option in the JSON
def process_option(option, source_directory, base_directory):
    name = sanitize_name(option["Name"])
    files = option["Files"]

    for virtual_path, real_path in files.items():
        new_path = Path(name) / virtual_path
        full_destination_path = base_directory / new_path
        real_file_path = source_directory / real_path
        full_destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(real_file_path, full_destination_path)
        option["Files"][virtual_path] = str(new_path)

    return option

# Function to remove BOM if present
def remove_bom(data):
    if data.startswith('\ufeff'):
        print("BOM detected and removed.")
        return data[1:]
    return data

# Function to process each JSON file
def process_json_file(json_path, source_directory, base_directory):
    print(f"Attempting to process JSON file: {json_path}")

    # Check if the file is empty
    if json_path.stat().st_size == 0:
        print(f"File is empty, skipping: {json_path}")
        return

    try:
        with open(json_path, 'r', encoding='utf-8-sig') as file:
            data = remove_bom(file.read())
            data = json.loads(data)
            print(f"Successfully loaded JSON file: {json_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file: {json_path}. Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error processing file: {json_path}. Error: {e}")
        return

    if "Options" in data:
        for option in data["Options"]:
            option = process_option(option, source_directory, base_directory)

    output_path = base_directory / json_path.name
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Processed and saved JSON file to: {output_path}")

# Function to process the meta.json file
def process_meta_json(meta_json_path, base_directory):
    print(f"Attempting to process meta.json: {meta_json_path}")

    try:
        with open(meta_json_path, 'r', encoding='utf-8-sig') as file:
            data = remove_bom(file.read())
            meta_data = json.loads(data)
            print(f"Successfully loaded meta.json")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in meta.json: {meta_json_path}. Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error processing meta.json: {meta_json_path}. Error: {e}")
        return

    if "Name" in meta_data:
        meta_data["Name"] = f"{meta_data['Name']} - De-Obfuscated"

    output_path = base_directory / meta_json_path.name
    with open(output_path, 'w') as file:
        json.dump(meta_data, file, indent=4)
    print(f"Processed and saved meta.json to: {output_path}")

# Main processing function
def process_directory(selected_directory):
    source_directory = Path(selected_directory)
    destination_directory = source_directory.with_name(f"{source_directory.name} - De-Obfuscated")

    # heliosphere_json_path = source_directory / "heliosphere.json"
    # if not heliosphere_json_path.exists():
    #     messagebox.showinfo("Error", "No heliosphere.json found in the selected directory.")
    #     return

    destination_directory.mkdir(parents=True, exist_ok=True)

    json_files = list(source_directory.rglob("*.json"))
    progress_bar["maximum"] = len(json_files)
    
    for index, json_file in enumerate(json_files):
        if json_file.name.lower() in ["meta.json", "heliosphere.json"]:
            print(f"Ignoring file: {json_file.name}")
            continue
        process_json_file(json_file, source_directory, destination_directory)
        progress_bar["value"] = index + 1
        root.update_idletasks()

    meta_json_path = source_directory / "meta.json"
    if meta_json_path.exists():
        process_meta_json(meta_json_path, destination_directory)

    messagebox.showinfo("Success", f"Processing complete. Output directory:\n{destination_directory}")

# GUI Application
def select_directory():
    selected_directory = filedialog.askdirectory(title="Select Directory")
    if selected_directory:
        directory_label.config(text=f"Selected Directory: {selected_directory}")
        process_button.config(state=tk.NORMAL)
        selected_directory_path.set(selected_directory)

# Main Application Window
root = tk.Tk()
root.title("Penumbra Mod De-Obfuscator")
root.geometry("500x300")

# Variables
selected_directory_path = tk.StringVar()

# GUI Components
title_label = tk.Label(root, text="Penumbra Mod De-Obfuscator", font=("Helvetica", 16))
title_label.pack(pady=10)

subtitle_label = tk.Label(root, text="Creates a copy of the mod for easy reading", font=("Helvetica", 12))
subtitle_label.pack(pady=10)

directory_label = tk.Label(root, text="Select a Penumbra Mod Directory (Not PMP)", wraplength=400)
directory_label.pack(pady=10)

select_button = tk.Button(root, text="Select Directory", command=select_directory)
select_button.pack(pady=10)

process_button = tk.Button(root, text="Start Processing", command=lambda: process_directory(selected_directory_path.get()), state=tk.DISABLED)
process_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)

# Run the application
root.mainloop()
