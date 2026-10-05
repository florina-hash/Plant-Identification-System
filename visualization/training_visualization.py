import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to training history
HISTORY_FILE = "../data/history.csv"

# Create results folder
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Read training history
history = pd.read_csv(HISTORY_FILE)

# Display available columns
print("Training history:")
print(history.head())

# Training and validation accuracy
plt.figure(figsize=(10, 6))

plt.plot(history["epoch"], history["accuracy"], label="Training Accuracy")
plt.plot(history["epoch"], history["val_accuracy"], label="Validation Accuracy")

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training and Validation Accuracy")

plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(RESULTS_DIR, "training_accuracy.png")
)

plt.show()


# Training and validation loss
plt.figure(figsize=(10, 6))

plt.plot(history["epoch"], history["loss"], label="Training Loss")
plt.plot(history["epoch"], history["val_loss"], label="Validation Loss")

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training and Validation Loss")

plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(RESULTS_DIR, "training_loss.png")
)

plt.show()

print("Training visualization completed.")