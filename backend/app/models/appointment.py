"""
Appointment Model
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..database import Base

class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Appointment(Base):
    __tablename__ = "appointments"
    
    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="RESTRICT"), nullable=False)
    doctor_id = Column(String(20), ForeignKey("doctors.doctor_id", ondelete="RESTRICT"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    token_number = Column(String(50), unique=True, nullable=False)
    doctor_charges = Column(Numeric(10, 2), nullable=False)
    hospital_charges = Column(Numeric(10, 2), nullable=False, default=0)
    status = Column(String(20), default="Scheduled", nullable=False)
    created_by = Column(Integer, ForeignKey("admin_users.admin_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_appointment_date', 'appointment_date'),
        Index('idx_patient', 'patient_id'),
        Index('idx_doctor', 'doctor_id'),
        Index('idx_token', 'token_number'),
        Index('idx_appointment_doctor_date', 'doctor_id', 'appointment_date'),
    )
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    creator = relationship("AdminUser", foreign_keys=[created_by], back_populates="created_appointments")
    bill = relationship("Bill", back_populates="appointment", uselist=False)
    additional_expenses = relationship("AdditionalExpense", back_populates="appointment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Appointment(id={self.appointment_id}, token='{self.token_number}', date={self.appointment_date})>"
    
    @property
    def total_charges(self):
        """Calculate total charges including additional expenses"""
        additional_total = sum(expense.amount for expense in self.additional_expenses)
        return float(self.doctor_charges) + float(self.hospital_charges) + float(additional_total)
    
    @property
    def full_info(self):
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_date": self.appointment_date.isoformat(),
            "appointment_time": self.appointment_time.isoformat(),
            "token_number": self.token_number,
            "doctor_charges": float(self.doctor_charges),
            "hospital_charges": float(self.hospital_charges),
            "status": self.status.value,
            "patient_name": self.patient.patient_name if self.patient else None,
            "doctor_name": self.doctor.doctor_name if self.doctor else None,
            "specialization": self.doctor.specialization if self.doctor else None,
            "total_charges": self.total_charges
        }