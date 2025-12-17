#!/usr/bin/env python3
"""
Test FastAPI Login Endpoint
"""
import requests
import json

def test_fastapi_login():
    """Test the FastAPI login endpoint with detailed error reporting"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Testing FastAPI Login Endpoint...")
    print("=" * 50)
    
    # Test data
    login_data = {"username": "admin", "password": "admin123"}
    
    try:
        # Make request with detailed error handling
        response = requests.post(
            f"{base_url}/api/auth/login", 
            json=login_data, 
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Login failed with status {response.status_code}")
            print(f"Response text: {response.text}")
            
            # Try to parse error details
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_fastapi_login()