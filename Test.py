from Goal_Analyzer import analyze_goal
from Meal_Planner import meal_planner
from Workout_Recommender import workout_recommender
from Scheduler import checkin_scheduler
from Tracker import progress_tracker

# Goal Analyzer
goal = analyze_goal("lose 5kg in 2 months")
assert isinstance(goal, dict)
assert set(goal.keys()) == {"quantity", "metric", "duration"}
try:
    analyze_goal("")
    assert False, "Should fail on empty input"
except Exception:
    pass

# Meal Planner
meal = meal_planner("vegetarian")
assert isinstance(meal, dict)
assert "days" in meal and isinstance(meal["days"], list)
try:
    meal_planner("")
    assert False, "Should fail on empty input"
except Exception:
    pass

# Workout Recommender
workout = workout_recommender("gain muscle")
assert isinstance(workout, dict)
assert "days" in workout and isinstance(workout["days"], list)
try:
    workout_recommender("")
    assert False, "Should fail on empty input"
except Exception:
    pass

# Scheduler
checkin = checkin_scheduler(1)
assert isinstance(checkin, dict)
assert set(checkin.keys()) == {"status", "user_id"}
try:
    checkin_scheduler("")
    assert False, "Should fail on invalid user id"
except Exception:
    pass

# Progress Tracker
progress = progress_tracker(1, "completed workout")
assert isinstance(progress, dict)
assert set(progress.keys()) == {"status", "user_id", "update"}
try:
    progress_tracker(1, "")
    assert False, "Should fail on empty update"
except Exception:
    pass

print("All tests passed!")