"""
Additional Expense Schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class AdditionalExpenseCreate(BaseModel):
    appointment_id: int = Field(..., gt=0)
    service_type: str = Field(..., min_length=1, max_length=100)
    service_description: Optional[str] = Field(None, max_length=255)
    amount: float = Field(..., ge=0)
    
    @validator('amount')
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Amount cannot be negative')
        return round(v, 2)

class AdditionalExpenseResponse(BaseModel):
    expense_id: int
    appointment_id: int
    service_type: str
    service_description: Optional[str]
    amount: float
    created_at: datetime
    
    class Config:
        from_attributes = True