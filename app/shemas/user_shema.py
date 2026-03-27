from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str
    nom: str
    prenom: str
    date_naissance: date
    lieu_residence: str
    adresse: str
    telephone: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    date_creation: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True  # Remplace orm_mode = True dans Pydantic v2