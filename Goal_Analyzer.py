from typing import TypedDict
from agents.tool import function_tool
from Guardrails import validate_goal_input
import re

class GoalAnalysisDict(TypedDict):
    quantity: float
    metric: str
    duration: str
    goal_type: str
    difficulty: str

def analyze_goal(goal_text: str):
    """Analyze and parse a user goal string into structured data as a dict."""
    if not validate_goal_input(goal_text):
        raise ValueError("Invalid goal input format.")
    
    goal_text = goal_text.lower()
    
    # Extract quantity and metric
    quantity = 5.0
    metric = "kg"
    duration = "2 months"
    goal_type = "weight_loss"
    difficulty = "moderate"
    
    # Parse weight loss goals
    if "lose" in goal_text or "weight" in goal_text:
        goal_type = "weight_loss"
        # Extract number and unit
        weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|pounds?|lbs?|kilos?)', goal_text)
        if weight_match:
            quantity = float(weight_match.group(1))
            unit = weight_match.group(2)
            if unit in ["pounds", "lbs", "pound"]:
                metric = "pounds"
            else:
                metric = "kg"
    
    # Parse muscle gain goals
    elif "gain" in goal_text or "muscle" in goal_text or "build" in goal_text:
        goal_type = "muscle_gain"
        weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|pounds?|lbs?|kilos?)', goal_text)
        if weight_match:
            quantity = float(weight_match.group(1))
            unit = weight_match.group(2)
            if unit in ["pounds", "lbs", "pound"]:
                metric = "pounds"
            else:
                metric = "kg"
    
    # Parse fitness goals
    elif "fit" in goal_text or "endurance" in goal_text or "strength" in goal_text:
        goal_type = "fitness"
        quantity = 1.0
        metric = "fitness_level"
    
    # Extract duration
    time_match = re.search(r'(\d+)\s*(weeks?|months?|days?)', goal_text)
    if time_match:
        amount = int(time_match.group(1))
        unit = time_match.group(2)
        if unit in ["week", "weeks"]:
            duration = f"{amount} weeks"
        elif unit in ["month", "months"]:
            duration = f"{amount} months"
        elif unit in ["day", "days"]:
            duration = f"{amount} days"
    
    # Determine difficulty
    if quantity > 10 or "months" in duration and int(duration.split()[0]) > 3:
        difficulty = "challenging"
    elif quantity < 3 or "weeks" in duration and int(duration.split()[0]) < 2:
        difficulty = "easy"
    else:
        difficulty = "moderate"
    
    return {
        "quantity": quantity,
        "metric": metric,
        "duration": duration,
        "goal_type": goal_type,
        "difficulty": difficulty,
        "description": goal_text
    }

analyze_goal_tool = function_tool(analyze_goal) 