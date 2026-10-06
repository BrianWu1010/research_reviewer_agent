import argparse
import os
import sys

from rich.console import Console

from pipeline import ReviewConfig, run_review
from report import write_report


def parse_args() -> argparse.Namespace:
    defaults = ReviewConfig()
    parser = argparse.ArgumentParser(description="Answer a research question from arXiv literature.")
    parser.add_argument("question", nargs="?", help="Research question (prompted for if omitted)")
    parser.add_argument("--max-rounds", type=int, default=defaults.max_rounds)
    parser.add_argument("--queries-per-round", type=int, default=defaults.queries_per_round)
    parser.add_argument("--results-per-query", type=int, default=defaults.results_per_query)
    parser.add_argument("--min-score", type=int, default=defaults.min_score, help="Relevance cutoff, 0-10")
    parser.add_argument("--max-papers", type=int, default=defaults.max_papers)
    parser.add_argument("--model", help="OpenAI model (default: $OPENAI_MODEL or gpt-4.1-mini)")
    parser.add_argument("--output-dir", default="output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.model:
        os.environ["OPENAI_MODEL"] = args.model

    console = Console()
    question = args.question or console.input("[bold]Research question:[/bold] ").strip()
    if not question:
        sys.exit("No question given.")

    config = ReviewConfig(
        max_rounds=args.max_rounds,
        queries_per_round=args.queries_per_round,
        results_per_query=args.results_per_query,
        min_score=args.min_score,
        max_papers=args.max_papers,
    )
    result = run_review(question, config, log=console.print)
    run_dir = write_report(result, args.output_dir)

    console.print(f"\n[green]Report written to {run_dir / 'report.md'}[/green]")


if __name__ == "__main__":
    main()
