from sqlalchemy.orm import Session
from app.database.models import Transaction

def create_transaction(db: Session, user_id: int, amount: float, currency: str, description: str):
    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        currency=currency,
        description=description
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
