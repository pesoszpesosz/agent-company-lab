import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_model_api_egress_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "model-api-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "model-api-egress-apply-preflight-blocker-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "model-api-egress-apply-preflight-blocker-v1.schema.json"


class ModelApiEgressApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_prevents_model_apply_until_real_signed_decision_and_command_contract_exist(self) -> None:
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
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_model_api_egress_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertFalse(validation["apply_command_contract_present"])
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["provider_key_use_allowed"])
        self.assertFalse(validation["provider_keys_used"])
        self.assertFalse(validation["model_api_call_allowed"])
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["training_data_upload_allowed"])
        self.assertFalse(validation["training_data_uploaded"])
        self.assertEqual(validation["max_cost_usd"], 0)
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["target_route_id"]["const"], "model_api_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "model_api")
        self.assertEqual(schema["properties"]["apply_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["model_api_call_allowed"]["const"], False)

        checks = {item["check_id"]: item for item in report["checks"]}
        for required in [
            "gateway_docket_validation_passes",
            "model_api_signed_decision_guard_passes_for_target_route",
            "agent_egress_event_ledger_validation_passes",
            "identity_envelope_validation_passes",
            "real_signed_decision_absent",
            "model_api_apply_command_contract_absent",
        ]:
            self.assertIn(required, checks)
            self.assertTrue(checks[required]["passed"])

        self.assertEqual(
            report["next_action"],
            "Provide a real signed operator model/API egress-route decision artifact, then build a model/API apply-command contract before any provider key use, model/API call, data upload, worker start, service-request mutation, or live egress can be considered.",
        )


if __name__ == "__main__":
    unittest.main()
