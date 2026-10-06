from concurrent.futures import ThreadPoolExecutor

from models import Paper, PaperNotes
from tools.llm import chat_json

SYSTEM = """You are the Summarizer in a multi-agent literature review system.
Extract structured notes from one arXiv paper, focused on a specific research question.

You only have the title and abstract. Strict grounding rules:
- Use only information stated in the abstract. Do not invent numbers, datasets, or baselines.
- If the abstract does not state something (e.g. limitations), leave that field empty
  rather than guessing.
- "relevance" should explain concretely what this paper contributes to answering the question."""


def summarize_paper(question: str, paper: Paper) -> PaperNotes:
    user = (
        f"Research question:\n{question}\n\n"
        f"paper_id: {paper.id}\n"
        f"title: {paper.title}\n"
        f"published: {paper.published}\n"
        f"abstract: {paper.abstract}"
    )
    notes = chat_json(SYSTEM, user, PaperNotes)
    notes.paper_id = paper.id
    return notes


def run_summarizer(question: str, papers: list[Paper], max_workers: int = 8) -> list[PaperNotes]:
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(lambda paper: summarize_paper(question, paper), papers))
