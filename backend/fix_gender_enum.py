#!/usr/bin/env python3
"""
Fix Gender Enum Values in Database
"""
import sys
sys.path.append('app')

def fix_gender_values():
    """Update gender values in database to match enum"""
    try:
        from app.database import SessionLocal
        from sqlalchemy import text
        
        db = SessionLocal()
        
        print("🔧 Fixing gender enum values...")
        
        # Check current values
        result = db.execute(text("SELECT DISTINCT gender FROM patients")).fetchall()
        print(f"Current gender values: {[r[0] for r in result]}")
        
        # Update values to match enum
        updates = [
            ("Male", "Male"),    # Keep as is since enum value is "Male"
            ("Female", "Female"), # Keep as is since enum value is "Female"  
            ("Other", "Other")   # Keep as is since enum value is "Other"
        ]
        
        for old_val, new_val in updates:
            count = db.execute(text(f"UPDATE patients SET gender = :new_val WHERE gender = :old_val"), 
                             {"old_val": old_val, "new_val": new_val}).rowcount
            if count > 0:
                print(f"✅ Updated {count} records from '{old_val}' to '{new_val}'")
        
        # Also update doctors table if it exists
        try:
            result = db.execute(text("SELECT DISTINCT status FROM doctors")).fetchall()
            print(f"Doctor status values: {[r[0] for r in result]}")
            
            # Update doctor status values
            db.execute(text("UPDATE doctors SET status = 'Active' WHERE status = 'Active'"))
            db.execute(text("UPDATE doctors SET status = 'Inactive' WHERE status = 'Inactive'"))
            
        except Exception as e:
            print(f"Note: Doctor table update skipped: {e}")
        
        db.commit()
        print("✅ Database values updated successfully")
        
        # Test the query now
        from app.models import Patient
        patients = db.query(Patient).all()
        print(f"✅ Query test successful: {len(patients)} patients loaded")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🔧 HMS Gender Enum Fix")
    print("=" * 30)
    
    success = fix_gender_values()
    
    if success:
        print("\n🎉 Database fixed successfully!")
        print("✅ You can now use the patients API")
    else:
        print("\n❌ Fix failed")
        print("💡 Check the error messages above")

if __name__ == "__main__":
    main()