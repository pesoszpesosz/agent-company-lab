import unittest
from pathlib import Path

from generated_artifact_helpers import (
    assert_clean_fixture_validation,
    assert_false_fields,
    assert_zero_fields,
    run_validator_load_artifacts,
)


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_telemetry_export_egress_apply_command_contract.py"
VALIDATION = ROOT / "reports" / "telemetry-export-egress-apply-command-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "telemetry-export-egress-apply-command-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "telemetry-export-egress-apply-command-contract-v1.schema.json"


class TelemetryExportEgressApplyCommandContractTest(unittest.TestCase):
    def test_contract_rejects_live_telemetry_export_apply_commands(self) -> None:
        validation, report, schema = run_validator_load_artifacts(
            self,
            root=ROOT,
            tool=TOOL,
            validation_path=VALIDATION,
            report_path=REPORT,
            schema_path=SCHEMA,
        )

        assert_clean_fixture_validation(self, validation, min_fixture_count=45)
        self.assertEqual(validation["target_route_id"], "telemetry_export_gateway")
        self.assertEqual(validation["target_egress_type"], "telemetry_export")
        self.assertEqual(validation["accepted_count"], 2)
        self.assertEqual(validation["rejected_count"], validation["fixture_count"] - 2)
        assert_false_fields(
            self,
            validation,
            [
                "apply_command_allowed",
                "apply_allowed",
                "gateway_registration_allowed",
                "gateway_start_allowed",
                "live_egress_allowed",
                "telemetry_export_allowed",
                "external_trace_export_allowed",
                "private_prompt_upload_allowed",
                "credential_export_allowed",
                "unredacted_log_sync_allowed",
                "redaction_policy_approved",
                "destination_scope_approved",
                "retention_policy_approved",
                "sample_trace_artifact_approved",
                "browser_session_start_allowed",
                "mcp_tool_calls",
                "model_api_calls",
                "public_actions",
                "account_actions",
                "wallet_actions",
                "payment_actions",
                "real_money_actions",
                "external_side_effects",
            ],
        )
        assert_zero_fields(
            self,
            validation,
            [
                "telemetry_exports",
                "external_trace_exports",
                "private_prompts_uploaded",
                "credentials_exported",
                "unredacted_logs_synced",
                "browser_sessions_started",
                "service_requests_assigned",
                "service_requests_updated",
                "apply_commands_written",
                "apply_commands_executed",
                "worker_starts",
                "runtime_starts",
            ],
        )

        self.assertEqual(schema["properties"]["command_type"]["enum"][0], "deny_noop")
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "telemetry_export_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "telemetry_export")
        self.assertEqual(schema["properties"]["telemetry_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["external_trace_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["private_prompt_upload_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["credential_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["unredacted_log_sync_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        accepted = [item for item in report["results"] if item["result"]["accepted_for_contract_only"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            payload = item["result"]
            self.assertEqual(payload["target_route_id"], "telemetry_export_gateway")
            self.assertFalse(payload["apply_command_allowed"])
            self.assertFalse(payload["telemetry_export_allowed"])
            self.assertFalse(payload["external_trace_export_allowed"])
            self.assertFalse(payload["private_prompt_upload_allowed"])
            self.assertFalse(payload["credential_export_allowed"])
            self.assertFalse(payload["unredacted_log_sync_allowed"])

        self.assertEqual(
            report["next_action"],
            "Build telemetry_export_gateway apply-command guard only after a real signed operator decision, redaction "
            "policy, destination scope, retention policy, sample trace artifact, and immutable command preview exist; "
            "until then, keep telemetry export egress blocked.",
        )


if __name__ == "__main__":
    unittest.main()
