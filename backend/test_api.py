"""
Test HMS API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(name, url, method="GET", data=None):
    """Test an API endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"Method: {method}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
            data = response.json()
            if isinstance(data, list):
                print(f"   Returned {len(data)} items")
                if len(data) > 0:
                    print(f"   First item: {json.dumps(data[0], indent=2)}")
            elif isinstance(data, dict):
                print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Failed!")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Is the server running?")
    except requests.exceptions.Timeout:
        print("❌ Timeout - Server took too long to respond")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("="*60)
    print("HMS API Test Suite")
    print("="*60)
    
    # Test 1: Health check
    test_endpoint("Health Check", f"{BASE_URL}/api/health")
    
    # Test 2: Dashboard stats
    test_endpoint("Dashboard Stats", f"{BASE_URL}/api/dashboard/stats")
    
    # Test 3: Get patients
    test_endpoint("Get Patients", f"{BASE_URL}/api/patients")
    
    # Test 4: Get doctors
    test_endpoint("Get Doctors", f"{BASE_URL}/api/doctors")
    
    # Test 5: Get appointments
    test_endpoint("Get Appointments", f"{BASE_URL}/api/appointments")
    
    # Test 6: Get services
    test_endpoint("Get Services", f"{BASE_URL}/api/services")
    
    print("\n" + "="*60)
    print("Test completed!")
    print("="*60)

if __name__ == "__main__":
    main()
