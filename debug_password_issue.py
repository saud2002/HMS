#!/usr/bin/env python3
"""
Debug Password Issue
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

def debug_password_issue():
    """Debug the password verification issue"""
    try:
        from backend.app.database import SessionLocal
        from backend.app.models.user import AdminUser
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        db = SessionLocal()
        
        print("🔍 Debugging Password Issue...")
        
        # Get admin user
        admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        
        if admin:
            print(f"✅ Admin user found: {admin.username}")
            print(f"Password hash length: {len(admin.password_hash)}")
            print(f"Password hash: {admin.password_hash}")
            
            # Test different password inputs
            test_passwords = [
                "admin123",
                "admin123"[:72],  # Truncated
            ]
            
            for i, pwd in enumerate(test_passwords):
                print(f"\nTest {i+1}: Password '{pwd}' (length: {len(pwd)})")
                try:
                    result = pwd_context.verify(pwd, admin.password_hash)
                    print(f"   ✅ Verification result: {result}")
                except Exception as e:
                    print(f"   ❌ Verification error: {e}")
            
            # Check if the hash itself is the issue
            print(f"\nHash analysis:")
            print(f"   Starts with $2b$: {admin.password_hash.startswith('$2b$')}")
            print(f"   Hash parts: {admin.password_hash.split('$')}")
            
        else:
            print("❌ Admin user not found")
            return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_password_issue()