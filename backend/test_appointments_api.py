#!/usr/bin/env python3
"""
Test Appointments API
"""
import sys
sys.path.append('app')

def test_appointments_query():
    """Test appointments database query"""
    try:
        from app.database import SessionLocal
        from app.models import Appointment
        
        db = SessionLocal()
        
        print("🔍 Testing appointments query...")
        
        # Test basic query
        appointments = db.query(Appointment).all()
        print(f"✅ Found {len(appointments)} appointments")
        
        # Test individual appointment if exists
        if appointments:
            a = appointments[0]
            print(f"✅ First appointment: {a.token_number}")
            print(f"   Status: {a.status} (type: {type(a.status)})")
            
            # Test serialization
            appointment_dict = {
                "appointment_id": a.appointment_id,
                "patient_id": a.patient_id,
                "doctor_id": a.doctor_id,
                "appointment_date": a.appointment_date.isoformat(),
                "token_number": a.token_number,
                "doctor_charges": float(a.doctor_charges),
                "hospital_charges": float(a.hospital_charges),
                "status": a.status,
                "created_at": a.created_at.isoformat()
            }
            print("✅ Serialization successful")
            print(f"   Appointment dict: {appointment_dict}")
        
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
        response = client.get("/api/appointments")
        
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
    print("🐛 HMS Appointments API Debug")
    print("=" * 40)
    
    print("\n1. Testing Database Query...")
    db_success = test_appointments_query()
    
    print("\n2. Testing API Endpoint...")
    api_success = test_api_endpoint()
    
    print("\n" + "=" * 40)
    if db_success and api_success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")

if __name__ == "__main__":
    main()