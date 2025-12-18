"""
Service Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    category: str = Field(default="Other", max_length=50)

class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = Field(None, max_length=50)

class ServiceResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    category: str
    created_at: datetime
    updated_at: datetime
    is_active: str
    
    class Config:
        from_attributes = True