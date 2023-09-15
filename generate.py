import argparse
import json
from huggingface_hub import HfApi
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', type=str, required=True)
    parser.add_argument('--filter', type=str, default='')
    args = parser.parse_args()

    username = args.user
    filter_str = args.filter.lower()

    api = HfApi()
    print("Fetching all models")
    all_models = api.list_models()

    print("Filtering models for user:", username)
    user_models = [model for model in all_models if model.modelId.startswith(username + "/")]

    print("Number of models for user:", len(user_models))

    print("Applying filter:", filter_str)
    filtered_models = [model for model in user_models if filter_str in model.modelId.lower()]

    print("Number of models after applying filter:", len(filtered_models))

    repo_table = []
    print("Processing models:")
    for model in tqdm(filtered_models, desc="Processing models"):
        repo_data = {
            "name": model.modelId,
            "branches": []
        }

        # Get all branches and files for each branch
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
    with open('modelsss.json', 'w') as f:
        json.dump(repo_table, f, indent=4)

    print("Done!")

if __name__ == "__main__":
    main()