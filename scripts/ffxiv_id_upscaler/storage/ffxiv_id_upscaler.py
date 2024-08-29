import subprocess
import sys
import os

# starts in input
# exits at output

def run_script(script_name):
    print(f"Running {script_name}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script_name}:")
        print(result.stderr)
        sys.exit(1)
    print(f"Finished running {script_name}")
    print(result.stdout)

def main():
    scripts = [
        "band_nested_dirs_extract_rg.py",
        "band_nested_dirs_split.py",
        "band_nested_dirs_intermediate_upscales.py",
        "band_nested_dirs_merge.py",
        "band_nested_dirs_final_bc5.py"
    ]

    for script in scripts:
        if not os.path.exists(script):
            print(f"Error: {script} not found in the current directory.")
            sys.exit(1)

    for script in scripts:
        run_script(script)

    print("All scripts have been executed successfully.")

if __name__ == "__main__":
    main()