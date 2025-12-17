#!/usr/bin/env python3
"""
Test minimal login
"""
import requests
import json

def test_minimal_login():
    """Test the minimal login endpoint"""
    base_url = "http://127.0.0.1:8001"
    
    print("🔍 Testing Minimal Login Endpoint...")
    
    # Test data
    login_data = {"username": "admin", "password": "admin123"}
    
    try:
        response = requests.post(
            f"{base_url}/login", 
            json=login_data, 
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_minimal_login()