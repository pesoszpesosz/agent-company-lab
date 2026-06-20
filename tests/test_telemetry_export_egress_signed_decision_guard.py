import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_telemetry_export_egress_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "telemetry-export-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "telemetry-export-egress-signed-decision-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "telemetry-export-egress-signed-decision-guard-v1.schema.json"


class TelemetryExportEgressSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_report_only_telemetry_export_preflight_decisions(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            timeout=30,
        )

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

        self.assertTrue(validation["all_checks_passed"])
        self.assertEqual(validation["failure_count"], 0)
        self.assertEqual(validation["target_route_id"], "telemetry_export_gateway")
        self.assertEqual(validation["target_egress_type"], "telemetry_export")
        self.assertGreaterEqual(validation["fixture_count"], 45)
        self.assertEqual(validation["accepted_count"], 2)
        self.assertEqual(validation["rejected_count"], validation["fixture_count"] - 2)
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["telemetry_export_allowed"])
        self.assertEqual(validation["telemetry_exports"], 0)
        self.assertFalse(validation["external_trace_export_allowed"])
        self.assertEqual(validation["external_trace_exports"], 0)
        self.assertFalse(validation["private_prompt_upload_allowed"])
        self.assertEqual(validation["private_prompts_uploaded"], 0)
        self.assertFalse(validation["credential_export_allowed"])
        self.assertEqual(validation["credentials_exported"], 0)
        self.assertFalse(validation["unredacted_log_sync_allowed"])
        self.assertEqual(validation["unredacted_logs_synced"], 0)
        self.assertFalse(validation["redaction_policy_approved"])
        self.assertFalse(validation["destination_scope_approved"])
        self.assertFalse(validation["retention_policy_approved"])
        self.assertFalse(validation["sample_trace_artifact_approved"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["account_actions"])
        self.assertFalse(validation["wallet_actions"])
        self.assertFalse(validation["payment_actions"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(schema["properties"]["route_id"]["const"], "telemetry_export_gateway")
        self.assertEqual(schema["properties"]["egress_type"]["const"], "telemetry_export")
        self.assertEqual(schema["properties"]["telemetry_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["external_trace_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["private_prompt_upload_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["credential_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["unredacted_log_sync_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        required = set(report["target_route_required_gates"])
        self.assertEqual(
            required,
            {
                "telemetry_privacy_export_gate_v1",
                "agent_egress_event_ledger_v1",
                "secrets_credentials_handling_gate",
            },
        )
        blocked = set(report["blocked_actions"])
        self.assertEqual(
            blocked,
            {
                "external_trace_export",
                "private_prompt_upload",
                "credential_export",
                "unredacted_log_sync",
            },
        )

        accepted = [item for item in report["results"] if item["result"]["accepted_for_apply_preflight"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            payload = item["result"]
            self.assertFalse(payload["telemetry_export_allowed"])
            self.assertFalse(payload["external_trace_export_allowed"])
            self.assertFalse(payload["private_prompt_upload_allowed"])
            self.assertFalse(payload["credential_export_allowed"])
            self.assertFalse(payload["unredacted_log_sync_allowed"])

        self.assertEqual(
            report["next_action"],
            "Build telemetry_export_gateway apply preflight blocker before any external trace export, private prompt upload, credential export, unredacted log sync, service-request mutation, worker start, model/MCP call, live egress, or external side effect.",
        )


if __name__ == "__main__":
    unittest.main()
