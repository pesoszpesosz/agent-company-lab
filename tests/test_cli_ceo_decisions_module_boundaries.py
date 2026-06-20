import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_ceo_decision_cli_commands_are_registered() -> None:
    from agent_company_core.cli_ceo_decisions import CEO_DECISION_CLI_COMMANDS, add_ceo_decision_commands

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_ceo_decision_commands(sub)

    parsed = parser.parse_args([
        "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract",
        "--path",
        "contract.md",
        "--json-path",
        "contract.json",
        "--validation-path",
        "contract.validation.json",
    ])

    assert parsed.cmd in CEO_DECISION_CLI_COMMANDS
    assert parsed.path == "contract.md"
    assert parsed.json_path == "contract.json"
    assert parsed.validation_path == "contract.validation.json"
    assert CEO_DECISION_CLI_COMMANDS[0] == "write-ceo-gate-blocker-board"
    assert CEO_DECISION_CLI_COMMANDS[-1] == "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-closeout"
    assert len(CEO_DECISION_CLI_COMMANDS) == 36


def test_ceo_decision_cli_dispatch_initializes_and_calls_handler(monkeypatch) -> None:
    from agent_company_core import cli_ceo_decisions

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="write-ceo-decision-parser-apply-readiness-positive-runner")

    monkeypatch.setattr(cli_ceo_decisions, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_ceo_decisions,
        "write_ceo_decision_parser_apply_readiness_positive_runner",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_ceo_decisions.handle_ceo_decision_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_ceo_decisions.handle_ceo_decision_command(conn, SimpleNamespace(cmd="status")) is False