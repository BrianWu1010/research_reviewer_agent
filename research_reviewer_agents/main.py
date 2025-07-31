from agents.planner import run_planner
from agents.retriever import run_retriever
from agents.summarizer import run_summarizer
from agents.critic import run_critic

import glob
import time

def get_latest_summary():
    summary_files = sorted(glob.glob("output/summary_*.md"))
    return summary_files[-1] if summary_files else None

if __name__ == "__main__":
    user_query = "How does curiosity improve exploration in reinforcement learning?"

    for attempt in range(3):  # Max 3 loops to avoid infinite retry
        print(f"\n🔁 Attempt #{attempt + 1}\n")

        print("🧠 Planning...")
        subqueries = run_planner(user_query)
        for q in subqueries:
            print(" -", q)

        print("🔍 Retrieving papers...")
        run_retriever(subqueries)

        print("📝 Summarizing papers...")
        run_summarizer()

        print("🤔 Critiquing summary...")
        latest = get_latest_summary()
        with open(latest, "r") as f:
            summary = f.read()

        critique = run_critic(user_query, summary)
        print(f"🧪 Verdict: {critique['verdict']}")
        print(f"📋 Justification: {critique['justification']}")

        if critique["verdict"] == "good":
            print("✅ Summary is good enough. Finished.")
            break
        else:
            print(f"🔄 Replanning based on suggestion: {critique['suggestion']}")
            user_query = critique['suggestion']
            time.sleep(2)

    else:
        print("❌ Max attempts reached. Stopping.")