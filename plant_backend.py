"""
Plant Identification backend for the Plant Identification System.

Expected project layout:
    plant_model.keras
    class_names.json
    data/plant_info.json
    plant_backend.py

The function identify_plant(image) accepts a file path, a PIL image, bytes,
or a file-like object (including Streamlit's UploadedFile).
"""
from functools import lru_cache
#lru_cache auto saves function results and discards old unused ones to speed future runs witout repeating work
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "plant_model.keras"
CLASS_NAMES_PATH = BASE_DIR / "class_names.json"
METADATA_PATH = BASE_DIR / "data" / "plant_info.json"
IMG_SIZE = (224, 224)


@lru_cache(maxsize=1)
def _load_assets():
    """Load the model and supporting JSON files once per Python process."""
    for path in (MODEL_PATH, CLASS_NAMES_PATH, METADATA_PATH):
        if not path.is_file():
            raise FileNotFoundError(f"Required project file not found: {path}")

    model = tf.keras.models.load_model(MODEL_PATH)

    with CLASS_NAMES_PATH.open("r", encoding="utf-8") as f:
        class_names = json.load(f)

    with METADATA_PATH.open("r", encoding="utf-8") as f:
        plant_info = json.load(f)

    if not isinstance(class_names, list) or not class_names:
        raise ValueError("class_names.json must contain a non-empty JSON list.")

    output_shape = model.output_shape
    output_count = output_shape[-1] if isinstance(output_shape, tuple) else None
    if output_count is not None and output_count != len(class_names):
        raise ValueError(
            f"Model has {output_count} outputs but class_names.json has "
            f"{len(class_names)} labels. Do not use mismatched model/labels."
        )

    return model, class_names, plant_info


def _open_image(image):
    """Convert a path, PIL image, bytes, or file-like upload into RGB PIL image."""
    if isinstance(image, Image.Image):
        img = image
    elif isinstance(image, (bytes, bytearray)):
        from io import BytesIO
        img = Image.open(BytesIO(image))
    else:
        # Streamlit UploadedFile and most file-like objects support seek().
        if hasattr(image, "seek"):
            image.seek(0)
        img = Image.open(image)
    return img.convert("RGB")


def _find_metadata(plant_name, plant_info):
    """Exact match first, then case-insensitive match for small naming differences."""
    if plant_name in plant_info:
        return plant_info[plant_name]
    wanted = plant_name.strip().casefold()
    for key, value in plant_info.items():
        if str(key).strip().casefold() == wanted:
            return value
    return None


def identify_plant(image, top_k=5):
    """
    Identify a plant leaf and return prediction plus metadata.

    Returns:
        {
          "success": bool,
          "plant": str,
          "confidence": float,            # 0.0 to 1.0
          "top_predictions": [{"plant": str, "confidence": float}, ...],
          "metadata": dict | None,
          "warning": str | None
        }
    """
    model, class_names, plant_info = _load_assets()
    img = _open_image(image).resize(IMG_SIZE)

    image_array = np.asarray(img, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)

    # Must match the MobileNetV2 preprocessing used during training.
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)

    scores = np.asarray(model.predict(image_array, verbose=0))[0]
    if scores.ndim != 1 or len(scores) != len(class_names):
        raise ValueError(
            f"Prediction output has {len(scores)} scores but there are "
            f"{len(class_names)} class labels."
        )

    k = max(1, min(int(top_k), len(class_names)))
    indices = np.argsort(scores)[::-1][:k]
    top_predictions = [
        {"plant": str(class_names[int(i)]), "confidence": float(scores[int(i)])}
        for i in indices
    ]

    best = top_predictions[0]
    metadata = _find_metadata(best["plant"], plant_info)
    warning = None
    if metadata is None:
        warning = (
            f"No metadata entry found for predicted class '{best['plant']}'. "
            "Check the plant names in data/plant_info.json."
        )
    elif best["confidence"] < 0.50:
        warning = (
            "The model is uncertain about this image. Treat the prediction as "
            "a suggestion and compare the other top predictions."
        )

    return {
        "success": metadata is not None,
        "plant": best["plant"],
        "confidence": best["confidence"],
        "top_predictions": top_predictions,
        "metadata": metadata,
        "warning": warning,
    }


def check_backend():
    """Return a quick readiness report without running image inference."""
    model, class_names, plant_info = _load_assets()
    return {
        "model_path": str(MODEL_PATH),
        "class_count": len(class_names),
        "model_output_count": int(model.output_shape[-1]),
        "metadata_count": len(plant_info),
        "missing_metadata_classes": [
            name for name in class_names if _find_metadata(name, plant_info) is None
        ],
    }


""""""