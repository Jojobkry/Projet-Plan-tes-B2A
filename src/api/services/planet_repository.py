# services/planet_repository.py
import json
from pathlib import Path

def save_json(file_path, data):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Sauvegardé {len(data)} entrées dans {file_path}")

def save_raw_planets(raw_planets, file_path="data/raw/raw_planets.json"):
    save_json(file_path, raw_planets)

def save_cleaned_planets(cleaned_planets, file_path="data/cleaned/cleaned_planets.json"):
    save_json(file_path, cleaned_planets)
