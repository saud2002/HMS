#!/usr/bin/env python3
"""
Test Raw Login Endpoint
"""
import requests
import json

def test_raw_login():
    """Test the raw login endpoint"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Testing Raw Login Endpoint...")
    print("=" * 50)
    
    # Test data
    login_data = {"username": "admin", "password": "admin123"}
    
    try:
        # Test raw endpoint
        response = requests.post(
            f"{base_url}/api/auth/login-raw", 
            json=login_data, 
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Raw endpoint - Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Raw endpoint - Response: {json.dumps(result, indent=2)}")
        else:
            print(f"Raw endpoint - Error: {response.text}")
            
        # Test regular endpoint
        response = requests.post(
            f"{base_url}/api/auth/login", 
            json=login_data, 
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nRegular endpoint - Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Regular endpoint - Response: {json.dumps(result, indent=2)}")
        else:
            print(f"Regular endpoint - Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_raw_login()