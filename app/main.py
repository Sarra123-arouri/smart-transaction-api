from fastapi import FastAPI
from app.database.db import Base, engine
from app.database import models
from app.routes.auth_route import router as auth_router
from app.routes.transaction_route import router as transaction_router
from app.routes import ml_route
from fastapi.middleware.cors import CORSMiddleware
from app.routes.fraude_route import router as fraud_router


app = FastAPI(title="Smart Transaction Anomaly Detection API")

# Crée les tables automatiquement
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(ml_route.router)
app.include_router(fraud_router)
origins = [
  
    "http://localhost:4200",    # si tu utilises le port standard ng serve
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # autorise ces frontends
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE...
    allow_headers=["*"],        # Content-Type, Authorization...
)