from typing import TypedDict
from agents.tool import function_tool
from Guardrails import validate_diet_input

class MealPlanDict(TypedDict):
    days: list[str]
    total_calories: int
    macros: dict

def meal_planner(diet_preferences: str):
    """Generate a meal plan as a dict based on user preferences."""
    if not validate_diet_input(diet_preferences):
        raise ValueError("Invalid diet preferences input.")
    
    diet_preferences = diet_preferences.lower()
    
    # Define meal plans based on preferences
    meal_plans = {
        "vegetarian": {
            "days": [
                "Day 1: Breakfast - Greek yogurt with berries and granola (300 cal) | Lunch - Quinoa salad with chickpeas and vegetables (450 cal) | Dinner - Lentil curry with brown rice (500 cal)",
                "Day 2: Breakfast - Oatmeal with banana and nuts (350 cal) | Lunch - Hummus wrap with vegetables (400 cal) | Dinner - Stuffed bell peppers with quinoa (480 cal)",
                "Day 3: Breakfast - Smoothie bowl with fruits and seeds (320 cal) | Lunch - Mediterranean pasta salad (420 cal) | Dinner - Black bean tacos with avocado (460 cal)",
                "Day 4: Breakfast - Whole grain toast with avocado and eggs (380 cal) | Lunch - Buddha bowl with tofu and vegetables (440 cal) | Dinner - Vegetable stir-fry with brown rice (470 cal)",
                "Day 5: Breakfast - Chia pudding with fruits (300 cal) | Lunch - Falafel wrap with tahini sauce (410 cal) | Dinner - Mushroom risotto (490 cal)",
                "Day 6: Breakfast - Protein smoothie with spinach (280 cal) | Lunch - Caprese salad with whole grain bread (390 cal) | Dinner - Stuffed zucchini boats (450 cal)",
                "Day 7: Breakfast - Breakfast burrito with beans (350 cal) | Lunch - Greek salad with feta cheese (380 cal) | Dinner - Vegetable lasagna (520 cal)"
            ],
            "total_calories": 1800,
            "macros": {"protein": "15%", "carbs": "55%", "fat": "30%"}
        },
        "vegan": {
            "days": [
                "Day 1: Breakfast - Smoothie with almond milk and protein powder (280 cal) | Lunch - Buddha bowl with quinoa and vegetables (420 cal) | Dinner - Chickpea curry with rice (480 cal)",
                "Day 2: Breakfast - Overnight oats with fruits and nuts (320 cal) | Lunch - Vegan wrap with hummus and vegetables (380 cal) | Dinner - Lentil soup with whole grain bread (450 cal)",
                "Day 3: Breakfast - Tofu scramble with vegetables (300 cal) | Lunch - Mediterranean salad with olives (350 cal) | Dinner - Vegan pasta with tomato sauce (420 cal)",
                "Day 4: Breakfast - Chia pudding with coconut milk (290 cal) | Lunch - Quinoa salad with black beans (400 cal) | Dinner - Stuffed bell peppers with rice (460 cal)",
                "Day 5: Breakfast - Protein smoothie bowl (310 cal) | Lunch - Vegan sushi rolls (360 cal) | Dinner - Vegetable curry with naan (440 cal)",
                "Day 6: Breakfast - Whole grain toast with avocado (280 cal) | Lunch - Buddha bowl with tempeh (410 cal) | Dinner - Vegan chili with cornbread (470 cal)",
                "Day 7: Breakfast - Oatmeal with fruits and seeds (330 cal) | Lunch - Mediterranean wrap (370 cal) | Dinner - Vegan lasagna (450 cal)"
            ],
            "total_calories": 1700,
            "macros": {"protein": "12%", "carbs": "60%", "fat": "28%"}
        },
        "keto": {
            "days": [
                "Day 1: Breakfast - Eggs with avocado and bacon (450 cal) | Lunch - Grilled chicken salad with olive oil (380 cal) | Dinner - Salmon with asparagus and butter (520 cal)",
                "Day 2: Breakfast - Keto smoothie with coconut milk (420 cal) | Lunch - Tuna salad with celery (350 cal) | Dinner - Beef stir-fry with cauliflower rice (480 cal)",
                "Day 3: Breakfast - Keto pancakes with berries (380 cal) | Lunch - Cobb salad with ranch dressing (400 cal) | Dinner - Pork chops with green beans (460 cal)",
                "Day 4: Breakfast - Scrambled eggs with cheese (440 cal) | Lunch - Grilled shrimp with avocado (360 cal) | Dinner - Chicken thighs with broccoli (490 cal)",
                "Day 5: Breakfast - Keto granola with almond milk (400 cal) | Lunch - Turkey roll-ups with cream cheese (320 cal) | Dinner - Lamb chops with cauliflower (470 cal)",
                "Day 6: Breakfast - Keto waffles with butter (420 cal) | Lunch - Grilled fish with salad (380 cal) | Dinner - Beef burger with cheese (no bun) (450 cal)",
                "Day 7: Breakfast - Eggs benedict with hollandaise (460 cal) | Lunch - Chicken Caesar salad (no croutons) (390 cal) | Dinner - Steak with mushrooms (500 cal)"
            ],
            "total_calories": 2000,
            "macros": {"protein": "25%", "carbs": "5%", "fat": "70%"}
        },
        "mediterranean": {
            "days": [
                "Day 1: Breakfast - Greek yogurt with honey and nuts (320 cal) | Lunch - Mediterranean salad with olive oil (380 cal) | Dinner - Grilled salmon with quinoa (480 cal)",
                "Day 2: Breakfast - Whole grain toast with olive oil (300 cal) | Lunch - Hummus with vegetables and pita (350 cal) | Dinner - Chicken with roasted vegetables (420 cal)",
                "Day 3: Breakfast - Oatmeal with fruits and nuts (340 cal) | Lunch - Greek salad with feta (360 cal) | Dinner - Fish with lemon and herbs (440 cal)",
                "Day 4: Breakfast - Smoothie with berries and yogurt (310 cal) | Lunch - Mediterranean wrap (370 cal) | Dinner - Lamb with couscous (460 cal)",
                "Day 5: Breakfast - Eggs with whole grain bread (330 cal) | Lunch - Tuna salad with olive oil (340 cal) | Dinner - Vegetable pasta with olive oil (410 cal)",
                "Day 6: Breakfast - Greek yogurt parfait (320 cal) | Lunch - Mediterranean bowl (380 cal) | Dinner - Grilled chicken with rice (430 cal)",
                "Day 7: Breakfast - Whole grain pancakes with honey (350 cal) | Lunch - Mediterranean soup (320 cal) | Dinner - Fish with vegetables (420 cal)"
            ],
            "total_calories": 1800,
            "macros": {"protein": "20%", "carbs": "45%", "fat": "35%"}
        }
    }
    
    # Default to balanced diet if preference not found
    default_plan = {
        "days": [
            "Day 1: Breakfast - Oatmeal with fruits and nuts (350 cal) | Lunch - Grilled chicken salad (400 cal) | Dinner - Salmon with vegetables (450 cal)",
            "Day 2: Breakfast - Greek yogurt with granola (320 cal) | Lunch - Turkey sandwich with vegetables (380 cal) | Dinner - Lean beef with brown rice (420 cal)",
            "Day 3: Breakfast - Smoothie with protein powder (300 cal) | Lunch - Quinoa bowl with vegetables (360 cal) | Dinner - Grilled fish with sweet potato (410 cal)",
            "Day 4: Breakfast - Eggs with whole grain toast (340 cal) | Lunch - Mediterranean salad (370 cal) | Dinner - Chicken stir-fry (390 cal)",
            "Day 5: Breakfast - Protein pancakes (330 cal) | Lunch - Tuna salad with vegetables (350 cal) | Dinner - Lean pork with quinoa (400 cal)",
            "Day 6: Breakfast - Chia pudding with fruits (310 cal) | Lunch - Grilled vegetables with hummus (340 cal) | Dinner - Turkey with vegetables (380 cal)",
            "Day 7: Breakfast - Whole grain cereal with milk (320 cal) | Lunch - Mediterranean wrap (360 cal) | Dinner - Fish with brown rice (420 cal)"
        ],
        "total_calories": 1800,
        "macros": {"protein": "25%", "carbs": "45%", "fat": "30%"}
    }
    
    # Find matching plan
    for key, plan in meal_plans.items():
        if key in diet_preferences:
            return plan
    
    return default_plan

meal_planner_tool = function_tool(meal_planner) 