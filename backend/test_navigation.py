#!/usr/bin/env python3
"""
Test Navigation Links
"""
import requests

BASE_URL = "http://localhost:8000"

def test_navigation():
    """Test navigation links"""
    print("🧭 Testing Navigation Links")
    print("=" * 30)
    
    # Test all main navigation routes
    routes = [
        ("/", "Dashboard (root)"),
        ("/index.html", "Dashboard (index.html)"),
        ("/patients.html", "Patients"),
        ("/doctors.html", "Doctors"),
        ("/appointments.html", "Appointments"),
        ("/vouchers.html", "Vouchers"),
        ("/reports.html", "Reports"),
        ("/settings.html", "Settings")
    ]
    
    print("Route Status Check:")
    for route, name in routes:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"  {status} {name}: {response.status_code}")
            
            # Check if it's redirecting to login (expected without auth)
            if response.status_code == 200 and "HMS Login" in response.text:
                print(f"      → Redirected to login (auth required)")
            elif response.status_code == 200:
                print(f"      → Content served successfully")
                
        except Exception as e:
            print(f"  ❌ {name}: Error - {e}")
    
    print(f"\n🎯 Navigation testing completed!")
    print("Note: Login redirects are expected for protected routes")

if __name__ == "__main__":
    test_navigation()