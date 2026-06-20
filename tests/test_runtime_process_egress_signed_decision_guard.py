import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_runtime_process_egress_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "runtime-process-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "runtime-process-egress-signed-decision-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "runtime-process-egress-signed-decision-guard-v1.schema.json"


class RuntimeProcessEgressSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_report_only_runtime_process_preflight_decisions(self) -> None:
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
        self.assertGreaterEqual(validation["fixture_count"], 35)
        self.assertEqual(validation["accepted_count"], 2)
        self.assertEqual(validation["rejected_count"], validation["fixture_count"] - 2)
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["runtime_start_allowed"])
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["dependency_installs"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(schema["properties"]["route_id"]["const"], "runtime_process_gateway")
        self.assertEqual(schema["properties"]["egress_type"]["const"], "runtime_start")
        self.assertEqual(schema["properties"]["runtime_start_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        required = set(report["target_route_required_gates"])
        self.assertEqual(
            required,
            {
                "runtime_start_preflight_v1",
                "runtime_start_signed_decision_guard_v1",
                "runtime_start_apply_preflight_blocker_v1",
                "runtime_dependency_install_preflight_v1",
                "agent_egress_event_ledger_v1",
            },
        )

        accepted = [item for item in report["results"] if item["result"]["accepted_for_apply_preflight"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            result_payload = item["result"]
            self.assertFalse(result_payload["runtime_start_allowed"])
            self.assertEqual(result_payload["runtime_starts"], 0)
            self.assertFalse(result_payload["worker_start_allowed"])
            self.assertEqual(result_payload["worker_starts"], 0)
            self.assertEqual(result_payload["dependency_installs"], 0)

        self.assertEqual(
            report["next_action"],
            "Build runtime_process_gateway apply preflight blocker before any dependency install, runtime process start, worker start, queue mutation, service-request mutation, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
