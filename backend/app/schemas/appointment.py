"""
Appointment Schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime

class AppointmentCreate(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: str = Field(..., min_length=1, max_length=20)
    appointment_date: date
    hospital_charges: float = Field(default=0, ge=0)
    
    @validator('appointment_date')
    def validate_appointment_date(cls, v):
        if v < date.today():
            raise ValueError('Appointment date cannot be in the past')
        return v
    
    @validator('hospital_charges')
    def validate_hospital_charges(cls, v):
        return round(v, 2)

class AppointmentResponse(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: str
    appointment_date: date
    appointment_time: datetime
    token_number: str
    doctor_charges: float
    hospital_charges: float
    status: str
    created_at: datetime
    
    # Optional related data
    patient_name: Optional[str] = None
    patient_nic: Optional[str] = None
    patient_phone: Optional[str] = None
    doctor_name: Optional[str] = None
    specialization: Optional[str] = None
    
    class Config:
        from_attributes = True

class AppointmentStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(Scheduled|Completed|Cancelled)$")