#!/usr/bin/env python3
"""
Check Voucher Table Schema
"""
import pymysql

def check_voucher_table():
    """Check voucher table schema"""
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='hms'
        )
        cursor = conn.cursor()
        
        # Check if voucher table exists
        cursor.execute("SHOW TABLES LIKE 'vouchers'")
        result = cursor.fetchall()
        print(f"Voucher tables found: {result}")
        
        if result:
            # Show table structure
            cursor.execute("DESC vouchers")
            columns = cursor.fetchall()
            print("\nCurrent voucher table structure:")
            for col in columns:
                print(f"  {col[0]} - {col[1]} - {col[2]} - {col[3]} - {col[4]} - {col[5]}")
            
            # Drop the table
            print("\nDropping existing voucher table...")
            cursor.execute("DROP TABLE vouchers")
            conn.commit()
            print("✅ Voucher table dropped")
        else:
            print("No voucher table found")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_voucher_table()