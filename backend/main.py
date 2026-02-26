
import sys
import os
import json
import subprocess
import importlib.util
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from the root of the workspace
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(workspace_root, '.env'))

app = FastAPI(title="AI Agents Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Agent 01 Integration (importlib for explicit, safe loading) ---
agent01_module = None
try:
    agent01_path = os.path.join(workspace_root, 'agent01-math-assistant', 'main.py')
    agent01_dir = os.path.join(workspace_root, 'agent01-math-assistant')
    # Ensure agent01 and its core sub-package are importable
    if agent01_dir not in sys.path:
        sys.path.insert(0, agent01_dir)
    spec = importlib.util.spec_from_file_location("agent01_main", agent01_path)
    agent01_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent01_module)
    print("✅ Agent 01 imported successfully.")
except ImportError as e:
    print(f"❌ Error importing Agent 01: {e}")
except Exception as e:
    print(f"❌ Error initializing Agent 01: {e}")

# --- Agent 03: Subprocess path (uses its own venv2 to avoid dep conflicts) ---
# Determine the correct venv Python for agent03
agent03_dir = os.path.join(workspace_root, 'agent03')
agent03_python = os.path.join(agent03_dir, 'venv2', 'Scripts', 'python.exe')
agent03_runner = os.path.join(agent03_dir, 'run_workflow.py')

agent03_available = os.path.isfile(agent03_python) and os.path.isfile(agent03_runner)
if agent03_available:
    print("✅ Agent 03 subprocess runner ready.")
else:
    print(f"❌ Agent 03 runner not found. Expected: {agent03_python}")


# --- Data Models ---
class QueryRequest(BaseModel):
    query: str

class ResearchRequest(BaseModel):
    topic: str


# --- Endpoints ---

@app.get("/")
def health_check():
    return {"status": "ok", "agents": {
        "agent01": agent01_module is not None,
        "agent03": agent03_available
    }}

@app.post("/api/agent01/query")
def query_agent01(request: QueryRequest):
    if not agent01_module:
        raise HTTPException(status_code=503, detail="Agent 01 is not available (failed to load).")

    try:
        result = agent01_module.run_query(request.query)

        # Parse result
        output = "No output returned."
        if isinstance(result, dict):
            output = result.get("output", str(result))
        elif hasattr(result, "output"):
            output = result.output
        else:
            output = str(result)

        return {"response": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent03/research")
def research_agent03(request: ResearchRequest):
    if not agent03_available:
        raise HTTPException(status_code=503, detail="Agent 03 is not available.")

    if not request.topic:
        raise HTTPException(status_code=400, detail="Topic is required.")

    try:
        print(f"Running research on: {request.topic}")

        # Run agent03 in its own isolated venv via subprocess
        proc = subprocess.run(
            [agent03_python, agent03_runner, request.topic],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute max
            cwd=agent03_dir,
        )

        # Find the last JSON line in stdout (workflow may print other logs before it)
        output_lines = [l.strip() for l in proc.stdout.strip().splitlines() if l.strip()]
        json_result = None
        for line in reversed(output_lines):
            try:
                json_result = json.loads(line)
                break
            except json.JSONDecodeError:
                continue

        if json_result is None:
            raise ValueError(f"No JSON output from agent03. stderr: {proc.stderr[-500:]}")

        if "error" in json_result:
            raise HTTPException(status_code=500, detail=json_result["error"])

        return {
            "final_output": json_result.get("final_output", ""),
            "tasks_output": json_result.get("tasks_output", [])
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Agent 03 timed out after 5 minutes.")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in Agent 03: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
