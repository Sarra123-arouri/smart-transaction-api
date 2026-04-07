from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Transaction, User
from app.routes.auth_route import get_current_user # On sécurise !
from sqlalchemy import or_

router = APIRouter(prefix="/fraud", tags=["Fraud"])

@router.get("/notifications")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # On récupère les transactions marquées comme fraude 
    # ET qui ne sont pas explicitement marquées comme lues (is_read est False ou NULL)
    notifications = db.query(Transaction)\
        .filter(Transaction.is_fraud == True)\
        .filter(or_(Transaction.is_read == False, Transaction.is_read == None))\
        .order_by(Transaction.created_at.desc())\
        .limit(10)\
        .all()
    
    print(f"🔔 Notifs envoyées à {current_user.username}: {len(notifications)}")
    return notifications

@router.post("/notifications/{transaction_id}/read")
def mark_as_read(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    
    transaction.is_read = True
    db.commit()
    return {"status": "success", "message": "Notification marquée comme lue"}
@router.post("/notifications/read-all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # On cherche toutes les fraudes de l'utilisateur qui ne sont pas encore lues
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_fraud == True,
        or_(Transaction.is_read == False, Transaction.is_read == None)
    )
    
    # On les met toutes à True d'un coup
    updated_count = query.update({Transaction.is_read: True}, synchronize_session=False)
    db.commit()
    
    return {"status": "success", "count": updated_count}
@router.post("/verify-mfa")
def verify_mfa(data: dict, db: Session = Depends(get_db)):
    tx_id = data.get("transaction_id")
    user_code = data.get("code")

    transaction = db.query(Transaction).filter(Transaction.id == tx_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")

    # Vérification du code généré dans crud.py
    if transaction.verification_code == user_code:
        transaction.status = "APPROVED"
        transaction.is_fraud = False # Ce n'est plus une fraude si le code est bon
        transaction.is_read = True   # On cache la notif car c'est validé
        db.commit()
        return {"status": "success", "message": "Transaction approuvée"}
    
    raise HTTPException(status_code=400, detail="Code invalide")

# --- ✅ CORRECTION : Route de confirmation de fraude ---
@router.post("/confirm") # Retrait du /fraud/ ici car il est déjà dans le prefix du router
def confirm_fraud(data: dict, db: Session = Depends(get_db)):
    tx_id = data.get("transaction_id")
    transaction = db.query(Transaction).filter(Transaction.id == tx_id).first()
    
    if transaction:
        # On rend la fraude visible sur le dashboard (is_read = False)
        transaction.is_read = False 
        transaction.status = "FRAUD_CONFIRMED"
        db.commit()
        return {"status": "success", "message": "Fraude confirmée"}
    
    raise HTTPException(status_code=404, detail="Transaction not found")