
import os
import json
import numpy as np
import tensorflow as tf

from tensorflow.keras.utils import load_img, img_to_array

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "plant_model.keras")
CLASS_NAMES_PATH = os.path.join(BASE_DIR,"class_names.json")

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)


def predict_plant(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)

    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array
    )

    predictions = model.predict(image_array, verbose=0)[0]
    top_indices = np.argsort(predictions)[::-1][:5]

    top_predictions = []

    for index in top_indices:
        top_predictions.append({
            "plant": class_names[index],
            "confidence": float(predictions[index])
        })

    best_index = top_indices[0]

    return {
        "plant": class_names[best_index],
        "confidence": float(predictions[best_index]),
        "top_predictions": top_predictions
    }


if __name__ == "__main__":
    image_path = input("Enter the full path of a leaf image: ").strip().strip('"')

    if not os.path.isfile(image_path):
        print("Error: Image file not found.")
    else:
        try:
            result = predict_plant(image_path)

            print("\n===== PLANT IDENTIFICATION RESULT =====")
            print("Predicted plant:", result["plant"])
            print(f"Confidence: {result['confidence'] * 100:.2f}%")
            print("\nTop 5 predictions:")

            for item in result["top_predictions"]:
                print(
                    f"{item['plant']}: "
                    f"{item['confidence'] * 100:.2f}%"
                )

        except Exception as e:
            print("Prediction failed:", e)
