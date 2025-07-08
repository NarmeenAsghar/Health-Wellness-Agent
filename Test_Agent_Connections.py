#!/usr/bin/env python3
"""
Test script to verify agent connections and tools are working properly.
"""

import asyncio
from Agent import create_health_agent
from Context import UserSessionContext
from agents import Runner

async def test_agent_connections():
    """Test that the agent can be created and responds properly."""
    print("🔍 Testing Agent Connections...")
    
    # Test 1: Create agent
    try:
        agent = create_health_agent()
        print(f"✅ Agent created successfully: {agent.name}")
        print(f"   Tools: {len(agent.tools)}")
        print(f"   Handoffs: {len(agent.handoffs)}")
        
        # List tools
        for i, tool in enumerate(agent.tools):
            print(f"   Tool {i+1}: {tool.name}")
            
        # List handoffs
        for handoff_name, handoff_agent in agent.handoffs.items():
            print(f"   Handoff '{handoff_name}': {handoff_agent.name}")
            
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        return False
    
    # Test 2: Test basic response
    try:
        context = UserSessionContext(name="TestUser", uid=999)
        print(f"\n🧪 Testing agent response...")
        
        result = await Runner.run(
            starting_agent=agent,
            input="Hello, can you help me with my health goals?",
            context=context
        )
        
        # Extract response from final_output (non-streaming approach)
        if hasattr(result, 'final_output') and result.final_output:
            response_text = str(result.final_output)
            print(f"✅ Agent responded: {response_text.strip()[:100]}...")
            return True
        elif hasattr(result, 'output') and result.output:
            response_text = str(result.output)
            print(f"✅ Agent responded: {response_text.strip()[:100]}...")
            return True
        else:
            print("❌ Agent did not generate a response")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test agent response: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_connections())
    if success:
        print("\n🎉 All agent connections are working properly!")
    else:
        print("\n💥 Agent connections have issues that need to be fixed.") 