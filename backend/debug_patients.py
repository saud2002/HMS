#!/usr/bin/env python3
"""
Debug Patients API Issue
"""
import sys
sys.path.append('app')

def test_patient_query():
    """Test patient database query"""
    try:
        from app.database import SessionLocal
        from app.models import Patient
        
        db = SessionLocal()
        
        print("🔍 Testing patient query...")
        
        # Test basic query
        patients = db.query(Patient).all()
        print(f"✅ Found {len(patients)} patients")
        
        # Test individual patient
        if patients:
            p = patients[0]
            print(f"✅ First patient: {p.patient_name}")
            print(f"   Gender: {p.gender} (type: {type(p.gender)})")
            print(f"   Gender value: {p.gender.value if hasattr(p.gender, 'value') else 'No value attr'}")
            
            # Test serialization
            patient_dict = {
                "patient_id": p.patient_id,
                "patient_name": p.patient_name,
                "age": p.age,
                "phone_number": p.phone_number,
                "gender": str(p.gender),
                "nic": p.nic,
                "registration_date": p.registration_date.isoformat(),
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat()
            }
            print("✅ Serialization successful")
            print(f"   Patient dict: {patient_dict}")
        
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
        response = client.get("/api/patients")
        
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
    print("🐛 HMS Patients API Debug")
    print("=" * 40)
    
    print("\n1. Testing Database Query...")
    db_success = test_patient_query()
    
    print("\n2. Testing API Endpoint...")
    api_success = test_api_endpoint()
    
    print("\n" + "=" * 40)
    if db_success and api_success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")
        print("💡 Check the error messages above")

if __name__ == "__main__":
    main()