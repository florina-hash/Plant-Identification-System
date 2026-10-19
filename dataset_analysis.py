import os
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


# ============================================================
# 1. SETTINGS
# ============================================================

# CHANGE THIS PATH to your dataset folder
DATASET_PATH = r"c:\Users\comp\Downloads\Leaves of 48 Plants Dataset"

# Results folder
RESULTS_PATH = "results"

# Supported image formats
IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

# Create results folder if it does not exist
os.makedirs(RESULTS_PATH, exist_ok=True)


# ============================================================
# 2. CHECK DATASET PATH
# ============================================================

if not os.path.exists(DATASET_PATH):

    print("ERROR: Dataset path does not exist!")
    print("Please change DATASET_PATH in this file.")
    exit()

print("=" * 60)
print("PLANT IDENTIFICATION - DATASET ANALYSIS")
print("=" * 60)

print("\nDataset path:")
print(DATASET_PATH)


# ============================================================
# 3. FIND PLANT CLASSES
# ============================================================

classes = []

for item in os.listdir(DATASET_PATH):

    full_path = os.path.join(DATASET_PATH, item)

    if os.path.isdir(full_path):

        classes.append(item)

classes = sorted(classes)

print("\n" + "=" * 60)
print("1. CLASS INFORMATION")
print("=" * 60)

print("Number of plant classes:", len(classes))

print("\nPlant classes:")

for number, plant in enumerate(classes, start=1):

    print(f"{number}. {plant}")


# ============================================================
# 4. ANALYZE ALL IMAGES
# ============================================================

all_data = []
corrupted_images = []

total_images = 0

print("\n" + "=" * 60)
print("2. ANALYZING IMAGES")
print("=" * 60)

for plant in classes:

    folder = os.path.join(
        DATASET_PATH,
        plant
    )

    for file in os.listdir(folder):

        # Check image extension
        if not file.lower().endswith(IMAGE_EXTENSIONS):
            continue

        image_path = os.path.join(
            folder,
            file
        )

        total_images += 1

        try:

            # Open image
            image = Image.open(image_path)

            # Check that image is not corrupted
            image.verify()

            # Open again after verify()
            image = Image.open(image_path)

            width, height = image.size
            image_format = image.format

            all_data.append({
                "Plant": plant,
                "Filename": file,
                "Width": width,
                "Height": height,
                "Format": image_format,
                "Status": "Valid"
            })

        except Exception as error:

            print("\nCorrupted/problematic image:")
            print(image_path)
            print("Error:", error)

            corrupted_images.append({
                "Plant": plant,
                "Filename": file,
                "Path": image_path,
                "Status": "Corrupted"
            })

            all_data.append({
                "Plant": plant,
                "Filename": file,
                "Width": None,
                "Height": None,
                "Format": None,
                "Status": "Corrupted"
            })


# ============================================================
# 5. CREATE DATAFRAME
# ============================================================

image_df = pd.DataFrame(all_data)

print("\nTotal images found:", total_images)

print(
    "Valid images:",
    len(image_df[image_df["Status"] == "Valid"])
)

print(
    "Corrupted images:",
    len(corrupted_images)
)


# ============================================================
# 6. IMAGE COUNT PER CLASS
# ============================================================

print("\n" + "=" * 60)
print("3. IMAGES PER PLANT CLASS")
print("=" * 60)

class_counts = (
    image_df[
        image_df["Status"] == "Valid"
    ]
    .groupby("Plant")
    .size()
    .reset_index(name="Image_Count")
)

print(class_counts.to_string(index=False))


# Save class counts
class_counts.to_csv(
    os.path.join(
        RESULTS_PATH,
        "class_counts.csv"
    ),
    index=False
)


# ============================================================
# 7. CLASS IMBALANCE
# ============================================================

print("\n" + "=" * 60)
print("4. CLASS IMBALANCE")
print("=" * 60)

