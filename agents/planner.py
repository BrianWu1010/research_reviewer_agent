from models import SearchPlan
from tools.llm import chat_json

SYSTEM = """You are the Planner in a multi-agent literature review system.
You turn a research question into search queries for the arXiv API.

arXiv query syntax:
- Field prefixes: ti: (title), abs: (abstract), cat: (category, e.g. cat:cs.LG).
- Boolean operators in UPPERCASE: AND, OR, ANDNOT. Group with parentheses.
- Quote multi-word phrases: abs:"reinforcement learning".
- Bare unprefixed words are matched loosely and return noisy results, so always use field prefixes.

Good query: abs:"intrinsic motivation" AND abs:exploration AND abs:"reinforcement learning"
Good query: (ti:curiosity OR ti:novelty) AND abs:"sparse reward"

Guidelines:
- Each query should target a different facet of the question (mechanisms, methods, evaluations, failure modes, ...).
- Use the vocabulary researchers actually use, including common synonyms (combine them with OR).
- Combine 2-4 concepts with AND. Too many ANDs returns nothing; too few returns noise."""


def run_planner(
    question: str,
    num_queries: int = 4,
    missing_aspects: list[str] | None = None,
    previous_queries: list[str] | None = None,
) -> list[str]:
    user = f"Research question:\n{question}\n\nWrite {num_queries} arXiv queries."
    if missing_aspects:
        gaps = "\n".join(f"- {aspect}" for aspect in missing_aspects)
        user += (
            "\n\nA reviewer found the current literature review is missing these aspects. "
            f"Target them specifically:\n{gaps}"
        )
    if previous_queries:
        done = "\n".join(f"- {query}" for query in previous_queries)
        user += f"\n\nThese queries were already run; do not repeat them:\n{done}"

    plan = chat_json(SYSTEM, user, SearchPlan)
    return [query.strip() for query in plan.queries if query.strip()][:num_queries]
