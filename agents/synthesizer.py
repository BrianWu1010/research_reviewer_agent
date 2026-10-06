from models import Paper, PaperNotes
from tools.llm import chat_text

SYSTEM = """You are the Synthesizer in a multi-agent literature review system.
Write a concise, well-organized answer to the research question using ONLY the provided paper notes.

Requirements:
- Cite papers inline by their number, e.g. [2] or [1, 4]. Every substantive claim needs a citation.
- Organize by theme or mechanism, not paper by paper.
- Point out agreements, disagreements, and open questions across papers.
- If the evidence is thin or only partially addresses the question, say so explicitly.
- Do not use outside knowledge to fill gaps.
- Write in the voice of a literature review: refer to "the papers" or "this literature",
  never to "the notes" or "the abstracts", and do not use first person.
- Output Markdown with these sections: "## Answer" (2-4 sentence direct answer),
  "## Key findings", "## Open questions and gaps". No reference list; it is added separately."""


def format_notes(papers: list[Paper], notes: dict[str, PaperNotes]) -> str:
    blocks = []
    for number, paper in enumerate(papers, start=1):
        note = notes[paper.id]
        findings = "\n".join(f"  - {finding}" for finding in note.findings)
        limitations = "\n".join(f"  - {item}" for item in note.limitations) or "  - (not stated)"
        blocks.append(
            f"[{number}] {paper.title} ({paper.published[:4]})\n"
            f"Relevance: {note.relevance}\n"
            f"Contribution: {note.contribution}\n"
            f"Method: {note.method}\n"
            f"Findings:\n{findings}\n"
            f"Limitations:\n{limitations}"
        )
    return "\n\n".join(blocks)


def run_synthesizer(question: str, papers: list[Paper], notes: dict[str, PaperNotes]) -> str:
    user = f"Research question:\n{question}\n\nPaper notes:\n\n{format_notes(papers, notes)}"
    return chat_text(SYSTEM, user).strip()
