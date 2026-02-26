# 🤖 AI Agent Workspace

A full-stack **multi-agent AI dashboard** built with FastAPI (backend) and React/Vite (frontend).  
Each agent is independently developed and exposed through a unified web interface where you can interact with them in real time.

---

## 🧩 Agents Overview

| Agent                                     | Type        | Tech Stack                | Description                                                                                                                   |
| ----------------------------------------- | ----------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Agent 01** — Math & Knowledge Assistant | Chat        | LangChain + Groq          | Solves math problems and answers knowledge questions using a multi-LLM fallback strategy (Groq → OpenAI-compatible → WatsonX) |
| **Agent 02** — AI NourishBot              | Gradio App  | CrewAI + WatsonX + Gradio | Detects food ingredients from images, estimates calories, runs nutrient analysis, and suggests recipes                        |
| **Agent 03** — Research Workflow Agent    | Multi-Agent | CrewAI + Groq + Serper    | Autonomously researches any topic, writes a blog post, and generates LinkedIn/Twitter social media content                    |

---

## 🏗️ Project Structure

```
ai-agent-projects/
│
├── agent01-math-assistant/       # LangChain ReAct agent
│   ├── core/                     # Config, logger, exceptions
│   ├── tools.py                  # Math + Wikipedia tools
│   ├── main.py                   # Agent initialization + run_query()
│   ├── run_query.py              # Subprocess entry point (used by backend)
│   └── requirements.txt
│
├── agent02/
│   └── Smart-Nutritional-App/    # CrewAI + Gradio nutrition app
│
├── agent03/                      # CrewAI multi-agent research workflow
│   ├── agents.py                 # Research, Writer, Social Media agents
│   ├── tasks.py                  # Task factory (get_tasks())
│   ├── workflow.py               # Crew orchestration
│   ├── run_workflow.py           # Subprocess entry point (used by backend)
│   └── requirements.txt
│
├── backend/                      # FastAPI server
│   ├── main.py                   # API routes for agent01 and agent03
│   └── requirements.txt
│
├── frontend/                     # React + Vite dashboard
│   └── src/
│       ├── App.jsx               # Main UI with agent cards + terminal modal
│       ├── projects.json         # Agent metadata and API endpoints
│       └── index.css
│
└── .env                          # API keys (not committed)
```

---

## ⚙️ Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- API Keys (add to `.env` in the project root):

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
OPENAI_API_KEY=your_groq_api_key        # Groq used as OpenAI-compatible fallback
OPENAI_MODEL_NAME=openai/gpt-oss-120b
OPENAI_API_BASE_URL=https://api.groq.com/openai/v1
```

---

## 🚀 Setup & Running

### 1. Backend (FastAPI)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The backend will load Agent 01 directly and run Agent 03 via subprocess using `agent03/venv2`.

### 2. Agent 01 — Math Assistant (standalone venv)

```powershell
cd agent01-math-assistant
python -m venv venv1
.\venv1\Scripts\activate
pip install langchain==0.2.16 langchain-groq langchain-openai langchain-community wikipedia python-dotenv
```

> The backend calls `agent01/run_query.py` via this venv automatically.

### 3. Agent 03 — Research Workflow (standalone venv)

```powershell
cd agent03
python -m venv venv2
.\venv2\Scripts\activate
pip install -r requirements.txt
```

> The backend calls `agent03/run_workflow.py` via this venv automatically.

### 4. Frontend (React + Vite)

```powershell
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🌐 API Endpoints

| Method | Endpoint                | Description                                           |
| ------ | ----------------------- | ----------------------------------------------------- |
| `GET`  | `/`                     | Health check — shows which agents are available       |
| `POST` | `/api/agent01/query`    | `{ "query": "..." }` → Math / knowledge answer        |
| `POST` | `/api/agent03/research` | `{ "topic": "..." }` → Research + blog + social posts |

### Agent 03 Response Shape

```json
{
  "final_output": "...",
  "tasks_output": [
    { "agent": "Senior Research Analyst", "output": "..." },
    { "agent": "Tech Content Strategist", "output": "..." },
    { "agent": "Social Media Strategist", "output": "..." }
  ]
}
```

---

## 🖥️ Frontend Dashboard

- **Agent cards** for each project with tags, description, and a launch button
- **Terminal modal** to interact with Agent 01 (math chat) and Agent 03 (research workflow)
- **Per-agent output sections** — Agent 03 results are displayed in separate labeled panels for each agent in the crew
- **ReactMarkdown rendering** for formatted outputs

---

## 🔑 Key Design Decisions

- **Subprocess isolation**: Agent 01 and Agent 03 each run in their own virtual environments via subprocess, avoiding dependency conflicts between LangChain and CrewAI versions
- **Task factory pattern**: `get_tasks()` in `agent03/tasks.py` creates fresh CrewAI Task instances per request, preventing shared state across concurrent API calls
- **Graceful error handling**: All `sys.exit()` calls replaced with proper exceptions so the FastAPI server never dies on agent failures

---

## 📄 License

See [LICENSE.md](./LICENSE.md) for details.

# agent01:

title: Math Assistant
description: A Math problem solving agent which demonstrates the fundamental working of tool calling in AI Agents.

======================================================================================================================================

# agent02:

---

title: AI_NourishBot
app_file: app.py
sdk: gradio
sdk_version: 5.12.0

