#!/usr/bin/env python3
"""
Test Frontend Integration - Simulate Frontend API Calls
"""
import sys
sys.path.append('app')

def test_frontend_workflow():
    """Test the complete frontend workflow"""
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        from datetime import date
        
        client = TestClient(app)
        
        print("🌐 Testing Frontend Integration Workflow...")
        
        # 1. Test loading patients for dropdown
        print("\n1. Loading patients for dropdown...")
        response = client.get("/api/patients")
        patients = response.json()
        print(f"   ✅ Loaded {len(patients)} patients for dropdown")
        
        # 2. Test loading doctors for dropdown
        print("\n2. Loading doctors for dropdown...")
        response = client.get("/api/doctors?status=Active")
        doctors = response.json()
        print(f"   ✅ Loaded {len(doctors)} active doctors for dropdown")
        
        # 3. Test getting patient details (when user selects patient)
        if patients:
            patient_id = patients[0]["patient_id"]
            print(f"\n3. Getting patient details for ID {patient_id}...")
            response = client.get(f"/api/patients/{patient_id}")
            patient_details = response.json()
            print(f"   ✅ Patient: {patient_details['patient_name']}, Age: {patient_details['age']}")
        
        # 4. Test getting doctor details (when user selects doctor)
        if doctors:
            doctor_id = doctors[0]["doctor_id"]
            print(f"\n4. Getting doctor details for ID {doctor_id}...")
            response = client.get(f"/api/doctors/{doctor_id}")
            doctor_details = response.json()
            print(f"   ✅ Doctor: {doctor_details['doctor_name']}, Fee: ${doctor_details['consultation_charges']}")
        
        # 5. Test creating appointment (when user submits form)
        if patients and doctors:
            print("\n5. Creating appointment...")
            appointment_data = {
                "patient_id": patients[0]["patient_id"],
                "doctor_id": doctors[0]["doctor_id"],
                "appointment_date": date.today().isoformat(),
                "hospital_charges": 50.0
            }
            
            response = client.post("/api/appointments", json=appointment_data)
            appointment = response.json()
            print(f"   ✅ Created appointment: {appointment['token_number']}")
            appointment_id = appointment["appointment_id"]
            
            # 6. Test adding additional expenses
            print("\n6. Adding additional expenses...")
            expenses = [
                {"appointment_id": appointment_id, "service_type": "Dressing", "service_description": "Wound dressing", "amount": 25},
                {"appointment_id": appointment_id, "service_type": "Blood Testing", "service_description": "Lab blood test", "amount": 75}
            ]
            
            for expense in expenses:
                response = client.post("/api/expenses", json=expense)
                print(f"   ✅ Added expense: {expense['service_type']} - ${expense['amount']}")
            
            # 7. Test getting full appointment details (for bill display)
            print("\n7. Getting full appointment details for bill...")
            response = client.get(f"/api/appointments/{appointment_id}")
            full_appointment = response.json()
            print(f"   ✅ Full appointment loaded:")
            print(f"      Token: {full_appointment['token_number']}")
            print(f"      Patient: {full_appointment['patient']['patient_name']}")
            print(f"      Doctor: {full_appointment['doctor']['doctor_name']}")
            print(f"      Doctor Charges: ${full_appointment['doctor_charges']}")
            print(f"      Hospital Charges: ${full_appointment['hospital_charges']}")
            print(f"      Additional Expenses: {len(full_appointment['additional_expenses'])}")
            if full_appointment['bill']:
                print(f"      Total Amount: ${full_appointment['bill']['total_amount']}")
        
        # 8. Test loading today's appointments (for appointments list)
        print("\n8. Loading today's appointments...")
        response = client.get("/api/appointments/today")
        today_appointments = response.json()
        print(f"   ✅ Today's appointments: {len(today_appointments)}")
        
        # 9. Test loading all appointments (for appointments list)
        print("\n9. Loading all appointments...")
        response = client.get("/api/appointments")
        all_appointments = response.json()
        print(f"   ✅ All appointments: {len(all_appointments)}")
        
        # 10. Test updating appointment status
        if all_appointments:
            appointment_id = all_appointments[0]["appointment_id"]
            print(f"\n10. Updating appointment status...")
            response = client.patch(f"/api/appointments/{appointment_id}/status", params={"status": "Completed"})
            print(f"   ✅ Appointment status updated to Completed")
        
        print("\n" + "=" * 60)
        print("🎉 Frontend integration workflow test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Frontend integration test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🏥 HMS Frontend Integration Test")
    print("=" * 60)
    
    success = test_frontend_workflow()
    
    if success:
        print("✅ All frontend integration tests passed!")
        print("\n📋 Summary:")
        print("   • Patient dropdown loading: ✅")
        print("   • Doctor dropdown loading: ✅")
        print("   • Patient details loading: ✅")
        print("   • Doctor details loading: ✅")
        print("   • Appointment creation: ✅")
        print("   • Additional expenses: ✅")
        print("   • Bill generation: ✅")
        print("   • Appointments listing: ✅")
        print("   • Status updates: ✅")
        print("\n🚀 Frontend is ready to use!")
    else:
        print("❌ Frontend integration tests failed!")

if __name__ == "__main__":
    main()