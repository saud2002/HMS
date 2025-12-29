#!/usr/bin/env python3
"""
Check Voucher JavaScript File
"""
import os

def check_voucher_js():
    """Check voucher JavaScript file"""
    print("🔧 Checking Voucher JavaScript")
    print("=" * 35)
    
    try:
        file_path = os.path.join('..', 'frontend', 'js', 'vouchers.js')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key updates
        checks = [
            ('openModal function used', 'openModal(' in content),
            ('closeModal function used', 'closeModal(' in content),
            ('Bootstrap removed', 'bootstrap' not in content.lower()),
            ('Custom showAlert', 'slideIn' in content),
            ('HMS modal system', 'new bootstrap.Modal' not in content)
        ]
        
        print("JavaScript Updates:")
        for name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {name}")
        
        all_passed = all(check[1] for check in checks)
        
        print(f"\nFile size: {len(content)} characters")
        
        if all_passed:
            print("\n🎉 JavaScript successfully updated for HMS design!")
        else:
            failed = len(checks) - sum(1 for _, passed in checks if passed)
            print(f"\n⚠️ {failed} checks failed - may need additional updates")
            
    except FileNotFoundError:
        print("❌ JavaScript file not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_voucher_js()