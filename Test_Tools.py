#!/usr/bin/env python3
"""
Test script to verify all tools provide real, meaningful responses.
"""

from Goal_Analyzer import analyze_goal
from Meal_Planner import meal_planner
from Workout_Recommender import workout_recommender
from Scheduler import checkin_scheduler
from Tracker import progress_tracker

def test_all_tools():
    """Test all tools to ensure they provide real responses."""
    print("🧪 Testing All Tools for Real Responses")
    print("=" * 50)
    
    # Test 1: Goal Analyzer
    print("\n1️⃣ Testing Goal Analyzer:")
    print("-" * 30)
    test_goals = [
        "I want to lose 5kg in 2 months",
        "Build muscle and gain 10 pounds in 3 months",
        "Improve endurance for running"
    ]
    
    for goal in test_goals:
        print(f"\nGoal: {goal}")
        result = analyze_goal(goal)
        print(f"Analysis: {result}")
        if "Sample" in str(result) or "TODO" in str(result):
            print("❌ Still returning generic response!")
        else:
            print("✅ Providing real analysis!")
    
    # Test 2: Meal Planner
    print("\n2️⃣ Testing Meal Planner:")
    print("-" * 30)
    test_diets = ["vegetarian", "vegan", "keto", "mediterranean"]
    
    for diet in test_diets:
        print(f"\nDiet: {diet}")
        result = meal_planner(diet)
        print(f"Meal Plan: {len(result.get('days', []))} days")
        if result.get('days'):
            first_meal = result['days'][0]
            print(f"Sample: {first_meal[:100]}...")
            if "Sample Meal" in first_meal:
                print("❌ Still returning generic response!")
            else:
                print("✅ Providing real meal plan!")
    
    # Test 3: Workout Recommender
    print("\n3️⃣ Testing Workout Recommender:")
    print("-" * 30)
    test_workout_goals = ["lose weight", "build muscle", "improve endurance"]
    
    for goal in test_workout_goals:
        print(f"\nGoal: {goal}")
        result = workout_recommender(goal)
        print(f"Workout Plan: {len(result.get('days', []))} days")
        if result.get('days'):
            first_workout = result['days'][0]
            print(f"Sample: {first_workout[:100]}...")
            if "Sample Workout" in first_workout:
                print("❌ Still returning generic response!")
            else:
                print("✅ Providing real workout plan!")
    
    # Test 4: Scheduler
    print("\n4️⃣ Testing Scheduler:")
    print("-" * 30)
    result = checkin_scheduler(1)
    print(f"Scheduler Result: {result}")
    if "scheduled" in str(result) and "next_checkin" in str(result):
        print("✅ Providing real scheduling info!")
    else:
        print("❌ Still returning generic response!")
    
    # Test 5: Progress Tracker
    print("\n5️⃣ Testing Progress Tracker:")
    print("-" * 30)
    test_updates = [
        "Lost 2kg this week",
        "Completed all workouts",
        "Feeling more energetic"
    ]
    
    for update in test_updates:
        print(f"\nUpdate: {update}")
        result = progress_tracker(1, update)
        print(f"Tracker Result: {result}")
        if "motivational_message" in str(result):
            print("✅ Providing real progress tracking!")
        else:
            print("❌ Still returning generic response!")
    
    print("\n" + "=" * 50)
    print("🎉 Tool Testing Complete!")
    print("\nAll tools should now provide real, meaningful responses instead of generic 'Sample' responses.")

if __name__ == "__main__":
    test_all_tools() 