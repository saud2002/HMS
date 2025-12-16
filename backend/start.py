#!/usr/bin/env python3
"""
HMS Application Startup Script
"""
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import fastapi
        import sqlalchemy
        import pymysql
        import passlib
        import jose
        import pydantic
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_database():
    """Check database connection"""
    try:
        sys.path.append('app')
        from app.database import test_connection
        if test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Environment file found")
        return True
    else:
        print("⚠️ No .env file found, using default settings")
        print("Consider copying .env.example to .env and updating values")
        return True

def main():
    """Main startup function"""
    print("🏥 HMS Application Startup")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Check environment
    check_env_file()
    
    # Check database
    if not check_database():
        print("\n💡 To initialize the database, run:")
        print("python init_database.py")
        return False
    
    print("\n🚀 Starting HMS Application...")
    print("Access the API at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)
    
    # Start the application
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--port", "8000",
            "--host", "127.0.0.1"
        ])
    except KeyboardInterrupt:
        print("\n👋 HMS Application stopped")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)