from __future__ import annotations

from pathlib import Path
from typing import Any


def forbidden_runtime_imports_in_source() -> list[dict[str, Any]]:
    forbidden_prefixes = [
        "import temporalio",
        "from temporalio",
        "import inngest",
        "from inngest",
    ]
    findings: list[dict[str, Any]] = []
    source_dir = Path(__file__).resolve().parent
    source_paths = sorted(source_dir.glob("durable_adapter*.py"))
    for source_path in source_paths:
        for line_number, line in enumerate(source_path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip().lower()
            if any(stripped.startswith(prefix) for prefix in forbidden_prefixes):
                findings.append({"path": str(source_path), "line": line_number, "text": line.strip()})
    return findings
