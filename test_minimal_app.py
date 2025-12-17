#!/usr/bin/env python3
"""
Minimal FastAPI app to test login
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

# Simple password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    """Simple login test"""
    print(f"Login attempt: {data.username}")
    
    # Test password hash (for "admin123")
    test_hash = "$2b$12$frW1yOUOTVQC82z27DVla.UgB1xTLhQ5NM//z3ZS0mRkK8n78JoY2"
    
    if data.username == "admin":
        # Test bcrypt verification
        is_valid = pwd_context.verify(data.password, test_hash)
        if is_valid:
            return {"message": "Login successful", "token": "test-token"}
        else:
            raise HTTPException(status_code=401, detail="Invalid password")
    else:
        raise HTTPException(status_code=401, detail="Invalid username")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)