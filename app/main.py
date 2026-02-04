from fastapi import FastAPI
from app.database.db import Base, engine
from app.database import models
from app.routes.auth_route import router as auth_router

app = FastAPI(title="Smart Transaction Anomaly Detection API")

# Crée les tables automatiquement
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)