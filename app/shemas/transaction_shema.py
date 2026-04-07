from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import Column, Boolean



class TransactionCreate(BaseModel):
    amount: float
    currency: str
    description: str | None = None

class TransactionResponse(BaseModel):
    id: int
    amount: float
    currency: str
    description: str | None
    created_at: datetime

    is_read : bool
    is_fraud: bool            # Pour que le badge passe au rouge
    fraud_probability: float  # Pour afficher l'indice de risque (%)
    status: str | None


    class Config:
        from_attributes = True
