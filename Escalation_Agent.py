from agents import Agent

def create_escalation_agent(handoff_description=None, hooks=None):
    return Agent(
        name="EscalationAgent",
        instructions="You are an escalation agent. When a user requests to speak to a human coach, take over and provide guidance or escalate as needed.",
        tools=[],
        handoff_description=handoff_description,
        hooks=hooks,
    ) 