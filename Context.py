from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime

class UserSessionContext(BaseModel):
    name: str
    uid: int
    email: Optional[str] = None
    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []
    conversation_history: List[Dict[str, str]] = []
    created_at: Optional[str] = None
    last_updated: Optional[str] = None 