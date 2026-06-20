import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_service_worker_cli_commands_are_registered() -> None:
    from agent_company_core.cli_service_workers import SERVICE_WORKER_CLI_COMMANDS, add_service_worker_commands

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_service_worker_commands(sub)

    parsed = parser.parse_args([
        "write-service-worker-execution-readiness",
        "--request-id",
        "req-1",
        "--lane-id",
        "lane-1",
        "--status",
        "needs_review",
        "--worker-agent-id",
        "worker-1",
    ])

    assert parsed.cmd in SERVICE_WORKER_CLI_COMMANDS
    assert parsed.request_id == "req-1"
    assert parsed.worker_agent_id == "worker-1"
    assert len(SERVICE_WORKER_CLI_COMMANDS) == 18


def test_service_worker_cli_dispatch_initializes_and_calls_handler(monkeypatch) -> None:
    from agent_company_core import cli_service_workers

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="write-service-worker-chain-integrity")

    monkeypatch.setattr(cli_service_workers, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_service_workers,
        "write_service_worker_chain_integrity",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_service_workers.handle_service_worker_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_service_workers.handle_service_worker_command(conn, SimpleNamespace(cmd="status")) is False