import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_service_worker_operator_decision_docket.py"
REPORT = ROOT / "reports" / "service-worker-operator-decision-docket-v1-20260617.json"
VALIDATION = ROOT / "reports" / "service-worker-operator-decision-docket-v1-validation-20260617.json"
SCHEMA = ROOT / "architecture" / "service-worker-operator-decision-docket-v1.schema.json"


class ServiceWorkerOperatorDecisionDocketTest(unittest.TestCase):
    def test_docket_ranks_all_parked_requests_without_granting_authority(self) -> None:
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
        self.assertEqual(validation["docket_status"], "ready_for_manual_operator_review")
        self.assertEqual(validation["docket_count"], 11)
        self.assertEqual(validation["ready_for_manual_review_count"], 11)
        self.assertFalse(validation["approval_granted_by_docket"])
        self.assertFalse(validation["decision_authority_granted_by_docket"])
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertEqual(validation["service_requests_assigned_by_docket"], 0)
        self.assertEqual(validation["service_requests_updated_by_docket"], 0)
        self.assertEqual(validation["service_requests_mutated_by_docket"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertFalse(validation["api_calls"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["payment_actions"])
        self.assertFalse(validation["wallet_actions"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["docket_status"]["enum"][0], "ready_for_manual_operator_review")

        rows = report["docket_rows"]
        self.assertEqual(len(rows), 11)
        self.assertEqual([row["rank"] for row in rows], list(range(1, 12)))
        self.assertTrue(all(row["service_status"] == "needs_review" for row in rows))
        self.assertTrue(all(row["approve_preview_present"] and row["reject_preview_present"] for row in rows))
        self.assertTrue(all(not row["approval_granted_by_docket_row"] for row in rows))
        self.assertTrue(any(row["request_type"] == "security_report_submission" for row in rows))


if __name__ == "__main__":
    unittest.main()
