# 💪 Health & Wellness Planner Agent - CLI Version

A comprehensive command-line interface for an AI-powered health and wellness planning agent built with OpenAI Agents SDK.

## 🚀 Features

- **User Registration & Login**: Individual user accounts with email/password authentication
- **Multi-Agent System**: Main health planner with specialized agents for nutrition, injury support, and escalation
- **Modular Tools**: Goal analysis, meal planning, workout recommendations, progress tracking, and scheduling
- **Context Management**: Persistent user sessions with SQLite database
- **Conversation History**: Complete chat history tracking and persistence
- **PDF Reports**: Generate comprehensive health reports for users
- **Command Interface**: Easy-to-use CLI commands for common tasks
- **Progress Tracking**: Individual user progress monitoring

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd health_agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🎯 Usage

### Start the CLI Application

```bash
uv run cli.py
```

### User Registration & Login

1. **Register**: Create a new account with your name, email, and password
2. **Login**: Use your email or user ID to access your account
3. **Session Management**: Your conversation history and progress are automatically saved

### Available Commands

| Command | Description |
|---------|-------------|
| `register` | Register a new user account |
| `login` | Login with email and password |
| `login-id` | Login with user ID |
| `users` | Show all registered users (admin) |
| `report` | Download your health report (PDF + JSON) |
| `context` | Show your current context and data |
| `clear` | Clear conversation history |
| `logout` | Logout current user |
| `help` | Show help information |
| `quit` | Exit the application |

### Chat Commands

After logging in, you can chat directly with the AI agent! Just type your message and press Enter.

**Example conversation:**
```
💬 You: I want to lose 5kg in 2 months
🤖 Agent: I'll help you create a plan to lose 5kg in 2 months! Let me analyze your goal...

💬 You: Can you create a meal plan for me?
🤖 Agent: I'll create a personalized meal plan based on your goals...

💬 You: What about a workout routine?
🤖 Agent: Here's a workout routine designed for weight loss...
```

**The system will:**
- Remember your previous conversations
- Track your goals and progress
- Generate personalized meal and workout plans
- Schedule check-ins and track progress
- Save all conversations automatically

### Example Session

```
============================================================
💪 Health & Wellness Planner Agent - CLI Version
============================================================
Agent: HealthWellnessPlanner
Tools: 5
Handoffs: 3
User: User (ID: 1)
============================================================
Type 'help' for commands, 'quit' to exit
============================================================

💬 You: I want to lose 10 pounds in 3 months
🤖 Agent is thinking...
🔧 Tool used: analyze_goal
🤖 Agent: I'll help you create a plan to lose 10 pounds in 3 months! Let me analyze your goal and create a personalized approach.

💬 You: goal lose 10 pounds in 3 months
✅ Goal set: lose 10 pounds in 3 months

💬 You: diet vegetarian
✅ Diet preferences set: vegetarian

💬 You: plan
🎯 Generating meal and workout plans...
🤖 Agent is thinking...
🔧 Tool used: meal_planner
🔧 Tool used: workout_recommender
🤖 Agent: Here's your personalized plan for losing 10 pounds in 3 months:

**Meal Plan (Vegetarian):**
- Day 1: High-protein vegetarian breakfast...
- Day 2: Nutrient-rich lunch options...

**Workout Plan:**
- Day 1: Cardio and strength training...
- Day 2: Flexibility and core work...
```

## 🏗️ Architecture

### Agents
- **HealthWellnessPlanner**: Main agent coordinating all health planning
- **NutritionExpertAgent**: Specialized agent for dietary needs
- **InjurySupportAgent**: Agent for injury-specific workout plans
- **EscalationAgent**: Agent for human coach handoffs

### Tools
- `analyze_goal`: Parse and structure user goals
- `meal_planner`: Generate personalized meal plans
- `workout_recommender`: Create workout recommendations
- `checkin_scheduler`: Schedule weekly check-ins
- `progress_tracker`: Log and track user progress

### Data Management
- **SQLite Database**: Persistent user sessions
- **Context Management**: Real-time state updates
- **Session Persistence**: Automatic save/load functionality

## 🔧 Development

### Project Structure
```
health_agent/
├── cli.py                 # Main CLI application
├── agent.py              # Agent creation and configuration
├── context.py            # User session context model
├── db.py                 # Database operations
├── orchestrator.py       # Tool output handling
├── guardrails.py         # Input validation
├── tools/                # Agent tools
│   ├── goal_analyzer.py
│   ├── meal_planner.py
│   ├── workout_recommender.py
│   ├── scheduler.py
│   └── tracker.py
├── agents/               # Specialized agents
│   ├── escalation_agent.py
│   ├── nutrition_expert_agent.py
│   └── injury_support_agent.py
└── requirements.txt      # Dependencies
```

### Testing
Run the agent connection test:
```bash
python test_agent_connections.py
```

## 📝 Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in `requirements.txt`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
