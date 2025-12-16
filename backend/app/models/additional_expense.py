"""
Additional Expense Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class AdditionalExpense(Base):
    __tablename__ = "additional_expenses"
    
    expense_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id", ondelete="CASCADE"), nullable=False)
    service_type = Column(String(50), nullable=False)
    service_description = Column(String(255), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('amount >= 0', name='check_amount_positive'),
        Index('idx_appointment', 'appointment_id'),
        Index('idx_service_type', 'service_type'),
    )
    
    # Relationships
    appointment = relationship("Appointment", back_populates="additional_expenses")
    
    def __repr__(self):
        return f"<AdditionalExpense(id={self.expense_id}, type='{self.service_type}', amount={self.amount})>"
    
    @property
    def full_info(self):
        return {
            "expense_id": self.expense_id,
            "appointment_id": self.appointment_id,
            "service_type": self.service_type,
            "service_description": self.service_description,
            "amount": float(self.amount),
            "created_at": self.created_at.isoformat()
        }