if len(class_counts) > 0:

    maximum = class_counts["Image_Count"].max()
    minimum = class_counts["Image_Count"].min()

    maximum_class = class_counts.loc[
        class_counts["Image_Count"].idxmax(),
        "Plant"
    ]

    minimum_class = class_counts.loc[
        class_counts["Image_Count"].idxmin(),
        "Plant"
    ]

    imbalance_ratio = maximum / minimum

    print(
        f"Maximum images: {maximum} ({maximum_class})"
    )

    print(
        f"Minimum images: {minimum} ({minimum_class})"
    )

    print(
        f"Imbalance ratio: {imbalance_ratio:.2f}"
    )

    if imbalance_ratio > 2:

        print(
            "Result: Dataset shows possible class imbalance."
        )

    else:

        print(
            "Result: Dataset is relatively balanced."
        )


# ============================================================
# 8. IMAGE FORMATS
# ============================================================

print("\n" + "=" * 60)
print("5. IMAGE FORMATS")
print("=" * 60)

valid_images = image_df[
    image_df["Status"] == "Valid"
]

format_counts = valid_images["Format"].value_counts()

print(format_counts)


# Save format information
format_counts.to_csv(
    os.path.join(
        RESULTS_PATH,
        "image_formats.csv"
    )
)


# ============================================================
# 9. IMAGE DIMENSIONS
# ============================================================

print("\n" + "=" * 60)
print("6. IMAGE DIMENSIONS")
print("=" * 60)

dimension_counts = (
    valid_images
    .groupby(
        ["Width", "Height"]
    )
    .size()
    .reset_index(
        name="Image_Count"
    )
    .sort_values(
        "Image_Count",
        ascending=False
    )
)

print(
    dimension_counts.head(20).to_string(
        index=False
    )
)


# Save dimensions
dimension_counts.to_csv(
    os.path.join(
        RESULTS_PATH,
        "image_dimensions.csv"
    ),
    index=False
)


# ============================================================
# 10. CORRUPTED IMAGES
# ============================================================

print("\n" + "=" * 60)
print("7. CORRUPTED / PROBLEMATIC IMAGES")
print("=" * 60)

if len(corrupted_images) == 0:

    print("No corrupted images found.")

else:

    print(
        "Number of corrupted images:",
        len(corrupted_images)
    )

    for item in corrupted_images:

        print(
            item["Path"]
        )


# Save corrupted images
if len(corrupted_images) > 0:

    corrupted_df = pd.DataFrame(
        corrupted_images
    )

else:

    corrupted_df = pd.DataFrame(
        columns=[
            "Plant",
            "Filename",
            "Path",
            "Status"
        ]
    )

corrupted_df.to_csv(
    os.path.join(
        RESULTS_PATH,
        "corrupted_images.csv"
    ),
    index=False
)


# ============================================================
# 11. SAVE COMPLETE IMAGE ANALYSIS
# ============================================================

image_df.to_csv(
    os.path.join(
        RESULTS_PATH,
        "complete_image_analysis.csv"
    ),
    index=False
)


# ============================================================
# 12. CREATE CLASS DISTRIBUTION GRAPH
# ============================================================

print("\nCreating class distribution graph...")

plt.figure(figsize=(15, 7))

plt.bar(
    class_counts["Plant"],
    class_counts["Image_Count"]
)

plt.xlabel("Plant Class")
plt.ylabel("Number of Images")

plt.title(
    "Number of Images per Plant Class"
)

plt.xticks(
    rotation=90
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        RESULTS_PATH,
        "class_distribution.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATASET ANALYSIS COMPLETED")
print("=" * 60)

print(
    "Number of classes:",
    len(classes)
)

print(
    "Total images:",
    total_images
)

print(
    "Valid images:",
    len(valid_images)
)

print(
    "Corrupted images:",
    len(corrupted_images)
)

print("\nResults saved in:")

print(
    os.path.abspath(RESULTS_PATH)
)

print("\nGenerated files:")

print("1. class_counts.csv")
print("2. image_formats.csv")
print("3. image_dimensions.csv")
print("4. corrupted_images.csv")
print("5. complete_image_analysis.csv")
print("6. class_distribution.png")

print("\nDone!")