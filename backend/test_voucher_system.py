#!/usr/bin/env python3
"""
Test Voucher System
"""
import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

def test_voucher_endpoints():
    """Test voucher system endpoints"""
    print("🧪 Testing Voucher System")
    print("=" * 40)
    
    # Test 1: Get voucher summary
    print("1. Testing voucher summary...")
    try:
        response = requests.get(f"{BASE_URL}/api/vouchers/summary")
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Summary: {summary['total_vouchers']} total vouchers")
        else:
            print(f"❌ Summary failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Summary error: {e}")
    
    # Test 2: Get all vouchers
    print("\n2. Testing get all vouchers...")
    try:
        response = requests.get(f"{BASE_URL}/api/vouchers")
        if response.status_code == 200:
            vouchers = response.json()
            print(f"✅ Retrieved {len(vouchers)} vouchers")
        else:
            print(f"❌ Get vouchers failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get vouchers error: {e}")
    
    # Test 3: Get doctors (needed for voucher creation)
    print("\n3. Testing get doctors...")
    try:
        response = requests.get(f"{BASE_URL}/api/doctors")
        if response.status_code == 200:
            doctors = response.json()
            print(f"✅ Retrieved {len(doctors)} doctors")
            if doctors:
                doctor_id = doctors[0]['doctor_id']
                print(f"Using doctor: {doctor_id}")
                
                # Test 4: Create doctor payment voucher
                print("\n4. Testing create doctor payment voucher...")
                voucher_data = {
                    "voucher_type": "DOCTOR_PAYMENT",
                    "doctor_id": doctor_id,
                    "amount": 5000.00,
                    "description": "Monthly payment for consultations",
                    "voucher_date": date.today().isoformat(),
                    "payment_period_start": "2024-12-01",
                    "payment_period_end": "2024-12-31"
                }
                
                response = requests.post(
                    f"{BASE_URL}/api/vouchers",
                    json=voucher_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    voucher = response.json()
                    print(f"✅ Created voucher: {voucher['voucher_number']}")
                    voucher_id = voucher['voucher_id']
                    
                    # Test 5: Submit for approval
                    print("\n5. Testing submit for approval...")
                    response = requests.post(f"{BASE_URL}/api/vouchers/{voucher_id}/submit")
                    if response.status_code == 200:
                        print("✅ Voucher submitted for approval")
                        
                        # Test 6: Approve voucher
                        print("\n6. Testing approve voucher...")
                        response = requests.post(f"{BASE_URL}/api/vouchers/{voucher_id}/approve")
                        if response.status_code == 200:
                            print("✅ Voucher approved")
                            
                            # Test 7: Mark as paid
                            print("\n7. Testing mark as paid...")
                            response = requests.post(f"{BASE_URL}/api/vouchers/{voucher_id}/pay")
                            if response.status_code == 200:
                                print("✅ Voucher marked as paid")
                            else:
                                print(f"❌ Mark as paid failed: {response.status_code}")
                        else:
                            print(f"❌ Approve failed: {response.status_code}")
                    else:
                        print(f"❌ Submit failed: {response.status_code}")
                else:
                    print(f"❌ Create voucher failed: {response.status_code} - {response.text}")
            else:
                print("⚠️ No doctors found, skipping voucher creation test")
        else:
            print(f"❌ Get doctors failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Doctors error: {e}")
    
    # Test 8: Create hospital expense voucher
    print("\n8. Testing create hospital expense voucher...")
    try:
        expense_data = {
            "voucher_type": "HOSPITAL_EXPENSE",
            "amount": 2500.00,
            "description": "Medical equipment maintenance",
            "voucher_date": date.today().isoformat()
        }
        
        response = requests.post(
            f"{BASE_URL}/api/vouchers",
            json=expense_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            voucher = response.json()
            print(f"✅ Created expense voucher: {voucher['voucher_number']}")
        else:
            print(f"❌ Create expense voucher failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Expense voucher error: {e}")
    
    print("\n🎉 Voucher system testing completed!")

if __name__ == "__main__":
    test_voucher_endpoints()