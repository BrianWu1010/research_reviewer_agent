import json
import re
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from pipeline import ReviewResult


def _slug(text: str, max_len: int = 50) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:max_len].rstrip("-")


def render_markdown(result: ReviewResult) -> str:
    lines = [f"# {result.question}", ""]

    if result.answer:
        lines += [result.answer, ""]
    else:
        lines += ["_No sufficiently relevant papers were found for this question._", ""]

    critique = result.final_critique
    if critique:
        lines += [
            "## Reviewer assessment",
            "",
            f"**Verdict:** {critique.verdict} ({critique.score}/10). {critique.justification}",
            "",
        ]
        if critique.missing_aspects:
            lines += ["Still missing:", *[f"- {aspect}" for aspect in critique.missing_aspects], ""]

    if result.papers:
        lines += ["## References", ""]
        for number, paper in enumerate(result.papers, start=1):
            authors = ", ".join(paper.authors[:3]) + (" et al." if len(paper.authors) > 3 else "")
            score = result.scores[paper.id].score
            lines.append(
                f"{number}. **{paper.title}**. {authors} ({paper.published[:4]}). "
                f"[arXiv:{paper.id}]({paper.url}) (relevance {score}/10)"
            )
        lines.append("")

        lines += ["## Paper notes", ""]
        for number, paper in enumerate(result.papers, start=1):
            note = result.notes[paper.id]
            lines += [
                f"### [{number}] {paper.title}",
                "",
                f"- **Relevance:** {note.relevance}",
                f"- **Contribution:** {note.contribution}",
                f"- **Method:** {note.method}",
                "- **Findings:**",
                *[f"  - {finding}" for finding in note.findings],
            ]
            if note.limitations:
                lines += ["- **Limitations (from abstract):**", *[f"  - {item}" for item in note.limitations]]
            lines.append("")

    lines += ["## Search log", ""]
    for round_log in result.rounds:
        lines.append(f"**Round {round_log.number}** ({round_log.new_candidates} new candidates)")
        lines += [f"- `{query}`" for query in round_log.queries]
        lines.append("")

    return "\n".join(lines)


def write_report(result: ReviewResult, output_dir: str | Path = "output") -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = Path(output_dir) / f"{timestamp}_{_slug(result.question)}"
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "report.md").write_text(render_markdown(result))

    trace = {
        "question": result.question,
        "answer": result.answer,
        "selected_ids": [paper.id for paper in result.papers],
        "rounds": [
            {**asdict(round_log), "critique": round_log.critique.model_dump() if round_log.critique else None}
            for round_log in result.rounds
        ],
        "candidates": [
            {
                **paper.model_dump(),
                "relevance": result.scores[paper.id].model_dump() if paper.id in result.scores else None,
                "notes": result.notes[paper.id].model_dump() if paper.id in result.notes else None,
            }
            for paper in result.candidates.values()
        ],
    }
    (run_dir / "run.json").write_text(json.dumps(trace, indent=2))
    return run_dir
