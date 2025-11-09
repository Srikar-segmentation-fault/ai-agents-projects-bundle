# ============================================================
# core/config.py
# ============================================================
# Central configuration for LLM models and environment.
# ============================================================

import os
from dotenv import load_dotenv
from core.exceptions import MissingAPIKeyError

# Load .env
load_dotenv()

def get_env_var(key: str, required: bool = False, default=None):
    """Helper to safely fetch environment variables."""
    value = os.getenv(key, default)
    if required and value is None:
        raise MissingAPIKeyError(f"Missing required environment variable: {key}")
    return value


# LLM configurations
LLM_PREFERENCES = {
    "groq": {
        "api_key": get_env_var("GROQ_API_KEY"),
        "model": get_env_var("GROQ_MODEL", default="llama-3.1-8b-instant"),
    },
    "openai": {
        "api_key": get_env_var("OPENAI_API_KEY"),
        "model": get_env_var("OPENAI_MODEL", default="gpt-4o-mini"),
    },
    "watsonx": {
        "api_key": get_env_var("WATSONX_API_KEY"),
        "model": get_env_var("WATSONX_MODEL_ID", default="ibm/granite-3-2-8b-instruct"),
        "url": get_env_var("WATSONX_URL", default="https://us-south.ml.cloud.ibm.com"),
        "project_id": get_env_var("WATSONX_PROJECT_ID"),
    },
}
