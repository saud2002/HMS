"""
Voucher Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class VoucherBase(BaseModel):
    voucher_type: str = Field(..., description="Type of voucher (DOCTOR_PAYMENT, HOSPITAL_EXPENSE, ADJUSTMENT)")
    doctor_id: Optional[str] = Field(None, description="Doctor ID for doctor payment vouchers")
    payment_period_start: Optional[date] = Field(None, description="Start date of payment period")
    payment_period_end: Optional[date] = Field(None, description="End date of payment period")
    amount: Decimal = Field(..., gt=0, description="Voucher amount")
    description: Optional[str] = Field(None, description="Voucher description")
    voucher_date: date = Field(default_factory=date.today, description="Voucher date")

class VoucherCreate(VoucherBase):
    pass

class VoucherUpdate(BaseModel):
    voucher_type: Optional[str] = None
    doctor_id: Optional[str] = None
    payment_period_start: Optional[date] = None
    payment_period_end: Optional[date] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    voucher_date: Optional[date] = None

class VoucherResponse(VoucherBase):
    voucher_id: int
    voucher_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    doctor_name: Optional[str] = None

    class Config:
        from_attributes = True

class VoucherSummary(BaseModel):
    total_vouchers: int
    draft_count: int
    pending_approval_count: int
    approved_count: int
    paid_count: int
    rejected_count: int
    total_amount: Decimal
    pending_amount: Decimal

class DoctorPaymentSummary(BaseModel):
    doctor_id: str
    doctor_name: str
    total_consultations: int
    total_earnings: Decimal
    paid_amount: Decimal
    pending_amount: Decimal
    last_payment_date: Optional[date] = None