import json
import os

def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: '{file_path}' contains invalid JSON.")
        return []

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)