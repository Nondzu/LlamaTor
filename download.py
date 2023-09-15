import os
import threading
import time
import json
import sys
import subprocess

# Global flag that all threads can check
should_exit = False

def get_folder_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def check_folder_size(folder):
    global should_exit
    while not should_exit:
        try:
            size = get_folder_size(folder)
            print(f'Current size of {folder}: {size / 1024**3:.2f} GB')
            time.sleep(20)  # check every 5 seconds
        except Exception as e:
            print(f"Error checking size: {e}")
            break

# Load models from JSON file
with open('models.json', 'r') as f:
    models = json.load(f)

# Set output folder
output_folder = "/media/kamil/bfd0f237-f145-47c7-8cc9-6c103587f2f6/models"  # replace this with your desired output folder

try:
    # Check if there are any models
    if models:
        # Get the models
        for model in models:
            creator = model['creator']
            repo = model['repo']
            model_name = f"{creator}/{repo}"
            output_dir = f"{output_folder}/{model_name}"  # specify the folder where you want to save the model

            # Check if the model has already been downloaded
            if os.path.exists(output_dir):
                print(f"{model_name} has already been downloaded.")
                continue

            # Create directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Start a new thread to check the size of the output folder
            threading.Thread(target=check_folder_size, args=(output_dir,), daemon=True).start()

            # Clone the repository
            print(f"Cloning {model_name} into {output_dir}...")
            process = subprocess.Popen(f"git lfs clone https://huggingface.co/{model_name} {output_dir}", shell=True)
            while process.poll() is None:  # While process is still running
                if should_exit:
                    process.terminate()  # If should_exit is True, terminate the process
                    break
                time.sleep(0.1)  # Check every 100 ms
            print(f"Finished cloning {model_name}.")
    else:
        print("No models found.")
except KeyboardInterrupt:
    print("\nStopping script...")
    should_exit = True  # Set the flag to signal all threads to exit
    time.sleep(1)  # Give threads a chance to notice
    sys.exit()
