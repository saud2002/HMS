"""
User/Admin Schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class AdminCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    admin_id: int
    username: str
    full_name: str
    email: Optional[str]
    status: str
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int