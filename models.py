from typing import Literal

from pydantic import BaseModel, Field


class Paper(BaseModel):
    id: str
    title: str
    abstract: str
    authors: list[str]
    published: str
    url: str
    categories: list[str] = Field(default_factory=list)


class SearchPlan(BaseModel):
    queries: list[str] = Field(description="arXiv API search queries")


class RelevanceScore(BaseModel):
    paper_id: str
    score: int = Field(ge=0, le=10)
    reason: str


class ScreeningResult(BaseModel):
    scores: list[RelevanceScore]


class PaperNotes(BaseModel):
    paper_id: str
    relevance: str = Field(description="How this paper bears on the research question")
    contribution: str
    method: str
    findings: list[str]
    limitations: list[str] = Field(
        default_factory=list,
        description="Only limitations stated or clearly implied by the abstract",
    )


class Critique(BaseModel):
    verdict: Literal["sufficient", "needs_more"]
    score: int = Field(ge=1, le=10)
    justification: str
    missing_aspects: list[str] = Field(default_factory=list)
