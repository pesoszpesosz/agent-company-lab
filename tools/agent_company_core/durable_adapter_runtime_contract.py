from __future__ import annotations

"""Compatibility facade for durable adapter runtime contracts."""

from .durable_adapter_runtime_import_guard import forbidden_runtime_imports_in_source
from .durable_adapter_runtime_interface_contract import write_durable_adapter_runtime_interface_contract
from .durable_adapter_service_worker_integration import write_durable_adapter_service_worker_integration

__all__ = [
    "write_durable_adapter_service_worker_integration",
    "forbidden_runtime_imports_in_source",
    "write_durable_adapter_runtime_interface_contract",
]
