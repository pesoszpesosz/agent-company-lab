import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_prompt_eval_cli_commands_are_registered() -> None:
    from agent_company_core.cli_prompt_eval import PROMPT_EVAL_COMMANDS, add_prompt_eval_commands

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_prompt_eval_commands(sub)

    parsed = parser.parse_args([
        "record-eval-run",
        "--eval-run-id",
        "eval-1",
        "--dataset-id",
        "dataset-1",
        "--runtime",
        "local",
        "--status",
        "passed",
        "--score",
        "0.8",
    ])

    assert parsed.cmd in PROMPT_EVAL_COMMANDS
    assert parsed.eval_run_id == "eval-1"
    assert parsed.score == 0.8
    assert len(PROMPT_EVAL_COMMANDS) == 6


def test_prompt_eval_cli_dispatch_initializes_and_calls_handler(monkeypatch) -> None:
    from agent_company_core import cli_prompt_eval

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="record-human-review")

    monkeypatch.setattr(cli_prompt_eval, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_prompt_eval,
        "record_human_review",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_prompt_eval.handle_prompt_eval_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_prompt_eval.handle_prompt_eval_command(conn, SimpleNamespace(cmd="status")) is False


def test_prompt_eval_report_dispatch_preserves_path_argument(monkeypatch) -> None:
    from agent_company_core import cli_prompt_eval

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="write-prompt-eval-report", path="report.md")

    monkeypatch.setattr(cli_prompt_eval, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_prompt_eval,
        "write_prompt_eval_report",
        lambda value, path: events.append(("report", value, path)),
    )

    assert cli_prompt_eval.handle_prompt_eval_command(conn, args) is True
    assert events == [("init", conn, None), ("report", conn, "report.md")]