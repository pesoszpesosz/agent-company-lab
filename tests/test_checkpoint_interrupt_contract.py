import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_checkpoint_interrupt_contract.py"
VALIDATION = ROOT / "reports" / "checkpoint-interrupt-contract-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "checkpoint-interrupt-contract-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "checkpoint-interrupt-contract-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "checkpoint-interrupt-contract-v1-fixtures"


class CheckpointInterruptContractTest(unittest.TestCase):
    def test_checkpoint_interrupts_pause_without_resuming_or_applying(self) -> None:
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
        self.assertEqual(validation["accepted_count"], 3)
        self.assertGreaterEqual(validation["rejected_count"], 12)
        self.assertFalse(validation["resume_allowed"])
        self.assertFalse(validation["apply_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["resume_commands_written"], 0)
        self.assertEqual(validation["resume_commands_executed"], 0)
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["external_side_effects"])
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 15)
        self.assertEqual(schema["properties"]["source_kind"]["enum"][0], "lane_task")
        self.assertTrue(report["source_state"]["wave15_validation_ready"])
        self.assertTrue(report["source_state"]["operator_docket_validation_ready"])
        self.assertTrue(report["source_state"]["apply_preflight_validation_ready"])


if __name__ == "__main__":
    unittest.main()
