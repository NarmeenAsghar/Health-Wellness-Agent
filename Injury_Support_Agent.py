from agents import Agent

def create_injury_support_agent(handoff_description=None, hooks=None):
    return Agent(
        name="InjurySupportAgent",
        instructions="You are an injury support agent. Assist users with physical limitations or injury-specific workout plans and advice.",
        tools=[],
        handoff_description=handoff_description,
        hooks=hooks,
    ) 