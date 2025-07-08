from typing import TypedDict
from agents.tool import function_tool
from Guardrails import validate_goal_input

class CheckinStatusDict(TypedDict):
    status: str
    user_id: int

def checkin_scheduler(user_id: int):
    """Schedule a weekly check-in for the user and return status as a dict."""
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID input for check-in scheduler.")
    
    from datetime import datetime, timedelta
    
    # Calculate next check-in date (next Monday at 9 AM)
    today = datetime.now()
    days_ahead = 7 - today.weekday()  # Monday is 0
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    next_monday = today + timedelta(days=days_ahead)
    next_checkin = next_monday.replace(hour=9, minute=0, second=0, microsecond=0)
    
    return {
        "status": "scheduled",
        "user_id": user_id,
        "next_checkin": next_checkin.strftime("%Y-%m-%d %H:%M"),
        "frequency": "weekly",
        "reminder": "You'll receive a reminder 24 hours before your check-in",
        "checkin_topics": [
            "Progress towards your goals",
            "Current weight and measurements",
            "Workout completion rate",
            "Meal plan adherence",
            "Energy levels and mood",
            "Any challenges or obstacles"
        ]
    }

checkin_scheduler_tool = function_tool(checkin_scheduler) 