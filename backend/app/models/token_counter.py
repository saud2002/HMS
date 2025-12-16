"""
Token Counter Model
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class TokenCounter(Base):
    __tablename__ = "token_counter"
    
    counter_id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String(20), ForeignKey("doctors.doctor_id", ondelete="CASCADE"), nullable=False)
    token_date = Column(Date, nullable=False)
    last_token_number = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Constraints and Indexes
    __table_args__ = (
        Index('unique_doctor_date', 'doctor_id', 'token_date', unique=True),
        Index('idx_token_date', 'token_date'),
    )
    
    # Relationships
    doctor = relationship("Doctor", back_populates="token_counters")
    
    def __repr__(self):
        return f"<TokenCounter(doctor_id='{self.doctor_id}', date={self.token_date}, count={self.last_token_number})>"
    
    def generate_token_number(self):
        """Generate formatted token number"""
        date_str = self.token_date.strftime("%Y%m%d")
        return f"{self.doctor_id}-{date_str}-{self.last_token_number:03d}"