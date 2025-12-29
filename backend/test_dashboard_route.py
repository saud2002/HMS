#!/usr/bin/env python3
"""
Test Dashboard Route
"""
import requests

BASE_URL = "http://localhost:8000"

def test_dashboard_routes():
    """Test dashboard routing"""
    print("🏠 Testing Dashboard Routes")
    print("=" * 30)
    
    routes_to_test = [
        ("/", "Root route"),
        ("/index.html", "Index.html route")
    ]
    
    for route, description in routes_to_test:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            print(f"{description}: {response.status_code}")
            
            if response.status_code == 200:
                # Check if it's the login page (redirect) or actual dashboard
                content = response.text
                if "HMS Login" in content:
                    print(f"  → Redirected to login (expected without auth)")
                elif "HMS Dashboard" in content or "Dashboard" in content:
                    print(f"  → Dashboard content served")
                else:
                    print(f"  → Other content served")
            else:
                print(f"  → Error: {response.status_code}")
                
        except Exception as e:
            print(f"{description}: Error - {e}")
    
    print("\n✅ Dashboard route testing completed!")

if __name__ == "__main__":
    test_dashboard_routes()