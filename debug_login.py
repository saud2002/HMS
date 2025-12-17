#!/usr/bin/env python3
"""
Debug Login Issue
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

def debug_login():
    """Debug the login issue"""
    try:
        from backend.app.database import SessionLocal
        from backend.app.models.user import AdminUser
        from passlib.context import CryptContext
        from sqlalchemy import text
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        db = SessionLocal()
        
        print("🔍 Debugging Login Issue...")
        
        # 1. Check if admin user exists
        print("\n1. Checking admin user...")
        admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        
        if admin:
            print(f"   ✅ Admin user found: {admin.username}")
            print(f"   Full name: {admin.full_name}")
            print(f"   Status: {admin.status}")
            print(f"   Password hash: {admin.password_hash[:50]}...")
            
            # 2. Test password verification
            print("\n2. Testing password verification...")
            test_password = "admin123"
            is_valid = pwd_context.verify(test_password, admin.password_hash)
            print(f"   Password 'admin123' valid: {is_valid}")
            
            if not is_valid:
                print("   ❌ Password verification failed!")
                print("   Let's create a new hash and update...")
                
                # Create new hash
                new_hash = pwd_context.hash(test_password)
                print(f"   New hash: {new_hash[:50]}...")
                
                # Update in database
                db.execute(text("""
                    UPDATE admin_users 
                    SET password_hash = :new_hash 
                    WHERE username = 'admin'
                """), {"new_hash": new_hash})
                db.commit()
                
                print("   ✅ Password hash updated!")
                
                # Verify again
                admin_updated = db.query(AdminUser).filter(AdminUser.username == "admin").first()
                is_valid_now = pwd_context.verify(test_password, admin_updated.password_hash)
                print(f"   Password verification after update: {is_valid_now}")
            
        else:
            print("   ❌ Admin user not found!")
            return False
        
        # 3. Test API endpoint
        print("\n3. Testing API endpoint...")
        from backend.app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        login_data = {"username": "admin", "password": "admin123"}
        response = client.post("/api/auth/login", json=login_data)
        
        print(f"   API Response Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Login API working!")
            result = response.json()
            print(f"   Token type: {result.get('token_type')}")
            print(f"   Expires in: {result.get('expires_in')} seconds")
        else:
            print(f"   ❌ Login API failed: {response.text}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    print("🔍 HMS Login Debug")
    print("=" * 30)
    
    success = debug_login()
    
    if success:
        print("\n🎉 Debug completed!")
        print("Try logging in again with admin/admin123")
    else:
        print("\n❌ Debug failed!")

if __name__ == "__main__":
    main()