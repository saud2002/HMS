#!/usr/bin/env python3
"""
HMS Complete Setup Script
This script will set up the entire Hospital Management System
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_backend():
    """Set up the backend environment"""
    print("\n🔧 Setting up Backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    os.chdir(backend_dir)
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && pip install -r requirements.txt"
    else:  # Linux/Mac
        activate_cmd = "source venv/bin/activate && pip install -r requirements.txt"
    
    if not run_command(activate_cmd, "Installing Python dependencies"):
        return False
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from template")
        print("⚠️ Please update database credentials in backend/.env")
    
    os.chdir("..")
    return True

def setup_database():
    """Initialize the database"""
    print("\n🗄️ Setting up Database...")
    
    backend_dir = Path("backend")
    os.chdir(backend_dir)
    
    # Run database initialization
    if os.name == 'nt':  # Windows
        init_cmd = "venv\\Scripts\\activate && python init_database.py"
    else:  # Linux/Mac
        init_cmd = "source venv/bin/activate && python init_database.py"
    
    success = run_command(init_cmd, "Initializing database")
    os.chdir("..")
    return success

def create_startup_scripts():
    """Create convenient startup scripts"""
    print("\n📝 Creating startup scripts...")
    
    # Windows batch file
    with open("start_hms.bat", "w") as f:
        f.write("""@echo off
echo Starting HMS Backend...
cd backend
call venv\\Scripts\\activate
python start.py
pause
""")
    
    # Linux/Mac shell script
    with open("start_hms.sh", "w") as f:
        f.write("""#!/bin/bash
echo "Starting HMS Backend..."
cd backend
source venv/bin/activate
python start.py
""")
    
    # Make shell script executable
    if os.name != 'nt':
        os.chmod("start_hms.sh", 0o755)
    
    print("✅ Created startup scripts")
    return True

def main():
    """Main setup function"""
    print("🏥 Hospital Management System - Complete Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        return False
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        print("💡 Make sure MySQL is running and credentials are correct in backend/.env")
        return False
    
    # Create startup scripts
    create_startup_scripts()
    
    print("\n🎉 HMS Setup Complete!")
    print("=" * 60)
    print("📋 Next Steps:")
    print("1. Update database credentials in backend/.env if needed")
    print("2. Start the backend server:")
    if os.name == 'nt':
        print("   - Windows: Double-click start_hms.bat")
    else:
        print("   - Linux/Mac: ./start_hms.sh")
    print("   - Or manually: cd backend && python start.py")
    print("3. Open frontend/index.html in your web browser")
    print("4. Login with username: admin, password: admin123")
    print("\n📚 Documentation:")
    print("- API Docs: http://localhost:8000/docs")
    print("- README: See README.md for detailed instructions")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)