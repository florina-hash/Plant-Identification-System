PLANT LEAF IDENTIFICATION USING MACHINE LEARNING

PROJECT OVERVIEW
This project identifies plant species from leaf images using deep learning.

TECHNOLOGIES USED
1. Python
2. TensorFlow and Keras
3. MobileNetV2
4. NumPy
5. Pandas
6. Scikit-learn
7. Matplotlib

DATASET DETAILS
Total images: 4,427
Plant classes: 48
Training images: 3,098
Validation images: 664
Testing images: 665

MODEL
MobileNetV2 with transfer learning is used to classify plant leaf images.

MODEL PERFORMANCE
Test accuracy: 78.95%

FEATURES
1. Plant leaf image classification
2. Prediction confidence percentage
3. Top 5 plant predictions
4. Classification report
5. Confusion matrix
6. Dataset analysis

HOW TO RUN
1. Activate the project environment.
2. Run ml/train_model.py to train the model.
3. Run ml/evaluate_model.py to evaluate the model.
4. Run ml/predict.py to predict a plant.

RESULT
The system predicts the plant name from a leaf image and displays the confidence score.