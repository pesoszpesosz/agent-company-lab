from __future__ import annotations

"""Compatibility facade for durable-adapter report writers and reducer helpers."""

from .durable_adapter_core import (
    resolve_durable_adapter_result_path,
    add_durable_adapter_validation_error,
    require_durable_adapter_nonempty_string,
    validate_durable_adapter_fixture_doc,
    dry_run_durable_service_request_reducer,
)

from .durable_adapter_runtime_contract import (
    write_durable_adapter_service_worker_integration,
    forbidden_runtime_imports_in_source,
    write_durable_adapter_runtime_interface_contract,
)

from .durable_adapter_runtime_fixtures import (
    durable_runtime_negative_fixture_definitions,
    write_durable_adapter_runtime_negative_fixtures,
    write_durable_adapter_runtime_implementation_preflight,
    durable_runtime_report_only_fixture_definitions,
    write_durable_adapter_runtime_report_only_fixtures,
)

from .durable_adapter_scaffolding import (
    write_durable_adapter_runtime_report_only_scaffolding_packet,
    scaffolding_artifact_filename,
    materialized_scaffolding_artifact_content,
    write_durable_adapter_runtime_report_only_scaffolding_artifacts,
)

from .durable_adapter_human_decision import (
    write_durable_adapter_runtime_human_approval_packet,
    write_durable_adapter_runtime_human_decision_intake_packet,
)

__all__ = [
    "resolve_durable_adapter_result_path",
    "add_durable_adapter_validation_error",
    "require_durable_adapter_nonempty_string",
    "validate_durable_adapter_fixture_doc",
    "dry_run_durable_service_request_reducer",
    "write_durable_adapter_service_worker_integration",
    "forbidden_runtime_imports_in_source",
    "write_durable_adapter_runtime_interface_contract",
    "durable_runtime_negative_fixture_definitions",
    "write_durable_adapter_runtime_negative_fixtures",
    "write_durable_adapter_runtime_implementation_preflight",
    "durable_runtime_report_only_fixture_definitions",
    "write_durable_adapter_runtime_report_only_fixtures",
    "write_durable_adapter_runtime_report_only_scaffolding_packet",
    "scaffolding_artifact_filename",
    "materialized_scaffolding_artifact_content",
    "write_durable_adapter_runtime_report_only_scaffolding_artifacts",
    "write_durable_adapter_runtime_human_approval_packet",
    "write_durable_adapter_runtime_human_decision_intake_packet",
]
