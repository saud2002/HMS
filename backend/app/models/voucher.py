"""
Voucher System Models for Doctor Payments and Hospital Finance Management
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, date
from enum import Enum

from ..database import Base

class VoucherType(str, Enum):
    DOCTOR_PAYMENT = "Doctor Payment"
    HOSPITAL_EXPENSE = "Hospital Expense"
    HOSPITAL_INCOME = "Hospital Income"
    ADJUSTMENT = "Adjustment"

class VoucherStatus(str, Enum):
    DRAFT = "Draft"
    PENDING_APPROVAL = "Pending Approval"
    APPROVED = "Approved"
    PAID = "Paid"
    REJECTED = "Rejected"

class Voucher(Base):
    __tablename__ = "vouchers"
    
    voucher_id = Column(Integer, primary_key=True, index=True)
    voucher_number = Column(String(50), unique=True, nullable=False, index=True)
    voucher_date = Column(Date, nullable=False, default=date.today)
    voucher_type = Column(SQLEnum(VoucherType), nullable=False)
    status = Column(SQLEnum(VoucherStatus), nullable=False, default=VoucherStatus.DRAFT)
    
    # Financial Details
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)
    description = Column(Text, nullable=True)
    
    # Doctor Payment Specific (nullable for other voucher types)
    doctor_id = Column(String(20), ForeignKey("doctors.doctor_id"), nullable=True)
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    
    # Approval Workflow
    created_by = Column(Integer, nullable=False, default=1)  # Admin ID
    approved_by = Column(Integer, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    paid_by = Column(Integer, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Audit Trail
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    doctor = relationship("Doctor", back_populates="vouchers")
    voucher_items = relationship("VoucherItem", back_populates="voucher", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Voucher(number='{self.voucher_number}', type='{self.voucher_type}', amount={self.total_amount})>"

class VoucherItem(Base):
    __tablename__ = "voucher_items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    voucher_id = Column(Integer, ForeignKey("vouchers.voucher_id", ondelete="CASCADE"), nullable=False)
    
    # Item Details
    description = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_amount = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    
    # Reference to source (for doctor payments, this could be appointment_id)
    reference_type = Column(String(50), nullable=True)  # "appointment", "expense", "income"
    reference_id = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    voucher = relationship("Voucher", back_populates="voucher_items")
    
    def __repr__(self):
        return f"<VoucherItem(description='{self.description}', amount={self.total_amount})>"

class DoctorPaymentSummary(Base):
    __tablename__ = "doctor_payment_summaries"
    
    summary_id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String(20), ForeignKey("doctors.doctor_id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Payment Calculations
    total_appointments = Column(Integer, nullable=False, default=0)
    total_consultation_fees = Column(Numeric(10, 2), nullable=False, default=0)
    hospital_share_percentage = Column(Numeric(5, 2), nullable=False, default=30.00)  # Hospital takes 30%
    hospital_share_amount = Column(Numeric(10, 2), nullable=False, default=0)
    doctor_share_amount = Column(Numeric(10, 2), nullable=False, default=0)
    
    # Status
    is_processed = Column(String(10), nullable=False, default="No")
    voucher_id = Column(Integer, ForeignKey("vouchers.voucher_id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    doctor = relationship("Doctor")
    voucher = relationship("Voucher")
    
    def __repr__(self):
        return f"<DoctorPaymentSummary(doctor='{self.doctor_id}', period={self.period_start}-{self.period_end}, amount={self.doctor_share_amount})>"