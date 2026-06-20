import argparse
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_digital_products_cli_commands_are_registered() -> None:
    from agent_company_core.cli_digital_products import DIGITAL_PRODUCTS_CLI_COMMANDS, add_digital_products_commands

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    add_digital_products_commands(sub)

    parsed = parser.parse_args([
        "write-digital-products-local-gate-choice",
        "--path",
        "gate.md",
        "--json-path",
        "gate.json",
        "--validation-path",
        "gate.validation.json",
    ])

    assert parsed.cmd in DIGITAL_PRODUCTS_CLI_COMMANDS
    assert parsed.path == "gate.md"
    assert parsed.json_path == "gate.json"
    assert parsed.validation_path == "gate.validation.json"
    assert len(DIGITAL_PRODUCTS_CLI_COMMANDS) == 21


def test_digital_products_cli_dispatch_initializes_and_calls_handler(monkeypatch) -> None:
    from agent_company_core import cli_digital_products

    events: list[tuple[str, object, object | None]] = []
    conn = object()
    args = SimpleNamespace(cmd="write-digital-products-local-package-files")

    monkeypatch.setattr(cli_digital_products, "init_db", lambda value: events.append(("init", value, None)))
    monkeypatch.setattr(
        cli_digital_products,
        "write_digital_products_local_package_files",
        lambda value, parsed: events.append(("handler", value, parsed)),
    )

    assert cli_digital_products.handle_digital_products_command(conn, args) is True
    assert events == [("init", conn, None), ("handler", conn, args)]
    assert cli_digital_products.handle_digital_products_command(conn, SimpleNamespace(cmd="status")) is False