#!/usr/bin/env python3
"""
Initialize Voucher Table for HMS
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models.voucher import Voucher

def init_voucher_table():
    """Initialize voucher table"""
    try:
        print("🔄 Creating voucher table...")
        
        # Create the voucher table
        Voucher.__table__.create(engine, checkfirst=True)
        
        print("✅ Voucher table created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating voucher table: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🏥 HMS Voucher Table Initialization")
    print("=" * 50)
    
    success = init_voucher_table()
    
    if success:
        print("\n✅ Voucher system is ready!")
        print("You can now:")
        print("- Create doctor payment vouchers")
        print("- Create hospital expense vouchers") 
        print("- Create adjustment vouchers")
        print("- Manage voucher approval workflow")
    else:
        print("\n❌ Voucher table initialization failed!")
        sys.exit(1)