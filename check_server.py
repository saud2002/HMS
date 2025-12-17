#!/usr/bin/env python3
"""
Check HMS Server Status
"""
import requests
import json

def check_server():
    """Check if HMS server is running and accessible"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Checking HMS Server Status...")
    print("=" * 40)
    
    # 1. Check if server is running
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"✅ Server is running: {response.status_code}")
        print(f"   Health check: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        print("   Please start the server with: python backend/start.py")
        return False
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        return False
    
    # 2. Test login endpoint
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=5)
        
        print(f"\n🔐 Login endpoint test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"   Token type: {result.get('token_type')}")
            print(f"   Expires in: {result.get('expires_in')} seconds")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
    
    # 3. Check frontend access
    try:
        response = requests.get(f"{base_url}/login.html", timeout=5)
        print(f"\n🌐 Frontend access: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend check failed: {e}")
    
    return True

if __name__ == "__main__":
    check_server()