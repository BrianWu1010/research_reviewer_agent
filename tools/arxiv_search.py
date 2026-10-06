import re

import arxiv

from models import Paper

# arXiv asks API clients to wait ~3s between requests.
_client = arxiv.Client(page_size=50, delay_seconds=3.0, num_retries=3)


def search_arxiv(query: str, max_results: int = 10) -> list[Paper]:
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    papers = []
    for result in _client.results(search):
        papers.append(
            Paper(
                id=re.sub(r"v\d+$", "", result.get_short_id()),
                title=" ".join(result.title.split()),
                abstract=" ".join(result.summary.split()),
                authors=[author.name for author in result.authors],
                published=str(result.published.date()),
                url=result.entry_id,
                categories=list(result.categories),
            )
        )
    return papers
