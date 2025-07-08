#!/usr/bin/env python3
"""
Simple test to verify the agent is working properly.
"""

import asyncio
from Agent import create_health_agent
from Context import UserSessionContext
from agents import Runner

async def test_agent():
    """Test the agent with a simple message."""
    print("🧪 Testing Health Agent...")
    
    # Create agent and context
    agent = create_health_agent()
    context = UserSessionContext(name="TestUser", uid=999)
    
    print(f"✅ Agent created: {agent.name}")
    print(f"✅ Tools: {len(agent.tools)}")
    print(f"✅ Handoffs: {len(agent.handoffs)}")
    
    # Test with a simple message
    test_input = "Hello, can you help me with my health goals?"
    print(f"\n💬 Testing with: '{test_input}'")
    
    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=test_input,
            context=context
        )
        
        print("🤖 Agent response:")
        print("-" * 40)
        
        response_parts = []
        async for event in result.stream_events():
            # Print event type for debugging
            event_type = type(event).__name__
            print(f"[DEBUG] Event: {event_type}")
            
            # Try to extract response
            if hasattr(event, 'raw_item') and hasattr(event.raw_item, 'content') and event.raw_item.content:
                content = event.raw_item.content
                if isinstance(content, list):
                    for item in content:
                        if hasattr(item, 'text') and item.text:
                            response_parts.append(str(item.text))
                            print(f"📝 Response part: {item.text}")
                elif isinstance(content, str):
                    response_parts.append(content)
                    print(f"📝 Response part: {content}")
            
            # Check for tool usage
            if hasattr(event, 'tool_name') and hasattr(event, 'tool_output'):
                print(f"🔧 Tool: {event.tool_name}")
        
        # Combine response parts
        full_response = " ".join(response_parts)
        if full_response.strip():
            print(f"\n✅ SUCCESS! Agent responded: {full_response[:100]}...")
            return True
        else:
            print("\n❌ FAILED! No response generated.")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent())
    if success:
        print("\n🎉 Agent test PASSED!")
    else:
        print("\n💥 Agent test FAILED!") 