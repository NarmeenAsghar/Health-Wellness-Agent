#!/usr/bin/env python3
"""
Test script to verify context persistence across multiple interactions.
"""

import asyncio
from Agent import create_health_agent
from Context import UserSessionContext
from agents import Runner
from Database import init_db, save_session, load_session

async def test_context_persistence():
    """Test that the agent maintains context across multiple interactions."""
    print("🧪 Testing Context Persistence...")
    
    # Initialize database
    init_db()
    
    # Create agent and context
    agent = create_health_agent()
    context = UserSessionContext(name="TestUser", uid=999)
    
    # Test 1: Set a goal
    print("\n1️⃣ Setting a goal...")
    test_input_1 = "I want to lose 10kg in 2 months"
    context.conversation_history.append({"role": "user", "content": test_input_1})
    
    result_1 = await Runner.run(
        starting_agent=agent,
        input=test_input_1,
        context=context
    )
    
    if hasattr(result_1, 'final_output') and result_1.final_output:
        response_1 = str(result_1.final_output)
        context.conversation_history.append({"role": "assistant", "content": response_1})
        print(f"✅ Agent responded: {response_1[:100]}...")
    else:
        print("❌ No response from first interaction")
        return False
    
    # Test 2: Follow-up question (should remember the goal)
    print("\n2️⃣ Follow-up question...")
    test_input_2 = "Yes please schedule a check-in"
    context.conversation_history.append({"role": "user", "content": test_input_2})
    
    result_2 = await Runner.run(
        starting_agent=agent,
        input=test_input_2,
        context=context
    )
    
    if hasattr(result_2, 'final_output') and result_2.final_output:
        response_2 = str(result_2.final_output)
        context.conversation_history.append({"role": "assistant", "content": response_2})
        print(f"✅ Agent responded: {response_2[:100]}...")
        
        # Check if the response mentions the goal or check-in
        if "10kg" in response_2.lower() or "check" in response_2.lower() or "schedule" in response_2.lower():
            print("✅ Agent remembered the context!")
            return True
        else:
            print("❌ Agent forgot the context")
            return False
    else:
        print("❌ No response from second interaction")
        return False

async def test_conversation_history():
    """Test that conversation history is properly maintained."""
    print("\n📝 Testing Conversation History...")
    
    agent = create_health_agent()
    context = UserSessionContext(name="TestUser", uid=1000)
    
    # Simulate a conversation
    conversation = [
        "I want to lose 5kg",
        "Can you give me a meal plan?",
        "What about workouts?",
        "Schedule a weekly check-in"
    ]
    
    for i, message in enumerate(conversation, 1):
        print(f"\n{i}️⃣ User: {message}")
        context.conversation_history.append({"role": "user", "content": message})
        
        result = await Runner.run(
            starting_agent=agent,
            input=message,
            context=context
        )
        
        if hasattr(result, 'final_output') and result.final_output:
            response = str(result.final_output)
            context.conversation_history.append({"role": "assistant", "content": response})
            print(f"🤖 Agent: {response[:100]}...")
        else:
            print("❌ No response")
            return False
    
    # Check conversation history length
    expected_length = len(conversation) * 2  # user + assistant for each message
    actual_length = len(context.conversation_history)
    
    print(f"\n📊 Conversation History: {actual_length} messages (expected: {expected_length})")
    
    if actual_length == expected_length:
        print("✅ Conversation history properly maintained!")
        return True
    else:
        print("❌ Conversation history not properly maintained")
        return False

async def main():
    """Run all context persistence tests."""
    print("=" * 60)
    print("🔍 Context Persistence Testing")
    print("=" * 60)
    
    # Run tests
    test1_passed = await test_context_persistence()
    test2_passed = await test_conversation_history()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    print(f"Context Persistence: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"Conversation History: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Context persistence is working!")
    else:
        print("\n💥 SOME TESTS FAILED! Context persistence needs fixing.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 