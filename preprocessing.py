import os
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# ============================================================
# SETTINGS
# ============================================================

DATASET_PATH = r"c:\Users\comp\Downloads\Leaves of 48 Plants Dataset"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)


# ============================================================
# GET CLASSES
# ============================================================

classes = sorted([
    folder
    for folder in os.listdir(DATASET_PATH)
    if os.path.isdir(
        os.path.join(DATASET_PATH, folder)
    )
])

print("Number of classes:", len(classes))
print("Classes:", classes)


# ============================================================
# GET IMAGE PATHS AND LABELS
# ============================================================

images = []
labels = []

for plant in classes:

    folder = os.path.join(
        DATASET_PATH,
        plant
    )

    for file in os.listdir(folder):

        if file.lower().endswith(
            IMAGE_EXTENSIONS
        ):

            images.append(
                os.path.join(
                    folder,
                    file
                )
            )

            labels.append(plant)


print("Total images:", len(images))


# ============================================================
# TRAIN / VALIDATION / TEST SPLIT
# ============================================================

train_images, temp_images, train_labels, temp_labels = (
    train_test_split(
        images,
        labels,
        test_size=0.30,
        random_state=SEED,
        stratify=labels
    )
)

val_images, test_images, val_labels, test_labels = (
    train_test_split(
        temp_images,
        temp_labels,
        test_size=0.50,
        random_state=SEED,
        stratify=temp_labels
    )
)


print("\nDataset split:")
print("Training:", len(train_images))
print("Validation:", len(val_images))
print("Testing:", len(test_images))


# ============================================================
# CLASS MAPPING
# ============================================================

class_to_index = {
    name: index
    for index, name in enumerate(classes)
}


# ============================================================
# CREATE DATAFRAMES
# ============================================================

train_df = pd.DataFrame({
    "filename": train_images,
    "label": [
        class_to_index[label]
        for label in train_labels
    ]
})

val_df = pd.DataFrame({
    "filename": val_images,
    "label": [
        class_to_index[label]
        for label in val_labels
    ]
})

test_df = pd.DataFrame({
    "filename": test_images,
    "label": [
        class_to_index[label]
        for label in test_labels
    ]
})


# ============================================================
# TRAINING DATA AUGMENTATION
# ============================================================

train_datagen = ImageDataGenerator(

    # MobileNetV2 preprocessing
    preprocessing_function=
    tf.keras.applications.mobilenet_v2
    .preprocess_input,

    # Data augmentation
    rotation_range=20,

    width_shift_range=0.10,

    height_shift_range=0.10,

    zoom_range=0.15,

    horizontal_flip=True
)


# ============================================================
# VALIDATION AND TEST PREPROCESSING
# ============================================================

val_test_datagen = ImageDataGenerator(

    preprocessing_function=
    tf.keras.applications.mobilenet_v2
    .preprocess_input
)


# ============================================================
# TRAIN GENERATOR
# ============================================================

train_generator = train_datagen.flow_from_dataframe(

    train_df,

    x_col="filename",

    y_col="label",

    target_size=IMG_SIZE,

    batch_size=BATCH_SIZE,

    class_mode="raw",

    shuffle=True,

    seed=SEED
)


# ============================================================
# VALIDATION GENERATOR
# ============================================================

val_generator = val_test_datagen.flow_from_dataframe(

    val_df,

    x_col="filename",

    y_col="label",

    target_size=IMG_SIZE,

    batch_size=BATCH_SIZE,

    class_mode="raw",

    shuffle=False
)


# ============================================================
# TEST GENERATOR
# ============================================================

test_generator = val_test_datagen.flow_from_dataframe(

    test_df,

    x_col="filename",

    y_col="label",

    target_size=IMG_SIZE,

    batch_size=BATCH_SIZE,

    class_mode="raw",

    shuffle=False
)


# ============================================================
# FINAL INFORMATION
# ============================================================

print("\nPreprocessing completed!")

print(
    "Training batches:",
    len(train_generator)
)

print(
    "Validation batches:",
    len(val_generator)
)

print(
    "Testing batches:",
    len(test_generator)
)