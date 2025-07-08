# 💪 Health & Wellness Planner Agent - CLI Version

A comprehensive command-line interface for an AI-powered health and wellness planning agent built with OpenAI Agents SDK.

## 🚀 Features

* **User Registration & Login**: Individual user accounts with email/password authentication
* **Multi-Agent System**: Main health planner with specialized agents for nutrition, injury support, and escalation
* **Modular Tools**: Goal analysis, meal planning, workout recommendations, progress tracking, and scheduling
* **Context Management**: Persistent user sessions with SQLite database
* **Conversation History**: Complete chat history tracking and persistence
* **PDF Reports**: Generate comprehensive health reports for users
* **Command Interface**: Easy-to-use CLI commands for common tasks
* **Progress Tracking**: Individual user progress monitoring

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd health_agent
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🎯 Usage

### Start the CLI Application

```bash
uv run cli.py
```

### User Registration & Login

* **Register**: Create a new account with your name, email, and password
* **Login**: Use your email or user ID to access your account
* **Session Management**: Your conversation history and progress are automatically saved

### Available Commands

| Command    | Description                              |
| ---------- | ---------------------------------------- |
| `register` | Register a new user account              |
| `login`    | Login with email and password            |
| `login-id` | Login with user ID                       |
| `users`    | Show all registered users (admin)        |
| `report`   | Download your health report (PDF + JSON) |
| `context`  | Show your current context and data       |
| `clear`    | Clear conversation history               |
| `logout`   | Logout current user                      |
| `help`     | Show help information                    |
| `quit`     | Exit the application                     |

### Chat Commands

After logging in, you can chat directly with the AI agent! Just type your message and press Enter.

**Example conversation:**

```
💬 You: I want to lose 5kg in 2 months  
🤖 Agent: I'll help you create a plan to lose 5kg in 2 months! Let me analyze your goal...

💬 You: Can you create a meal plan for me?  
🤖 Agent: Here's your personalized vegetarian meal plan...

💬 You: What about a workout routine?  
🤖 Agent: Here's a workout routine designed for weight loss...
```

## 🏗️ Architecture Overview

* **Agents**: Main planner + Nutrition, Injury, and Escalation agents
* **Tools**: Goal analyzer, meal planner, workout recommender, scheduler, tracker
* **Database**: SQLite for user sessions and chat logs
* **Context**: Keeps track of user goals, preferences, and progress
* **PDF/JSON Reports**: Export user progress and plans

## 📝 Requirements

* Python 3.8+
* OpenAI API key
* Dependencies listed in `requirements.txt`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
