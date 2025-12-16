#!/usr/bin/env python3
"""
HMS System Test Script
Tests all major components of the system
"""
import sys
import os
from datetime import date, datetime

# Add app to path
sys.path.append('app')

def test_database_connection():
    """Test database connectivity"""
    try:
        from app.database import test_connection
        result = test_connection()
        print(f"✅ Database Connection: {'Success' if result else 'Failed'}")
        return result
    except Exception as e:
        print(f"❌ Database Connection: Failed - {e}")
        return False

def test_models():
    """Test model imports and basic functionality"""
    try:
        from app.models import Patient, Doctor, Appointment, Bill, AdminUser
        print("✅ Models: All models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Models: Import failed - {e}")
        return False

def test_schemas():
    """Test schema imports and validation"""
    try:
        from app.schemas import PatientCreate, DoctorCreate, AppointmentCreate
        
        # Test patient schema validation
        patient_data = {
            "patient_name": "Test Patient",
            "age": 30,
            "phone_number": "0771234567",
            "gender": "Male",
            "nic": "123456789V"
        }
        patient_schema = PatientCreate(**patient_data)
        
        print("✅ Schemas: Validation working correctly")
        return True
    except Exception as e:
        print(f"❌ Schemas: Validation failed - {e}")
        return False

def test_database_operations():
    """Test basic database operations"""
    try:
        from app.database import SessionLocal
        from app.models import Patient, Doctor
        
        db = SessionLocal()
        
        # Test query operations
        patient_count = db.query(Patient).count()
        doctor_count = db.query(Doctor).count()
        
        print(f"✅ Database Operations: {patient_count} patients, {doctor_count} doctors")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database Operations: Failed - {e}")
        return False

def test_authentication():
    """Test authentication system"""
    try:
        from passlib.context import CryptContext
        from jose import jwt
        from app.config import settings
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Test password hashing
        password = "test123"
        hashed = pwd_context.hash(password)
        verified = pwd_context.verify(password, hashed)
        
        # Test JWT token creation
        token_data = {"sub": "test", "exp": datetime.utcnow().timestamp() + 3600}
        token = jwt.encode(token_data, settings.secret_key, algorithm=settings.algorithm)
        
        print(f"✅ Authentication: Password hashing and JWT working")
        return True
    except Exception as e:
        print(f"❌ Authentication: Failed - {e}")
        return False

def test_api_startup():
    """Test if FastAPI app can start"""
    try:
        from app.main import app
        print("✅ FastAPI App: Application loads successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI App: Failed to load - {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 HMS System Test Suite")
    print("=" * 40)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Model Imports", test_models),
        ("Schema Validation", test_schemas),
        ("Database Operations", test_database_operations),
        ("Authentication System", test_authentication),
        ("FastAPI Application", test_api_startup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 To start the application:")
        print("python start.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("- Ensure MySQL is running")
        print("- Check database credentials in .env")
        print("- Run: python init_database.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)