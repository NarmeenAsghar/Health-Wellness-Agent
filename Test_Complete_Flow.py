#!/usr/bin/env python3
"""
Complete flow test - from user creation to chat functionality.
"""

import asyncio
from Database import init_db, create_user, get_user_by_email, load_session, save_session
from Context import UserSessionContext
from Agent import create_health_agent
from Orchestrator import HealthOrchestrator

def test_complete_flow():
    """Test the complete flow from user creation to chat."""
    print("🧪 Testing Complete Flow")
    print("=" * 50)
    
    try:
        # 1. Initialize database
        print("1️⃣ Initializing database...")
        init_db()
        print("✅ Database initialized")
        
        # 2. Create test user
        print("\n2️⃣ Creating test user...")
        test_name = "Hamza"
        test_email = "hamza@test.com"
        test_password = "test123"
        
        # Check if user exists
        existing_user = get_user_by_email(test_email)
        if existing_user:
            print(f"✅ User already exists (ID: {existing_user['uid']})")
            uid = existing_user['uid']
        else:
            uid = create_user(test_name, test_email, test_password)
            print(f"✅ User created (ID: {uid})")
        
        # 3. Load user session
        print("\n3️⃣ Loading user session...")
        context = load_session(uid)
        if context:
            print(f"✅ Session loaded for: {context.name}")
            print(f"   Email: {context.email}")
            print(f"   UID: {context.uid}")
        else:
            print("❌ Failed to load session")
            return False
        
        # 4. Create agent and orchestrator
        print("\n4️⃣ Creating agent and orchestrator...")
        agent = create_health_agent()
        orchestrator = HealthOrchestrator()
        print(f"✅ Agent created: {agent.name}")
        print(f"✅ Orchestrator created")
        
        # 5. Test chat functionality
        print("\n5️⃣ Testing chat functionality...")
        test_message = "I want to lose 5kg in 2 months"
        print(f"🤖 Sending message: '{test_message}'")
        
        # Add user message to conversation history
        context.conversation_history.append({
            "role": "user",
            "content": test_message,
            "timestamp": "2024-01-01T10:00:00"
        })
        
        # Run agent
        result = orchestrator.run_agent(agent, test_message, context)
        
        if result:
            print("✅ Agent responded successfully")
            
            # Extract response
            response = "No response generated"
            if hasattr(result, 'final_output') and result.final_output:
                response = str(result.final_output)
            elif hasattr(result, 'output') and result.output:
                response = str(result.output)
            elif isinstance(result, str):
                response = result
            
            print(f"🤖 Agent response: {response[:100]}...")
            
            # Add assistant response to conversation history
            context.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": "2024-01-01T10:01:00"
            })
            
            # Save updated context
            save_session(context)
            print("✅ Conversation history saved")
            
        else:
            print("❌ Agent failed to respond")
            return False
        
        # 6. Test context persistence
        print("\n6️⃣ Testing context persistence...")
        reloaded_context = load_session(uid)
        if reloaded_context and reloaded_context.conversation_history:
            print(f"✅ Context persisted: {len(reloaded_context.conversation_history)} messages")
            for i, msg in enumerate(reloaded_context.conversation_history):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")[:50] + "..." if len(msg.get("content", "")) > 50 else msg.get("content", "")
                print(f"   {i+1}. [{role}]: {content}")
        else:
            print("❌ Context not persisted properly")
            return False
        
        print("\n🎉 Complete flow test passed!")
        print("\n📋 Test Results:")
        print(f"   ✅ User creation: {test_name} (ID: {uid})")
        print(f"   ✅ Session management: Working")
        print(f"   ✅ Agent communication: Working")
        print(f"   ✅ Context persistence: Working")
        print(f"   ✅ Conversation history: {len(reloaded_context.conversation_history)} messages")
        
        print(f"\n🚀 Ready to use! Login credentials:")
        print(f"   Email: {test_email}")
        print(f"   Password: {test_password}")
        print(f"   User ID: {uid}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    if success:
        print("\n✅ All systems working! You can now run:")
        print("   uv run cli.py")
        print("\nThen login with:")
        print("   Email: hamza@test.com")
        print("   Password: test123")
    else:
        print("\n❌ Some systems have issues. Please check the errors above.") 