from pydantic import BaseModel, ValidationError
from typing import Any

def validate_goal_input(goal_text: str) -> bool:
    """Validate goal input format and content."""
    if not goal_text or len(goal_text.strip()) < 3:
        return False
    
    goal_text = goal_text.lower()
    
    # Check for valid goal keywords
    valid_goal_keywords = [
        "lose", "gain", "weight", "muscle", "fit", "endurance", "strength",
        "build", "tone", "slim", "bulk", "cardio", "health", "wellness"
    ]
    
    if not any(keyword in goal_text for keyword in valid_goal_keywords):
        return False
    
    # Check for reasonable quantities and timeframes
    import re
    quantity_match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|pounds?|lbs?|kilos?)', goal_text)
    time_match = re.search(r'(\d+)\s*(weeks?|months?|days?)', goal_text)
    
    if quantity_match:
        quantity = float(quantity_match.group(1))
        if quantity > 50:  # Unrealistic weight goal
            return False
    
    if time_match:
        amount = int(time_match.group(1))
        unit = time_match.group(2)
        if unit in ["day", "days"] and amount > 365:  # More than a year
            return False
        elif unit in ["week", "weeks"] and amount > 52:  # More than a year
            return False
        elif unit in ["month", "months"] and amount > 12:  # More than a year
            return False
    
    return True

def validate_diet_input(diet_text: str) -> bool:
    """Validate dietary preferences input."""
    if not diet_text or len(diet_text.strip()) < 2:
        return False
    
    diet_text = diet_text.lower()
    
    # Check for valid diet keywords
    valid_diet_keywords = [
        "vegetarian", "vegan", "keto", "paleo", "mediterranean", "low-carb",
        "high-protein", "gluten-free", "dairy-free", "balanced", "healthy"
    ]
    
    if not any(keyword in diet_text for keyword in valid_diet_keywords):
        return False
    
    return True

def validate_injury_input(injury_text: str) -> bool:
    """Validate injury-related input."""
    if not injury_text or len(injury_text.strip()) < 3:
        return False
    
    injury_text = injury_text.lower()
    
    # Check for valid injury keywords
    valid_injury_keywords = [
        "knee", "back", "shoulder", "ankle", "wrist", "hip", "neck",
        "pain", "injury", "surgery", "recovery", "physical therapy",
        "limited", "restricted", "avoid", "careful"
    ]
    
    if not any(keyword in injury_text for keyword in valid_injury_keywords):
        return False
    
    return True

def output_guardrail(output: Any, model: BaseModel) -> bool:
    try:
        model.parse_obj(output)
        return True
    except ValidationError:
        return False 