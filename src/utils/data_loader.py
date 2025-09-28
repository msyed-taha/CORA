import json
from datasets import load_dataset
from pathlib import Path

# Load Python subset of CodeSearchNet
dataset = load_dataset("code_search_net", "python")

# Extract (code, docstring) pairs
def extract_examples(split, max_samples=None):
    data = []
    for i, item in enumerate(dataset[split]):
        if max_samples and i >= max_samples:
            break
        if item["func_code_string"] and item["func_documentation_string"]:
            data.append({
                "code": item["func_code_string"],
                "doc": item["func_documentation_string"]
            })
    return data

# Limit for quick processing (you can increase later)
train_data = extract_examples("train", max_samples=5000)
val_data   = extract_examples("validation", max_samples=1000)
test_data  = extract_examples("test", max_samples=1000)

# Save to data/processed/
Path("data/processed").mkdir(parents=True, exist_ok=True)

with open("data/processed/codesearchnet_python_train.json", "w") as f:
    json.dump(train_data, f, indent=2)

with open("data/processed/codesearchnet_python_val.json", "w") as f:
    json.dump(val_data, f, indent=2)

with open("data/processed/codesearchnet_python_test.json", "w") as f:
    json.dump(test_data, f, indent=2)

print("✅ CodeSearchNet JSON files saved in data/processed/")
