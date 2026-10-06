import pipeline
from models import Critique, Paper, PaperNotes, RelevanceScore
from pipeline import ReviewConfig, run_review, select_papers
from report import render_markdown


def make_paper(paper_id: str) -> Paper:
    return Paper(
        id=paper_id,
        title=f"Paper {paper_id}",
        abstract="...",
        authors=["A", "B", "C", "D"],
        published="2024-01-01",
        url=f"http://arxiv.org/abs/{paper_id}",
    )


def make_notes(paper: Paper) -> PaperNotes:
    return PaperNotes(paper_id=paper.id, relevance="r", contribution="c", method="m", findings=["f"])


def test_select_papers_filters_and_ranks():
    candidates = {pid: make_paper(pid) for pid in ["a", "b", "c", "d"]}
    scores = {
        "a": RelevanceScore(paper_id="a", score=5, reason=""),
        "b": RelevanceScore(paper_id="b", score=9, reason=""),
        "c": RelevanceScore(paper_id="c", score=7, reason=""),
    }
    selected = select_papers(candidates, scores, min_score=6, max_papers=5)
    assert [paper.id for paper in selected] == ["b", "c"]


def test_loop_keeps_original_question_and_feeds_back_gaps(monkeypatch):
    planner_calls = []
    searches = iter([[make_paper("1"), make_paper("2")], [make_paper("3")]])
    critiques = iter(
        [
            Critique(verdict="needs_more", score=4, justification="thin", missing_aspects=["gap X"]),
            Critique(verdict="sufficient", score=8, justification="ok"),
        ]
    )
    seen_questions = set()

    def fake_planner(question, n, missing, previous):
        planner_calls.append((missing, list(previous or [])))
        seen_questions.add(question)
        return [f"q{len(planner_calls)}"]

    monkeypatch.setattr(pipeline, "run_planner", fake_planner)
    monkeypatch.setattr(pipeline, "run_retriever", lambda queries, seen, k: next(searches))
    monkeypatch.setattr(
        pipeline,
        "run_screener",
        lambda q, papers: {p.id: RelevanceScore(paper_id=p.id, score=8, reason="") for p in papers},
    )
    monkeypatch.setattr(pipeline, "run_summarizer", lambda q, papers: [make_notes(p) for p in papers])
    monkeypatch.setattr(pipeline, "run_synthesizer", lambda q, papers, notes: f"answer from {len(papers)}")
    monkeypatch.setattr(pipeline, "run_critic", lambda q, answer, papers: next(critiques))

    result = run_review("original?", ReviewConfig(max_rounds=3), log=lambda _: None)

    assert seen_questions == {"original?"}
    assert planner_calls[1] == (["gap X"], ["q1"])
    assert len(result.rounds) == 2
    assert result.answer == "answer from 3"
    assert result.final_critique.verdict == "sufficient"

    report = render_markdown(result)
    assert "## References" in report
    assert "A, B, C et al." in report


def test_stops_when_no_new_relevant_papers(monkeypatch):
    monkeypatch.setattr(pipeline, "run_planner", lambda *args: ["q"])
    monkeypatch.setattr(pipeline, "run_retriever", lambda queries, seen, k: [make_paper("1")] if not seen else [])
    monkeypatch.setattr(
        pipeline,
        "run_screener",
        lambda q, papers: {p.id: RelevanceScore(paper_id=p.id, score=8, reason="") for p in papers},
    )
    monkeypatch.setattr(pipeline, "run_summarizer", lambda q, papers: [make_notes(p) for p in papers])
    monkeypatch.setattr(pipeline, "run_synthesizer", lambda *args: "answer")
    monkeypatch.setattr(
        pipeline,
        "run_critic",
        lambda *args: Critique(verdict="needs_more", score=5, justification="", missing_aspects=["more"]),
    )

    result = run_review("q?", ReviewConfig(max_rounds=5), log=lambda _: None)
    assert len(result.rounds) == 2
