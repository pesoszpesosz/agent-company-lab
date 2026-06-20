import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_paid_code_cli_commands_are_registered() -> None:
    from agent_company_core.cli_paid_code import PAID_CODE_CLI_COMMANDS, add_paid_code_commands

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_paid_code_commands(sub)

    parsed = parser.parse_args([
        "write-paid-code-browser-refresh-decision-packet",
        "--answers-path",
        "answers.json",
        "--validation-path",
        "packet.validation.json",
    ])

    assert parsed.cmd in PAID_CODE_CLI_COMMANDS
    assert parsed.answers_path == "answers.json"
    assert parsed.validation_path == "packet.validation.json"
    assert len(PAID_CODE_CLI_COMMANDS) == 3


def test_paid_code_cli_dispatch_initializes_and_calls_handler(monkeypatch) -> None:
    from agent_company_core import cli_paid_code

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="write-paid-code-local-worksheet-answers")

    monkeypatch.setattr(cli_paid_code, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_paid_code,
        "write_paid_code_local_worksheet_answers",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_paid_code.handle_paid_code_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_paid_code.handle_paid_code_command(conn, SimpleNamespace(cmd="status")) is False