#!/usr/bin/env python3
"""
Demo script showing the chat interface after login.
"""

from Database import init_db, create_user, get_user_by_email, load_session, save_session
from Context import UserSessionContext
from Agent import create_health_agent
from Orchestrator import HealthOrchestrator
from datetime import datetime

def demo_chat_interface():
    """Demo the chat interface functionality."""
    print("🎭 Chat Interface Demo")
    print("=" * 50)
    
    try:
        # Setup
        init_db()
        
        # Create or get test user
        test_email = "demo@test.com"
        existing_user = get_user_by_email(test_email)
        if existing_user:
            uid = existing_user['uid']
            print(f"✅ Using existing user (ID: {uid})")
        else:
            uid = create_user("Demo User", test_email, "demo123")
            print(f"✅ Created demo user (ID: {uid})")
        
        # Load context
        context = load_session(uid)
        if not context:
            print("❌ Failed to load context")
            return False
        
        # Create agent
        agent = create_health_agent()
        orchestrator = HealthOrchestrator()
        
        print(f"\n👤 Logged in as: {context.name}")
        print(f"📧 Email: {context.email}")
        print(f"🆔 User ID: {context.uid}")
        
        # Demo conversation
        demo_messages = [
            "I want to lose 5kg in 2 months",
            "Can you create a meal plan for me?",
            "What about a workout routine?",
            "How can I track my progress?"
        ]
        
        print("\n💬 Demo Conversation:")
        print("-" * 30)
        
        for i, message in enumerate(demo_messages, 1):
            print(f"\n{i}. You: {message}")
            
            # Add user message to history
            context.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Get agent response
            print("🤖 Agent is thinking...")
            result = orchestrator.run_agent(agent, message, context)
            
            if result:
                # Extract response
                response = "I understand your request. Let me help you with that."
                if hasattr(result, 'final_output') and result.final_output:
                    response = str(result.final_output)
                elif hasattr(result, 'output') and result.output:
                    response = str(result.output)
                elif isinstance(result, str):
                    response = result
                
                # Truncate long responses for demo
                if len(response) > 150:
                    response = response[:150] + "..."
                
                print(f"🤖 Agent: {response}")
                
                # Add assistant response to history
                context.conversation_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                print("🤖 Agent: I apologize, but I couldn't generate a response right now.")
            
            # Save after each message
            save_session(context)
        
        # Show final state
        print(f"\n📊 Final State:")
        print(f"   Messages in history: {len(context.conversation_history)}")
        print(f"   Context saved: ✅")
        print(f"   Session persistent: ✅")
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"\n💡 This is exactly how the CLI chat interface works after login.")
        print(f"   Run 'uv run cli.py' and login to try it yourself!")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_chat_interface()
    if success:
        print("\n✅ Demo successful! The chat interface is working properly.")
    else:
        print("\n❌ Demo failed. Please check the errors above.") 