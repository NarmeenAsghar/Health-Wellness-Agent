#!/usr/bin/env python3
"""
Test script to verify all components are working correctly.
"""

import sys
import traceback
from datetime import datetime
from Context import UserSessionContext
from Database import init_db, create_user, get_user_by_email, save_session, load_session
from Agent import create_health_agent
from Orchestrator import HealthOrchestrator, update_context_after_tool
from PDF_Report import generate_user_report
from Goal_Analyzer import analyze_goal_tool
from Meal_Planner import meal_planner_tool
from Workout_Recommender import workout_recommender_tool
from Scheduler import checkin_scheduler_tool
from Tracker import progress_tracker_tool
from Escalation_Agent import create_escalation_agent
from Nutrition_Expert_Agent import create_nutrition_expert_agent
from Injury_Support_Agent import create_injury_support_agent

def test_imports():
    """Test all imports."""
    print("🔍 Testing imports...")
    
    try:
        from Context import UserSessionContext
        print("✅ context.py - UserSessionContext imported")
    except Exception as e:
        print(f"❌ context.py - Error: {e}")
        return False
    
    try:
        from Database import init_db, create_user, get_user_by_email, save_session, load_session
        print("✅ db.py - Database functions imported")
    except Exception as e:
        print(f"❌ db.py - Error: {e}")
        return False
    
    try:
        from Agent import create_health_agent
        print("✅ agent.py - create_health_agent imported")
    except Exception as e:
        print(f"❌ agent.py - Error: {e}")
        return False
    
    try:
        from Orchestrator import HealthOrchestrator, update_context_after_tool
        print("✅ orchestrator.py - HealthOrchestrator imported")
    except Exception as e:
        print(f"❌ orchestrator.py - Error: {e}")
        return False
    
    try:
        from PDF_Report import generate_user_report
        print("✅ pdf_report.py - generate_user_report imported")
    except Exception as e:
        print(f"❌ pdf_report.py - Error: {e}")
        return False
    
    try:
        from Goal_Analyzer import analyze_goal_tool
        from Meal_Planner import meal_planner_tool
        from Workout_Recommender import workout_recommender_tool
        from Scheduler import checkin_scheduler_tool
        from Tracker import progress_tracker_tool
        print("✅ All tool modules imported")
    except Exception as e:
        print(f"❌ Tool modules - Error: {e}")
        return False
    
    try:
        from Escalation_Agent import create_escalation_agent
        from Nutrition_Expert_Agent import create_nutrition_expert_agent
        from Injury_Support_Agent import create_injury_support_agent
        print("✅ All agent creation modules imported")
    except Exception as e:
        print(f"❌ Agent creation modules - Error: {e}")
        return False
    
    return True

def test_database():
    """Test database operations."""
    print("\n🗄️ Testing database operations...")
    
    try:
        from Database import init_db, create_user, get_user_by_email, save_session, load_session
        from Context import UserSessionContext
        
        # Initialize database
        init_db()
        print("✅ Database initialized")
        
        # Test user creation
        test_email = "test@example.com"
        test_name = "Test User"
        
        # Check if user exists
        existing_user = get_user_by_email(test_email)
        if existing_user:
            print(f"✅ User {test_email} already exists (ID: {existing_user['uid']})")
            uid = existing_user['uid']
        else:
            uid = create_user(test_name, test_email, "testpassword")
            print(f"✅ User created with ID: {uid}")
        
        # Test session loading
        context = load_session(uid)
        if context:
            print(f"✅ Session loaded for user: {context.name}")
        else:
            print("❌ Failed to load session")
            return False
        
        # Test session saving
        context.goal = {"description": "Test goal", "target": "5kg"}
        save_session(context)
        print("✅ Session saved successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        traceback.print_exc()
        return False

def test_agent_creation():
    """Test agent creation."""
    print("\n🤖 Testing agent creation...")
    
    try:
        from Agent import create_health_agent
        
        agent = create_health_agent()
        print(f"✅ Agent created: {agent.name}")
        print(f"✅ Tools: {len(agent.tools)}")
        print(f"✅ Handoffs: {len(agent.handoffs)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        traceback.print_exc()
        return False

def test_orchestrator():
    """Test orchestrator."""
    print("\n🎼 Testing orchestrator...")
    
    try:
        from Orchestrator import HealthOrchestrator
        from Agent import create_health_agent
        from Context import UserSessionContext
        
        orchestrator = HealthOrchestrator()
        agent = create_health_agent()
        context = UserSessionContext(name="Test User", uid=1)
        
        print("✅ Orchestrator created")
        print("✅ Agent and context ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        traceback.print_exc()
        return False

def test_tools():
    """Test individual tools."""
    print("\n🔧 Testing tools...")
    
    try:
        from Goal_Analyzer import analyze_goal_tool
        from Meal_Planner import meal_planner_tool
        from Workout_Recommender import workout_recommender_tool
        from Scheduler import checkin_scheduler_tool
        from Tracker import progress_tracker_tool
        
        # Test goal analyzer
        goal_result = analyze_goal_tool.func("lose 5kg in 2 months")
        print(f"✅ Goal analyzer: {goal_result}")
        
        # Test meal planner
        meal_result = meal_planner_tool.func("vegetarian")
        print(f"✅ Meal planner: {meal_result}")
        
        # Test workout recommender
        workout_result = workout_recommender_tool.func("lose weight")
        print(f"✅ Workout recommender: {workout_result}")
        
        # Test scheduler
        schedule_result = checkin_scheduler_tool.func(1)
        print(f"✅ Scheduler: {schedule_result}")
        
        # Test tracker
        track_result = progress_tracker_tool.func(1, "Lost 1kg this week")
        print(f"✅ Tracker: {track_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        traceback.print_exc()
        return False

def test_pdf_report():
    """Test PDF report generation."""
    print("\n📊 Testing PDF report generation...")
    
    try:
        from PDF_Report import generate_user_report
        from Context import UserSessionContext
        
        # Create test context
        context = UserSessionContext(
            name="Test User",
            uid=999,
            email="test@example.com",
            goal={"description": "Lose 5kg", "target": "5kg"},
            diet_preferences="Vegetarian",
            workout_plan={"days": ["Day 1: Cardio", "Day 2: Strength"]},
            meal_plan=["Day 1: Oatmeal", "Day 2: Salad"],
            progress_logs=[{"date": "2024-01-01", "weight": "70kg"}],
            conversation_history=[
                {"role": "user", "content": "I want to lose weight", "timestamp": "2024-01-01T10:00:00"},
                {"role": "assistant", "content": "I'll help you create a plan", "timestamp": "2024-01-01T10:01:00"}
            ],
            created_at="2024-01-01T00:00:00",
            last_updated="2024-01-01T10:00:00"
        )
        
        # Generate report
        report_path = generate_user_report(context)
        print(f"✅ PDF report generated: {report_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF report test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 Health Agent Component Test Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("Agent Creation", test_agent_creation),
        ("Orchestrator", test_orchestrator),
        ("Tools", test_tools),
        ("PDF Report", test_pdf_report),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 