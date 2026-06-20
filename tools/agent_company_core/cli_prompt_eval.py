from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for prompt-evaluation commands."""

from agent_company_core.prompt_eval import (
    record_eval_dataset,
    record_eval_run,
    record_human_review,
    record_prompt_template,
    record_prompt_version,
    write_prompt_eval_report,
)
from agent_company_core.schema import init_db


PROMPT_EVAL_COMMANDS = (
    "record-prompt-template",
    "record-prompt-version",
    "record-eval-dataset",
    "record-eval-run",
    "record-human-review",
    "write-prompt-eval-report",
)


def add_prompt_eval_commands(sub: Any) -> None:
    prompt_template = sub.add_parser("record-prompt-template")
    prompt_template.add_argument("--template-id", required=True)
    prompt_template.add_argument("--lane-id")
    prompt_template.add_argument("--name", required=True)
    prompt_template.add_argument("--purpose", required=True)
    prompt_template.add_argument("--owner-agent-id")
    prompt_template.add_argument("--default-stop-gates-json")
    prompt_template.add_argument("--default-stop-gates-file")

    prompt_version = sub.add_parser("record-prompt-version")
    prompt_version.add_argument("--prompt-version-id", required=True)
    prompt_version.add_argument("--template-id", required=True)
    prompt_version.add_argument("--version-label", required=True)
    prompt_version.add_argument("--prompt-text")
    prompt_version.add_argument("--prompt-file")
    prompt_version.add_argument("--source-artifact-path")
    prompt_version.add_argument("--status", default="draft")

    eval_dataset = sub.add_parser("record-eval-dataset")
    eval_dataset.add_argument("--dataset-id", required=True)
    eval_dataset.add_argument("--lane-id")
    eval_dataset.add_argument("--name", required=True)
    eval_dataset.add_argument("--purpose", required=True)
    eval_dataset.add_argument("--cases-json")
    eval_dataset.add_argument("--cases-file")

    eval_run = sub.add_parser("record-eval-run")
    eval_run.add_argument("--eval-run-id", required=True)
    eval_run.add_argument("--dataset-id", required=True)
    eval_run.add_argument("--prompt-version-id")
    eval_run.add_argument("--lane-id")
    eval_run.add_argument("--runner-agent-id")
    eval_run.add_argument("--runtime", required=True)
    eval_run.add_argument("--status", required=True)
    eval_run.add_argument("--score", type=float)
    eval_run.add_argument("--results-json")
    eval_run.add_argument("--results-file")
    eval_run.add_argument("--artifact-path")

    human_review = sub.add_parser("record-human-review")
    human_review.add_argument("--review-id", required=True)
    human_review.add_argument("--lane-id")
    human_review.add_argument("--artifact-id")
    human_review.add_argument("--trace-id")
    human_review.add_argument("--prompt-version-id")
    human_review.add_argument("--reviewer-agent-id")
    human_review.add_argument("--status", required=True)
    human_review.add_argument("--decision", required=True)
    human_review.add_argument("--notes")

    prompt_eval_report = sub.add_parser("write-prompt-eval-report")
    prompt_eval_report.add_argument("--path")


def prompt_eval_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "record-prompt-template": record_prompt_template,
        "record-prompt-version": record_prompt_version,
        "record-eval-dataset": record_eval_dataset,
        "record-eval-run": record_eval_run,
        "record-human-review": record_human_review,
        "write-prompt-eval-report": write_prompt_eval_report,
    }


def handle_prompt_eval_command(conn: Any, args: Any) -> bool:
    handler = prompt_eval_command_handlers().get(args.cmd)
    if handler is None:
        return False
    init_db(conn)
    if args.cmd == "write-prompt-eval-report":
        handler(conn, args.path)
    else:
        handler(conn, args)
    return True


__all__ = [
    "PROMPT_EVAL_COMMANDS",
    "add_prompt_eval_commands",
    "handle_prompt_eval_command",
    "prompt_eval_command_handlers",
]