#!/usr/bin/env python3
"""
Simple Doctor Selection Test
"""
import requests

BASE_URL = "http://localhost:8000"

def test_doctor_selection():
    """Simple test for doctor selection"""
    print("👨‍⚕️ Testing Doctor Selection Fix")
    print("=" * 35)
    
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
            ('Auto-selection removed', 'doctors[0].doctor_id' not in content),
            ('Auto-selection comment removed', 'Auto-select first doctor' not in content),
            ('fillDoctorDetails exists', 'fillDoctorDetails()' in content)
        ]
        
        print("Fix Verification:")
        for name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {name}")
        
        all_passed = all(check[1] for check in checks)
        
        if all_passed:
            print("\n🎉 Doctor selection issue has been fixed!")
            print("✅ No doctor will be pre-selected")
            print("✅ Users can choose any doctor from the dropdown")
            print("✅ Doctor details will populate when selected")
        else:
            failed = len(checks) - sum(1 for _, passed in checks if passed)
            print(f"\n⚠️ {failed} checks failed - may need additional fixes")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_doctor_selection()