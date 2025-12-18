"""
Service Model for Additional Services
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from datetime import datetime

from ..database import Base

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), default="Other", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(String(10), default="Active", nullable=False)
    
    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', price={self.price})>"