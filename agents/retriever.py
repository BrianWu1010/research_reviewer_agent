from models import Paper
from tools.arxiv_search import search_arxiv


def run_retriever(
    queries: list[str],
    seen_ids: set[str],
    per_query: int = 10,
) -> list[Paper]:
    """Return papers for `queries` that are not in `seen_ids`."""
    new_papers: dict[str, Paper] = {}
    for query in queries:
        try:
            results = search_arxiv(query, max_results=per_query)
        except Exception as err:
            print(f"  arXiv search failed for {query!r}: {err}")
            continue
        for paper in results:
            if paper.id not in seen_ids and paper.id not in new_papers:
                new_papers[paper.id] = paper
    return list(new_papers.values())
