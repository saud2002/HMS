#!/usr/bin/env python3
"""
Check Voucher File Structure
"""
import os

def check_voucher_file():
    """Check voucher HTML file structure"""
    print("📄 Checking Voucher File Structure")
    print("=" * 40)
    
    try:
        file_path = os.path.join('..', 'frontend', 'vouchers.html')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key elements
        checks = [
            ('sidebar div', 'class="sidebar"' in content),
            ('topbar div', 'class="topbar"' in content),
            ('main-content div', 'class="main-content"' in content),
            ('stats-grid div', 'class="stats-grid"' in content),
            ('voucher-table class', 'class="voucher-table"' in content),
            ('create modal', 'id="createVoucherModal"' in content),
            ('view modal', 'id="viewVoucherModal"' in content),
            ('common.js script', '/static/js/common.js' in content),
            ('vouchers.js script', '/static/js/vouchers.js' in content),
            ('styles.css link', '/static/css/styles.css' in content)
        ]
        
        print("Structure Checks:")
        for name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {name}")
        
        all_passed = all(check[1] for check in checks)
        
        print(f"\nFile size: {len(content)} characters")
        print(f"Total checks: {len(checks)}")
        print(f"Passed: {sum(1 for _, passed in checks if passed)}")
        
        if all_passed:
            print("\n🎉 All structure checks passed!")
            print("✅ Voucher page has been successfully updated to match HMS design")
        else:
            print(f"\n⚠️ {len(checks) - sum(1 for _, passed in checks if passed)} checks failed")
            
    except FileNotFoundError:
        print("❌ Voucher file not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_voucher_file()