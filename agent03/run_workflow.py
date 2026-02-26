"""
run_workflow.py — Subprocess entry point for agent03.
Called by the backend via subprocess using agent03's own venv.
Accepts topic as a CLI argument, outputs JSON result to stdout.
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
        print(json.dumps({"error": "No topic provided"}))
        sys.exit(1)

    topic = sys.argv[1]

    try:
        from workflow import run_workflow
        result = run_workflow(topic)

        tasks = []
        if hasattr(result, "tasks_output"):
            for t in result.tasks_output:
                tasks.append({
                    "description": t.description,
                    "output": t.raw,
                    "agent": t.agent
                })

        output = {
            "final_output": result.raw,
            "tasks_output": tasks
        }
        print(json.dumps(output))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
