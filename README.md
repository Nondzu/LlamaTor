# LlamaTor: Decentralized AI Model Distribution via BitTorrent

LlamaTor is a community-driven project that offers a decentralized, efficient, and user-friendly method for downloading and distributing AI models. By leveraging the robustness of the BitTorrent protocol, LlamaTor enables the creation and sharing of torrent files for AI models, ensuring model distribution is not solely dependent on any centralized site.

**Pre-generated torrent files are available in the [LlamaTor Torrents Branch](https://github.com/Nondzu/LlamaTor/tree/torrents/torrents). Download and use them with a torrent client like [qBittorrent](https://www.qbittorrent.org/).**

## Key Features

- Generate a JSON file with the structure of AI models using `generate.py`
- Download all models from a JSON list using `download.py`
- Generate torrent files for downloaded models using `make_torrent.py`

## How to Use LlamaTor

### 1. Generate a JSON file with the structure of AI models

Run the `generate.py` script with the following arguments to generate a JSON file with the structure of AI models:

- `--user`: Filter models by the author's username (required)
- `--filter`: Filter models by keywords (optional)
- `--age`: Filter models by the number of days since the last update (default: 30)
- `--sort`: Sort models by "lastModified" or "name" (default: "lastModified")
- `--limit`: Limit the number of models in the output (optional)
- `--rd` or `--remove-duplicates`: Enable removing duplicate repositories (optional)
- `--filename`: Output filename for the JSON file (default: "string_model_\<current_date\>")

Example usage:

```bash
python generate.py --user TheBloke --filter GPTQ --age 30 --sort lastModified --limit 10 --rd --filename my_models
```

This command creates a JSON file named `my_models-models.json` containing up to 10 AI models created by the user "TheBloke" that contain the word "GPTQ" in their name, have been updated within the last 30 days, and are sorted by the last modified date. Duplicate repositories will be removed.

### 2. Download AI models 

Run the `download.py` script with the `--output_folder` and `--models_file` arguments to download the models:

```bash
python download.py --output_folder /media/user/models/ --models_file ./models.json 
```

This command downloads all models listed in the `models.json` file into the specified output folder.

### 3. Generate torrent files for AI models

Run the `make_torrent.py` script to generate torrent files for the downloaded models:

```python
python make_torrent.py --input_folder /path/to/input/folder --output_folder /path/to/output/folder
```

Replace `/path/to/input/folder` with the path to the folder containing the downloaded models, and `/path/to/output/folder` with the path to the folder where you want to save the generated torrent files.

The script processes each folder in the input folder, creates a torrent file for it, and saves the torrent file in the output folder. It uses a list of predefined trackers and a 512KB piece size for the torrent files.

After running the script, you can find the generated torrent files in the output folder. Share these torrent files with others to distribute the AI models using the BitTorrent protocol.

[https://github.com/Nondzu/LlamaTor/tree/torrents](https://github.com/Nondzu/LlamaTor/tree/torrents/torrents)

## Contribute to LlamaTor

LlamaTor is a community-driven project, and we value your contributions. If you have any suggestions for improvements, find any bugs, or want to contribute in any other way, please feel free to make a pull request or open an issue.

### Support LlamaTor

1. **Seed Torrents:** After downloading a model, keep your torrent client open so that others can download from you. The more seeders, the faster the download speed for everyone.
2. **Add or Build Your Own Seedbox:** If you have a seedbox, consider adding it to the network to increase download speeds and reliability.
3. **Donate:** Keeping seedboxes online and renting more storage costs money. Any donations to support this project are greatly appreciated.
4. **Spread the Word:** Share information about the LlamaTor project with your friends, colleagues, and social media networks. Raising awareness about the project helps to grow the community and attract more contributors, ultimately benefiting everyone involved.

## License

LlamaTor is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](LICENSE) file.
