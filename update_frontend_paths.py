#!/usr/bin/env python3
"""
Update Frontend Paths for Integrated Server
"""
import os
import re
from pathlib import Path

def update_html_file(file_path):
    """Update paths in HTML file"""
    print(f"Updating {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update CSS paths
    content = re.sub(r'href="css/', r'href="/static/css/', content)
    
    # Update JS paths
    content = re.sub(r'src="js/', r'src="/static/js/', content)
    
    # Update navigation links to work with integrated server
    content = re.sub(r'href="([^"]+\.html)"', r'href="/\1"', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {file_path}")

def main():
    """Update all HTML files"""
    print("🔧 Updating Frontend Paths for Integrated Server")
    print("=" * 50)
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Find all HTML files
    html_files = list(frontend_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found")
        return False
    
    # Update each file
    for html_file in html_files:
        update_html_file(html_file)
    
    print(f"\n✅ Updated {len(html_files)} HTML files")
    print("🎉 Frontend is now ready for integrated server!")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)