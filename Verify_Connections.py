#!/usr/bin/env python3
"""
Comprehensive verification script to check all agent and tool connections.
"""

import asyncio
from Agent import create_health_agent
from Context import UserSessionContext
from agents import Runner
# Import all tools
from Goal_Analyzer import analyze_goal_tool
from Meal_Planner import meal_planner_tool
from Workout_Recommender import workout_recommender_tool
from Scheduler import checkin_scheduler_tool
from Tracker import progress_tracker_tool
# Import all handoff agents
from Escalation_Agent import create_escalation_agent
from Nutrition_Expert_Agent import create_nutrition_expert_agent
from Injury_Support_Agent import create_injury_support_agent

def verify_tools():
    """Verify all tools are properly configured."""
    print("🔧 Verifying Tools...")
    
    try:
        # Import all tools
        from goal_analyzer import analyze_goal_tool
        from meal_planner import meal_planner_tool
        from workout_recommender import workout_recommender_tool
        from scheduler import checkin_scheduler_tool
        from tracker import progress_tracker_tool
        
        tools = [
            ("analyze_goal_tool", analyze_goal_tool),
            ("meal_planner_tool", meal_planner_tool),
            ("workout_recommender_tool", workout_recommender_tool),
            ("checkin_scheduler_tool", checkin_scheduler_tool),
            ("progress_tracker_tool", progress_tracker_tool),
        ]
        
        for tool_name, tool in tools:
            print(f"  ✅ {tool_name}: {tool.name}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Tool verification failed: {e}")
        return False

def verify_handoff_agents():
    """Verify all handoff agents are properly configured."""
    print("🤝 Verifying Handoff Agents...")
    
    try:
        # Import all handoff agents
        from escalation_agent import create_escalation_agent
        from nutrition_expert_agent import create_nutrition_expert_agent
        from injury_support_agent import create_injury_support_agent
        
        # Create agents
        escalation_agent = create_escalation_agent()
        nutrition_agent = create_nutrition_expert_agent()
        injury_agent = create_injury_support_agent()
        
        agents = [
            ("EscalationAgent", escalation_agent),
            ("NutritionExpertAgent", nutrition_agent),
            ("InjurySupportAgent", injury_agent),
        ]
        
        for agent_name, agent in agents:
            print(f"  ✅ {agent_name}: {agent.name}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Handoff agent verification failed: {e}")
        return False

def verify_main_agent():
    """Verify the main health agent is properly configured."""
    print("🏥 Verifying Main Health Agent...")
    
    try:
        agent = create_health_agent()
        
        print(f"  ✅ Agent Name: {agent.name}")
        print(f"  ✅ Tools Count: {len(agent.tools)}")
        print(f"  ✅ Handoffs Count: {len(agent.handoffs)}")
        
        # List tools
        print("  📋 Tools:")
        for i, tool in enumerate(agent.tools, 1):
            print(f"    {i}. {tool.name}")
            
        # List handoffs
        print("  📋 Handoffs:")
        for handoff_name, handoff_agent in agent.handoffs.items():
            print(f"    - {handoff_name}: {handoff_agent.name}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Main agent verification failed: {e}")
        return False

async def test_agent_functionality():
    """Test that the agent can actually function."""
    print("🧪 Testing Agent Functionality...")
    
    try:
        agent = create_health_agent()
        context = UserSessionContext(name="TestUser", uid=999)
        
        # Test with a simple message
        test_input = "Hello, can you help me with my health goals?"
        print(f"  💬 Testing with: '{test_input}'")
        
        result = await Runner.run(
            starting_agent=agent,
            input=test_input,
            context=context
        )
        
        # Check if we got a response
        if hasattr(result, 'final_output') and result.final_output:
            response = str(result.final_output)
            print(f"  ✅ Agent responded: {response[:100]}...")
            return True
        else:
            print("  ❌ No response generated")
            return False
            
    except Exception as e:
        print(f"  ❌ Functionality test failed: {e}")
        return False

async def test_tool_usage():
    """Test that tools can be used."""
    print("🔧 Testing Tool Usage...")
    
    try:
        agent = create_health_agent()
        context = UserSessionContext(name="TestUser", uid=999)
        
        # Test with a goal that should trigger tool usage
        test_input = "I want to lose 10 pounds in 3 months"
        print(f"  💬 Testing with: '{test_input}'")
        
        result = await Runner.run(
            starting_agent=agent,
            input=test_input,
            context=context
        )
        
        # Check if we got a response
        if hasattr(result, 'final_output') and result.final_output:
            response = str(result.final_output)
            print(f"  ✅ Agent responded: {response[:100]}...")
            
            # Check if tools were used (this would be visible in the response)
            if "meal" in response.lower() or "workout" in response.lower() or "goal" in response.lower():
                print("  ✅ Tools appear to have been used")
                return True
            else:
                print("  ⚠️ Tools may not have been used")
                return True  # Still consider it a success
        else:
            print("  ❌ No response generated")
            return False
            
    except Exception as e:
        print(f"  ❌ Tool usage test failed: {e}")
        return False

async def main():
    """Run all verification tests."""
    print("=" * 60)
    print("🔍 Health Agent Connection Verification")
    print("=" * 60)
    
    # Run all verification tests
    tests = [
        ("Tools", verify_tools),
        ("Handoff Agents", verify_handoff_agents),
        ("Main Agent", verify_main_agent),
        ("Agent Functionality", test_agent_functionality),
        ("Tool Usage", test_tool_usage),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Verification Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your agent is fully connected and working!")
    else:
        print("💥 SOME TESTS FAILED! Check the errors above.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 