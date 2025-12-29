#!/usr/bin/env python3
"""
Verify Doctor Selection Fix
"""
import os

def verify_fix():
    """Verify the doctor selection fix"""
    print("🔍 Verifying Doctor Selection Fix")
    print("=" * 35)
    
    try:
        file_path = os.path.join('..', 'frontend', 'appointments.html')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key elements
        checks = [
            ('Doctor dropdown exists', 'id="appointmentDoctor"' in content),
            ('Default option exists', '-- Select Doctor --' in content),
            ('Auto-selection code removed', 'doctors[0].doctor_id' not in content),
            ('Auto-selection comment removed', 'Auto-select first doctor' not in content),
            ('fillDoctorDetails function exists', 'fillDoctorDetails()' in content),
            ('Doctor onchange event exists', 'onchange="fillDoctorDetails()"' in content)
        ]
        
        print("Fix Verification:")
        for name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {name}")
        
        all_passed = all(check[1] for check in checks)
        
        print(f"\nFile size: {len(content)} characters")
        print(f"Total checks: {len(checks)}")
        print(f"Passed: {sum(1 for _, passed in checks if passed)}")
        
        if all_passed:
            print("\n🎉 Doctor selection fix verified successfully!")
            print("✅ Auto-selection has been removed")
            print("✅ Users can now freely select any doctor")
            print("✅ Doctor details will populate when selected")
        else:
            failed = len(checks) - sum(1 for _, passed in checks if passed)
            print(f"\n⚠️ {failed} checks failed")
            
    except FileNotFoundError:
        print("❌ Appointments file not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_fix()