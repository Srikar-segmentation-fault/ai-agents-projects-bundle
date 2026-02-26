"""
run_query.py — Subprocess entry point for agent01.
Called by the backend via subprocess using agent01's own venv1.
Accepts query as a CLI argument, outputs JSON result to stdout.
"""
import sys
import json
import os

# Ensure .env is loaded from project root
from dotenv import load_dotenv
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(workspace_root, '.env'))

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}))
        sys.exit(1)

    query = sys.argv[1]

    try:
        # Import main to initialize the agent
        from main import run_query
        result = run_query(query)

        output = "No output returned."
        if isinstance(result, dict):
            output = result.get("output", str(result))
        elif hasattr(result, "output"):
            output = result.output
        else:
            output = str(result)

        print(json.dumps({"response": output}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
