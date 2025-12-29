#!/usr/bin/env python3
"""
Test Voucher Page Design
"""
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8000"

def test_voucher_page_design():
    """Test voucher page design elements"""
    print("🎨 Testing Voucher Page Design")
    print("=" * 40)
    
    try:
        # Get the voucher page
        response = requests.get(f"{BASE_URL}/vouchers.html")
        if response.status_code != 200:
            print(f"❌ Failed to load voucher page: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Test 1: Check for sidebar and topbar
        sidebar = soup.find('div', {'class': 'sidebar', 'id': 'sidebar'})
        topbar = soup.find('div', {'class': 'topbar', 'id': 'topbar'})
        
        if sidebar and topbar:
            print("✅ Sidebar and topbar elements found")
        else:
            print("❌ Missing sidebar or topbar elements")
        
        # Test 2: Check for main-content wrapper
        main_content = soup.find('div', {'class': 'main-content'})
        if main_content:
            print("✅ Main content wrapper found")
        else:
            print("❌ Missing main content wrapper")
        
        # Test 3: Check for stats-grid
        stats_grid = soup.find('div', {'class': 'stats-grid'})
        if stats_grid:
            print("✅ Stats grid found")
        else:
            print("❌ Missing stats grid")
        
        # Test 4: Check for voucher table
        voucher_table = soup.find('table', {'class': 'voucher-table'})
        if voucher_table:
            print("✅ Voucher table found")
        else:
            print("❌ Missing voucher table")
        
        # Test 5: Check for modals
        create_modal = soup.find('div', {'id': 'createVoucherModal'})
        view_modal = soup.find('div', {'id': 'viewVoucherModal'})
        
        if create_modal and view_modal:
            print("✅ Voucher modals found")
        else:
            print("❌ Missing voucher modals")
        
        # Test 6: Check for correct script includes
        scripts = soup.find_all('script')
        script_sources = [script.get('src') for script in scripts if script.get('src')]
        
        if '/static/js/common.js' in script_sources and '/static/js/vouchers.js' in script_sources:
            print("✅ Correct script files included")
        else:
            print("❌ Missing or incorrect script files")
            print(f"Found scripts: {script_sources}")
        
        # Test 7: Check for CSS link
        css_links = soup.find_all('link', {'rel': 'stylesheet'})
        css_hrefs = [link.get('href') for link in css_links]
        
        if '/static/css/styles.css' in css_hrefs:
            print("✅ Correct CSS file included")
        else:
            print("❌ Missing or incorrect CSS file")
            print(f"Found CSS: {css_hrefs}")
        
        print("\n🎉 Voucher page design testing completed!")
        
    except Exception as e:
        print(f"❌ Error testing voucher page: {e}")

if __name__ == "__main__":
    test_voucher_page_design()