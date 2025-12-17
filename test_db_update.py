#!/usr/bin/env python3
"""
Test database update issue
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

def test_db_update():
    """Test if database update is causing the issue"""
    try:
        from backend.app.database import SessionLocal
        from backend.app.models.user import AdminUser
        from passlib.context import CryptContext
        from datetime import datetime
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        db = SessionLocal()
        
        print("🔍 Testing Database Update Issue...")
        
        # Get admin user
        admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        
        if admin:
            print(f"✅ Admin user found: {admin.username}")
            print(f"Password hash before: {admin.password_hash}")
            print(f"Last login before: {admin.last_login}")
            
            # Test password verification BEFORE update
            print("\n1. Testing password verification BEFORE update:")
            try:
                result = pwd_context.verify("admin123", admin.password_hash)
                print(f"   ✅ Verification result: {result}")
            except Exception as e:
                print(f"   ❌ Verification error: {e}")
            
            # Update last login (simulate what happens during login)
            print("\n2. Updating last_login field...")
            admin.last_login = datetime.utcnow()
            db.commit()
            print("   ✅ Database updated")
            
            # Refresh the object from database
            db.refresh(admin)
            print(f"Password hash after: {admin.password_hash}")
            print(f"Last login after: {admin.last_login}")
            
            # Test password verification AFTER update
            print("\n3. Testing password verification AFTER update:")
            try:
                result = pwd_context.verify("admin123", admin.password_hash)
                print(f"   ✅ Verification result: {result}")
            except Exception as e:
                print(f"   ❌ Verification error: {e}")
            
            # Check if hash changed
            print("\n4. Checking if hash changed:")
            admin2 = db.query(AdminUser).filter(AdminUser.username == "admin").first()
            print(f"Hash from fresh query: {admin2.password_hash}")
            
            if admin.password_hash == admin2.password_hash:
                print("   ✅ Hash is consistent")
            else:
                print("   ❌ Hash changed!")
                
        else:
            print("❌ Admin user not found")
            return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_db_update()