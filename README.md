"# Smart Transaction Anomaly Detection API

API pour détecter les transactions frauduleuses à l'aide d'un modèle de machine learning (Random Forest).

---

##  Installation

1. **Cloner le dépôt**
git clone https://github.com/Sarra123-arouri/smart-transaction-api.git
cd smart-transaction-api

2. **Créer un environnement virtuel**
python -m venv fintech

3. **Activer l'environnement**
# Windows
fintech\Scripts\activate
# Mac/Linux
source fintech/bin/activate

4. **Installer les dépendances**
pip install -r app/requirements.txt

---

##  Organisation du projet

app/
├── data/                 # Contient le dataset local (non inclus dans le repo)
├── ml/                   # Scripts ML et modèles sauvegardés (exclus du repo)
├── routes/               # Routes FastAPI
├── services/             # Logique métier
├── database/             # Modèles et configuration DB
├── shemas/               # Pydantic schemas
└── main.py               # Point d'entrée de l'application

> ⚠️ Le dataset creditcard.csv et le modèle fraud_model.pkl **ne sont pas inclus** dans le dépôt.

---

## Utilisation

1. **Lancer le serveur**
uvicorn app.main:app --reload

---

## Liens

- Dataset : https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

