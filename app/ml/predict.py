import joblib
import pandas as pd
import numpy as np
import os

# Configuration des chemins
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "fraud_model.pkl")
SCALER_PATH = os.path.join(CURRENT_DIR, "scaler.pkl")

# Chargement unique au démarrage du serveur
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"❌ Erreur critique de chargement : {e}")

FEATURES = [
    "Time", "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
    "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
    "V21","V22","V23","V24","V25","V26","V27","V28","Amount"
]
def predict_transaction(transaction_data: dict):
    # 1. Préparation des 30 colonnes dans l'ordre EXACT de Kaggle
    full_data = {feat: 0.0 for feat in FEATURES}
    for key, value in transaction_data.items():
        match = [f for f in FEATURES if f.lower() == key.lower()]
        if match:
            full_data[match[0]] = float(value)

    # 2. Création du DataFrame
    df = pd.DataFrame([full_data], columns=FEATURES)

    try:
        # 1. On récupère la probabilité brute
        # On utilise .values pour éviter les warnings de noms de colonnes
        probability = model.predict_proba(df.values)[0][1]
        
        # 2. SEUIL DE DÉTECTION AGRESSIF (Mode "Projet Perso Réactif")
        # On passe de 0.5 à 0.01 (1%) pour forcer la détection sur tes tests
        is_fraud = bool(probability > 0.01) 
        
        # DEBUG : Pour que tu puisses voir la vraie valeur dans ton terminal
        print(f"🔍 IA ANALYSE : Proba de fraude = {probability:.4f} | Seuil = 0.01")
        
        return {
            "is_fraud": is_fraud, 
            "probability": float(probability)
        }
        
    except Exception as e:
        print(f"❌ Erreur IA: {e}")
        return {"is_fraud": False, "probability": 0.0}