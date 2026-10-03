import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "plant_info.json"


def load_plant_data():
    """Load plant information from the JSON metadata file."""
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_plant_info(plant_name):
    """Return metadata for a predicted plant name."""
    plant_data = load_plant_data()

    return plant_data.get(plant_name)


def get_all_plant_names():
    """Return all plant names available in the metadata."""
    plant_data = load_plant_data()

    return list(plant_data.keys())

def create_prediction_result(plant_name, confidence):
    """Combine a predicted plant name and confidence with its metadata."""

    plant_info = get_plant_info(plant_name)

    if plant_info is None:
        return {
            "plant": plant_name,
            "confidence": confidence,
            "error": "Plant metadata not found"
        }

    return {
        "plant": plant_name,
        "confidence": confidence,
        **plant_info
    }