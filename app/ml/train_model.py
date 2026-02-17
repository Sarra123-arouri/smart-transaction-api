import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Chemin vers le dataset
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # remonte d'un niveau depuis ml/
DATA_PATH = os.path.join(BASE_DIR, "data", "creditcard.csv")
print("Loading dataset from:", DATA_PATH)

# 1️⃣ Charger dataset
df = pd.read_csv(DATA_PATH)

# 2️⃣ Séparer features / label
X = df.drop("Class", axis=1)
y = df["Class"]

# 3️⃣ Train / Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 4️⃣ Modèle (gestion imbalance)
model = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# 5️⃣ Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 6️⃣ Sauvegarde modèle
MODEL_PATH = os.path.join(BASE_DIR, "ml", "fraud_model.pkl")
joblib.dump(model, MODEL_PATH)

print("✅ Model saved successfully at:", MODEL_PATH)
