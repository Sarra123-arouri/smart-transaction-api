from fastapi import APIRouter, Depends
from app.ml.predict import predict_transaction
from app.routes.auth_route import get_current_user
from app.database.models import User
from pydantic import BaseModel

router = APIRouter(prefix="/ml", tags=["ML"])

class TransactionInput(BaseModel):
    Time: float 
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float

@router.post("/predict")
def predict(transaction: TransactionInput, current_user: User = Depends(get_current_user)):
    result = predict_transaction(transaction.dict())
    return result
