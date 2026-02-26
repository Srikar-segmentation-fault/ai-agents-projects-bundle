# workflow.py
import time
from crewai import Crew, Process
from agents import AGENTS
from tasks import get_tasks


TOKEN_LIMIT = 8000  # Groq safe buffer (12k TPM limit)
COOLDOWN_TIME = 15  # seconds before next run if exceeded


def print_token_budget(result):
    """Show token usage summary and handle rate limit warning."""
    usage = getattr(result, "token_usage", None)
    if not usage:
        print("⚠️ No token usage info found in result.")
        return

    total = usage.total_tokens
    prompt = usage.prompt_tokens
    completion = usage.completion_tokens

    print("\n📊 Token Usage Summary:")
    print(f"Total: {total} | Prompt: {prompt} | Completion: {completion}")

    if total >= TOKEN_LIMIT:
        print("\n🚨 TOKEN LIMIT ALERT!")
        print(f"⚠️ Token usage reached {total} (limit {TOKEN_LIMIT})")
        print("🧠 CrewAI agents will now stop to avoid hitting Groq rate limits.")
        print(f"💤 Cooling down for {COOLDOWN_TIME} seconds...\n")
        time.sleep(COOLDOWN_TIME)
        raise RuntimeError(
            f"Token limit reached ({total}/{TOKEN_LIMIT}). "
            f"Cooled down for {COOLDOWN_TIME}s. Please retry."
        )


def run_workflow(topic: str):
    """Run the complete CrewAI multi-agent workflow."""
    print("🚀 Initializing Multi-Agent Workflow...\n")

    # Fresh task instances per request — avoids shared state between API calls
    tasks = get_tasks()

    crew = Crew(
        agents=[
            AGENTS["Research Agent"],
            AGENTS["Writer Agent"],
            AGENTS["Social Media Agent"]
        ],
        tasks=[
            tasks["Research Task"],
            tasks["Writer Task"],
            tasks["Social Media Task"]
        ],
        process=Process.sequential,
        verbose=True
    )

    print(f"🧩 Running workflow for topic: {topic}\n")

    try:
        result = crew.kickoff(inputs={"topic": topic})
        print("\n✅ Workflow Completed!\n")
        print("🧾 Final Combined Output:\n")
        print(result.raw[:1500])  # Print only part to avoid long scrolls

        # Per-task outputs
        print("\n📘 Task-wise Outputs:")
        for idx, task_output in enumerate(result.tasks_output):
            print(f"\n--- Task {idx+1} ---")
            print(f"{task_output.raw[:600]}...")
            print("\n-----------------------------")

        # Token check
        print_token_budget(result)
        return result

    except RuntimeError:
        # Re-raise rate-limit errors (from print_token_budget) as-is
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("💡 Tip: You might be hitting Groq rate limits. Wait a few seconds and retry.")
        raise


if __name__ == "__main__":
    topic = input("Enter topic for AI Research: ") or "Future of Agentic AI Platforms"
    run_workflow(topic)
