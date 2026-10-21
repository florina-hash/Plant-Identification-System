# Plant Identification backend handoff for Anti-Gravity

## Backend interface
Import this function from the project root:

```python
from plant_backend import identify_plant
result = identify_plant(uploaded_image)
```

`uploaded_image` can be a Streamlit `UploadedFile`, a file path, bytes, or a PIL image.

The returned dictionary has:
- `success`: whether metadata was found
- `plant`: predicted plant class
- `confidence`: confidence as a decimal from 0 to 1
- `top_predictions`: ranked list of plant names and confidence scores
- `metadata`: metadata dictionary containing fields such as scientific name, family, description, and uses
- `warning`: optional uncertainty or missing-metadata message

For a readiness check:
```python
from plant_backend import check_backend
print(check_backend())
```

## Expected files
Keep these files together in the project root:
- `plant_backend.py` (included in this handoff)
- `plant_model.keras` (existing project file; not included because it is the model asset)
- `class_names.json` (existing project file)
- `data/plant_info.json` (existing metadata file)

## Important findings from the current project
- `class_names.json` contains 48 alphabetically sorted labels.
- `preprocessing.py` also sorts the dataset folder names before creating integer labels. This is consistent **if this exact class order was used to train the existing model**.
- Training and prediction use MobileNetV2 `preprocess_input`, which is consistent.
- `train_model.py` saves outputs under a parent-level `models` folder, while the current prediction assets are in the project root. Do not retrain or overwrite the current model as part of UI integration.
- The dataset path currently hard-coded in `preprocessing.py` does not exist on the current computer. This blocks rerunning training until that path is corrected, but it does not prevent inference with the existing model.
- A successful prediction/metadata lookup proves the code runs; it does **not** prove that the model identifies every plant correctly. Validate with several known leaf images when time permits.

## Dependency note
This module uses TensorFlow, NumPy, and Pillow. Do not reinstall them if they already import successfully in the project's virtual environment.
