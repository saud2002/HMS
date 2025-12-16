"""
Patient Model
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, CheckConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime, date
import enum

from ..database import Base

class Gender(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String(15), nullable=False)
    gender = Column(String(10), nullable=False)
    nic = Column(String(20), unique=True, nullable=False)
    registration_date = Column(Date, nullable=False, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('age > 0', name='check_age_positive'),
        Index('idx_nic', 'nic'),
        Index('idx_phone', 'phone_number'),
        Index('idx_registration_date', 'registration_date'),
        Index('idx_patient_registration', 'registration_date', 'patient_name'),
    )
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    
    def __repr__(self):
        return f"<Patient(id={self.patient_id}, name='{self.patient_name}', nic='{self.nic}')>"
    
    @property
    def full_info(self):
        return {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "age": self.age,
            "phone_number": self.phone_number,
            "gender": self.gender.value,
            "nic": self.nic,
            "registration_date": self.registration_date.isoformat(),
            "created_at": self.created_at.isoformat()
        }