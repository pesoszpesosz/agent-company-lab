import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_runtime_process_egress_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "runtime-process-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "runtime-process-egress-apply-preflight-blocker-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "runtime-process-egress-apply-preflight-blocker-v1.schema.json"


class RuntimeProcessEgressApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_prevents_runtime_apply_until_real_signed_decision_and_command_contract_exist(self) -> None:
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
        self.assertEqual(validation["target_route_id"], "runtime_process_gateway")
        self.assertEqual(validation["target_egress_type"], "runtime_start")
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_runtime_process_egress_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertFalse(validation["apply_command_contract_present"])
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["runtime_start_allowed"])
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["dependency_installs"], 0)
        self.assertEqual(validation["queue_mutations"], 0)
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["target_route_id"]["const"], "runtime_process_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "runtime_start")
        self.assertEqual(schema["properties"]["apply_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["runtime_start_allowed"]["const"], False)

        checks = {item["check_id"]: item for item in report["checks"]}
        for required in [
            "gateway_docket_validation_passes",
            "runtime_process_signed_decision_guard_passes_for_target_route",
            "runtime_start_preflight_validation_passes",
            "runtime_start_signed_decision_guard_validation_passes",
            "agent_egress_event_ledger_validation_passes",
            "real_signed_decision_absent",
            "runtime_process_apply_command_contract_absent",
        ]:
            self.assertIn(required, checks)
            self.assertTrue(checks[required]["passed"])

        self.assertEqual(
            report["next_action"],
            "Provide a real signed operator runtime_process_gateway decision artifact, then build a runtime_process_gateway apply-command contract before any dependency install, runtime process start, worker start, queue mutation, service-request mutation, or live egress can be considered.",
        )


if __name__ == "__main__":
    unittest.main()
