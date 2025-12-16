#!/usr/bin/env python3
"""
Quick HMS Test - Basic functionality check
"""
import sys
import os

# Add app to path
sys.path.append('app')

def test_basic_imports():
    """Test basic imports"""
    try:
        from app.database import test_connection
        from app.models import Patient, Doctor
        from app.schemas import PatientCreate
        print("✅ Basic imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        from app.database import test_connection
        result = test_connection()
        print(f"✅ Database: {'Connected' if result else 'Failed'}")
        return result
    except Exception as e:
        print(f"❌ Database: {e}")
        return False

def test_schema_validation():
    """Test schema validation"""
    try:
        from app.schemas import PatientCreate
        
        # Test valid data
        patient_data = {
            "patient_name": "Test Patient",
            "age": 30,
            "phone_number": "0771234567",
            "gender": "Male",
            "nic": "123456789V"
        }
        patient = PatientCreate(**patient_data)
        print("✅ Schema validation working")
        return True
    except Exception as e:
        print(f"❌ Schema validation: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation"""
    try:
        from app.main import app
        print("✅ FastAPI app loads successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI app: {e}")
        return False

def main():
    """Run quick tests"""
    print("🚀 HMS Quick Test")
    print("=" * 30)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Database Connection", test_database),
        ("Schema Validation", test_schema_validation),
        ("FastAPI App", test_fastapi_app)
    ]
    
    passed = 0
    for name, test_func in tests:
        print(f"\n🔍 {name}...")
        if test_func():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Ready to start HMS.")
        print("\n🚀 To start the application:")
        print("python start.py")
        return True
    else:
        print("❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)