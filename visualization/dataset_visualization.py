import os
import matplotlib.pyplot as plt

# Dataset folder (always the "data" folder next to the visualization folder)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(SCRIPT_DIR, "..", "data")
print("Looking for dataset in:", os.path.abspath(DATASET_PATH))

# Image extensions
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# Count images in each class
class_counts = {}

for class_name in os.listdir(DATASET_PATH):
    class_path = os.path.join(DATASET_PATH, class_name)

    if os.path.isdir(class_path):
        count = 0

        for root, dirs, files in os.walk(class_path):
            for file in files:
                if file.lower().endswith(IMAGE_EXTENSIONS):
                    count += 1

        if count > 0:
            class_counts[class_name] = count

# Display results
print("Number of images in each plant class:")

for class_name, count in class_counts.items():
    print(class_name, ":", count)

# Create bar chart
plt.figure(figsize=(12, 6))

plt.bar(class_counts.keys(), class_counts.values())

plt.xlabel("Plant Classes")
plt.ylabel("Number of Images")
plt.title("Number of Images in Each Plant Class")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.show()