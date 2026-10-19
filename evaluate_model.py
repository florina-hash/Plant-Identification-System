
import os
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from preprocessing import test_generator, classes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "plant_model.keras")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

print("Loading trained plant identification model...")
model = tf.keras.models.load_model(MODEL_PATH)

print("Evaluating test images...")
test_generator.reset()
probabilities = model.predict(test_generator, verbose=1)

y_pred = np.argmax(probabilities, axis=1)
y_true = np.asarray(test_generator.labels, dtype=int)

accuracy = accuracy_score(y_true, y_pred)

print("\n========== MODEL EVALUATION ==========")
print(f"Test Accuracy: {accuracy * 100:.2f}%")

report = classification_report(
    y_true,
    y_pred,
    labels=list(range(len(classes))),
    target_names=classes,
    zero_division=0
)

print("\nClassification Report:")
print(report)

with open(os.path.join(RESULTS_DIR, "classification_report.txt"), "w",
          encoding="utf-8") as f:
    f.write(f"Test Accuracy: {accuracy * 100:.2f}%\n\n")
    f.write(report)

cm = confusion_matrix(y_true, y_pred, labels=list(range(len(classes))))
pd.DataFrame(cm, index=classes, columns=classes).to_csv(
    os.path.join(RESULTS_DIR, "confusion_matrix.csv")
)

print("\nEvaluation completed!")
print("Results saved in:", RESULTS_DIR)
