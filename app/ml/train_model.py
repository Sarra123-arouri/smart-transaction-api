import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

# Gestion des chemins relative au fichier actuel
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(CURRENT_DIR, "..")
DATA_PATH = os.path.join(BASE_DIR, "data", "creditcard.csv")
MODEL_PATH = os.path.join(CURRENT_DIR, "fraud_model.pkl")
SCALER_PATH = os.path.join(CURRENT_DIR, "scaler.pkl")

print(f"🚀 Chargement : {DATA_PATH}")

# 1️⃣ Chargement
df = pd.read_csv(DATA_PATH)

# 2️⃣ Feature Engineering : Normalisation
scaler = StandardScaler()
# On transforme 'Amount' et 'Time' directement dans le DataFrame original
df['Amount'] = scaler.fit_transform(df[['Amount']])
df['Time'] = scaler.fit_transform(df[['Time']])

# 3️⃣ Séparation Features / Label
X = df.drop("Class", axis=1) # Contient maintenant Time et Amount scalés
y = df["Class"]

# 4️⃣ Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 5️⃣ Modèle
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10, 
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

print("⏳ Entraînement...")
model.fit(X_train, y_train)

# 6️⃣ Evaluation
print("\n📊 RAPPORT :", classification_report(y_test, model.predict(X_test)))

# 7️⃣ Sauvegarde des deux artefacts
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
print(f"✅ Modèle & Scaler sauvés dans {CURRENT_DIR}")