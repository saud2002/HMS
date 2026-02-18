"""
Test database connection and check tables
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, test_connection
from sqlalchemy import text, inspect

def main():
    print("=" * 60)
    print("HMS Database Connection Test")
    print("=" * 60)
    
    # Test 1: Basic connection
    print("\n1. Testing database connection...")
    if test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
        return
    
    # Test 2: Check database exists
    print("\n2. Checking database...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()[0]
            print(f"✅ Connected to database: {db_name}")
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return
    
    # Test 3: List all tables
    print("\n3. Checking tables...")
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("⚠️ No tables found in database!")
            print("   Run 'python init_database.py' to create tables")
    except Exception as e:
        print(f"❌ Error listing tables: {e}")
        return
    
    # Test 4: Check specific tables
    print("\n4. Checking required tables...")
    required_tables = ['patients', 'doctors', 'appointments', 'bills', 'users']
    missing_tables = []
    
    for table in required_tables:
        if table in tables:
            print(f"✅ {table} table exists")
        else:
            print(f"❌ {table} table missing")
            missing_tables.append(table)
    
    if missing_tables:
        print(f"\n⚠️ Missing tables: {', '.join(missing_tables)}")
        print("   Run 'python init_database.py' to create missing tables")
    
    # Test 5: Count records in key tables
    print("\n5. Checking data...")
    try:
        with engine.connect() as conn:
            for table in ['patients', 'doctors', 'appointments']:
                if table in tables:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"   {table}: {count} records")
    except Exception as e:
        print(f"⚠️ Error counting records: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
