from typing import TypedDict
from agents.tool import function_tool
from Guardrails import validate_goal_input
from datetime import datetime
import re

class ProgressUpdateDict(TypedDict):
    status: str
    user_id: int
    update: str

def progress_tracker(user_id: int, update: str):
    """Track progress and update context, returning a dict."""
    if not isinstance(update, str) or len(update.strip()) < 3:
        raise ValueError("Invalid progress update input.")
    
    # Analyze the update to extract key information
    update_lower = update.lower()
    
    # Extract weight changes
    weight_change = None
    if "lost" in update_lower or "lose" in update_lower:
        weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|pounds?|lbs?)', update_lower)
        if weight_match:
            weight_change = f"-{weight_match.group(1)} {weight_match.group(2)}"
    
    # Determine progress category
    progress_category = "general"
    if any(word in update_lower for word in ["weight", "lost", "gain", "pound", "kg"]):
        progress_category = "weight"
    elif any(word in update_lower for word in ["workout", "exercise", "gym", "run", "cardio"]):
        progress_category = "fitness"
    elif any(word in update_lower for word in ["meal", "diet", "food", "eat"]):
        progress_category = "nutrition"
    elif any(word in update_lower for word in ["energy", "mood", "feel", "sleep"]):
        progress_category = "wellness"
    
    # Generate motivational response
    motivational_responses = {
        "weight": "Great job on your weight management! Keep up the consistent effort.",
        "fitness": "Excellent work on your fitness routine! Your dedication is paying off.",
        "nutrition": "Fantastic progress with your nutrition! You're building healthy habits.",
        "wellness": "Wonderful to hear about your wellness improvements! Keep prioritizing your health.",
        "general": "Thank you for the update! Every step forward counts towards your goals."
    }
    
    return {
        "status": "progress updated",
        "user_id": user_id,
        "update": update,
        "timestamp": datetime.now().isoformat(),
        "category": progress_category,
        "weight_change": weight_change,
        "motivational_message": motivational_responses.get(progress_category, motivational_responses["general"]),
        "next_steps": [
            "Continue with your current routine",
            "Stay consistent with your meal plan",
            "Keep tracking your progress",
            "Stay hydrated and get enough sleep"
        ]
    }

progress_tracker_tool = function_tool(progress_tracker) 