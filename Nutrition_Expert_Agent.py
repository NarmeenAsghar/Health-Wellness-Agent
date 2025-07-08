from agents import Agent

def create_nutrition_expert_agent(handoff_description=None, hooks=None):
    return Agent(
        name="NutritionExpertAgent",
        instructions="You are a nutrition expert. Help users with complex dietary needs such as diabetes or allergies, and provide specialized meal plans and advice.",
        tools=[],
        handoff_description=handoff_description,
        hooks=hooks,
    ) 