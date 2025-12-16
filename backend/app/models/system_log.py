"""
System Log Model for Audit Trail
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    log_id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admin_users.admin_id", ondelete="SET NULL"), nullable=True)
    action_type = Column(String(50), nullable=False)
    table_name = Column(String(50), nullable=True)
    record_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_action_type', 'action_type'),
        Index('idx_created_at', 'created_at'),
    )
    
    # Relationships
    admin = relationship("AdminUser", back_populates="system_logs")
    
    def __repr__(self):
        return f"<SystemLog(id={self.log_id}, action='{self.action_type}', table='{self.table_name}')>"
    
    @classmethod
    def log_action(cls, db_session, admin_id: int, action: str, table: str = None, 
                   record_id: int = None, description: str = None, ip_address: str = None):
        """Create a new system log entry"""
        log_entry = cls(
            admin_id=admin_id,
            action_type=action,
            table_name=table,
            record_id=record_id,
            description=description,
            ip_address=ip_address
        )
        db_session.add(log_entry)
        db_session.commit()
        return log_entry