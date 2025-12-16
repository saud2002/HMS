"""
Patient Schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
import re

class PatientCreate(BaseModel):
    patient_name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=0, le=150)
    phone_number: str = Field(..., min_length=10, max_length=15)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    nic: str = Field(..., min_length=9, max_length=20)
    registration_date: Optional[date] = None
    
    @validator('phone_number')
    def validate_phone(cls, v):
        # Remove any non-digit characters for validation
        digits_only = re.sub(r'\D', '', v)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must be 10-15 digits')
        return v
    
    @validator('nic')
    def validate_nic(cls, v):
        # Basic NIC validation (can be enhanced based on country)
        if not re.match(r'^[0-9]{9}[vVxX]?$|^[0-9]{12}$', v):
            raise ValueError('Invalid NIC format')
        return v.upper()

class PatientUpdate(BaseModel):
    patient_name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, gt=0, le=150)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    nic: Optional[str] = Field(None, min_length=9, max_length=20)

class PatientResponse(BaseModel):
    patient_id: int
    patient_name: str
    age: int
    phone_number: str
    gender: str
    nic: str
    registration_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True