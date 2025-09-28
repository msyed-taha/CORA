import json

DATASETS = {
    "bugsinpy": "data/processed/json/bugsinpy_clean.jsonl",
    "codesearchnet": "data/processed/json/codesearchnet_clean.jsonl",
    "stdlib": "data/processed/json/stdlib_clean.jsonl",
}

OUT_FILE = "data/processed/json/unified_dataset.jsonl"

def merge():
    count = 0
    with open(OUT_FILE, "w", encoding="utf-8") as f_out:
        # BugsInPy → bug_fix
        with open(DATASETS["bugsinpy"], "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                record = {
                    "id": obj["id"],
                    "task": "bug_fix",
                    "buggy_code": obj["buggy_code"],
                    "fixed_code": obj["fixed_code"],
                    "description": obj.get("description", ""),
                    "source": "bugsinpy",
                }
                f_out.write(json.dumps(record) + "\n")
                count += 1

        # CodeSearchNet → doc_gen
        with open(DATASETS["codesearchnet"], "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                record = {
                    "id": obj["id"],
                    "task": "doc_gen",
                    "function_name": obj["function_name"],
                    "code": obj["code"],
                    "docstring": obj["docstring"],
                    "source": "codesearchnet",
                }
                f_out.write(json.dumps(record) + "\n")
                count += 1

        # Stdlib → doc_gen
        with open(DATASETS["stdlib"], "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                record = {
                    "id": obj["id"],
                    "task": "doc_gen",
                    "function_name": obj["function_name"],
                    "code": obj["code"],
                    "docstring": obj["docstring"],
                    "source": "stdlib",
                }
                f_out.write(json.dumps(record) + "\n")
                count += 1

    print(f"✅ Unified dataset saved → {OUT_FILE} with {count} records")

if __name__ == "__main__":
    merge()
