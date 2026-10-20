from predict import predict_plant
from plant_info.lookup import create_prediction_result

# Change this to the path of an actual leaf image on your laptop.
IMAGE_PATH = r"C:\Users\Asus\Pictures\Screenshots\Screenshot 2026-10-20 120532.png"

try:
    # 1. Run the ML prediction
    prediction = predict_plant(IMAGE_PATH)

    print("\n=== ML PREDICTION ===")
    print("Plant:", prediction["plant"])
    print(f"Confidence: {prediction['confidence']:.2%}")
    print("Top predictions:", prediction["top_predictions"])

    # 2. Retrieve metadata for the predicted plant
    result = create_prediction_result(
        prediction["plant"],
        prediction["confidence"]
    )

    print("\n=== INTEGRATED RESULT ===")
    for key, value in result.items():
        print(f"{key}: {value}")

    # 3. Check whether metadata was found
    if "error" in result:
        print("\nINTEGRATION WARNING:", result["error"])
    else:
        print("\nSUCCESS: Prediction and metadata integration works!")

except Exception as error:
    print("\nTEST FAILED:", error)