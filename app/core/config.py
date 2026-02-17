from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # PostgreSQL URL: postgresql://user:password@host:port/dbname
    DATABASE_URL: str = "postgresql://postgres:user1230@localhost:5432/fintech_db"
    SECRET_KEY: str = "CHANGE_THIS_TO_A_SECURE_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
