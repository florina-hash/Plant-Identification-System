
import os
import json
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = (224, 224)
EPOCHS = 5

# Import generators from preprocessing.py
from preprocessing import (
    train_generator,
    val_generator,
    test_generator,
    classes
)

print("\nStarting Plant Identification model training...")
print("Number of plant classes:", len(classes))

# Save class names in the correct label order
class_names = list(classes)

with open(os.path.join(MODEL_DIR, "class_names.json"), "w", encoding="utf-8") as f:
    json.dump(class_names, f, indent=2)

# Load pretrained MobileNetV2
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)
base_model.trainable = False

# Build classification model
inputs = layers.Input(shape=(224, 224, 3))
x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(len(class_names), activation="softmax")(x)

model = models.Model(inputs, outputs)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Train model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# Save trained model
model_path = os.path.join(MODEL_DIR, "plant_model.keras")
model.save(model_path)

print("\nTraining completed successfully!")
print("Model saved at:", model_path)
print("Class names saved successfully.")
