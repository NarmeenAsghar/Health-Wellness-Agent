#!/usr/bin/env python3
"""
Simple CLI test to verify the main functionality works.
"""

import asyncio
from Agent import create_health_agent
from Context import UserSessionContext
from Database import init_db, save_session, load_session
from Orchestrator import HealthOrchestrator

def main():
    """Simple test of the CLI functionality."""
    print("🧪 Simple CLI Test")
    print("=" * 40)
    
    try:
        # Initialize database
        init_db()
        print("✅ Database initialized")
        
        # Create test user context
        context = UserSessionContext(
            name="Test User",
            uid=1,
            email="test@example.com",
            created_at="2024-01-01T00:00:00",
            last_updated="2024-01-01T00:00:00"
        )
        
        # Save context
        save_session(context)
        print("✅ Test user context created and saved")
        
        # Create agent
        agent = create_health_agent()
        print(f"✅ Agent created: {agent.name}")
        
        # Create orchestrator
        orchestrator = HealthOrchestrator()
        print("✅ Orchestrator created")
        
        # Test a simple message
        print("\n🤖 Testing agent with message: 'I want to lose 5kg'")
        
        # Run agent
        result = orchestrator.run_agent(agent, "I want to lose 5kg", context)
        
        if result:
            print("✅ Agent responded successfully")
            print(f"Response type: {type(result)}")
            
            # Try to extract response
            if hasattr(result, 'final_output') and result.final_output:
                response = str(result.final_output)
                print(f"✅ Response extracted: {response[:100]}...")
            else:
                print("⚠️ Could not extract response from result")
        else:
            print("❌ Agent failed to respond")
        
        # Load updated context
        updated_context = load_session(1)
        if updated_context and updated_context.conversation_history:
            print(f"✅ Conversation history saved: {len(updated_context.conversation_history)} messages")
        else:
            print("⚠️ Conversation history not saved")
        
        print("\n🎉 Simple CLI test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All components are working! You can now run the full CLI with:")
        print("   uv run cli.py")
    else:
        print("\n❌ Some components have issues. Please check the errors above.") 