"""
Bill Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class BillResponse(BaseModel):
    bill_id: int
    appointment_id: int
    bill_date: date
    bill_time: datetime
    doctor_charges: float
    hospital_charges: float
    additional_expenses_total: float
    subtotal: float
    total_amount: float
    payment_status: str
    created_at: datetime
    
    # Optional related data
    token_number: Optional[str] = None
    patient_name: Optional[str] = None
    patient_nic: Optional[str] = None
    patient_phone: Optional[str] = None
    doctor_name: Optional[str] = None
    specialization: Optional[str] = None
    
    class Config:
        from_attributes = True

class PaymentStatusUpdate(BaseModel):
    payment_status: str = Field(..., pattern="^(Pending|Paid|Partial)$")