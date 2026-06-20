from __future__ import annotations

from typing import Any

"""
Durable chain source-spec seed integrity specs.
"""

from .constants import (
    SOURCE_SPEC_SEED_APPLY_VALIDATION_JSON,
    SOURCE_SPEC_SEED_PACKETS_VALIDATION_JSON,
)


def durable_source_spec_integrity_specs() -> list[dict[str, Any]]:
    return [
        {
            "id": "source_spec_seed_packets",
            "label": "Source Spec Seed Packets",
            "path": SOURCE_SPEC_SEED_PACKETS_VALIDATION_JSON,
            "count_key": "seed_packet_count",
            "expected": {
                "schema_version": "agent_company.source_spec_seed_packets_validation.v1",
                "seed_packet_count": 0,
                "missing_source_spec_lane_count": 0,
                "source_spec_gap_count_from_gap_map": 0,
                "all_gap_lanes_have_seed_packet": True,
                "all_seed_packets_report_only": True,
                "source_specs_table_rows_before": 13,
                "source_specs_table_rows_after": 13,
                "source_specs_inserted_by_packet": 0,
                "registry_file_modified_by_packet": False,
                "all_checks_passed": True,
                "failure_count": 0,
                "browser_sessions_started": 0,
                "account_actions": False,
                "wallet_actions": False,
                "payment_actions": False,
                "public_actions": False,
                "security_testing_actions": False,
                "real_money_actions": False,
                "service_requests_updated": 0,
                "service_requests_assigned": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
        {
            "id": "source_spec_seed_apply",
            "label": "Source Spec Seed Apply",
            "path": SOURCE_SPEC_SEED_APPLY_VALIDATION_JSON,
            "count_key": "applied_spec_count",
            "expected": {
                "schema_version": "agent_company.source_spec_seed_apply_validation.v1",
                "seed_packet_count": 3,
                "applied_spec_count": 3,
                "source_specs_table_rows_before": 10,
                "source_specs_table_rows_after": 13,
                "source_specs_registry_count_before": 10,
                "source_specs_registry_count_after": 13,
                "source_specs_inserted_or_updated": 3,
                "all_applied_specs_present_in_db": True,
                "all_applied_specs_present_in_registry": True,
                "source_spec_gap_count_after_apply": 0,
                "registry_file_modified_by_apply": True,
                "all_checks_passed": True,
                "failure_count": 0,
                "browser_sessions_started": 0,
                "account_actions": False,
                "wallet_actions": False,
                "payment_actions": False,
                "public_actions": False,
                "security_testing_actions": False,
                "real_money_actions": False,
                "service_requests_updated": 0,
                "service_requests_assigned": 0,
                "worker_starts": 0,
                "api_calls": False,
                "external_side_effects": False,
            },
        },
    ]


__all__ = ["durable_source_spec_integrity_specs"]
