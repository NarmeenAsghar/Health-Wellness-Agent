#!/usr/bin/env python3
"""
Create a test user for testing the chat functionality.
"""

from Database import init_db, create_user, get_user_by_email
from Context import UserSessionContext

def create_test_user():
    """Create a test user for testing."""
    print("🧪 Creating test user...")
    
    try:
        # Initialize database
        init_db()
        print("✅ Database initialized")
        
        # Test user details
        test_name = "Test User"
        test_email = "test@example.com"
        test_password = "test123"
        
        # Check if user already exists
        existing_user = get_user_by_email(test_email)
        if existing_user:
            print(f"✅ Test user already exists (ID: {existing_user['uid']})")
            return existing_user['uid']
        
        # Create new test user
        uid = create_user(test_name, test_email, test_password)
        print(f"✅ Test user created successfully!")
        print(f"   Name: {test_name}")
        print(f"   Email: {test_email}")
        print(f"   Password: {test_password}")
        print(f"   User ID: {uid}")
        
        return uid
        
    except Exception as e:
        print(f"❌ Failed to create test user: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    uid = create_test_user()
    if uid:
        print(f"\n🎉 Test user ready! You can now login with:")
        print(f"   Email: test@example.com")
        print(f"   Password: test123")
        print(f"   Or User ID: {uid}")
        print(f"\nRun: uv run cli.py")
    else:
        print("\n❌ Failed to create test user.") 