import arxiv

def search_arxiv(query: str, max_results: int = 3):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.entry_id,
            "authors": [author.name for author in result.authors],
            "published": str(result.published.date())
        })
    return results