#!/usr/bin/env python3
"""
Simple Voucher Page Test
"""
import requests

BASE_URL = "http://localhost:8000"

def test_voucher_page():
    """Simple test for voucher page"""
    print("🧪 Testing Voucher Page")
    print("=" * 30)
    
    try:
        # Test voucher page
        response = requests.get(f"{BASE_URL}/vouchers.html")
        if response.status_code == 200:
            content = response.text
            
            # Check for key elements
            checks = [
                ('sidebar', 'class="sidebar"' in content),
                ('topbar', 'class="topbar"' in content),
                ('main-content', 'class="main-content"' in content),
                ('stats-grid', 'class="stats-grid"' in content),
                ('voucher-table', 'class="voucher-table"' in content),
                ('create modal', 'id="createVoucherModal"' in content),
                ('view modal', 'id="viewVoucherModal"' in content),
                ('common.js', '/static/js/common.js' in content),
                ('vouchers.js', '/static/js/vouchers.js' in content),
                ('styles.css', '/static/css/styles.css' in content)
            ]
            
            print("Page Structure Checks:")
            for name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"  {status} {name}")
            
            all_passed = all(check[1] for check in checks)
            if all_passed:
                print("\n🎉 All checks passed! Voucher page is properly structured.")
            else:
                print("\n⚠️ Some checks failed. Page may need adjustments.")
                
        else:
            print(f"❌ Failed to load voucher page: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_voucher_page()