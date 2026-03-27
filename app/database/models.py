from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Date
from app.database.db import Base 
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False) # Ajouté
    hashed_password = Column(String, nullable=False)
    nom = Column(String, nullable=False) # Ajouté
    prenom = Column(String, nullable=False) # Ajouté
    date_naissance = Column(Date, nullable=False) # Ajouté (type Date)
    lieu_residence = Column(String) # Ajouté
    adresse = Column(String) # Ajouté
    telephone = Column(String) # Ajouté
    date_creation = Column(DateTime, default=datetime.utcnow) # Pour le suivi
    is_active = Column(Boolean, default=True)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    description = Column(String)
    # 💡 On ajoute 'status' ou 'is_fraud' pour corriger l'erreur de tout à l'heure
    status = Column(String, default="normal") 
    is_fraud = Column(Boolean, default=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))