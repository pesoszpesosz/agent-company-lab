from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for paid-code commands."""

from agent_company_core.paid_code import (
    write_paid_code_browser_refresh_decision_packet,
    write_paid_code_duplicate_check_worksheet,
    write_paid_code_local_worksheet_answers,
)
from agent_company_core.schema import init_db


PAID_CODE_CLI_COMMANDS = (
    "write-paid-code-duplicate-check-worksheet",
    "write-paid-code-local-worksheet-answers",
    "write-paid-code-browser-refresh-decision-packet",
)


def add_paid_code_commands(sub: Any) -> None:
    paid_code_duplicate_check_worksheet = sub.add_parser("write-paid-code-duplicate-check-worksheet")
    paid_code_duplicate_check_worksheet.add_argument("--path")
    paid_code_duplicate_check_worksheet.add_argument("--json-path")
    paid_code_duplicate_check_worksheet.add_argument("--validation-path")
    paid_code_duplicate_check_worksheet.add_argument("--proof-path")
    paid_code_local_worksheet_answers = sub.add_parser("write-paid-code-local-worksheet-answers")
    paid_code_local_worksheet_answers.add_argument("--path")
    paid_code_local_worksheet_answers.add_argument("--json-path")
    paid_code_local_worksheet_answers.add_argument("--validation-path")
    paid_code_local_worksheet_answers.add_argument("--worksheet-path")
    paid_code_browser_refresh_decision_packet = sub.add_parser("write-paid-code-browser-refresh-decision-packet")
    paid_code_browser_refresh_decision_packet.add_argument("--path")
    paid_code_browser_refresh_decision_packet.add_argument("--json-path")
    paid_code_browser_refresh_decision_packet.add_argument("--validation-path")
    paid_code_browser_refresh_decision_packet.add_argument("--answers-path")


def paid_code_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "write-paid-code-duplicate-check-worksheet": write_paid_code_duplicate_check_worksheet,
        "write-paid-code-local-worksheet-answers": write_paid_code_local_worksheet_answers,
        "write-paid-code-browser-refresh-decision-packet": write_paid_code_browser_refresh_decision_packet,
    }


def handle_paid_code_command(conn: Any, args: Any) -> bool:
    handler = paid_code_command_handlers().get(args.cmd)
    if handler is None:
        return False
    init_db(conn)
    handler(conn, args)
    return True


__all__ = [
    "PAID_CODE_CLI_COMMANDS",
    "add_paid_code_commands",
    "paid_code_command_handlers",
    "handle_paid_code_command",
]