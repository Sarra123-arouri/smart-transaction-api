from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Transaction # Assurez-vous d'avoir ce modèle

router = APIRouter(prefix="/fraud", tags=["Fraud"])
# app/api/endpoints/fraud.py

@router.get("/notifications")
def get_notifications(db: Session = Depends(get_db)):
    notifications = db.query(Transaction)\
        .filter(Transaction.is_read == False)\
        .order_by(Transaction.created_at.desc())\
        .limit(10)\
        .all()
    
    return notifications
    
@router.post("/notifications/clear")
def clear_notifications(db: Session = Depends(get_db)):
    db.query(Transaction)\
        .filter(Transaction.is_read == False)\
        .update({Transaction.is_read: True})

    db.commit()

    return {"message": "Notifications marquées comme lues"}