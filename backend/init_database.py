#!/usr/bin/env python3
"""
Database Initialization Script for HMS
Run this script to set up the database with proper schema, views, and procedures
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import create_database_schema, test_connection, engine
from app.config import settings
from app.models import *

def create_sample_data():
    """Create sample data for testing"""
    from app.database import SessionLocal
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db = SessionLocal()
    
    try:
        # Create admin user if not exists
        admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if not admin:
            from app.models.user import UserStatus
            admin = AdminUser(
                username="admin",
                password_hash=pwd_context.hash("admin123"),
                full_name="System Administrator",
                email="admin@hospital.com",
                status=UserStatus.ACTIVE
            )
            db.add(admin)
            print("✅ Created default admin user (username: admin, password: admin123)")
        
        # Create sample doctor if not exists
        doctor = db.query(Doctor).filter(Doctor.doctor_id == "DOC001").first()
        if not doctor:
            from app.models.doctor import DoctorStatus
            doctor = Doctor(
                doctor_id="DOC001",
                doctor_name="Dr. John Smith",
                specialization="General Medicine",
                consultation_charges=2500.00,
                status=DoctorStatus.ACTIVE
            )
            db.add(doctor)
            print("✅ Created sample doctor (DOC001)")
        
        # Create sample patient if not exists
        patient = db.query(Patient).filter(Patient.nic == "123456789V").first()
        if not patient:
            from datetime import date
            from app.models.patient import Gender
            patient = Patient(
                patient_name="John Doe",
                age=35,
                phone_number="0771234567",
                gender=Gender.MALE,
                nic="123456789V",
                registration_date=date.today()
            )
            db.add(patient)
            print("✅ Created sample patient")
        
        db.commit()
        print("✅ Sample data created successfully")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("🏥 HMS Database Initialization")
    print("=" * 50)
    
    # Test connection
    print("1. Testing database connection...")
    if not test_connection():
        print("❌ Database connection failed!")
        print("Please check your database configuration in config.py")
        return False
    print("✅ Database connection successful")
    
    # Create schema
    print("\n2. Creating database schema...")
    try:
        create_database_schema()
        print("✅ Database schema created successfully")
    except Exception as e:
        print(f"❌ Schema creation failed: {e}")
        return False
    
    # Create sample data
    print("\n3. Creating sample data...")
    create_sample_data()
    
    print("\n🎉 Database initialization completed!")
    print("\nDefault login credentials:")
    print("Username: admin")
    print("Password: admin123")
    print("\nYou can now start the application with:")
    print("uvicorn app.main:app --reload --port 8000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)