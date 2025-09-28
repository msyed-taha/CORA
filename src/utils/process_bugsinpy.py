import json
import os
from pathlib import Path

IN_FILE = "data/processed/json/bugsinpy.jsonl"
OUT_FILE = "data/processed/json/bugsinpy_clean.jsonl"

def normalize_code(code: str) -> str:
    """Basic cleanup of code: strip whitespace, normalize indentation."""
    if not code:
        return ""
    return code.strip()

def is_meaningful(buggy: str, fixed: str) -> bool:
    """Filter out trivial or empty changes."""
    if not buggy or not fixed:
        return False
    if buggy == fixed:  # no change
        return False
    if len(buggy) < 5 or len(fixed) < 5:  # too small
        return False
    return True

def process():
    Path(os.path.dirname(OUT_FILE)).mkdir(parents=True, exist_ok=True)

    with open(IN_FILE, "r") as f_in, open(OUT_FILE, "w") as f_out:
        kept = 0
        for line in f_in:
            record = json.loads(line)

            buggy = normalize_code(record.get("buggy_code", ""))
            fixed = normalize_code(record.get("fixed_code", ""))

            if not is_meaningful(buggy, fixed):
                continue

            clean_record = {
                "id": f"{record['project']}-{record['bug_id']}",
                "project": record["project"],
                "bug_id": record["bug_id"],
                "buggy_code": buggy,
                "fixed_code": fixed,
                "description": record.get("bug_info", {}).get("description", "")
            }

            f_out.write(json.dumps(clean_record) + "\n")
            kept += 1

    print(f"✅ Processed dataset saved to {OUT_FILE}")
    print(f"   Records kept: {kept}")

if __name__ == "__main__":
    process()
