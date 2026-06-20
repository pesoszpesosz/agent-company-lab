import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_model_api_egress_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "model-api-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "model-api-egress-signed-decision-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "model-api-egress-signed-decision-guard-v1.schema.json"


class ModelApiEgressSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_report_only_model_api_preflight_decisions(self) -> None:
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
        self.assertEqual(validation["target_route_id"], "model_api_gateway")
        self.assertEqual(validation["target_egress_type"], "model_api")
        self.assertGreaterEqual(validation["fixture_count"], 40)
        self.assertEqual(validation["accepted_count"], 2)
        self.assertEqual(validation["rejected_count"], validation["fixture_count"] - 2)
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["provider_key_use_allowed"])
        self.assertFalse(validation["provider_keys_used"])
        self.assertFalse(validation["model_api_call_allowed"])
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["training_data_upload_allowed"])
        self.assertFalse(validation["training_data_uploaded"])
        self.assertEqual(validation["max_cost_usd"], 0)
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(schema["properties"]["route_id"]["const"], "model_api_gateway")
        self.assertEqual(schema["properties"]["egress_type"]["const"], "model_api")
        self.assertEqual(schema["properties"]["model_api_call_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        required = set(report["target_route_required_gates"])
        self.assertEqual(
            required,
            {
                "model_api_execution_gate",
                "secrets_credentials_handling_gate",
                "agent_egress_event_ledger_v1",
                "cost_budget_signed_decision",
            },
        )

        accepted = [item for item in report["results"] if item["result"]["accepted_for_apply_preflight"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            result_payload = item["result"]
            self.assertFalse(result_payload["model_api_call_allowed"])
            self.assertFalse(result_payload["model_api_calls"])
            self.assertFalse(result_payload["provider_key_use_allowed"])
            self.assertFalse(result_payload["training_data_upload_allowed"])
            self.assertEqual(result_payload["max_cost_usd"], 0)

        self.assertEqual(
            report["next_action"],
            "Build model API egress apply preflight blocker for the accepted model_api_gateway decision before any provider key use, model/API call, data upload, worker start, service-request mutation, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
