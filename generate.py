import argparse
import json
from huggingface_hub import HfApi, ModelFilter
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', type=str, default=None)
    parser.add_argument('--filter', type=str, nargs='+', default=[])
    args = parser.parse_args()

    if args.user is None and len(args.filter) == 0:
        raise ValueError("At least one of --user or --filter must be provided")

    username = args.user
    filter_strs = [f.lower() for f in args.filter]

    api = HfApi()
    print("Fetching models")
    model_filter = ModelFilter(author=username) if username else None
    all_models = api.list_models(filter=model_filter)

    print("Filtering models")
    # filtered_models = [model for model in all_models if any(filter_str in model.modelId.lower() for filter_str in filter_strs)]
    filtered_models = [model for model in all_models if all(filter_str in model.modelId.lower() for filter_str in filter_strs)]

    print("Number of models after filtering:", len(filtered_models))

    repo_table = []
    print("Processing models:")
    for model in tqdm(filtered_models, desc="Processing models"):
        repo_data = {
            "name": model.modelId,
            "branches": []
        }

        print("Fetching branches for model:", model.modelId)
        try:
            git_refs = api.list_repo_refs(model.modelId, repo_type="model")
            for branch_info in git_refs.branches:
                branch = branch_info.name
                branch_data = {
                    "name": branch,
                    "files": []
                }
                print("Fetching files for branch:", branch)
                try:
                    files = api.list_repo_files(model.modelId, revision=branch)
                    for file in files:
                        if not file.endswith(".gitattributes") and not file.startswith(".git"):  # exclude git files
                            branch_data["files"].append(file)
                    repo_data["branches"].append(branch_data)
                except Exception as e:
                    print(f"Error fetching files for model {model.modelId} on branch {branch}: {e}")
                    continue
        except Exception as e:
            print(f"Error fetching branches for model {model.modelId}: {e}")
            continue

        repo_table.append(repo_data)

    print("Writing data to models.json")
    with open('models.json', 'w') as f:
        json.dump(repo_table, f, indent=4)

    print("Done!")

if __name__ == "__main__":
    main()
