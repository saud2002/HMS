#!/usr/bin/env python3
"""
Test HMS Server - Quick server functionality test
"""
import sys
import time
import subprocess
import requests
from threading import Thread

def start_server():
    """Start the server in background"""
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--port", "8001",  # Use different port for testing
            "--host", "127.0.0.1"
        ], cwd=".", capture_output=True)
    except:
        pass

def test_server():
    """Test server endpoints"""
    base_url = "http://127.0.0.1:8001"
    
    print("🧪 Testing HMS Server")
    print("=" * 30)
    
    # Wait for server to start
    print("⏳ Starting server...")
    time.sleep(3)
    
    try:
        # Test root endpoint
        print("🔍 Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test health endpoint
        print("🔍 Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test docs endpoint
        print("🔍 Testing docs endpoint...")
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API docs working")
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
        
        print("\n🎉 All server tests passed!")
        print(f"🌐 Server is running at: {base_url}")
        print(f"📚 API Documentation: {base_url}/docs")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("💡 Make sure the server is running with: python start.py")
        return False
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def main():
    """Main test function"""
    # Start server in background
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Test server
    success = test_server()
    
    if success:
        print("\n✅ HMS Server is working perfectly!")
        print("\n🚀 To start your HMS:")
        print("1. Run: python start.py")
        print("2. Visit: http://127.0.0.1:8000")
        print("3. Open: frontend/index.html")
    else:
        print("\n❌ Server tests failed")
        print("💡 Try running: python quick_test.py first")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted")
        sys.exit(0)