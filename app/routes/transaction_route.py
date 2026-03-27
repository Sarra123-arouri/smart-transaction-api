from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.shemas.transaction_shema import TransactionCreate, TransactionResponse
from app.database.models import User, Transaction
from app.services.transaction_service import create_transaction, get_all_transactions
from app.routes.auth_route import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# POST: ajouter une transaction
@router.post("/", response_model=TransactionResponse)
def add_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_transaction(
        db=db,
        user_id=current_user.id,
        amount=transaction.amount,
        currency=transaction.currency,
        description=transaction.description
    )

# GET: récupérer toutes les transactions
@router.get("/", response_model=list[TransactionResponse])
def all_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_transactions(db, current_user.id)