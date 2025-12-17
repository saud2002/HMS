#!/usr/bin/env python3
"""
Test Login Function Directly
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

def test_login_direct():
    """Test the login function directly"""
    try:
        from backend.app.database import SessionLocal
        from backend.app.models.user import AdminUser
        from backend.app.schemas.user import AdminLogin, TokenResponse
        from passlib.context import CryptContext
        from jose import jwt
        from backend.app.config import settings
        from datetime import datetime, timedelta
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        db = SessionLocal()
        
        print("🔍 Testing Login Function Directly...")
        
        # Create login data
        login_data = AdminLogin(username="admin", password="admin123")
        print(f"   Login data: {login_data}")
        
        # Get admin user
        admin = db.query(AdminUser).filter(AdminUser.username == login_data.username).first()
        if not admin:
            print("❌ Admin user not found")
            return False
        
        print(f"   ✅ Admin found: {admin.username}")
        
        # Verify password
        if not pwd_context.verify(login_data.password, admin.password_hash):
            print("❌ Password verification failed")
            return False
        
        print("   ✅ Password verified")
        
        # Check status
        if str(admin.status) != "Active":
            print(f"❌ Account inactive: {admin.status}")
            return False
        
        print("   ✅ Account is active")
        
        # Update last login
        admin.last_login = datetime.utcnow()
        db.commit()
        print("   ✅ Last login updated")
        
        # Create token
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        token_data = {"sub": admin.username, "admin_id": admin.admin_id, "exp": expire}
        
        print(f"   Token data: {token_data}")
        print(f"   Secret key: {settings.secret_key[:20]}...")
        print(f"   Algorithm: {settings.algorithm}")
        
        access_token = jwt.encode(token_data, settings.secret_key, algorithm=settings.algorithm)
        print(f"   ✅ Token created: {access_token[:50]}...")
        
        # Create response
        response = {
            "access_token": access_token, 
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60
        }
        
        print(f"   ✅ Response: {response}")
        
        # Validate with schema
        token_response = TokenResponse(**response)
        print(f"   ✅ Schema validation passed: {token_response}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_login_direct()