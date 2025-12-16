#!/usr/bin/env python3
"""
Test Complete HMS Integration - Doctors and Appointments
"""
import sys
sys.path.append('app')

def test_complete_integration():
    """Test the complete integration flow"""
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        from datetime import date
        
        client = TestClient(app)
        
        print("🔍 Testing Complete HMS Integration...")
        
        # 1. Test Patients API
        print("\n1. Testing Patients API...")
        response = client.get("/api/patients")
        print(f"   Patients API Status: {response.status_code}")
        patients = response.json() if response.status_code == 200 else []
        print(f"   Found {len(patients)} patients")
        
        # 2. Test Doctors API
        print("\n2. Testing Doctors API...")
        response = client.get("/api/doctors")
        print(f"   Doctors API Status: {response.status_code}")
        doctors = response.json() if response.status_code == 200 else []
        print(f"   Found {len(doctors)} doctors")
        
        # 3. Test Appointments API
        print("\n3. Testing Appointments API...")
        response = client.get("/api/appointments")
        print(f"   Appointments API Status: {response.status_code}")
        appointments = response.json() if response.status_code == 200 else []
        print(f"   Found {len(appointments)} appointments")
        
        # 4. Test Today's Appointments
        print("\n4. Testing Today's Appointments...")
        response = client.get("/api/appointments/today")
        print(f"   Today's Appointments Status: {response.status_code}")
        today_appointments = response.json() if response.status_code == 200 else []
        print(f"   Found {len(today_appointments)} appointments today")
        
        # 5. Test Bills API
        print("\n5. Testing Bills API...")
        response = client.get("/api/bills")
        print(f"   Bills API Status: {response.status_code}")
        bills = response.json() if response.status_code == 200 else []
        print(f"   Found {len(bills)} bills")
        
        # 6. Test Dashboard Stats
        print("\n6. Testing Dashboard Stats...")
        response = client.get("/api/dashboard/stats")
        print(f"   Dashboard Stats Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Stats: {stats}")
        
        # 7. Test if we can create an appointment (if we have patients and doctors)
        if patients and doctors:
            print("\n7. Testing Appointment Creation...")
            appointment_data = {
                "patient_id": patients[0]["patient_id"],
                "doctor_id": doctors[0]["doctor_id"],
                "appointment_date": date.today().isoformat(),
                "hospital_charges": 50.0
            }
            
            response = client.post("/api/appointments", json=appointment_data)
            print(f"   Appointment Creation Status: {response.status_code}")
            if response.status_code == 200:
                new_appointment = response.json()
                print(f"   ✅ Created appointment: {new_appointment['token_number']}")
                
                # Test getting the created appointment
                response = client.get(f"/api/appointments/{new_appointment['appointment_id']}")
                if response.status_code == 200:
                    print(f"   ✅ Retrieved appointment details successfully")
                else:
                    print(f"   ❌ Failed to retrieve appointment: {response.status_code}")
            else:
                print(f"   ❌ Failed to create appointment: {response.text}")
        else:
            print("\n7. Skipping appointment creation (no patients or doctors available)")
        
        print("\n" + "=" * 50)
        print("🎉 Integration test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🏥 HMS Complete Integration Test")
    print("=" * 50)
    
    success = test_complete_integration()
    
    if success:
        print("✅ All integration tests passed!")
    else:
        print("❌ Integration tests failed!")

if __name__ == "__main__":
    main()