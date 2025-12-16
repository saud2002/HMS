#!/usr/bin/env python3
"""
Simple HTTP Server for HMS Frontend
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def start_frontend_server(port=3000):
    """Start a simple HTTP server for the frontend"""
    
    # Change to frontend directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    # Create server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🌐 HMS Frontend Server")
            print(f"📁 Serving: {frontend_dir}")
            print(f"🔗 URL: http://127.0.0.1:{port}")
            print(f"📚 Backend API: http://127.0.0.1:8000")
            print(f"🔑 Login: admin / admin123")
            print("-" * 50)
            print("Press Ctrl+C to stop the server")
            
            # Open browser
            webbrowser.open(f'http://127.0.0.1:{port}')
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"💡 Try a different port: python start_frontend.py {port + 1}")
        else:
            print(f"❌ Server error: {e}")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    start_frontend_server(port)