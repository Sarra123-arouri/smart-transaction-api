from sqlalchemy.orm import Session
import random
from sqlalchemy import func
from app.database.models import Transaction
from app.ml.predict import predict_transaction 

def create_transaction(db: Session, user_id: int, amount: float, currency: str, description: str):
    # 1. Sécurisation des entrées
    desc_safe = description.lower() if description else ""
    amount_val = float(amount)

    # 2. LOGIQUE RÉELLE : Analyse de l'historique de l'utilisateur
    # On récupère la moyenne des transactions passées de cet utilisateur
    stats = db.query(func.avg(Transaction.amount)).filter(Transaction.user_id == user_id).scalar()
    avg_history = float(stats) if stats else amount_val # Si 1ère transaction, moyenne = montant actuel

    # 3. GÉNÉRATION DES FEATURES (V1, V2, V3...)
    # V1 : Écart statistique (Z-Score simplifié)
    # Si l'utilisateur dépense d'habitude 50€ et qu'il demande 5000€, v1 devient très négatif.
    v1_score = (avg_history - amount_val) / (avg_history if avg_history > 0 else 1)
    
    # V2 : Risque lié à la devise (Ex: Si ce n'est pas la devise locale habituelle)
    v2_score = -2.0 if currency.upper() not in ["TND", "EUR"] else 0.0
    
    # V3 : Analyse sémantique de la description
    v3_score = -5.0 if any(word in desc_safe for word in ["crypto", "suspect", "hack", "transfer"]) else 0.0

    # 4. PRÉPARATION POUR L'IA (Format attendu par ton Scaler/Model)
    input_data = {
        "Amount": amount_val,
        "V1": v1_score,
        "V2": v2_score,
        "V3": v3_score,
        "Time": 0.0 # Tu pourrais calculer le temps écoulé depuis la dernière transaction ici
    }

    # 5. APPEL DE L'IA
    prediction = predict_transaction(input_data)
    is_fraud_detected = prediction.get('is_fraud', False)
    probability = prediction.get('probability', 0.0)

    mfa_code = str(random.randint(100000, 999999)) if is_fraud_detected else None

    transaction = Transaction(
        user_id=user_id,
        amount=amount_val,
        currency=currency,
        description=description,
        is_fraud=is_fraud_detected,
        fraud_probability=probability,
        verification_code=mfa_code,
        # IMPORTANT: On marque is_read=True pour que la notification 
        # n'apparaisse pas tant que le MFA n'a pas échoué
        is_read=True if is_fraud_detected else False, 
        status="PENDING_MFA" if is_fraud_detected else "APPROVED"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction

def get_all_transactions(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.id.desc()).all()