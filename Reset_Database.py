#!/usr/bin/env python3
"""
Reset database script to ensure correct schema.
"""

import os
import sqlite3
from Database import DB_PATH

def reset_database():
    """Reset the database with correct schema."""
    print("🗄️ Resetting database...")
    
    try:
        # Remove existing database file
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print(f"✅ Removed existing database: {DB_PATH}")
        
        # Recreate database with correct schema
        from Database import init_db
        init_db()
        print("✅ Database recreated with correct schema")
        
        # Verify tables exist
        with sqlite3.connect(DB_PATH) as conn:
            # Check sessions table
            cursor = conn.execute("PRAGMA table_info(sessions)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"✅ Sessions table columns: {columns}")
            
            # Check users table
            cursor = conn.execute("PRAGMA table_info(users)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"✅ Users table columns: {columns}")
        
        print("🎉 Database reset completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database reset failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = reset_database()
    if success:
        print("\n✅ Database is ready! You can now run:")
        print("   uv run cli.py")
    else:
        print("\n❌ Database reset failed. Please check the errors above.") 