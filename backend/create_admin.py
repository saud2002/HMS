#!/usr/bin/env python3
"""
Create Admin User - Simple script to create admin user
"""
import sys
sys.path.append('app')

from app.database import SessionLocal
from app.models.user import AdminUser, UserStatus
from passlib.context import CryptContext

def create_admin():
    """Create admin user"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db = SessionLocal()
    
    try:
        from sqlalchemy import text
        
        # Check if admin exists
        existing = db.execute(text("SELECT * FROM admin_users WHERE username = 'admin'")).fetchone()
        
        if existing:
            print("✅ Admin user already exists")
            return True
        
        # Create admin user directly with SQL to avoid enum issues
        db.execute(text("""
            INSERT INTO admin_users (username, password_hash, full_name, email, status)
            VALUES (:username, :password_hash, :full_name, :email, :status)
        """), {
            'username': 'admin',
            'password_hash': pwd_context.hash('admin123'),
            'full_name': 'System Administrator',
            'email': 'admin@hospital.com',
            'status': 'Active'
        })
        
        db.commit()
        print("✅ Admin user created successfully")
        print("   Username: admin")
        print("   Password: admin123")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def create_sample_doctor():
    """Create sample doctor"""
    db = SessionLocal()
    
    try:
        from sqlalchemy import text
        
        # Check if doctor exists
        existing = db.execute(text("SELECT * FROM doctors WHERE doctor_id = 'DOC001'")).fetchone()
        
        if existing:
            print("✅ Sample doctor already exists")
            return True
        
        # Create doctor directly with SQL
        db.execute(text("""
            INSERT INTO doctors (doctor_id, doctor_name, specialization, consultation_charges, status)
            VALUES (:doctor_id, :doctor_name, :specialization, :consultation_charges, :status)
        """), {
            'doctor_id': 'DOC001',
            'doctor_name': 'Dr. John Smith',
            'specialization': 'General Medicine',
            'consultation_charges': 2500.00,
            'status': 'Active'
        })
        
        db.commit()
        print("✅ Sample doctor created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating doctor: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """Main function"""
    print("🏥 Creating HMS Admin User")
    print("=" * 30)
    
    success1 = create_admin()
    success2 = create_sample_doctor()
    
    if success1 and success2:
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 You can now:")
        print("1. Start the server: python start.py")
        print("2. Login with admin/admin123")
        return True
    else:
        print("\n❌ Setup failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)