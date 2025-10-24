from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import traceback
import sys

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- DEFINE THE EXPECTED MODEL COLUMNS ---
# CRITICAL: These MUST exactly match the columns and order used in X_train.
MODEL_COLUMNS = [
    # Base Features (Numerical) - Corrected based on CatBoost error: NO SPACE
    "Engine Size(L)",
    "Cylinders",
    "Fuel Consumption City (L/100 km)",
    "Fuel Consumption Hwy (L/100 km)",
    
    # Engineered Features (Numerical)
    "Fuel Consumption Comb (L/100 km)",
    "Fuel Consumption Comb (mpg)",
    
    # One-Hot Encoded Columns
    "Fuel Type Categorized_diesel", 
    "Fuel Type Categorized_ev", 
    "Fuel Type Categorized_gas", 
    "Fuel Type Categorized_petrol",
    "Vehicle Type_bike",
    "Vehicle Type_bus",
    "Vehicle Type_car",
    "Vehicle Type_truck",
    # Add any other OHE columns your model expects here 
]


# === Load your trained model ===
try:
    model = joblib.load("model/model.pkl")
    print("--- Model loaded successfully.")
except FileNotFoundError:
    print("!!! ERROR: 'model/model.pkl' not found. Ensure the path is correct.")
    model = None


# === Helper: Preprocess Input to Match Training Features (OHE) ===
def preprocess_input(data):
    
    # 1. Extract and standardize data from the request payload (using frontend keys)
    user_input = {
        # Store data under the model's required name "Engine Size(L)"
        "Engine Size(L)": float(data.get("Engine Size(L)", 0)),
        "Cylinders": float(data.get("Cylinders", 0)),
        "Fuel Consumption City (L/100 km)": float(data.get("Fuel Consumption City (L/100 km)", 0)),
        "Fuel Consumption Hwy (L/100 km)": float(data.get("Fuel Consumption Hwy (L/100 km)", 0)),
        
        # Categorical features must be lowercase to match training data before OHE
        "Fuel Type Categorized": data.get("Fuel Type", "").strip().lower(),
        "Vehicle Type": data.get("Vehicle Type", "").strip().lower()
    }
    
    # 2. Compute Combined Fuel Consumption (Feature Engineering)
    comb_l_100km = round(
        0.55 * user_input["Fuel Consumption City (L/100 km)"] +
        0.45 * user_input["Fuel Consumption Hwy (L/100 km)"], 2
    )
    user_input["Fuel Consumption Comb (L/100 km)"] = comb_l_100km
    
    # Calculate Fuel Consumption Comb (mpg)
    mpg = round(282.48 / comb_l_100km, 2) if comb_l_100km > 0 else 0
    user_input["Fuel Consumption Comb (mpg)"] = mpg

    # 3. Convert input into DataFrame
    user_input_df = pd.DataFrame([user_input])

    # 4. One-hot encode categorical features (MUST match the training process)
    try:
        user_input_df = pd.get_dummies(
            user_input_df,
            columns=["Fuel Type Categorized", "Vehicle Type"],
            prefix=["Fuel Type Categorized", "Vehicle Type"],
            drop_first=False
        )
    except KeyError as e:
        raise ValueError(f"Categorical column missing before OHE: {e}")

    # 5. Ensure the columns match training data (X_train.columns)
    final_df = pd.DataFrame(columns=MODEL_COLUMNS)
    final_df.loc[0] = 0 
    
    for col in user_input_df.columns:
        if col in final_df.columns:
            final_df.loc[0, col] = user_input_df.loc[0, col]

    # Reorder and filter columns to match the exact order of MODEL_COLUMNS
    final_df = final_df[MODEL_COLUMNS]

    return final_df


# === API Endpoint ===

@app.route("/predict-emission", methods=["POST"])
def predict_emission():
    if model is None:
        return jsonify({"error": "Model not loaded. Check server logs."}), 500
        
    try:
        data = request.get_json(force=True)
        
        if not data:
            return jsonify({"error": "No input data received or invalid JSON"}), 400

        input_df = preprocess_input(data)
        
        prediction = model.predict(input_df)

        # Returns the raw model output (g/km)
        return jsonify({"predicted_emission": float(prediction[0])})

    except Exception as e:
        print("!!! Error during prediction:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        
        return jsonify({"error": f"Internal Server Error during prediction. Check backend logs for full traceback. Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5005)