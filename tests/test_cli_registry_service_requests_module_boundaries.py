import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_registry_service_request_cli_commands_are_registered() -> None:
    from agent_company_core.cli_registry_service_requests import (
        REGISTRY_SERVICE_REQUEST_COMMANDS,
        add_registry_service_request_commands,
    )

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_registry_service_request_commands(sub)

    parsed = parser.parse_args([
        "create-service-request",
        "--request-id",
        "req-1",
        "--request-type",
        "research",
        "--risk-gate",
        "read_only",
        "--requested-action",
        "summarize",
    ])

    assert parsed.cmd in REGISTRY_SERVICE_REQUEST_COMMANDS
    assert parsed.request_id == "req-1"
    assert parsed.risk_gate == "read_only"
    assert len(REGISTRY_SERVICE_REQUEST_COMMANDS) == 17


def test_registry_service_request_dispatch_handles_positional_registry_calls(monkeypatch) -> None:
    from agent_company_core import cli_registry_service_requests

    events: list[tuple[object, ...]] = []
    conn = object()
    args = SimpleNamespace(
        cmd="register-agent",
        agent_id="agent-1",
        role_id="role-1",
        thread_id="thread-1",
        department_id="dept-1",
    )

    monkeypatch.setattr(cli_registry_service_requests, "init_db", lambda value: events.append(("init", value)))
    monkeypatch.setattr(
        cli_registry_service_requests,
        "register_agent",
        lambda conn_value, agent_id, role_id, thread_id, department_id: events.append(
            ("register", conn_value, agent_id, role_id, thread_id, department_id)
        ),
    )

    assert cli_registry_service_requests.handle_registry_service_request_command(conn, args) is True
    assert events == [
        ("init", conn),
        ("register", conn, "agent-1", "role-1", "thread-1", "dept-1"),
    ]


def test_registry_service_request_dispatch_handles_generic_args_handlers(monkeypatch) -> None:
    from agent_company_core import cli_registry_service_requests

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="record-artifact")

    monkeypatch.setattr(cli_registry_service_requests, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_registry_service_requests,
        "record_artifact",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_registry_service_requests.handle_registry_service_request_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_registry_service_requests.handle_registry_service_request_command(conn, SimpleNamespace(cmd="status")) is False