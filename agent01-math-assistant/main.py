# ============================================================
# main.py — Entry Point for AI Math & Knowledge Agent
# ============================================================

from core.logger import setup_logger
from core.config import LLM_PREFERENCES
from core.exceptions import LLMInitializationError
from tools import all_tools

# Modern LangChain 0.3+ agent API
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# ------------------------------------------------------------
# Step 1: Setup Logger
# ------------------------------------------------------------
logger = setup_logger("AgentMain")

# ------------------------------------------------------------
# Step 2: Initialize LLM Dynamically (Groq → OpenAI → WatsonX)
# ------------------------------------------------------------
llm = None
backend_used = None

try:
    # Try Groq first
    from langchain_groq import ChatGroq
    groq_api = LLM_PREFERENCES["groq"]["api_key"]
    if groq_api:
        llm = ChatGroq(
            groq_api_key=groq_api,
            model=LLM_PREFERENCES["groq"]["model"]
        )
        backend_used = "groq"
except Exception as e:
    logger.warning(f"Groq initialization failed: {e}")

if not llm:
    try:
        # Try OpenAI fallback
        from langchain_openai import ChatOpenAI
        openai_api = LLM_PREFERENCES["openai"]["api_key"]
        if openai_api:
            llm = ChatOpenAI(
                api_key=openai_api,
                model=LLM_PREFERENCES["openai"]["model"],
                base_url=LLM_PREFERENCES["openai"]["base_url"],
            )
            backend_used = "openai (Groq-compatible)"
    except Exception as e:
        logger.warning(f"OpenAI initialization failed: {e}")

if not llm:
    try:
        # Try IBM WatsonX
        from langchain_ibm import ChatWatsonx
        watson_cfg = LLM_PREFERENCES["watsonx"]
        if watson_cfg["api_key"]:
            llm = ChatWatsonx(
                model_id=watson_cfg["model"],
                url=watson_cfg["url"],
                project_id=watson_cfg["project_id"],
                api_key=watson_cfg["api_key"],
            )
            backend_used = "watsonx"
    except Exception as e:
        logger.error(f"WatsonX initialization failed: {e}")

if not llm:
    raise LLMInitializationError("No valid LLM initialized. Check API keys or .env file.")

logger.info(f"✅ Using {backend_used} backend.")


# ------------------------------------------------------------
# Step 3: Initialize Agent with Tools
# ------------------------------------------------------------
try:
    # Pull the standard ReAct prompt from LangChain Hub
    prompt = hub.pull("hwchase17/react")
    react_agent = create_react_agent(
        llm=llm,
        tools=all_tools,
        prompt=prompt,
    )
    agent = AgentExecutor(
        agent=react_agent,
        tools=all_tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )
    logger.info(f"🤖 Agent initialized successfully using {backend_used}.")
except Exception as e:
    logger.error(f"Agent initialization failed: {e}")
    raise


# ------------------------------------------------------------
# Step 4: Define Query Runner
# ------------------------------------------------------------
def run_query(prompt: str):
    """Run a query through the agent and return the result."""
    logger.info(f"💬 User Query: {prompt}")
    try:
        result = agent.invoke({"input": prompt})
        logger.info(f"🧩 Agent Output: {result}")
        # print("\n🧠 Result:", result) # Suppress print for API usage
        return result
    except Exception as e:
        logger.error(f"❌ Agent failed: {e}")
        return {"output": f"Error: {str(e)}"}


# ------------------------------------------------------------
# Step 5: Demo Queries
# ------------------------------------------------------------
if __name__ == "__main__":
    logger.info("🤖 Agent is live! Type 'exit' to quit.")
    while True:
        query = input("\n🧠 Enter your question: ")
        if query.lower() in ["exit", "quit", "q"]:
            print("👋 Exiting.")
            break
        run_query(query)

