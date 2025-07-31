# 🧠 Research Reviewer Agents

A multi-agent research assistant that automates the process of answering complex research questions using planning, retrieval, summarization, critique, and replanning.
<img width="608" height="642" alt="Screenshot 2025-07-31 at 3 50 24 PM" src="https://github.com/user-attachments/assets/f1b4939b-1f47-4a28-99bc-274be47ef82d" />

## 🚀 Features

- **Planner Agent**: Decomposes the user's query into keywords and refined search phrases.
- **Retriever Agent**: Searches arXiv using those phrases to retrieve relevant papers.
- **Summarizer Agent**: Summarizes key insights from the papers into a markdown file.
- **Critic Agent**: Evaluates whether the summary answers the original question; if not, suggests a better reformulation and triggers a replanning loop.

## 🔁 Workflow

1. User submits a query.
2. Planner generates search phrases.
3. Retriever fetches papers based on those phrases.
4. Summarizer produces a summary of the papers.
5. Critic evaluates the summary.
6. If verdict is “bad,” loop begins again using the Critic’s suggestion.

## 📦 Setup

```bash
conda env create -f environment.yml
conda activate research_agents
```

## ▶️ Run the System

```bash
python main.py
```

## 🗂️ Output

- Summaries are saved in: `output/summary_<timestamp>.md`
- Retrieved papers in: `data/papers.json`

## 💡 To Do

- Add Feedback Agent
- Improve Critic with LLM chaining
- Add UI for user interaction

## 👤 Author

Boyuan Wu

## Example output:
"
🔁 Attempt #1

🧠 Planning...
 - curiosity AND improvement AND exploration in reinforcement learning
 - impact of curiosity on exploration enhancement in reinforcement learning
 - curiosity-driven exploration AND performance improvement in reinforcement learning
🔍 Retrieving papers...

✅ Retrieved 9 unique papers.

📝 Summarizing papers...

🤔 Critiquing summary...

🧪 Verdict: good

📋 Justification: The papers 'From Curiosity to Competence: How World Models Interact with the Dynamics of Exploration', 'Optimizing Model Splitting and Device Task Assignment for Deceptive Signal Assisted Private Multi-hop Split Learning', 'Beyond-Expert Performance with Limited Demonstrations: Efficient Imitation Learning with Double Exploration', and 'Deep reinforcement learning for efficient exploration of combinatorial structural design spaces' provide relevant information to the user's query about how curiosity improves exploration in reinforcement learning. They discuss different methods and experiments that demonstrate the role of curiosity in improving exploration and performance in reinforcement learning tasks. The summaries are clear, detailed, and cover the key contributions, methods, experiments, findings, and limitations of the research.

✅ Summary is good enough. Finished.
"
