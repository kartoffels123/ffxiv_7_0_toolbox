import subprocess
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)

    def flush(self):
        pass

def run_script(script_name, upscale_factor):
    print(f"Running {script_name}...")
    env = os.environ.copy()
    env['UPSCALE_FACTOR'] = upscale_factor
    script_path = os.path.join(os.getcwd(), 'src', script_name)
    result = subprocess.run([sys.executable, script_path], 
                            capture_output=True, text=True, env=env,
                            cwd=os.getcwd())  # Set the working directory to the main folder
    if result.returncode != 0:
        print(f"Error running {script_name}:")
        print(result.stderr)
        return False
    print(f"Finished running {script_name}")
    print(result.stdout)
    return True

def main():
    root = tk.Tk()
    root.title("Texture Processing Tool")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Output Format:").grid(column=0, row=0, sticky=tk.W)
    output_format = tk.StringVar(value="bc5unorm")
    ttk.Radiobutton(frame, text="BC5 UNORM (recommended)", variable=output_format, value="bc5unorm").grid(column=1, row=0, sticky=tk.W)
    ttk.Radiobutton(frame, text="TGA", variable=output_format, value="tga").grid(column=2, row=0, sticky=tk.W)

    ttk.Label(frame, text="Upscale Factor:").grid(column=0, row=1, sticky=tk.W)
    upscale_factor = tk.StringVar(value="x2")
    ttk.Radiobutton(frame, text="x2 (recommended)", variable=upscale_factor, value="x2").grid(column=1, row=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="x4", variable=upscale_factor, value="x4").grid(column=2, row=1, sticky=tk.W)

    text_area = tk.Text(frame, wrap='word', width=80, height=20)
    text_area.grid(column=0, row=3, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text_area.yview)
    scrollbar.grid(column=3, row=3, sticky=(tk.N, tk.S))
    text_area['yscrollcommand'] = scrollbar.set

    sys.stdout = TextRedirector(text_area)
    sys.stderr = TextRedirector(text_area)

    def process():
        scripts = [
            "band_nested_dirs_extract_rg.py",
            "band_nested_dirs_split.py",
            "band_nested_dirs_intermediate_upscales.py",
            "band_nested_dirs_merge.py",
            "band_nested_dirs_final_bc5.py" if output_format.get() == "bc5unorm" else "band_nested_dirs_final_tga.py"
        ]

        if not os.path.exists("input"):
            messagebox.showerror("Error", "The 'input' directory does not exist. Please create it and add your input files.")
            return

        for script in scripts:
            if not os.path.exists(f"src/{script}"):
                messagebox.showerror("Error", f"Error: src/{script} not found.")
                return

        for script in scripts:
            if not run_script(script, upscale_factor.get()):
                messagebox.showerror("Error", f"An error occurred while running {script}. Please check the output for details.")
                return

        output_dir = "output_bc5_unorm" if output_format.get() == "bc5unorm" else "output_tga"
        messagebox.showinfo("Complete", f"All scripts have been executed successfully. Your output files can be found in the '{output_dir}' directory.")

    ttk.Button(frame, text="Process", command=process).grid(column=0, row=2, columnspan=3)

    ttk.Label(frame, text="Please ensure your input files are in the 'input' directory before processing.").grid(column=0, row=4, columnspan=3, sticky=tk.W)

    root.mainloop()

if __name__ == "__main__":
    main()