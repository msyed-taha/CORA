import os
import json

RAW_DIR = "data/raw/BugsInPy/projects"
OUT_FILE = "data/processed/json/bugsinpy.jsonl"


def parse_patch(patch_path):
    buggy, fixed = [], []
    try:
        with open(patch_path, "r", encoding="utf-8") as f:
            for line in f:
                # Skip metadata lines
                if line.startswith(("---", "+++", "@@")):
                    continue
                if line.startswith("-"):
                    buggy.append(line[1:].rstrip("\n"))
                elif line.startswith("+"):
                    fixed.append(line[1:].rstrip("\n"))
    except Exception as e:
        print(f"⚠️ Error reading patch {patch_path}: {e}")

    if not buggy and not fixed:
        print(f"⚠️ No code extracted from patch: {patch_path}")
    return "\n".join(buggy), "\n".join(fixed)


def parse_info(info_path):
    info = {}
    try:
        with open(info_path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, val = line.split(":", 1)
                    info[key.strip()] = val.strip()
    except Exception as e:
        print(f"⚠️ Error reading info {info_path}: {e}")
    return info


def main():
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    count = 0

    with open(OUT_FILE, "w", encoding="utf-8") as out:
        for project in os.listdir(RAW_DIR):
            proj_path = os.path.join(RAW_DIR, project, "bugs")
            if not os.path.isdir(proj_path):
                continue

            for bug_id in os.listdir(proj_path):
                bug_path = os.path.join(proj_path, bug_id)
                patch_path = os.path.join(bug_path, "bug_patch.txt")
                info_path = os.path.join(bug_path, "bug.info")

                if not (os.path.exists(patch_path) and os.path.exists(info_path)):
                    continue

                buggy, fixed = parse_patch(patch_path)
                info = parse_info(info_path)

                record = {
                    "project": project,
                    "bug_id": bug_id,
                    "buggy_code": buggy,
                    "fixed_code": fixed,
                    "bug_info": info,
                }

                out.write(json.dumps(record) + "\n")
                count += 1

    print(f"✅ Finished. Saved {count} bug records → {OUT_FILE}")


if __name__ == "__main__":
    main()
