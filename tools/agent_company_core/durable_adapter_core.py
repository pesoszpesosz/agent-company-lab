"""Compatibility facade for durable-adapter core helpers."""

from __future__ import annotations

from .durable_adapter_paths import resolve_durable_adapter_result_path
from .durable_adapter_reducer_dry_run import dry_run_durable_service_request_reducer
from .durable_adapter_validation import (
    add_durable_adapter_validation_error,
    require_durable_adapter_nonempty_string,
    validate_durable_adapter_fixture_doc,
)

__all__ = [
    "add_durable_adapter_validation_error",
    "dry_run_durable_service_request_reducer",
    "require_durable_adapter_nonempty_string",
    "resolve_durable_adapter_result_path",
    "validate_durable_adapter_fixture_doc",
]
