from dataclasses import dataclass, field
from typing import Callable

from agents.critic import run_critic
from agents.planner import run_planner
from agents.retriever import run_retriever
from agents.screener import run_screener
from agents.summarizer import run_summarizer
from agents.synthesizer import run_synthesizer
from models import Critique, Paper, PaperNotes, RelevanceScore


@dataclass
class ReviewConfig:
    max_rounds: int = 3
    queries_per_round: int = 4
    results_per_query: int = 10
    min_score: int = 6
    max_papers: int = 12


@dataclass
class RoundLog:
    number: int
    queries: list[str]
    new_candidates: int
    selected_ids: list[str]
    critique: Critique | None = None


@dataclass
class ReviewResult:
    question: str
    answer: str
    papers: list[Paper]
    notes: dict[str, PaperNotes]
    scores: dict[str, RelevanceScore]
    candidates: dict[str, Paper]
    rounds: list[RoundLog] = field(default_factory=list)

    @property
    def final_critique(self) -> Critique | None:
        critiques = [r.critique for r in self.rounds if r.critique]
        return critiques[-1] if critiques else None


def select_papers(
    candidates: dict[str, Paper],
    scores: dict[str, RelevanceScore],
    min_score: int,
    max_papers: int,
) -> list[Paper]:
    relevant = [paper for paper in candidates.values() if paper.id in scores and scores[paper.id].score >= min_score]
    relevant.sort(key=lambda paper: scores[paper.id].score, reverse=True)
    return relevant[:max_papers]


def run_review(
    question: str,
    config: ReviewConfig | None = None,
    log: Callable[[str], None] = print,
) -> ReviewResult:
    config = config or ReviewConfig()
    result = ReviewResult(question=question, answer="", papers=[], notes={}, scores={}, candidates={})
    queries_run: list[str] = []
    missing_aspects: list[str] | None = None

    for number in range(1, config.max_rounds + 1):
        log(f"\n[bold]Round {number}[/bold]")

        log("Planning search queries...")
        queries = run_planner(question, config.queries_per_round, missing_aspects, queries_run)
        queries_run.extend(queries)
        for query in queries:
            log(f"  - {query}")

        log("Searching arXiv...")
        new_papers = run_retriever(queries, set(result.candidates), config.results_per_query)
        result.candidates.update({paper.id: paper for paper in new_papers})
        log(f"  {len(new_papers)} new candidates ({len(result.candidates)} total)")

        if new_papers:
            log("Screening for relevance...")
            result.scores.update(run_screener(question, new_papers))

        selected = select_papers(result.candidates, result.scores, config.min_score, config.max_papers)
        round_log = RoundLog(number, queries, len(new_papers), [paper.id for paper in selected])
        result.rounds.append(round_log)
        log(f"  {len(selected)} papers scored >= {config.min_score}")

        if not selected:
            missing_aspects = ["No relevant papers found yet; broaden the queries and try synonyms"]
            continue
        if [paper.id for paper in selected] == [paper.id for paper in result.papers]:
            log("No new relevant papers this round; stopping.")
            break

        to_summarize = [paper for paper in selected if paper.id not in result.notes]
        if to_summarize:
            log(f"Summarizing {len(to_summarize)} papers...")
            result.notes.update({note.paper_id: note for note in run_summarizer(question, to_summarize)})

        log("Synthesizing answer...")
        result.papers = selected
        result.answer = run_synthesizer(question, selected, result.notes)

        log("Critiquing answer...")
        critique = run_critic(question, result.answer, selected)
        round_log.critique = critique
        log(f"  verdict: {critique.verdict} (score {critique.score}/10)")
        log(f"  {critique.justification}")

        if critique.verdict == "sufficient":
            break
        missing_aspects = critique.missing_aspects
        for aspect in missing_aspects:
            log(f"  missing: {aspect}")

    return result
