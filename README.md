# Welcome to LlamaTor

![LlamaTor Version](https://img.shields.io/badge/version-0.0.93-blue.svg?cacheSeconds=2592000)

LlamaTor is a community-driven project that provides a decentralized, efficient, and user-friendly method for downloading AI models. This tool enables the creation and sharing of torrent files for AI models, leveraging the robustness of the BitTorrent protocol to ensure model distribution is not solely dependent on any centralized site.

## Features

- Generate a JSON file with the structure of AI models using `generate.py`
- Download all models from a JSON list using `download.py`
- Generate torrent files for downloaded models using `make_torrent.py`

## Usage
### Generate a JSON file with the structure of AI models

1. Run the `generate.py` script with the `--user` and `--filter` arguments to generate a JSON file with the structure of AI models:

```bash
python generate.py --user TheBloke --filter GPTQ
```

This will create a JSON file containing all AI models created by the user "TheBloke" that contain the word "GPTQ" in their name. This is really useful to create a torrent mirror of Hugging Face.

### Download models 

2. Run the `download.py` script with the `--output_folder` and `--models_file` arguments to download the models:

```bash
python download.py --output_folder /media/user/models/ --models_file ./models.json 
```

This will download all models listed in the `models.json` file into the specified output folder.

### Generate torrent files

3. Run the `make_torrent.py` script to generate torrent files for the downloaded models:

```python
python make_torrent.py --input_folder /path/to/input/folder --output_folder /path/to/output/folder
```

Replace `/path/to/input/folder` with the path to the folder containing the downloaded models, and `/path/to/output/folder` with the path to the folder where you want to save the generated torrent files.

The script will process each folder in the input folder, create a torrent file for it, and save the torrent file in the output folder. It uses a list of predefined trackers and a 4MB piece size for the torrent files.

After running the script, you can find the generated torrent files in the output folder. You can then share these torrent files with others to distribute the models using the BitTorrent protocol.

[https://github.com/Nondzu/LlamaTor/tree/torrents](https://github.com/Nondzu/LlamaTor/tree/torrents/torrents)


## Contributing

LlamaTor is a community-driven project. We value your contributions. If you have any suggestions for improvements, find any bugs, or want to contribute in any other way, please feel free to make a pull request or open an issue.

### How You Can Help

1. **Seed Torrents:** After downloading a model, keep your torrent client open so that others can download from you. The more seeders, the faster the download speed for everyone.

2. **Add or Build Your Own Seedbox:** If you have a seedbox, consider adding it to the network to increase download speeds and reliability.

3. **Donate:** Keeping seedboxes online and renting more storage costs money. Any donations to support this project are greatly appreciated.

## License

LlamaTor is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](LICENSE) file.
