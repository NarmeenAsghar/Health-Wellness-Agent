from Context import UserSessionContext
from agents import Runner
from typing import Optional

def update_context_after_tool(tool_name: str, tool_output: dict, user_input: str, context: UserSessionContext):
    """
    Update the UserSessionContext based on which tool was called and its output.
    """
    if tool_name == "analyze_goal":
        context.goal = tool_output
    elif tool_name == "meal_planner":
        context.meal_plan = tool_output.get("days")
    elif tool_name == "workout_recommender":
        context.workout_plan = tool_output
    elif tool_name == "progress_tracker":
        context.progress_logs.append({"input": user_input, "result": tool_output})
    elif tool_name == "checkin_scheduler":
        # Log check-in scheduling
        context.progress_logs.append({"input": user_input, "result": tool_output})
        # Add to conversation history
        context.conversation_history.append({"role": "system", "content": f"Check-in scheduled: {tool_output}"})
    # Add more as needed for handoffs, etc.
    return context

class HealthOrchestrator:
    """Orchestrator for managing health agent interactions."""
    
    def __init__(self):
        pass
    
    def run_agent(self, agent, message: str, context: UserSessionContext):
        """
        Run the agent with the given message and context.
        Returns the agent's response.
        """
        try:
            import asyncio
            result = asyncio.run(Runner.run(
                starting_agent=agent,
                input=message,
                context=context
            ))
            return result
        except Exception as e:
            print(f"Error running agent: {e}")
            return None 