import json
from pathlib import Path

def write_json(file_path, data):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
