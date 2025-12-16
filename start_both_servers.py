#!/usr/bin/env python3
"""
Start Both HMS Backend and Frontend Servers
"""
import subprocess
import time
import webbrowser
import sys
import os
from pathlib import Path

def start_backend():
    """Start the backend server"""
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return None
    
    print("🚀 Starting HMS Backend Server...")
    
    # Activate venv and start server
    if os.name == 'nt':  # Windows
        cmd = ["cmd", "/c", "venv\\Scripts\\activate && python start.py"]
    else:  # Linux/Mac
        cmd = ["bash", "-c", "source venv/bin/activate && python start.py"]
    
    try:
        process = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print("✅ Backend server starting...")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend server"""
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return None
    
    print("🌐 Starting HMS Frontend Server...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, "start_frontend.py"],
            cwd=frontend_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print("✅ Frontend server starting...")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    """Main function"""
    print("🏥 HMS Complete System Startup")
    print("=" * 40)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Cannot start without backend")
        return False
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Wait a bit more
    time.sleep(3)
    
    # Open browser to frontend
    print("🌐 Opening HMS in browser...")
    webbrowser.open('http://127.0.0.1:3000')
    
    print("\n🎉 HMS System Started Successfully!")
    print("-" * 40)
    print("📊 Frontend: http://127.0.0.1:3000")
    print("🔧 Backend API: http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    print("🔑 Login: admin / admin123")
    print("-" * 40)
    print("Press Ctrl+C to stop all servers")
    
    try:
        # Keep script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopping HMS servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ All servers stopped")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Startup interrupted")
        sys.exit(0)