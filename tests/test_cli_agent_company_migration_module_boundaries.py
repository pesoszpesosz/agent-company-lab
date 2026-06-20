import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_cli_commands_are_registered() -> None:
    from agent_company_core.cli_agent_company_migration import (
        AGENT_COMPANY_MIGRATION_CLI_COMMANDS,
        add_agent_company_migration_commands,
    )

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_agent_company_migration_commands(sub)

    parsed = parser.parse_args([
        "write-agent-company-migration-decision-parser-write-approval-response-application-packet-contract",
        "--path",
        "packet.md",
        "--json-path",
        "packet.json",
        "--validation-path",
        "packet.validation.json",
    ])

    assert parsed.cmd in AGENT_COMPANY_MIGRATION_CLI_COMMANDS
    assert parsed.path == "packet.md"
    assert parsed.json_path == "packet.json"
    assert parsed.validation_path == "packet.validation.json"
    assert AGENT_COMPANY_MIGRATION_CLI_COMMANDS[0] == "write-agent-company-infrastructure-radar"
    assert AGENT_COMPANY_MIGRATION_CLI_COMMANDS[-1] == "write-agent-company-migration-decision-parser-write-approval-response-application-packet-runner-review"
    assert len(AGENT_COMPANY_MIGRATION_CLI_COMMANDS) == 34


def test_agent_company_migration_cli_dispatch_initializes_and_calls_handler(monkeypatch) -> None:
    from agent_company_core import cli_agent_company_migration

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="write-agent-company-migration-decision-parser-write-approval-response-application-packet-contract")

    monkeypatch.setattr(cli_agent_company_migration, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_agent_company_migration,
        "write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_agent_company_migration.handle_agent_company_migration_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_agent_company_migration.handle_agent_company_migration_command(conn, SimpleNamespace(cmd="status")) is False