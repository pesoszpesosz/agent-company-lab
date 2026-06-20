import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_service_worker_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "service-worker-signed-decision-guard-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "service-worker-signed-decision-guard-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "service-worker-signed-decision-guard-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "service-worker-signed-decision-guard-v1-fixtures"


class ServiceWorkerSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_template_bound_report_only_decisions(self) -> None:
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
        self.assertEqual(validation["guard_status"], "report_only_signed_decision_guard_ready")
        self.assertEqual(validation["accepted_count"], 3)
        self.assertGreaterEqual(validation["rejected_count"], 20)
        self.assertEqual(validation["service_template_count"], 13)
        self.assertGreaterEqual(validation["current_request_count"], 14)
        self.assertFalse(validation["approval_granted_by_guard"])
        self.assertFalse(validation["decision_authority_granted_by_guard"])
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["api_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 23)
        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(report["positive_authority"]["accepted_scopes"][0], "none")


if __name__ == "__main__":
    unittest.main()
