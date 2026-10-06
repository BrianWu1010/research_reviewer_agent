from models import Critique, Paper
from tools.llm import chat_json

SYSTEM = """You are the Critic in a multi-agent literature review system.
You review a literature-based answer to a research question and decide whether more searching is needed.

Evaluate:
- Coverage: does it address every part of the question?
- Grounding: are claims supported by the cited papers, without overreach?
- Evidence strength: is it based on enough relevant papers, or on one or two?

- Foundations: are the seminal / most-cited works on this topic among the papers used?

verdict = "sufficient" only if a researcher would find this a solid starting answer AND no
foundational work or major facet of the question is missing. If you can name important missing
papers or facets, the verdict must be "needs_more".
If "needs_more", list specific missing_aspects that a new literature search should target:
exact titles of missing papers where you know them, otherwise topics, method families, or evidence types.
Keep each aspect short and searchable."""


def run_critic(question: str, answer: str, papers: list[Paper]) -> Critique:
    titles = "\n".join(f"[{number}] {paper.title}" for number, paper in enumerate(papers, start=1))
    user = f"Research question:\n{question}\n\nPapers used:\n{titles}\n\nAnswer under review:\n{answer}"
    return chat_json(SYSTEM, user, Critique)
