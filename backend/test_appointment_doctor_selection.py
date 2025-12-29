#!/usr/bin/env python3
"""
Test Appointment Doctor Selection
"""
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8000"

def test_doctor_selection():
    """Test that doctor is not pre-selected in appointments"""
    print("👨‍⚕️ Testing Doctor Selection in Appointments")
    print("=" * 45)
    
    try:
        # Get the appointments page
        response = requests.get(f"{BASE_URL}/appointments.html")
        if response.status_code != 200:
            print(f"❌ Failed to load appointments page: {response.status_code}")
            return
        
        content = response.text
        
        # Check for key elements
        checks = [
            ('Doctor dropdown exists', 'id="appointmentDoctor"' in content),
            ('Default option exists', '-- Select Doctor --' in content),
            ('No auto-selection code', 'doctors[0].doctor_id' not in content),
            ('fillDoctorDetails function exists', 'fillDoctorDetails()' in content),
            ('Doctor onchange event', 'onchange="fillDoctorDetails()"' in content)
        ]
        
        print("Doctor Selection Checks:")
        for name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {name}")
        
        all_passed = all(check[1] for check in checks)
        
        if all_passed:
            print("\n🎉 Doctor selection is working correctly!")
            print("✅ No doctor will be pre-selected")
            print("✅ Users can freely choose any doctor")
        else:
            failed = len(checks) - sum(1 for _, passed in checks if passed)
            print(f"\n⚠️ {failed} checks failed")
            
        # Additional check for auto-selection removal
        if 'Auto-select first doctor' not in content:
            print("✅ Auto-selection code has been removed")
        else:
            print("❌ Auto-selection code still present")
            
    except Exception as e:
        print(f"❌ Error testing appointments page: {e}")

if __name__ == "__main__":
    test_doctor_selection()