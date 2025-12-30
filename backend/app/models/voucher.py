"""
Voucher Model for Doctor Payments and Hospital Expenses
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, Index, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
import enum

from ..database import Base

class VoucherType(str, enum.Enum):
    DOCTOR_PAYMENT = "DOCTOR_PAYMENT"
    HOSPITAL_EXPENSE = "HOSPITAL_EXPENSE"
    ADJUSTMENT = "ADJUSTMENT"

class VoucherStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    PAID = "PAID"
    REJECTED = "REJECTED"

class Voucher(Base):
    __tablename__ = "vouchers"
    
    voucher_id = Column(Integer, primary_key=True, index=True)
    voucher_number = Column(String(50), unique=True, nullable=False, index=True)
    voucher_type = Column(String(20), nullable=False)
    status = Column(String(20), default="DRAFT", nullable=False)
    
    # Doctor payment specific fields
    doctor_id = Column(String(20), ForeignKey("doctors.doctor_id", ondelete="RESTRICT"), nullable=True)
    payment_period_start = Column(Date, nullable=True)
    payment_period_end = Column(Date, nullable=True)
    
    # Financial fields
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    
    # Dates
    voucher_date = Column(Date, nullable=False, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Workflow fields
    created_by = Column(Integer, ForeignKey("admin_users.admin_id", ondelete="SET NULL"), nullable=True)
    approved_by = Column(Integer, ForeignKey("admin_users.admin_id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_voucher_type', 'voucher_type'),
        Index('idx_voucher_status', 'status'),
        Index('idx_voucher_date', 'voucher_date'),
        Index('idx_doctor_payment', 'doctor_id', 'voucher_type'),
    )
    
    # Relationships
    doctor = relationship("Doctor", back_populates="vouchers")
    creator = relationship("AdminUser", foreign_keys=[created_by], back_populates="created_vouchers")
    approver = relationship("AdminUser", foreign_keys=[approved_by], back_populates="approved_vouchers")
    
    def __repr__(self):
        return f"<Voucher(id={self.voucher_id}, number='{self.voucher_number}', type='{self.voucher_type}', amount={self.amount})>"
    
    @property
    def is_draft(self):
        return self.status == VoucherStatus.DRAFT
    
    @property
    def is_pending_approval(self):
        return self.status == VoucherStatus.PENDING_APPROVAL
    
    @property
    def is_approved(self):
        return self.status == VoucherStatus.APPROVED
    
    @property
    def is_paid(self):
        return self.status == VoucherStatus.PAID
    
    @property
    def is_rejected(self):
        return self.status == VoucherStatus.REJECTED
    
    @property
    def can_be_submitted(self):
        return self.status == VoucherStatus.DRAFT
    
    @property
    def can_be_approved(self):
        return self.status == VoucherStatus.PENDING_APPROVAL
    
    @property
    def can_be_paid(self):
        return self.status == VoucherStatus.APPROVED
    
    @property
    def full_info(self):
        return {
            "voucher_id": self.voucher_id,
            "voucher_number": self.voucher_number,
            "voucher_type": self.voucher_type,
            "status": self.status,
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor.doctor_name if self.doctor else None,
            "payment_period_start": self.payment_period_start.isoformat() if self.payment_period_start else None,
            "payment_period_end": self.payment_period_end.isoformat() if self.payment_period_end else None,
            "amount": float(self.amount),
            "description": self.description,
            "voucher_date": self.voucher_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_by": self.created_by,
            "approved_by": self.approved_by
        }