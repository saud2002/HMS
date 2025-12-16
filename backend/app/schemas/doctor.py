"""
Doctor Schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re

class DoctorCreate(BaseModel):
    doctor_id: str = Field(..., min_length=3, max_length=20)
    doctor_name: str = Field(..., min_length=2, max_length=100)
    specialization: str = Field(..., min_length=2, max_length=100)
    consultation_charges: float = Field(..., ge=0)
    
    @validator('doctor_id')
    def validate_doctor_id(cls, v):
        # Doctor ID should be alphanumeric, no spaces
        if not re.match(r'^[A-Za-z0-9]+$', v):
            raise ValueError('Doctor ID must be alphanumeric without spaces')
        return v.upper()
    
    @validator('consultation_charges')
    def validate_charges(cls, v):
        if v < 0:
            raise ValueError('Consultation charges cannot be negative')
        return round(v, 2)

class DoctorUpdate(BaseModel):
    doctor_name: Optional[str] = Field(None, min_length=2, max_length=100)
    specialization: Optional[str] = Field(None, min_length=2, max_length=100)
    consultation_charges: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(Active|Inactive)$")

class DoctorResponse(BaseModel):
    doctor_id: str
    doctor_name: str
    specialization: str
    consultation_charges: float
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True