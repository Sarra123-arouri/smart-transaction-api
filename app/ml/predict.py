import joblib
import pandas as pd
import numpy as np
import os

# Charger le modèle
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "fraud_model.pkl")
model = joblib.load(MODEL_PATH)

FEATURES = [
    "Time",
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
    "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
    "V21","V22","V23","V24","V25","V26","V27","V28","Amount"
]

def predict_transaction(transaction_data: dict):
    # Transformer dictionnaire en DataFrame avec colonnes correctes
    data = pd.DataFrame([transaction_data], columns=FEATURES)

    prediction = model.predict(data)
    probability = model.predict_proba(data)

    return {
        "is_fraud": bool(prediction[0]),
        "fraud_probability": float(probability[0][1])
    }
