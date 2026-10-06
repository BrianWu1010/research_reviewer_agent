from concurrent.futures import ThreadPoolExecutor

from models import Paper, RelevanceScore, ScreeningResult
from tools.llm import chat_json

SYSTEM = """You are the Screener in a multi-agent literature review system.
Given a research question and a batch of arXiv papers (title + abstract), rate how useful
each paper is for answering the question, from 0 to 10:

10 = directly studies the question; central evidence
7-9 = substantially relevant (proposes/evaluates a method the question is about)
4-6 = tangentially relevant (uses the concept in passing, different focus)
0-3 = off-topic (shares keywords only)

Judge from the abstract only. Be strict: keyword overlap is not relevance.
Return one score per paper, using the exact paper_id given."""


def _screen_batch(question: str, batch: list[Paper]) -> list[RelevanceScore]:
    listing = "\n\n".join(
        f"paper_id: {paper.id}\ntitle: {paper.title}\nabstract: {paper.abstract}" for paper in batch
    )
    user = f"Research question:\n{question}\n\nPapers:\n\n{listing}"
    result = chat_json(SYSTEM, user, ScreeningResult)
    batch_ids = {paper.id for paper in batch}
    return [score for score in result.scores if score.paper_id in batch_ids]


def run_screener(
    question: str,
    papers: list[Paper],
    batch_size: int = 10,
    max_workers: int = 4,
) -> dict[str, RelevanceScore]:
    batches = [papers[i : i + batch_size] for i in range(0, len(papers), batch_size)]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = pool.map(lambda batch: _screen_batch(question, batch), batches)
    return {score.paper_id: score for batch_scores in results for score in batch_scores}
