import argparse
from huggingface_hub import HfApi, ModelFilter
from tqdm import tqdm
import json
import time
import datetime
import requests
import datetime as dt
from dateutil.parser import parse

class ModelProcessor:
    def __init__(self, args):
        self.args = args
        self.api = HfApi()
        self.model_filter = ModelFilter(author=args.user) if args.user else None

    def fetch_and_filter_models(self):
        all_models = list(self.api.list_models(filter=self.model_filter))
        print(f"Total models count: {len(all_models)}")
        filtered_models = (
            [
                m
                for m in all_models
                if any(f.lower() in m.modelId.lower() for f in self.args.filter)
                and m.author.lower() == self.args.user.lower()
            ]
            if self.args.filter
            else all_models
        )
        if self.args.sort == "lastModified":
            filtered_models.sort(key=lambda x: x.lastModified, reverse=True)
        elif self.args.sort == "name":
            filtered_models.sort(key=lambda x: x.modelId.lower())
        if self.args.limit is not None:
            filtered_models = filtered_models[: self.args.limit]
        print("Number of models after filtering:", len(filtered_models))
        time.sleep(1)
        return filtered_models

    def process_models(self, filtered_models):
        now = dt.datetime.now().date()
        repo_table = []
        for model in tqdm(filtered_models, desc="Processing models"):
            try:
                last_modified = parse(model.lastModified).date()
                if (now - last_modified).days > self.args.age:
                    print(
                        f"Removed outdated repo: {(model.modelId)} : last update: {last_modified}"
                    )  # Added debug print info
                    continue
                repo_data = {
                    "name": model.modelId.replace("/", "#")
                    .replace("_", "#")
                    .replace("-", "#"),
                    "original_name": model.modelId,
                    "branches": [],
                }
                git_refs = self.api.list_repo_refs(model.modelId, repo_type="model")
                branches = [b for b in git_refs.branches if not b.name.startswith(".git")]
                repo_data["last_update"] = model.lastModified
                non_empty_branch_found = False
                for branch in branches:
                    try:
                        files = self.api.list_repo_files(model.modelId, revision=branch.name)
                        if files:
                            non_empty_branch_found = True
                            repo_data["branches"].append(
                                {
                                    "name": branch.name,
                                    "files": [
                                        f
                                        for f in files
                                        if not f.endswith(".gitattributes")
                                        and not f.startswith(".git")
                                    ],
                                }
                            )
                    except Exception as e:
                        print(f"Error fetching files for model {model.modelId} on branch {branch.name}: {e}")
                if non_empty_branch_found:
                    repo_table.append(repo_data)
                else:
                    print(
                        f"Empty repo detected and skipped: {model.modelId}"
                    )  # Print info about empty repo
            except Exception as e:
                print(f"Error fetching branches for model {model.modelId}: {e}")
        return repo_table

    def get_existing_torrents(self, url):
        response = requests.get(url)
        files = response.json()
        file_list = []
        for file in files:
            if file["type"] == "file":
                file_name = (
                    file["name"]
                    .replace(".torrent", "")
                    .replace("/", "#")
                    .replace("_", "#")
                    .replace("-", "#")
                )
                if not file_name.startswith(".gitattributes"):
                    file_list.append(file_name)
        return file_list

    def filter_and_output_repos(self, repo_table, existing_torrents):
        removed_repos = []
        duplicated_repos = []
        output_repos = []
        for repo in repo_table:
            if repo["name"] not in existing_torrents:
                output_repos.append(repo)
            else:
                if self.args.rd:
                    removed_repos.append(repo)
                    print(
                        f"Removed duplicated repo: {repo['original_name']}"
                    )  # Added debug print info
                else:
                    duplicated_repos.append(repo)
        with open(self.args.filename + "-models.json", "w") as f:
            json.dump(
                [{**repo, "name": repo["original_name"]} for repo in output_repos],
                f,
                indent=4,
            )
        if removed_repos:
            with open(self.args.filename + "removed_repos-models.json", "w") as f:
                json.dump(
                    {
                        "removed_repos": [
                            {"name": repo["original_name"]} for repo in removed_repos
                        ],
                        "duplicated_repos": [
                            {"name": repo["original_name"]} for repo in duplicated_repos
                        ],
                    },
                    f,
                    indent=4,
                )

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", type=str, default=None)
    parser.add_argument("--filter", type=str, nargs="+", default=[])
    parser.add_argument("--age", type=int, default=30)  # in days
    parser.add_argument(
        "--sort", type=str, default="lastModified", choices=["lastModified", "name"]
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--rd",
        "--remove-duplicates",
        action="store_true",
        help="Enable removing duplicate repositories",
    )
    parser.add_argument("--filename", type=str, default=f"string_model_{datetime.date.today().strftime('%d%m%Y')}")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if not (args.user or args.filter):
        raise ValueError("At least one of --user or --filter must be provided")
    processor = ModelProcessor(args)
    filtered_models = processor.fetch_and_filter_models()
    repo_table = processor.process_models(filtered_models)
    existing_torrents = processor.get_existing_torrents(
        "https://api.github.com/repos/Nondzu/LlamaTor/contents/torrents?ref=torrents"
    )
    processor.filter_and_output_repos(repo_table, existing_torrents)
if __name__ == "__main__":
    main()