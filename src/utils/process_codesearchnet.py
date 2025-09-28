import json
from pathlib import Path
from datasets import load_dataset

OUT_FILE = "data/processed/json/codesearchnet_clean.jsonl"

def normalize_text(text: str) -> str:
    """Basic cleanup for code/doc strings."""
    if not text:
        return ""
    return text.strip()

def process():
    # Load dataset from cache (already downloaded on your system)
    dataset = load_dataset("code_search_net", "python")

    Path(OUT_FILE).parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_FILE, "w", encoding="utf-8") as f_out:
        count = 0
        for split in ["train", "validation", "test"]:
            for i, record in enumerate(dataset[split]):
                code = normalize_text(record.get("func_code_string", ""))
                doc = normalize_text(record.get("func_documentation_string", ""))

                if not code or not doc:
                    continue

                clean_record = {
                    "id": f"{split}-{i}",
                    "function_name": record.get("func_name", ""),
                    "code": code,
                    "docstring": doc,
                    "source": "codesearchnet",
                    "split": split,
                    "url": record.get("func_code_url", "")
                }

                f_out.write(json.dumps(clean_record) + "\n")
                count += 1

    print(f"✅ Saved {count} records → {OUT_FILE}")

if __name__ == "__main__":
    process()
