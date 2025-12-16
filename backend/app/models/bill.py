"""
Bill Model
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, date

from ..database import Base

class Bill(Base):
    __tablename__ = "bills"
    
    bill_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id", ondelete="RESTRICT"), unique=True, nullable=False)
    bill_date = Column(Date, nullable=False, default=date.today)
    bill_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    doctor_charges = Column(Numeric(10, 2), nullable=False)
    hospital_charges = Column(Numeric(10, 2), nullable=False)
    additional_expenses_total = Column(Numeric(10, 2), nullable=False, default=0)
    subtotal = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String(20), default="Pending", nullable=False)
    created_by = Column(Integer, ForeignKey("admin_users.admin_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_bill_date', 'bill_date'),
        Index('idx_payment_status', 'payment_status'),
        Index('idx_bill_date_status', 'bill_date', 'payment_status'),
    )
    
    # Relationships
    appointment = relationship("Appointment", back_populates="bill")
    creator = relationship("AdminUser", foreign_keys=[created_by], back_populates="created_bills")
    
    def __repr__(self):
        return f"<Bill(id={self.bill_id}, appointment_id={self.appointment_id}, total={self.total_amount})>"
    
    @property
    def is_paid(self):
        return self.payment_status == "Paid"
    
    @property
    def is_pending(self):
        return self.payment_status == "Pending"
    
    @property
    def full_info(self):
        return {
            "bill_id": self.bill_id,
            "appointment_id": self.appointment_id,
            "bill_date": self.bill_date.isoformat(),
            "bill_time": self.bill_time.isoformat(),
            "doctor_charges": float(self.doctor_charges),
            "hospital_charges": float(self.hospital_charges),
            "additional_expenses_total": float(self.additional_expenses_total),
            "subtotal": float(self.subtotal),
            "total_amount": float(self.total_amount),
            "payment_status": self.payment_status,
            "created_at": self.created_at.isoformat()
        }