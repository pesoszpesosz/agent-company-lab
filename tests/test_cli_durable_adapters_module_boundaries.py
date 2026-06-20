import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_durable_adapter_cli_commands_are_registered() -> None:
    from agent_company_core.cli_durable_adapters import DURABLE_ADAPTER_COMMANDS, add_durable_adapter_commands

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_durable_adapter_commands(sub)

    parsed = parser.parse_args([
        "write-durable-adapter-runtime-interface-contract",
        "--integration-validation-path",
        "integration.json",
        "--readiness-validation-path",
        "readiness.json",
    ])

    assert parsed.cmd in DURABLE_ADAPTER_COMMANDS
    assert parsed.integration_validation_path == "integration.json"
    assert parsed.readiness_validation_path == "readiness.json"
    assert len(DURABLE_ADAPTER_COMMANDS) == 10


def test_durable_adapter_cli_dispatch_initializes_and_calls_handler(monkeypatch) -> None:
    from agent_company_core import cli_durable_adapters

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="write-durable-adapter-runtime-human-decision-intake-packet")

    monkeypatch.setattr(cli_durable_adapters, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_durable_adapters,
        "write_durable_adapter_runtime_human_decision_intake_packet",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_durable_adapters.handle_durable_adapter_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_durable_adapters.handle_durable_adapter_command(conn, SimpleNamespace(cmd="status")) is False