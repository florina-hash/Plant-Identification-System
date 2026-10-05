import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import os

# Path to prediction results
PREDICTIONS_FILE = "../data/test_predictions.csv"

# Results folder
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Read predictions
data = pd.read_csv(PREDICTIONS_FILE)

# Get actual and predicted labels
actual = data["actual"]
predicted = data["predicted"]

# Get class names
classes = sorted(set(actual) | set(predicted))

# Create confusion matrix
cm = confusion_matrix(actual, predicted, labels=classes)

# Display confusion matrix
plt.figure(figsize=(12, 10))

plt.imshow(cm)

plt.xticks(
    range(len(classes)),
    classes,
    rotation=90
)

plt.yticks(
    range(len(classes)),
    classes
)

plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")
plt.title("Confusion Matrix")

plt.colorbar()

plt.tight_layout()

plt.savefig(
    os.path.join(RESULTS_DIR, "confusion_matrix.png")
)

plt.show()

# Classification report
report = classification_report(
    actual,
    predicted,
    target_names=classes,
    output_dict=True,
    zero_division=0
)

# Save classification report
report_df = pd.DataFrame(report).transpose()

report_df.to_csv(
    os.path.join(RESULTS_DIR, "per_class_metrics.csv")
)

print("Confusion matrix completed.")
print("\nPer-class performance:")
print(report_df)