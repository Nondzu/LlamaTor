import os
import subprocess
import time

def generate_torrents(input_folder, output_folder):
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

    folders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
    total_folders = len(folders)

    start_time = time.time()

    for i, folder in enumerate(folders, start=1):
        output_file = os.path.join(output_folder, f"{folder}.torrent")
        command = ["mktorrent", "-l", "22", "-p", "-o", output_file]

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

# Usage
generate_torrents("/home/kamil/ml/models/WizardLM", "/home/kamil/app/wi1")
