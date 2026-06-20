import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_telemetry_export_egress_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "telemetry-export-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "telemetry-export-egress-apply-preflight-blocker-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "telemetry-export-egress-apply-preflight-blocker-v1.schema.json"


class TelemetryExportEgressApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_prevents_telemetry_export_apply_until_real_decision_evidence_and_contract_exist(self) -> None:
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
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_telemetry_export_egress_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertFalse(validation["redaction_policy_present"])
        self.assertFalse(validation["destination_scope_present"])
        self.assertFalse(validation["retention_policy_present"])
        self.assertFalse(validation["sample_trace_artifact_present"])
        self.assertFalse(validation["apply_command_contract_present"])
        self.assertEqual(validation["accepted_guard_decision_count"], 2)
        self.assertGreaterEqual(validation["rejected_guard_decision_count"], 60)
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
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
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["account_actions"])
        self.assertFalse(validation["wallet_actions"])
        self.assertFalse(validation["payment_actions"])
        self.assertFalse(validation["real_money_actions"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["target_route_id"]["const"], "telemetry_export_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "telemetry_export")
        self.assertEqual(schema["properties"]["apply_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["telemetry_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["external_trace_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["private_prompt_upload_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["credential_export_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["unredacted_log_sync_allowed"]["const"], False)

        checks = {item["check_id"]: item for item in report["checks"]}
        for required in [
            "gateway_docket_validation_passes",
            "signed_decision_intake_validation_passes",
            "telemetry_export_signed_decision_guard_passes_for_target_route",
            "agent_egress_event_ledger_validation_passes",
            "identity_envelope_validation_passes",
            "service_worker_chain_integrity_passes_without_start",
            "real_signed_decision_absent",
            "redaction_policy_absent",
            "destination_scope_absent",
            "retention_policy_absent",
            "sample_trace_artifact_absent",
            "telemetry_export_apply_command_contract_absent",
        ]:
            self.assertIn(required, checks)
            self.assertTrue(checks[required]["passed"])

        self.assertEqual(
            report["next_action"],
            "Provide a real signed operator telemetry_export_gateway decision artifact, redaction policy, destination scope, retention policy, sample trace artifact, and telemetry apply-command contract before any external trace export, private prompt upload, credential export, unredacted log sync, service-request mutation, worker/browser/model/MCP start or call, live egress, or external side effect can be considered.",
        )


if __name__ == "__main__":
    unittest.main()
