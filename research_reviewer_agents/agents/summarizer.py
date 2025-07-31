import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_paper(paper, prompt_template):
    prompt = prompt_template + "\n\n" + json.dumps(paper, indent=2)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def run_summarizer():
    with open("data/papers.json") as f:
        papers = json.load(f)

    with open("prompts/summarizer_prompt.txt") as f:
        template = f.read()

    summaries = []
    for paper in papers:
        summary = summarize_paper(paper, template)
        summaries.append(summary)


    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"output/summary_{timestamp}.md"

    with open(output_file, "w") as f:
        for summary in summaries:
            f.write(summary + "\n\n---\n\n")