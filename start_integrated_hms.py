#!/usr/bin/env python3
"""
Start Integrated HMS - Single URL for Frontend + Backend
"""
import sys
import os
import webbrowser
import time
from pathlib import Path

def start_integrated_server():
    """Start the integrated HMS server"""
    print("🏥 Starting Integrated HMS System")
    print("=" * 40)
    
    # Check if we're in the right directory
    backend_dir = Path("backend")
    frontend_dir = Path("frontend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        print("💡 Make sure you're running this from the project root")
        return False
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    print("🚀 Starting integrated server...")
    print("📁 Backend: API + Database")
    print("🌐 Frontend: Served by FastAPI")
    print("🔗 Single URL: http://127.0.0.1:8000")
    print("-" * 40)
    
    # Import and run the app
    try:
        import uvicorn
        
        # Wait a moment then open browser
        def open_browser():
            time.sleep(3)
            print("🌐 Opening HMS in browser...")
            webbrowser.open('http://127.0.0.1:8000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the server
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 HMS Server stopped")
        return True
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("\n💡 Try:")
        print("1. cd backend")
        print("2. venv\\Scripts\\activate")
        print("3. python -m uvicorn app.main:app --reload --port 8000")
        return False

def main():
    """Main function"""
    try:
        success = start_integrated_server()
        return success
    except KeyboardInterrupt:
        print("\n👋 Startup interrupted")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)