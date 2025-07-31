import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_critic(user_query, summary_text):
    prompt = f'''
You are a Critic Agent in a multi-agent research system.

Your job is to evaluate whether the following paper summaries provide a satisfactory answer to the user's original research query.

Respond in this exact JSON format:

{{
  "verdict": "good",
  "justification": "your reasoning here",
  "suggestion": "optional suggestion for improvement if verdict is bad"
}}

---

User Query:
{user_query}

Paper Summaries:
{summary_text}

Evaluate based on:
- Relevance to the query
- Clarity and usefulness of the summary
- Coverage of the research question
'''
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    output = response.choices[0].message.content

    try:
        return json.loads(output)
    except:
        print("⚠️ Failed to parse Critic response. Raw output:")
        print(output)
        return {"verdict": "bad", "justification": "Parse error", "suggestion": "Improve output format"}