import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os

# File containing prediction results
PREDICTIONS_FILE = "../data/test_predictions.csv"

# Folder to save results
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Read prediction data
data = pd.read_csv(PREDICTIONS_FILE)

# Select only incorrect predictions
wrong_predictions = data[
    data["actual"] != data["predicted"]
]

print("Number of misclassified images:",
      len(wrong_predictions))

# Save misclassification details
wrong_predictions.to_csv(
    os.path.join(
        RESULTS_DIR,
        "misclassified_images.csv"
    ),
    index=False
)

# Display first few misclassified images
num_images = min(12, len(wrong_predictions))

if num_images > 0:

    fig, axes = plt.subplots(
        3, 4,
        figsize=(12, 10)
    )

    axes = axes.flatten()

    for i in range(num_images):

        row = wrong_predictions.iloc[i]

        image_path = row["image_path"]

        try:
            image = Image.open(image_path)

            axes[i].imshow(image)
            axes[i].set_title(
                f"Actual: {row['actual']}\n"
                f"Predicted: {row['predicted']}"
            )
            axes[i].axis("off")

        except Exception as e:

            axes[i].text(
                0.5,
                0.5,
                "Image not found"
            )

            axes[i].axis("off")

    # Hide unused plots
    for i in range(num_images, len(axes)):
        axes[i].axis("off")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            RESULTS_DIR,
            "misclassified_images.png"
        )
    )

    plt.show()

else:

    print("No misclassified images found.")

print("Misclassification analysis completed.")