---

# AI NourishBot (aka AI Dietary Crew)

AI NourishBot is an AI-powered nutrition assistant that leverages advanced vision models and natural language processing to detect ingredients from food images, filter ingredients based on dietary restrictions, estimate calories, provide detailed nutrient analysis, and generate recipe suggestions. This project demonstrates the use of CrewAI, WatsonX, and other AI tools to deliver insightful and personalized nutritional feedback.

## Features

- **Ingredient Detection**  
  Detects ingredients from user-uploaded images using a vision AI model.

- **Dietary Filtering**  
  Filters detected ingredients based on user-defined dietary restrictions (e.g., vegan, gluten-free).

- **Calorie Estimation**  
  Estimates total calories from the detected ingredients.

- **Nutrient Analysis**  
  Provides a detailed breakdown of key nutrients such as protein, carbohydrates, fats, vitamins, and minerals.

- **Health Evaluation**  
  Summarizes the overall healthiness of the meal and provides a health evaluation.

- **Recipe Suggestion**  
  Generates recipe ideas based on the filtered ingredients and dietary restrictions.

## How It Works

The project is built using the CrewAI framework, which organizes agents and tasks into workflows for two primary use cases:

1. **Recipe Workflow**  
   Detects ingredients, filters them based on dietary restrictions, and suggests recipes.

2. **Analysis Workflow**  
   Directly estimates calories, performs nutrient analysis, and provides a health evaluation summary from a food image.

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (optional but recommended)
- Git

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HaileyTQuach/Smart-Nutritional-App.git
   cd Smart-Nutritional-App
   ```
2. **Create and activate a virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the required dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create a .env file in the root directory with the following keys**:
   ```bash
    WATSONX_API_KEY=your_watsonx_api_key
    WATSONX_URL=your_watsonx_url
    WATSONX_PROJECT_ID=your_watsonx_project_id
   ```

## Usage

### Run the Application

You can run the application using the following commands:

1. For recipe suggestions

```bash
python main.py <image_path> <dietary_restrictions> recipe
```

Example:

```bash
python main.py food.jpg vegan recipe
```

2. For food analysis

```bash
python main.py <image_path> analysis
```

Example:

```bash
python main.py food.jpg analysis
```

3. For training (future functionality - TODO)

```bash
python main.py train <n_iterations> <output_filename> <image_path> <dietary_restrictions> <workflow_type>
```

## File Structure

```
Smart-Nutritional-App-Crew/
│
├── config/
│   ├── agents.yaml               # Configuration for agents
│   └── tasks.yaml                # Configuration for tasks
│
├── src/
│   ├── crew.py                   # Crew definitions (agents, tasks, workflows)
│   ├── tools.py                  # Tool definitions for ingredient detection, filtering, etc.
│   └── main.py                   # Main script for running the application
│
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please create a pull request or open an issue.

## License

### License

This project is licensed under the **Hailey Thao Quach's Non-Commercial License**. See the `LICENSE` file for details.

## Contact

For any questions or support, please contact [Hailey Thao Quach](mailto:hailey@haileyq.com).

==========================================================================================

# 🤖 Agent03 — Multi-Agent AI Content Automation System

Agent03 is a **CrewAI-powered multi-agent system** designed to automate research, content writing, and social media strategy.  
This project demonstrates how multiple AI agents can collaborate like a human team — performing research, writing, and summarizing — all powered by LLMs and real-time tools.

---

## 🧠 **Overview**

This system uses **CrewAI**, **LangChain**, and **Groq LLMs** to simulate a cognitive workflow:

1. **Research Analyst Agent** → Gathers real-time insights from the web using Serper.
2. **Writer Agent** → Converts research into polished, reader-friendly blog content.
3. **Social Media Strategist Agent** → Creates short-form posts (LinkedIn, X/Twitter) from the blog summary.

All agents work **sequentially** under a unified CrewAI workflow.

---

## 🚀 **Project Structure**

agent03/
├── agents.py # Defines all CrewAI agents (Researcher, Writer, Social Media)
├── tasks.py # Defines each agent’s tasks and expected outputs
├── workflow.py # Runs the entire Crew workflow (sequential pipeline)
├── requirements.txt # Python dependencies

---

## ⚙️ **Setup Instructions**

### 1️⃣ Clone the Repository

git clone https://github.com/<your-username>/agent03.git
cd agent03

### 2️⃣ Create a Virtual Environment

python -m venv venv2
source venv2/bin/activate # For Linux/Mac
venv2\Scripts\activate

### 3️⃣ Install Dependencies

pip install -r requirements.txt

## Serper API (for web search)

SERPER_API_KEY=your_serper_api_key_here

## LLM API (OpenAI or Gemini etc.)

OPENAI_API_KEY=your_groq_api_key_here

## 🧩 How to Run

Run the complete workflow directly:
python workflow.py

## 🧪 Example Run

Enter topic for AI Research: generative ai
🚀 Initializing Multi-Agent Workflow...

🧩 Running workflow for topic: generative ai

✅ Workflow Complete!
📘 Task Outputs:
1️⃣ Research Summary → Key trends in GenAI
2️⃣ Blog Post → 4-paragraph article
3️⃣ Social Media Summary → Tweets and LinkedIn posts
📊 Token Usage: 8570 / 12000
