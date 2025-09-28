import os
import ast
import json
from pathlib import Path

RAW_DIR = "data/raw/cpython/Lib"   # stdlib lives under Lib/
OUT_FILE = "data/processed/json/stdlib_clean.jsonl"

def extract_functions_from_file(file_path, module_name):
    """Parse a .py file with AST and extract functions that have docstrings."""
    results = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except Exception as e:
        # Skip files that fail to parse (C extensions, etc.)
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            if doc:  # keep only documented functions
                code = ast.get_source_segment(open(file_path).read(), node)
                results.append({
                    "function_name": node.name,
                    "code": code.strip() if code else "",
                    "docstring": doc.strip(),
                    "module": module_name
                })
    return results

def process():
    Path(OUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    count = 0

    with open(OUT_FILE, "w", encoding="utf-8") as f_out:
        for root, _, files in os.walk(RAW_DIR):
            for file in files:
                if not file.endswith(".py"):
                    continue
                file_path = os.path.join(root, file)

                # module name = relative path inside Lib/
                rel_path = os.path.relpath(file_path, RAW_DIR)
                module_name = rel_path.replace(os.sep, ".").replace(".py", "")

                functions = extract_functions_from_file(file_path, module_name)
                for i, fn in enumerate(functions):
                    record = {
                        "id": f"stdlib-{module_name}-{i}",
                        "module": module_name,
                        "function_name": fn["function_name"],
                        "code": fn["code"],
                        "docstring": fn["docstring"],
                        "source": "stdlib"
                    }
                    f_out.write(json.dumps(record) + "\n")
                    count += 1

    print(f"✅ Saved {count} stdlib functions → {OUT_FILE}")

if __name__ == "__main__":
    process()
