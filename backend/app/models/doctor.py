"""
Doctor Model
"""
from sqlalchemy import Column, String, DateTime, Enum, Numeric, CheckConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..database import Base

class DoctorStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Doctor(Base):
    __tablename__ = "doctors"
    
    doctor_id = Column(String(20), primary_key=True)
    doctor_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    consultation_charges = Column(Numeric(10, 2), nullable=False)
    hospital_charges = Column(Numeric(10, 2), nullable=False, default=0.00)
    status = Column(String(20), default="Active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('consultation_charges >= 0', name='check_charges_positive'),
        CheckConstraint('hospital_charges >= 0', name='check_hospital_charges_positive'),
        Index('idx_specialization', 'specialization'),
        Index('idx_status', 'status'),
    )
    
    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    token_counters = relationship("TokenCounter", back_populates="doctor")
    vouchers = relationship("Voucher", back_populates="doctor")
    
    def __repr__(self):
        return f"<Doctor(id='{self.doctor_id}', name='{self.doctor_name}', spec='{self.specialization}')>"
    
    @property
    def is_active(self):
        return self.status == DoctorStatus.ACTIVE
    
    @property
    def full_info(self):
        return {
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor_name,
            "specialization": self.specialization,
            "consultation_charges": float(self.consultation_charges),
            "hospital_charges": float(self.hospital_charges),
            "status": self.status.value,
            "created_at": self.created_at.isoformat()
        }