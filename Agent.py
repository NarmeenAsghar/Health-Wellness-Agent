from agents import Agent
from Goal_Analyzer import analyze_goal_tool
from Meal_Planner import meal_planner_tool
from Workout_Recommender import workout_recommender_tool
from Scheduler import checkin_scheduler_tool
from Tracker import progress_tracker_tool
from Escalation_Agent import create_escalation_agent
from Nutrition_Expert_Agent import create_nutrition_expert_agent
from Injury_Support_Agent import create_injury_support_agent
from Guardrails import validate_goal_input, validate_diet_input, validate_injury_input
from Hooks import HealthRunHooks

# Wrapper result for guardrails
class GuardrailResult:
    def __init__(self, passed: bool):
        self.output = type('Output', (), {})()
        self.output.tripwire_triggered = not passed

class GoalInputGuardrail:
    async def run(self, agent, input, context):
        passed = validate_goal_input(input)
        return GuardrailResult(passed)
    def get_name(self):
        return "GoalInputGuardrail"

class DietInputGuardrail:
    async def run(self, agent, input, context):
        passed = validate_diet_input(input)
        return GuardrailResult(passed)
    def get_name(self):
        return "DietInputGuardrail"

class InjuryInputGuardrail:
    async def run(self, agent, input, context):
        passed = validate_injury_input(input)
        return GuardrailResult(passed)
    def get_name(self):
        return "InjuryInputGuardrail"

def create_health_agent():
    tools = [
        analyze_goal_tool,
        meal_planner_tool,
        workout_recommender_tool,
        checkin_scheduler_tool,
        progress_tracker_tool,
    ]
    handoffs = {
        "escalation": create_escalation_agent(handoff_description="Escalates to a human coach when the user requests human support or is dissatisfied with automated help."),
        "nutrition": create_nutrition_expert_agent(handoff_description="Handles complex dietary needs, allergies, or medical nutrition questions."),
        "injury": create_injury_support_agent(handoff_description="Supports users with physical limitations or injury-specific workout needs."),
    }
    input_guardrails = [GoalInputGuardrail(), DietInputGuardrail(), InjuryInputGuardrail()]
    return Agent(
        name="HealthWellnessPlanner",
        instructions="""You are a comprehensive Health & Wellness Planner Agent with expertise in fitness, nutrition, and wellness coaching. Your role is to provide personalized, actionable health advice and create detailed plans for users.

CORE RESPONSIBILITIES:
1. **Goal Analysis**: Help users set realistic, achievable health and fitness goals
2. **Meal Planning**: Create personalized meal plans based on dietary preferences and goals
3. **Workout Design**: Develop customized workout routines for different fitness levels and goals
4. **Progress Tracking**: Monitor user progress and provide motivational support
5. **Health Education**: Educate users about nutrition, exercise, and wellness best practices

RESPONSE GUIDELINES:
- Always provide specific, actionable advice rather than generic responses
- Use the available tools to generate personalized meal and workout plans
- Reference the user's conversation history to maintain context
- Provide detailed explanations for recommendations
- Include calorie information, macros, and nutritional guidance
- Suggest realistic timelines and expectations
- Offer encouragement and motivation
- Address user concerns and questions thoroughly

WHEN CREATING PLANS:
- Meal Plans: Include specific foods, portions, calorie counts, and timing
- Workout Plans: Specify exercises, sets, reps, duration, and intensity
- Progress Tracking: Set measurable milestones and check-in schedules
- Safety: Always consider user limitations and provide modifications

CONVERSATION STYLE:
- Be encouraging and supportive
- Use clear, easy-to-understand language
- Provide evidence-based recommendations
- Ask clarifying questions when needed
- Remember previous conversations and build on them

Always strive to provide comprehensive, personalized responses that help users achieve their health and wellness goals.""",
        tools=tools,
        handoffs=handoffs,
        input_guardrails=input_guardrails,
        hooks=HealthRunHooks(),
    ) 