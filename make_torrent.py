import os
import subprocess
import time
import argparse
import fnmatch

def generate_torrents(input_folder, output_folder, filter_pattern="*AWQ*"):
    trackers = [
        "http://atrack.pow7.com/announce",
        "udp://explodie.org:6969/announce",
        "udp://p4p.arenabg.com:1337/announce",
        "http://pow7.com:80/announce",
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://tracker.tiny-vps.com:6969/announce",
        "http://tracker2.itzmx.com:6961/announce",
        "udp://open.stealth.si:80/announce",
        "http://p4p.arenabg.com:1337/announce",
        "http://tracker.opentrackr.org:1337/announce"
    ]

    folders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f)) and fnmatch.fnmatch(f, filter_pattern)]
    total_folders = len(folders)


    start_time = time.time()

    for i, folder in enumerate(folders, start=1):
        output_file = os.path.join(output_folder, f"{folder}.torrent")
        command = ["mktorrent", "-l", "19", "-p", "-o", output_file]

        for tracker in trackers:
            command.extend(["-a", tracker])

        command.append(os.path.join(input_folder, folder))

        print(f"Processing {i} of {total_folders}: {folder}")

        folder_start_time = time.time()
        subprocess.run(command)
        folder_end_time = time.time()

        print(f"Time taken for {folder}: {folder_end_time - folder_start_time} seconds")

    end_time = time.time()

    print(f"Total time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate torrent files for AI models.")
    parser.add_argument('--input_folder', type=str, required=True, help='The folder containing the downloaded models.')
    parser.add_argument('--output_folder', type=str, required=True, help='The folder where the generated torrent files will be saved.')
    parser.add_argument('--filter', type=str, default="*", help="Filter pattern for folder names (e.g., *AWQ*). If you want to create torrents for all folders, leave this blank.")
    args = parser.parse_args()

    generate_torrents(args.input_folder, args.output_folder, filter_pattern=args.filter)
