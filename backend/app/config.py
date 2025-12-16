# ============== app/config.py ==============
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./hms.db"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:5500", "http://localhost:5500", "null"]
    
    class Config:
        env_file = ".env"

settings = Settings()


# ============== app/database.py ==============
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============== .env (create this file) ==============
# DATABASE_URL=sqlite:///./hms.db
# SECRET_KEY=your-super-secret-key-change-this
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30