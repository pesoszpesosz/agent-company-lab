# Agent Company Migration Decision Parser Module File Draft

Generated UTC: 2026-06-16T12:25:18Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-module-file-draft-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-module-file-draft-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_module_file_draft_ready_for_report_only_static_review`

Drafted the parser module file contents as a report-only artifact, including allowed decisions, guards, result builder, and parse entrypoint without writing an importable file.

## Module Source Draft

```python
"""Report-only parser for agent-company migration operator decisions."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

ALLOWED_DECISION_TYPES = ('hold', 'approve_sandbox_dry_run_only', 'request_rework', 'reject_migration_path')
RESULT_FIELDS = ('accepted', 'decision_type', 'result_state', 'refusal_reasons', 'artifact_paths', 'expires_at', 'signed_utc', 'report_only')
REFUSAL_REASONS = ('missing_required_fields', 'unknown_decision_type', 'forbidden_scope', 'missing_artifact_paths', 'expired_or_missing_expiration', 'unsigned_decision', 'artifact_path_mismatch', 'not_json_object')

REQUIRED_FIELDS = (
    'decision_id',
    'operator_name',
    'decision_type',
    'scope',
    'artifact_paths',
    'expires_at',
    'risk_acknowledgement',
    'signed_utc',
)

def guard_json_object_only(decision: object) -> list[str]:
    return [] if isinstance(decision, Mapping) else ['not_json_object']

def guard_required_fields_present(decision: Mapping[str, Any]) -> list[str]:
    missing = [field for field in REQUIRED_FIELDS if field not in decision]
    return ['missing_required_fields'] if missing else []

def guard_known_decision_type(decision: Mapping[str, Any]) -> list[str]:
    return [] if decision.get('decision_type') in ALLOWED_DECISION_TYPES else ['unknown_decision_type']

def guard_scope_boundaries(decision: Mapping[str, Any]) -> list[str]:
    scope = str(decision.get('scope', '')).lower()
    forbidden = ('live', 'wallet', 'browser', 'service_request', 'assign_worker')
    return ['forbidden_scope'] if any(token in scope for token in forbidden) else []

def guard_artifact_paths(decision: Mapping[str, Any]) -> list[str]:
    paths = decision.get('artifact_paths')
    return [] if isinstance(paths, Sequence) and not isinstance(paths, str) and len(paths) >= 4 else ['missing_artifact_paths']

def guard_expiration_and_signature(decision: Mapping[str, Any], now_utc: datetime | None = None) -> list[str]:
    now_utc = now_utc or datetime.now(timezone.utc)
    reasons: list[str] = []
    if 'signed_utc' not in decision:
        reasons.append('unsigned_decision')
    try:
        expires_at = datetime.fromisoformat(str(decision.get('expires_at')).replace('Z', '+00:00'))
        if expires_at <= now_utc:
            reasons.append('expired_or_missing_expiration')
    except ValueError:
        reasons.append('expired_or_missing_expiration')
    return reasons

def build_report_only_result(decision: Mapping[str, Any], refusals: list[str]) -> dict[str, Any]:
    accepted = not refusals
    return {
        'accepted': accepted,
        'decision_type': decision.get('decision_type'),
        'result_state': 'accepted_report_only' if accepted else 'rejected_report_only',
        'refusal_reasons': refusals,
        'artifact_paths': decision.get('artifact_paths', []),
        'expires_at': decision.get('expires_at'),
        'signed_utc': decision.get('signed_utc'),
        'report_only': True,
    }

def parse_report_only_decision(decision: object, now_utc: datetime | None = None) -> dict[str, Any]:
    refusals = guard_json_object_only(decision)
    if refusals:
        return build_report_only_result({}, refusals)
    typed = decision
    assert isinstance(typed, Mapping)
    refusals.extend(guard_required_fields_present(typed))
    refusals.extend(guard_known_decision_type(typed))
    refusals.extend(guard_scope_boundaries(typed))
    refusals.extend(guard_artifact_paths(typed))
    refusals.extend(guard_expiration_and_signature(typed, now_utc=now_utc))
    return build_report_only_result(typed, refusals)
```

## Boundary

This is a report-only module file draft. It does not write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Static-review the parser module file draft next; do not write, install, import, or run it.

