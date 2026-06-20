"""Durable-adapter path, schema, and reducer constants for Agent Company."""

from __future__ import annotations

from .paths import REPORTS_DIR

DURABLE_ORCHESTRATION_DIR = REPORTS_DIR / "durable-orchestration"
DURABLE_SERVICE_WORKER_INTEGRATION_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-service-worker-refresh-integration-latest.md"
)
DURABLE_SERVICE_WORKER_INTEGRATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-service-worker-refresh-integration-latest.json"
)
DURABLE_SERVICE_WORKER_INTEGRATION_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-service-worker-refresh-integration-validation-latest.json"
)
DURABLE_RUNTIME_INTERFACE_CONTRACT_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-interface-contract-latest.md"
)
DURABLE_RUNTIME_INTERFACE_CONTRACT_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-interface-contract-latest.json"
)
DURABLE_RUNTIME_INTERFACE_CONTRACT_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-interface-contract-validation-latest.json"
)
DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-interface-negative-fixtures-latest.md"
)
DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-interface-negative-fixtures-latest.json"
)
DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-interface-negative-fixtures-validation-latest.json"
)
DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-implementation-preflight-latest.md"
)
DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-implementation-preflight-latest.json"
)
DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-implementation-preflight-validation-latest.json"
)
DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-fixtures-latest.md"
)
DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-fixtures-latest.json"
)
DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-fixtures-validation-latest.json"
)
DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-scaffolding-packet-latest.md"
)
DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-scaffolding-packet-latest.json"
)
DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-scaffolding-packet-validation-latest.json"
)
DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACT_DIR = (
    DURABLE_ORCHESTRATION_DIR / "runtime-report-only-scaffolding-artifacts"
)
DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-scaffolding-artifacts-latest.md"
)
DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-scaffolding-artifacts-latest.json"
)
DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-report-only-scaffolding-artifacts-validation-latest.json"
)
DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-human-approval-packet-latest.md"
)
DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-human-approval-packet-latest.json"
)
DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-human-approval-packet-validation-latest.json"
)
DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_REPORT = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-human-decision-intake-packet-latest.md"
)
DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-human-decision-intake-packet-latest.json"
)
DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR
    / "temporal-inngest-adapter-runtime-human-decision-intake-packet-validation-latest.json"
)
DURABLE_ADAPTER_REDUCER_RESULT_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-cli-p2-cleanup-positive-result-20260615.json"
)
DURABLE_ADAPTER_RUNTIME_READINESS_VALIDATION_JSON = (
    DURABLE_ORCHESTRATION_DIR / "temporal-inngest-adapter-runtime-readiness-validation-20260615.json"
)
DURABLE_ADAPTER_FIXTURE_SCHEMA_VERSION = "agent_company.durable_adapter_reducer_fixture_set.v1"
DURABLE_ADAPTER_DRY_RUN_RESULT_SCHEMA_VERSION = "agent_company.durable_adapter_dry_run_result.v1"
DURABLE_ADAPTER_RESUME_REQUIREMENTS_ORDER_POLICY = (
    "strict_order_is_semantic_for_review_packet_display"
)
DURABLE_ADAPTER_REQUIRED_FIXTURE_FIELDS = [
    "fixture_id",
    "request_id",
    "input",
    "expected_output",
    "expected_exit",
]
DURABLE_ADAPTER_REQUIRED_INPUT_FIELDS = [
    "status_snapshot",
    "event_name",
    "risk_gate",
    "worker_type",
    "idempotency_key",
    "source_event_id",
]
DURABLE_ADAPTER_ACTION_FIELDS = [
    "ledger_mutation_allowed",
    "approval_granted",
    "assign_worker",
    "start_worker",
    "emit_followup_event",
    "schedule_activity",
    "call_api",
    "external_side_effects_allowed",
]
DURABLE_ADAPTER_ALLOWED_OUTPUT_STATES = {
    "parked.awaiting_human_review",
    "terminal.completed_from_ledger_snapshot",
    "terminal.rejected_from_ledger_snapshot",
}

__all__ = [
    "DURABLE_ORCHESTRATION_DIR",
    "DURABLE_SERVICE_WORKER_INTEGRATION_REPORT",
    "DURABLE_SERVICE_WORKER_INTEGRATION_JSON",
    "DURABLE_SERVICE_WORKER_INTEGRATION_VALIDATION_JSON",
    "DURABLE_RUNTIME_INTERFACE_CONTRACT_REPORT",
    "DURABLE_RUNTIME_INTERFACE_CONTRACT_JSON",
    "DURABLE_RUNTIME_INTERFACE_CONTRACT_VALIDATION_JSON",
    "DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_REPORT",
    "DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_JSON",
    "DURABLE_RUNTIME_INTERFACE_NEGATIVE_FIXTURES_VALIDATION_JSON",
    "DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_REPORT",
    "DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_JSON",
    "DURABLE_RUNTIME_IMPLEMENTATION_PREFLIGHT_VALIDATION_JSON",
    "DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_REPORT",
    "DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_JSON",
    "DURABLE_RUNTIME_REPORT_ONLY_FIXTURES_VALIDATION_JSON",
    "DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_REPORT",
    "DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_JSON",
    "DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_PACKET_VALIDATION_JSON",
    "DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACT_DIR",
    "DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_REPORT",
    "DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_JSON",
    "DURABLE_RUNTIME_REPORT_ONLY_SCAFFOLDING_ARTIFACTS_VALIDATION_JSON",
    "DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_REPORT",
    "DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_JSON",
    "DURABLE_RUNTIME_HUMAN_APPROVAL_PACKET_VALIDATION_JSON",
    "DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_REPORT",
    "DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_JSON",
    "DURABLE_RUNTIME_HUMAN_DECISION_INTAKE_PACKET_VALIDATION_JSON",
    "DURABLE_ADAPTER_REDUCER_RESULT_JSON",
    "DURABLE_ADAPTER_RUNTIME_READINESS_VALIDATION_JSON",
    "DURABLE_ADAPTER_FIXTURE_SCHEMA_VERSION",
    "DURABLE_ADAPTER_DRY_RUN_RESULT_SCHEMA_VERSION",
    "DURABLE_ADAPTER_RESUME_REQUIREMENTS_ORDER_POLICY",
    "DURABLE_ADAPTER_REQUIRED_FIXTURE_FIELDS",
    "DURABLE_ADAPTER_REQUIRED_INPUT_FIELDS",
    "DURABLE_ADAPTER_ACTION_FIELDS",
    "DURABLE_ADAPTER_ALLOWED_OUTPUT_STATES",
]
