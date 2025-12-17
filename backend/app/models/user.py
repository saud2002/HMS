"""
Admin User Model
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    admin_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    status = Column(String(20), default="Active", nullable=False)
    
    # Relationships
    created_appointments = relationship("Appointment", foreign_keys="[Appointment.created_by]", back_populates="creator")
    created_bills = relationship("Bill", foreign_keys="[Bill.created_by]", back_populates="creator")
    system_logs = relationship("SystemLog", back_populates="admin")
    
    def __repr__(self):
        return f"<AdminUser(id={self.admin_id}, username='{self.username}', name='{self.full_name}')>"