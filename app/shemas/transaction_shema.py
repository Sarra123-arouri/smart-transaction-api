from pydantic import BaseModel
from datetime import datetime

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

    class Config:
        from_attributes = True
