#!/usr/bin/env python3
"""
Health & Wellness Planner Agent - CLI with User Management
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Optional

from openai import OpenAI

from Agent import create_health_agent
from Context import UserSessionContext
from Database import init_db, create_user, get_user_by_email, get_user_by_uid, update_last_login, save_session, load_session, get_all_users
from Orchestrator import HealthOrchestrator
from PDF_Report import generate_user_report

# Initialize database
init_db()

class HealthAgentCLI:
    def __init__(self):
        self.client = OpenAI()
        self.orchestrator = HealthOrchestrator()
        self.current_user: Optional[UserSessionContext] = None
        self.agent = None
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self):
        """Print the application header."""
        print("=" * 60)
        print("💪 Health & Wellness Planner Agent")
        print("=" * 60)
        if self.current_user:
            print(f"👤 User: {self.current_user.name} (ID: {self.current_user.uid})")
            if self.current_user.email:
                print(f"📧 Email: {self.current_user.email}")
        print("=" * 60)
        
    def register_user(self) -> bool:
        """Register a new user."""
        print("\n📝 User Registration")
        print("-" * 30)
        
        name = input("Enter your name: ").strip()
        if not name:
            print("❌ Name is required!")
            return False
            
        email = input("Enter your email (optional): ").strip()
        if email:
            # Check if email already exists
            existing_user = get_user_by_email(email)
            if existing_user:
                print(f"❌ Email {email} is already registered!")
                return False
        
        # Simple password (in production, use proper hashing)
        password = input("Enter a password: ").strip()
        if not password:
            print("❌ Password is required!")
            return False
            
        try:
            uid = create_user(name, email, password)
            print(f"✅ User registered successfully! Your ID is: {uid}")
            return True
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return False
            
    def login_user(self) -> bool:
        """Login an existing user."""
        print("\n🔐 User Login")
        print("-" * 20)
        
        email = input("Enter your email: ").strip()
        if not email:
            print("❌ Email is required!")
            return False
            
        user = get_user_by_email(email)
        if not user:
            print("❌ User not found! Please register first.")
            return False
            
        password = input("Enter your password: ").strip()
        if not password:
            print("❌ Password is required!")
            return False
            
        # Simple password check (in production, use proper hashing)
        if password != user.get('password_hash', ''):
            print("❌ Invalid password!")
            return False
            
        # Load user session
        context = load_session(user['uid'])
        if not context:
            print("❌ Failed to load user session!")
            return False
            
        self.current_user = context
        update_last_login(user['uid'])
        print(f"✅ Welcome back, {user['name']}!")
        return True
        
    def login_by_uid(self) -> bool:
        """Login by user ID (for testing)."""
        print("\n🔢 Login by User ID")
        print("-" * 20)
        
        try:
            uid = int(input("Enter your user ID: ").strip())
        except ValueError:
            print("❌ Invalid user ID!")
            return False
            
        user = get_user_by_uid(uid)
        if not user:
            print("❌ User not found!")
            return False
            
        context = load_session(uid)
        if not context:
            print("❌ Failed to load user session!")
            return False
            
        self.current_user = context
        update_last_login(uid)
        print(f"✅ Welcome back, {user['name']}!")
        return True
        
    def show_users(self):
        """Show all registered users (admin function)."""
        print("\n👥 Registered Users")
        print("-" * 30)
        
        users = get_all_users()
        if not users:
            print("No users registered yet.")
            return
            
        for user in users:
            print(f"ID: {user['uid']} | Name: {user['name']} | Email: {user['email'] or 'N/A'}")
            print(f"  Created: {user['created_at']}")
            print(f"  Last Login: {user['last_login'] or 'Never'}")
            print()
            
    def download_report(self):
        """Download user's health report."""
        if not self.current_user:
            print("❌ Please login first!")
            return
        print(f"\n📊 Generating report for {self.current_user.name}...")
        try:
            # Generate PDF report
            report_path = generate_user_report(self.current_user)
            print(f"✅ Report generated successfully!")
            print(f"📁 Report saved to: {report_path}")
            # Also save as JSON for easy viewing
            json_path = f"user_{self.current_user.uid}_report.json"
            report_data = {
                "user_info": {
                    "name": self.current_user.name,
                    "uid": self.current_user.uid,
                    "email": self.current_user.email,
                    "created_at": self.current_user.created_at,
                    "last_updated": self.current_user.last_updated
                },
                "goals": self.current_user.goal,
                "diet_preferences": self.current_user.diet_preferences,
                "workout_plan": self.current_user.workout_plan,
                "meal_plan": self.current_user.meal_plan,
                "injury_notes": self.current_user.injury_notes,
                "progress_logs": self.current_user.progress_logs,
                "conversation_history": self.current_user.conversation_history[-10:],  # Last 10 messages
                "handoff_logs": self.current_user.handoff_logs
            }
            with open(json_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            print(f"📄 JSON report saved to: {json_path}")
        except Exception as e:
            print(f"❌ Failed to generate report: {e}")
            
    def show_help(self):
        """Show help information."""
        print("\n📖 Available Commands:")
        print("-" * 30)
        print("register    - Register a new user")
        print("login       - Login with email")
        print("login-id    - Login with user ID")
        print("users       - Show all users (admin)")
        print("report      - Download your health report")
        print("context     - Show current context")
        print("clear       - Clear conversation history")
        print("logout      - Logout current user")
        print("help        - Show this help")
        print("quit        - Exit the application")
        print()
        print("💬 Just type your message to chat with the agent!")
        
    def show_context(self):
        """Show current user context."""
        if not self.current_user:
            print("❌ Please login first!")
            return
            
        print(f"\n📋 Context for {self.current_user.name}:")
        print("-" * 40)
        print(f"User ID: {self.current_user.uid}")
        print(f"Email: {self.current_user.email or 'Not set'}")
        print(f"Created: {self.current_user.created_at}")
        print(f"Last Updated: {self.current_user.last_updated}")
        print(f"Goal: {self.current_user.goal or 'Not set'}")
        print(f"Diet Preferences: {self.current_user.diet_preferences or 'Not set'}")
        print(f"Workout Plan: {'Set' if self.current_user.workout_plan else 'Not set'}")
        print(f"Meal Plan: {'Set' if self.current_user.meal_plan else 'Not set'}")
        print(f"Injury Notes: {self.current_user.injury_notes or 'None'}")
        print(f"Progress Logs: {len(self.current_user.progress_logs)} entries")
        print(f"Conversation History: {len(self.current_user.conversation_history)} messages")
        print(f"Handoff Logs: {len(self.current_user.handoff_logs)} entries")
        
    def clear_conversation(self):
        """Clear conversation history."""
        if not self.current_user:
            print("❌ Please login first!")
            return
            
        self.current_user.conversation_history = []
        save_session(self.current_user)
        print("✅ Conversation history cleared!")
        
    def chat_with_agent(self, message: str):
        """Chat with the health agent."""
        if not self.current_user:
            print("❌ Please login first!")
            return
        print(f"\n🤖 Agent is thinking...")
        # Track consecutive failures
        if not hasattr(self, '_fail_count'):
            self._fail_count = 0
        try:
            # Add user message to conversation history
            self.current_user.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            # Create agent if not exists
            if not self.agent:
                self.agent = create_health_agent()
            # Run the agent
            run_result = self.orchestrator.run_agent(
                self.agent,
                message,
                self.current_user
            )
            # Debug: print the full run_result structure
            print("\n[DEBUG] Raw agent output:")
            print(run_result)
            print("[END DEBUG]\n")
            # Extract response - handle different result types
            response = None
            if run_result:
                # If it's a dict-like object
                if isinstance(run_result, dict):
                    if 'final_output' in run_result and run_result['final_output']:
                        response = run_result['final_output']
                    elif 'output' in run_result and run_result['output']:
                        response = run_result['output']
                    elif 'content' in run_result and run_result['content']:
                        response = run_result['content']
                    else:
                        response = '\n'.join(str(v) for v in run_result.values() if isinstance(v, str))
                elif hasattr(run_result, 'final_output') and getattr(run_result, 'final_output', None):
                    response = run_result.final_output
                elif hasattr(run_result, 'output') and getattr(run_result, 'output', None):
                    response = run_result.output
                elif hasattr(run_result, 'content') and getattr(run_result, 'content', None):
                    response = run_result.content
                elif isinstance(run_result, str):
                    response = run_result
                else:
                    response = str(run_result)
            # Fallback if no response
            if not response or not isinstance(response, str) or not response.strip():
                self._fail_count += 1
                if self._fail_count >= 3:
                    response = ("I'm having trouble generating a response. "
                                "Try rephrasing your question or type 'clear' to reset the conversation.")
                else:
                    response = ("I apologize, but I couldn't generate a response. "
                                "Please try again or type 'clear' to reset the conversation.")
            else:
                self._fail_count = 0  # Reset fail count on success
            # Add assistant response to conversation history
            self.current_user.conversation_history.append({
                "role": "assistant", 
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            # Save updated context
            save_session(self.current_user)
            print(f"🤖 Agent: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
            save_session(self.current_user)
            
    def run(self):
        """Main CLI loop."""
        self.clear_screen()
        self.print_header()
        print("Welcome to the Health & Wellness Planner Agent!")
        print("Please register or login to continue.")
        print()
        while True:
            try:
                if not self.current_user:
                    print("\n🔐 Authentication Required")
                    print("1. register - Create new account")
                    print("2. login - Login with email")
                    print("3. login-id - Login with user ID")
                    print("4. users - Show all users")
                    print("5. quit - Exit")
                    print("\n💡 Tip: You can enter the number (1-5) or the command name")
                    choice = input("\nEnter your choice: ").strip().lower()
                    if choice in ["1", "register"]:
                        if self.register_user():
                            print("✅ Registration successful! Please login.")
                    elif choice in ["2", "login"]:
                        self.login_user()
                    elif choice in ["3", "login-id"]:
                        self.login_by_uid()
                    elif choice in ["4", "users"]:
                        self.show_users()
                    elif choice in ["5", "quit"]:
                        print("👋 Goodbye!")
                        break
                    else:
                        print("❌ Invalid choice! Please enter 1-5 or the command name.")
                else:
                    # User is logged in - show main interface
                    self.clear_screen()
                    self.print_header()
                    print("🎉 Successfully logged in! You can now chat with the AI agent.")
                    print("Type 'help' for commands, 'quit' to exit")
                    print("-" * 60)
                    # Show welcome message for new users
                    if not self.current_user.conversation_history:
                        print("\n🤖 Welcome! I'm your Health & Wellness Planner Agent.")
                        print("I can help you with:")
                        print("  • Setting health and fitness goals")
                        print("  • Creating personalized meal plans")
                        print("  • Designing workout routines")
                        print("  • Tracking your progress")
                        print("  • Scheduling check-ins")
                        print("\nJust tell me what you'd like to work on!")
                        print()
                    else:
                        # Show recent conversation if any
                        print("\n💬 Recent conversation:")
                        recent = self.current_user.conversation_history[-10:]  # Last 10 messages
                        for msg in recent:
                            role = "You" if msg["role"] == "user" else "Agent"
                            print(f"{role}: {msg['content']}")
                        print()
                    user_input = input("💬 You: ").strip()
                    if not user_input:
                        continue
                    if user_input.lower() == "quit":
                        print("👋 Goodbye!")
                        break
                    elif user_input.lower() == "help":
                        self.show_help()
                    elif user_input.lower() == "register":
                        print("❌ You are already logged in!")
                    elif user_input.lower() == "login":
                        print("❌ You are already logged in!")
                    elif user_input.lower() == "users":
                        self.show_users()
                    elif user_input.lower() == "report":
                        self.download_report()
                    elif user_input.lower() == "context":
                        self.show_context()
                    elif user_input.lower() == "clear":
                        self.clear_conversation()
                    elif user_input.lower() == "logout":
                        self.current_user = None
                        self.agent = None
                        print("✅ Logged out successfully!")
                    else:
                        # Chat with agent
                        self.chat_with_agent(user_input)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    cli = HealthAgentCLI()
    cli.run() 