from __future__ import annotations

"""Compatibility facade for Profit Edge import parsing, routing, and command orchestration."""

from .profit_edge_import_command import (
    PROFIT_EDGE_REPORT_IMPORTS,
    import_profit_edge,
    write_profit_edge_import_report,
)
from .profit_edge_ledger_import import (
    SUBMITTED_PAYOUT_OWNERSHIP_NOTE,
    import_ledger_rows,
    normalize_profit_edge_lane,
)
from .profit_edge_source_summary import (
    extract_next_action_from_lines,
    find_first_key,
    find_first_url,
    infer_status,
    markdown_title,
    read_text_sample,
    summarize_json,
    summarize_jsonl,
    summarize_markdown,
    summarize_source_file,
)

__all__ = [
    "SUBMITTED_PAYOUT_OWNERSHIP_NOTE",
    "PROFIT_EDGE_REPORT_IMPORTS",
    "read_text_sample",
    "infer_status",
    "markdown_title",
    "extract_next_action_from_lines",
    "summarize_markdown",
    "find_first_key",
    "find_first_url",
    "summarize_json",
    "summarize_jsonl",
    "summarize_source_file",
    "normalize_profit_edge_lane",
    "import_ledger_rows",
    "write_profit_edge_import_report",
    "import_profit_edge",
]
