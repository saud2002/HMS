#!/usr/bin/env python3
"""
Test Doctors API
"""
import sys
sys.path.append('app')

def test_doctors_query():
    """Test doctors database query"""
    try:
        from app.database import SessionLocal
        from app.models import Doctor
        
        db = SessionLocal()
        
        print("🔍 Testing doctors query...")
        
        # Test basic query
        doctors = db.query(Doctor).all()
        print(f"✅ Found {len(doctors)} doctors")
        
        # Test individual doctor
        if doctors:
            d = doctors[0]
            print(f"✅ First doctor: {d.doctor_name}")
            print(f"   Status: {d.status} (type: {type(d.status)})")
            
            # Test serialization
            doctor_dict = {
                "doctor_id": d.doctor_id,
                "doctor_name": d.doctor_name,
                "specialization": d.specialization,
                "consultation_charges": float(d.consultation_charges),
                "status": d.status,
                "created_at": d.created_at.isoformat(),
                "updated_at": d.updated_at.isoformat()
            }
            print("✅ Serialization successful")
            print(f"   Doctor dict: {doctor_dict}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint():
    """Test the API endpoint directly"""
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/api/doctors")
        
        print(f"🌐 API Response Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ API Success: {response.json()}")
        else:
            print(f"❌ API Error: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ API Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    print("🐛 HMS Doctors API Debug")
    print("=" * 40)
    
    print("\n1. Testing Database Query...")
    db_success = test_doctors_query()
    
    print("\n2. Testing API Endpoint...")
    api_success = test_api_endpoint()
    
    print("\n" + "=" * 40)
    if db_success and api_success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")

if __name__ == "__main__":
    main()