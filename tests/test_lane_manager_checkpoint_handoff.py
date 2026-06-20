import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_lane_manager_checkpoint_handoff.py"
VALIDATION = ROOT / "reports" / "lane-manager-checkpoint-handoff-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "lane-manager-checkpoint-handoff-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "lane-manager-checkpoint-handoff-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "lane-manager-checkpoint-handoff-v1-fixtures"


class LaneManagerCheckpointHandoffTest(unittest.TestCase):
    def test_owned_active_lanes_get_pause_only_handoff_rows(self) -> None:
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
        self.assertEqual(validation["expected_lane_count"], len(report["expected_lane_ids"]))
        self.assertGreaterEqual(validation["expected_lane_count"], 11)
        self.assertNotIn("submitted_bounty_payouts", report["expected_lane_ids"])
        self.assertEqual(validation["accepted_count"], 1)
        self.assertEqual(validation["rejected_count"], report["expected_rejected_count"])
        self.assertFalse(validation["handoff_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertFalse(validation["service_request_mutation_allowed"])
        self.assertEqual(validation["tasks_created"], 0)
        self.assertEqual(validation["tasks_acquired"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertFalse(validation["external_side_effects"])
        self.assertNotIn("submitted_bounty_payouts", report["expected_lane_ids"])
        self.assertEqual(schema["properties"]["handoff_allowed"]["const"], False)
        self.assertTrue(FIXTURE_DIR.exists())


if __name__ == "__main__":
    unittest.main()
