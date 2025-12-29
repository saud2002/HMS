#!/usr/bin/env python3
"""
Test Frontend Voucher Access
"""
import requests

BASE_URL = "http://localhost:8000"

def test_frontend_access():
    """Test frontend voucher page access"""
    print("🌐 Testing Frontend Voucher Access")
    print("=" * 40)
    
    # Test 1: Access voucher page
    print("1. Testing voucher page access...")
    try:
        response = requests.get(f"{BASE_URL}/vouchers.html")
        if response.status_code == 200:
            print("✅ Voucher page accessible")
        else:
            print(f"❌ Voucher page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Voucher page error: {e}")
    
    # Test 2: Test API endpoints
    print("\n2. Testing API endpoints...")
    
    endpoints = [
        "/api/vouchers/summary",
        "/api/vouchers",
        "/api/doctors"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
            else:
                print(f"❌ {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    print("\n🎉 Frontend testing completed!")

if __name__ == "__main__":
    test_frontend_access()