"""
Authentication module for HMS
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .models.user import AdminUser
from .config import settings

# Create a fresh password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_admin(db: Session, username: str, password: str) -> dict:
    """
    Authenticate admin user and return token data
    """
    try:
        print(f"🔍 Authenticating user: {username}")
        
        # Get admin user
        admin = db.query(AdminUser).filter(AdminUser.username == username).first()
        
        if not admin:
            print(f"❌ User not found: {username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        print(f"✅ User found: {admin.username}")
        
        # Debug password verification
        print(f"🔍 Password verification:")
        print(f"   Original password: '{password}' (length: {len(password)})")
        print(f"   Password hash: '{admin.password_hash}' (length: {len(admin.password_hash)})")
        
        # Verify password (truncate to 72 bytes for bcrypt compatibility)
        password_to_verify = password[:72] if len(password) > 72 else password
        print(f"   Password to verify: '{password_to_verify}' (length: {len(password_to_verify)})")
        
        try:
            # Check if we're accidentally passing the wrong parameters
            print(f"   About to call pwd_context.verify('{password_to_verify}', '{admin.password_hash}')")
            print(f"   Parameter types: password={type(password_to_verify)}, hash={type(admin.password_hash)}")
            
            # Make sure we're not accidentally swapping the parameters
            if len(admin.password_hash) > 72:
                print(f"   ⚠️ WARNING: Hash is longer than 72 bytes: {len(admin.password_hash)}")
            
            is_valid = pwd_context.verify(password_to_verify, admin.password_hash)
            print(f"   Verification result: {is_valid}")
            
            if not is_valid:
                print("❌ Password verification failed")
                raise HTTPException(status_code=401, detail="Invalid username or password")
        except Exception as verify_error:
            print(f"❌ Password verification error: {verify_error}")
            print(f"   Error type: {type(verify_error)}")
            
            # Check if we accidentally swapped parameters
            if "password cannot be longer than 72 bytes" in str(verify_error):
                print("   🔍 This error suggests parameters might be swapped!")
                print(f"   Password length: {len(password_to_verify)}")
                print(f"   Hash length: {len(admin.password_hash)}")
            
            raise HTTPException(status_code=500, detail=f"Password verification failed: {str(verify_error)}")
        
        print("✅ Password verified")
        
        if str(admin.status) != "Active":
            print(f"❌ Account inactive: {admin.status}")
            raise HTTPException(status_code=403, detail="Account is inactive")
        
        print("✅ Account is active")
        
        # Update last login
        admin.last_login = datetime.utcnow()
        db.commit()
        print("✅ Last login updated")
        
        # Create token
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        token_data = {"sub": admin.username, "admin_id": admin.admin_id, "exp": expire}
        access_token = jwt.encode(token_data, settings.secret_key, algorithm=settings.algorithm)
        
        print("✅ Token created successfully")
        
        response = {
            "access_token": access_token, 
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60
        }
        
        print(f"✅ Authentication successful for {admin.username}")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"❌ Unexpected error in authentication: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")