from dotenv import load_dotenv
load_dotenv()

import asyncio
from Context import UserSessionContext
from Agent import create_health_agent
from agents import Runner


def main():
    user_name = input("Enter your name: ")
    user_id = 1  # For demo, static UID
    user_context = UserSessionContext(name=user_name, uid=user_id)
    agent = create_health_agent()
    print("Welcome to the Health & Wellness Planner Agent!")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        asyncio.run(run_agent(agent, user_input, user_context))

def print_stream(step_stream):
    for step in step_stream:
        print(step.pretty_output)

async def run_agent(agent, user_input, user_context):
    result = await Runner.run(agent, user_input, context=user_context)
    print(result.final_output)

if __name__ == "__main__":
    main()
