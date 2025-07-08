from typing import TypedDict
from agents.tool import function_tool
from Guardrails import validate_goal_input

class WorkoutPlanDict(TypedDict):
    days: list[str]
    intensity: str
    duration: str
    focus_areas: list[str]

def workout_recommender(goal: str):
    """Generate a workout plan as a dict based on the user's goal."""
    if not validate_goal_input(goal):
        raise ValueError("Invalid goal input for workout recommender.")
    
    goal = goal.lower()
    
    # Define workout plans based on goals
    workout_plans = {
        "weight_loss": {
            "days": [
                "Day 1: Cardio - 30 min HIIT (High-Intensity Interval Training) | Strength - Full body circuit (3 sets, 12 reps each)",
                "Day 2: Cardio - 45 min steady-state cardio (jogging/cycling) | Core - Planks, crunches, leg raises (15 min)",
                "Day 3: Strength - Upper body focus (chest, back, shoulders, arms) | Cardio - 20 min moderate intensity",
                "Day 4: Cardio - 30 min HIIT | Lower body strength (squats, lunges, deadlifts)",
                "Day 5: Active recovery - 30 min walking or yoga | Core and flexibility work",
                "Day 6: Strength - Full body compound movements | Cardio - 25 min interval training",
                "Day 7: Rest day - Light stretching or 20 min walking"
            ],
            "intensity": "moderate to high",
            "duration": "45-60 minutes",
            "focus_areas": ["cardio", "strength", "fat_burning"]
        },
        "muscle_gain": {
            "days": [
                "Day 1: Chest and Triceps - Bench press, push-ups, dips, chest flyes (4 sets, 8-12 reps)",
                "Day 2: Back and Biceps - Pull-ups, rows, deadlifts, bicep curls (4 sets, 8-12 reps)",
                "Day 3: Legs - Squats, lunges, leg press, calf raises (4 sets, 10-15 reps)",
                "Day 4: Shoulders and Arms - Overhead press, lateral raises, tricep extensions (4 sets, 8-12 reps)",
                "Day 5: Full Body - Compound movements, deadlifts, squats, rows (3 sets, 8-10 reps)",
                "Day 6: Core and Cardio - Planks, crunches, 20 min moderate cardio",
                "Day 7: Rest day - Light stretching and recovery"
            ],
            "intensity": "high",
            "duration": "60-75 minutes",
            "focus_areas": ["strength", "muscle_building", "progressive_overload"]
        },
        "endurance": {
            "days": [
                "Day 1: Long distance cardio - 45-60 min running/cycling at moderate pace",
                "Day 2: Interval training - 30 min HIIT with 1:1 work/rest ratio",
                "Day 3: Strength - Full body with higher reps (3 sets, 15-20 reps)",
                "Day 4: Tempo training - 40 min at 70-80% max heart rate",
                "Day 5: Cross-training - Swimming, rowing, or elliptical (45 min)",
                "Day 6: Recovery run - 30 min easy pace | Core work",
                "Day 7: Rest day - Light stretching and mobility work"
            ],
            "intensity": "moderate",
            "duration": "45-60 minutes",
            "focus_areas": ["endurance", "cardiovascular_fitness", "stamina"]
        },
        "strength": {
            "days": [
                "Day 1: Push day - Bench press, overhead press, dips, push-ups (5 sets, 5-8 reps)",
                "Day 2: Pull day - Deadlifts, pull-ups, rows, bicep curls (5 sets, 5-8 reps)",
                "Day 3: Legs - Squats, lunges, leg press, calf raises (5 sets, 6-10 reps)",
                "Day 4: Rest day - Light stretching and recovery",
                "Day 5: Full body - Compound movements, deadlifts, squats (4 sets, 5-8 reps)",
                "Day 6: Accessory work - Isolation exercises, core work (3 sets, 10-15 reps)",
                "Day 7: Rest day - Complete rest or light walking"
            ],
            "intensity": "very high",
            "duration": "60-90 minutes",
            "focus_areas": ["strength", "power", "compound_movements"]
        },
        "general_fitness": {
            "days": [
                "Day 1: Full body strength - Compound movements (3 sets, 10-12 reps)",
                "Day 2: Cardio - 30 min moderate intensity (running/cycling)",
                "Day 3: Upper body focus - Push and pull exercises (3 sets, 12-15 reps)",
                "Day 4: Lower body and core - Squats, lunges, planks (3 sets, 12-15 reps)",
                "Day 5: Cardio - 25 min HIIT or interval training",
                "Day 6: Flexibility and mobility - Yoga or stretching routine (30 min)",
                "Day 7: Rest day - Light activity or complete rest"
            ],
            "intensity": "moderate",
            "duration": "45 minutes",
            "focus_areas": ["overall_fitness", "balance", "functional_movement"]
        }
    }
    
    # Determine goal type and return appropriate plan
    if "lose" in goal or "weight" in goal:
        return workout_plans["weight_loss"]
    elif "gain" in goal or "muscle" in goal or "build" in goal:
        return workout_plans["muscle_gain"]
    elif "endurance" in goal or "stamina" in goal:
        return workout_plans["endurance"]
    elif "strength" in goal or "power" in goal:
        return workout_plans["strength"]
    else:
        return workout_plans["general_fitness"]

workout_recommender_tool = function_tool(workout_recommender) 