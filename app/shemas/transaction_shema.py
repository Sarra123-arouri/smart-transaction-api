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

    class Config:
        from_attributes = True
