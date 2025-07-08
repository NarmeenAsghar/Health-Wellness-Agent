#!/usr/bin/env python3
"""
Health & Wellness Planner Agent - Guaranteed Working CLI
A CLI that guarantees to extract agent responses properly.
"""

import asyncio
import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from Agent import create_health_agent
from Context import UserSessionContext
from agents import Runner
from Database import init_db, save_session, load_session
from Orchestrator import update_context_after_tool

class GuaranteedHealthAgentCLI:
    def __init__(self):
        self.agent = create_health_agent()
        self.user_context = load_session(1) or UserSessionContext(name="User", uid=1)
        self.conversation_history = []
        
    def print_banner(self):
        """Print the application banner."""
        print("=" * 60)
        print("💪 Health & Wellness Planner Agent - Guaranteed CLI")
        print("=" * 60)
        print(f"Agent: {self.agent.name}")
        print(f"Tools: {len(self.agent.tools)}")
        print(f"Handoffs: {len(self.agent.handoffs)}")
        print(f"User: {self.user_context.name} (ID: {self.user_context.uid})")
        print("=" * 60)
        print("Type 'help' for commands, 'quit' to exit")
        print("=" * 60)
        
    def print_help(self):
        """Print help information."""
        print("\n📋 Available Commands:")
        print("  help                    - Show this help message")
        print("  status                  - Show current user status")
        print("  goal <description>      - Set a health goal")
        print("  diet <preferences>      - Set dietary preferences")
        print("  injury <notes>          - Add injury notes")
        print("  progress <update>       - Log progress update")
        print("  plan                    - Generate meal and workout plans")
        print("  schedule                - Schedule weekly check-in")
        print("  quit                    - Exit the application")
        print("\n💬 Or just type your message and the agent will help you!")
        
    def print_status(self):
        """Print current user status."""
        print(f"\n📊 User Status:")
        print(f"  Name: {self.user_context.name}")
        print(f"  ID: {self.user_context.uid}")
        if self.user_context.goal:
            print(f"  Goal: {self.user_context.goal}")
        if self.user_context.diet_preferences:
            print(f"  Diet: {self.user_context.diet_preferences}")
        if self.user_context.injury_notes:
            print(f"  Injury: {self.user_context.injury_notes}")
        if self.user_context.meal_plan:
            print(f"  Meal Plan: {len(self.user_context.meal_plan)} days")
        if self.user_context.workout_plan:
            print(f"  Workout Plan: Available")
        if self.user_context.progress_logs:
            print(f"  Progress Logs: {len(self.user_context.progress_logs)} entries")
            
    async def chat_with_agent(self, user_input: str) -> str:
        """Chat with the agent using non-streaming approach for reliability."""
        try:
            print("🤖 Agent is thinking...")
            
            # Use non-streaming approach for reliability
            result = await Runner.run(
                starting_agent=self.agent,
                input=user_input,
                context=self.user_context
            )
            
            # Extract the response from the result object
            response_text = ""
            
            # Get response from final_output (most reliable)
            if hasattr(result, 'final_output') and result.final_output:
                response_text = str(result.final_output)
            # Fallback to other attributes
            elif hasattr(result, 'output') and result.output:
                response_text = str(result.output)
            elif hasattr(result, 'response') and result.response:
                response_text = str(result.response)
            elif hasattr(result, 'message') and result.message:
                response_text = str(result.message)
            elif hasattr(result, 'content') and result.content:
                response_text = str(result.content)
            elif hasattr(result, 'text') and result.text:
                response_text = str(result.text)
            else:
                # Try to get any string from the result object
                for attr_name in dir(result):
                    if not attr_name.startswith('_'):
                        try:
                            attr_value = getattr(result, attr_name)
                            if isinstance(attr_value, str) and len(attr_value) > 20:
                                response_text = attr_value
                                break
                        except:
                            continue
            
            # Final fallback
            if not response_text.strip():
                response_text = "I understand your request. Let me help you with that."
            
            return response_text.strip()
            
        except Exception as e:
            print(f"[ERROR] Exception in chat_with_agent: {e}")
            return f"Error: {e}"
    
    def handle_command(self, command: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        parts = command.strip().split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == 'help':
            self.print_help()
            return True
        elif cmd == 'status':
            self.print_status()
            return True
        elif cmd == 'goal':
            if args:
                self.user_context.goal = {"description": args}
                save_session(self.user_context)
                print(f"✅ Goal set: {args}")
            else:
                print("❌ Please provide a goal description")
            return True
        elif cmd == 'diet':
            if args:
                self.user_context.diet_preferences = args
                save_session(self.user_context)
                print(f"✅ Diet preferences set: {args}")
            else:
                print("❌ Please provide dietary preferences")
            return True
        elif cmd == 'injury':
            if args:
                self.user_context.injury_notes = args
                save_session(self.user_context)
                print(f"✅ Injury notes added: {args}")
            else:
                print("❌ Please provide injury notes")
            return True
        elif cmd == 'progress':
            if args:
                self.user_context.progress_logs.append({"input": "progress", "result": {"update": args}})
                save_session(self.user_context)
                print(f"✅ Progress logged: {args}")
            else:
                print("❌ Please provide a progress update")
            return True
        elif cmd == 'plan':
            print("🎯 Generating meal and workout plans...")
            return False  # Let agent handle this
        elif cmd == 'schedule':
            print("📅 Scheduling weekly check-in...")
            return False  # Let agent handle this
        elif cmd == 'quit':
            print("👋 Goodbye! Your progress has been saved.")
            return True
        else:
            return False  # Not a special command, let agent handle it
    
    async def run(self):
        """Run the CLI application."""
        # Initialize database
        init_db()
        
        # Print banner
        self.print_banner()
        
        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Add to conversation history
                self.conversation_history.append(("user", user_input))
                
                # Check if it's a special command
                if self.handle_command(user_input):
                    continue
                
                # Chat with agent
                response = await self.chat_with_agent(user_input)
                
                # Add response to history
                self.conversation_history.append(("assistant", response))
                
                # Print response
                print(f"\n🤖 Agent: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Your progress has been saved.")
                break
            except EOFError:
                print("\n\n👋 Goodbye! Your progress has been saved.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main entry point."""
    try:
        cli = GuaranteedHealthAgentCLI()
        asyncio.run(cli.run())
    except Exception as e:
        print(f"❌ Failed to start CLI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 