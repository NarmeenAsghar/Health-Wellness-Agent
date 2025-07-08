# 💪 Health & Wellness Planner Agent - CLI Version

An AI-powered assistant built to promote healthy living by providing expert-like guidance, answering medical queries, and suggesting personalized wellness advice. This project uses language models to simulate a natural and helpful conversation with users.

## 🌟 Key Features

- **🤖 AI Medical Q&A**  
  Ask health-related questions and receive reliable, AI-powered responses.

- **🍏 Lifestyle Coaching**  
  Get science-backed suggestions on diet, fitness, mental well-being, hydration, and sleep.

- **🩺 Symptom Checker**  
  Describe your symptoms to receive general advice and possible causes (for awareness only).

- **💬 Conversational Interface**  
  Seamlessly interact via natural language in the command line or web-based UI (if added).

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Health_Advisor_Agent.git
cd Health_Advisor_Agent
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI credentials

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the application

```bash
python main.py
```


## 💡 How to Use

Once the app is running, simply start chatting:

* `What are the symptoms of flu?`
* `How much water should I drink daily?`
* `Give me a healthy vegetarian meal plan.`

The agent will analyze your request and respond with structured, contextual advice.

## 🧰 Tech Stack

* **Python 3.x**
* **OpenAI API** (e.g., GPT-3.5/4 via `openai` SDK)
* Optional: **Flask** or **Streamlit** for UI
* **dotenv** for environment configuration
* Other dependencies listed in `requirements.txt`

## ⚠️ Disclaimer

> This application is for **educational and informational purposes only**.
> It does **not replace medical consultation**. Always seek guidance from a qualified healthcare provider.


## 🤝 Contributing

Contributions are welcome!

* Fork the repository
* Create a feature branch
* Commit and push your changes
* Submit a pull request


## 📜 License

This project is licensed under the [MIT License](LICENSE).
