import os
import json
import sys
import requests
import argparse
import logging
import datetime
from tqdm import tqdm
import signal

# Create the parser
parser = argparse.ArgumentParser(description="Download models from Hugging Face's model hub.")
# Add the arguments
parser.add_argument('--output_folder', type=str, required=True, help='The folder where the models will be saved.')
parser.add_argument('--models_file', type=str, required=True, help='The JSON file containing the models to download.')
parser.add_argument('--timeout', type=int, default=30, help='The timeout for the download process (in seconds).')
parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')
# Parse the arguments
args = parser.parse_args()

def download_file(file_url, file_path, logger):
    response = None
    try:
        response = requests.get(file_url, allow_redirects=True, timeout=args.timeout, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)  # create the folder if it does not exist
            with open(file_path, 'wb') as f:
                total_size = int(response.headers.get('content-length', 0))
                logger.info(f"Downloading file {file_path} ({total_size/ 1e6} Mbytes)")
                with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc=file_path, miniters=1, file=sys.stdout) as t:
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                        t.update(len(data))
    except Exception as e:
        logger.error(f"Error downloading {file_url}: {e}")

def signal_handler(sig, frame):
    logging.info("Interrupted by user. Exiting...")
    sys.exit(0)

def main():
    # Load models from JSON file
    try:
        with open(args.models_file, 'r') as f:
            models = json.load(f)
    except FileNotFoundError:
        logging.error(f"Models file {args.models_file} not found.")
        sys.exit(1)

    # Check if there are any models
    if models:
        # Get the models
        for model in models:
            model_name = model['name']
            dir_name = model_name.replace('/', '_')  # replace '/' with '_'
            output_dir = os.path.join(args.output_folder, dir_name)  # specify the folder where you want to save the model

            # Set up logging for this model
            logger = logging.getLogger(model_name)
            logger.setLevel(logging.INFO)
            log_dir = 'logs'
            os.makedirs(log_dir, exist_ok=True)
            current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            file_handler = logging.FileHandler(os.path.join(log_dir, f"{model_name.replace('/', '_')}_{current_time}.log"))
            stream_handler = logging.StreamHandler()  # This handler will print messages to the console
            formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
            # Download the files
            for branch in model['branches']:
                for file in branch['files']:
                    file_url = f"https://huggingface.co/{model_name}/resolve/{branch['name']}/{file}"
                    file_path = os.path.join(output_dir, branch['name'], file)
                    if os.path.exists(file_path):
                        logger.info(f"File {file_path} already exists. Skipping...")
                        continue
                    download_file(file_url, file_path, logger)
    else:
        logging.info("No models found.")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
