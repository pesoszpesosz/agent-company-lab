import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_money_path_cli_commands_are_registered() -> None:
    from agent_company_core.cli_money_paths import MONEY_PATH_CLI_COMMANDS, add_money_path_commands

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_money_path_commands(sub)

    parsed = parser.parse_args([
        "write-manager-proof-task-promotion-queue",
        "--preflight-path",
        "preflight.json",
        "--validation-path",
        "queue.validation.json",
    ])

    assert parsed.cmd in MONEY_PATH_CLI_COMMANDS
    assert parsed.preflight_path == "preflight.json"
    assert parsed.validation_path == "queue.validation.json"
    assert len(MONEY_PATH_CLI_COMMANDS) == 6


def test_money_path_cli_dispatch_initializes_and_calls_handler(monkeypatch) -> None:
    from agent_company_core import cli_money_paths

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="write-first-ranked-manager-proof")

    monkeypatch.setattr(cli_money_paths, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_money_paths,
        "write_first_ranked_manager_proof",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_money_paths.handle_money_path_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_money_paths.handle_money_path_command(conn, SimpleNamespace(cmd="status")) is False