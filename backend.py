import json
from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_FILE = BASE_DIR / "loan_default_model.pkl"
FEATURE_FILE = BASE_DIR / "loan_default_features.json"


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_FILE)


# ============================================================
# LOAD FEATURES
# ============================================================

with open(FEATURE_FILE, "r", encoding="utf-8") as file:
    feature_info = json.load(file)

FEATURES = feature_info["features"]


# ============================================================
# VALIDATE INPUT
# ============================================================

def validate_input(input_data):

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in input_data
    ]

    if missing_features:
        raise ValueError(
            "Missing features: "
            + ", ".join(missing_features)
        )


# ============================================================
# PREDICTION
# ============================================================

def predict_loan(input_data):

    # Validate input
    validate_input(input_data)

    # Create dataframe in exact feature order
    input_df = pd.DataFrame(
        [[input_data[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    # Prediction
    prediction = model.predict(input_df)[0]

    # Probability
    probability = None

    if hasattr(model, "predict_proba"):
        probability = float(
            model.predict_proba(input_df)[0][1]
        )

    # Convert prediction
    if int(prediction) == 1:
        result = "DEFAULT"
    else:
        result = "NO DEFAULT"

    return result, probability