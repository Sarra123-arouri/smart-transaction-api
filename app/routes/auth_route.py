from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.shemas.user_shema import UserCreate, UserLogin, UserResponse
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.database.db import get_db
from app.database.models import User
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import verify_token 


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Mapper tous les champs du schéma vers le modèle SQLAlchemy
    new_user = User(
        email=user.email,
        username=user.username,
        nom=user.nom,
        prenom=user.prenom,
        date_naissance=user.date_naissance,
        lieu_residence=user.lieu_residence,
        adresse=user.adresse,
        telephone=user.telephone,
        hashed_password=hash_password(user.password)
        # date_creation est géré par le default=datetime.now dans le modèle DB
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # ici on peut décoder le token pour obtenir l'utilisateur
    email = verify_token(token) 
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user
@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user