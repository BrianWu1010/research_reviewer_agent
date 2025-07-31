from tools.arxiv_search import search_arxiv
import json

def run_retriever(search_phrases):
    all_papers = []
    seen_titles = set()

    for phrase in search_phrases:
        papers = search_arxiv(phrase)
        for paper in papers:
            if paper['title'] not in seen_titles:
                all_papers.append(paper)
                seen_titles.add(paper['title'])

    with open("data/papers.json", "w") as f:
        json.dump(all_papers, f, indent=2)

    print(f"✅ Retrieved {len(all_papers)} unique papers.")
    return all_papers