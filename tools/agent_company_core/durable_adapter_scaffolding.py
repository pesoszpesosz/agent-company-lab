from __future__ import annotations

"""Compatibility facade for durable adapter scaffolding writers."""

from .durable_adapter_scaffolding_artifacts import (
    materialized_scaffolding_artifact_content,
    scaffolding_artifact_filename,
    write_durable_adapter_runtime_report_only_scaffolding_artifacts,
)
from .durable_adapter_scaffolding_packet import write_durable_adapter_runtime_report_only_scaffolding_packet

__all__ = [
    "write_durable_adapter_runtime_report_only_scaffolding_packet",
    "scaffolding_artifact_filename",
    "materialized_scaffolding_artifact_content",
    "write_durable_adapter_runtime_report_only_scaffolding_artifacts",
]
