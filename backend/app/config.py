"""
Configuration settings for HMS
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "mysql+pymysql://root:@localhost:3306/hms"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production-hms-2024"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480  # 8 hours
    
    # Application
    app_name: str = "Hospital Management System"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]
    
    # File uploads
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    upload_dir: str = "uploads"
    
    # Pagination
    default_page_size: int = 50
    max_page_size: int = 1000
    
    # Hospital settings
    hospital_name: str = "Private Medical Center"
    hospital_address: str = "123 Medical Street, City"
    hospital_phone: str = "+94-11-1234567"
    hospital_email: str = "info@medicalcenter.lk"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Database URL with fallback
DATABASE_URL = settings.database_url

# JWT Settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes