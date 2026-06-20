import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_service_worker_signed_decision_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "service-worker-signed-decision-apply-preflight-blocker-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "service-worker-signed-decision-apply-preflight-blocker-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "service-worker-signed-decision-apply-preflight-blocker-v1.schema.json"
GUARD_REPORT = ROOT / "reports" / "service-worker-signed-decision-guard-v1-20260617.json"


class ServiceWorkerSignedDecisionApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_rejects_apply_without_real_signed_decision(self) -> None:
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
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertFalse(validation["apply_allowed"])
        self.assertFalse(validation["decision_apply_allowed"])
        self.assertFalse(validation["assignment_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["accepted_guard_decision_count"], 3)
        self.assertEqual(validation["service_template_count"], 13)
        self.assertGreaterEqual(validation["current_request_count"], 14)
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["service_requests_mutated"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertFalse(validation["api_calls"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["apply_preflight_status"]["enum"][0], "blocked_no_real_signed_decision")
        self.assertEqual(report["blocker_reason"], "no_real_signed_operator_decision_artifact")

    def test_accepted_guard_fixture_is_not_a_real_apply_decision(self) -> None:
        guard = json.loads(GUARD_REPORT.read_text(encoding="utf-8"))
        accepted_fixture = next(
            item["path"]
            for item in guard["results"]
            if item["result"]["accepted_for_later_apply_preflight"]
        )
        result = subprocess.run(
            [sys.executable, str(TOOL), "--real-signed-decision-path", accepted_fixture],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            timeout=30,
        )

        self.assertNotEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
        self.assertFalse(validation["all_checks_passed"])
        self.assertEqual(validation["apply_preflight_status"], "blocked_fixture_decision_not_real")
        self.assertIn("accepted_guard_fixture_is_not_real_signed_decision", validation["failures"])
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["service_requests_mutated"], 0)


if __name__ == "__main__":
    unittest.main()
