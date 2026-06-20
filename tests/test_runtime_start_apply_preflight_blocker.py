import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_runtime_start_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "runtime-start-apply-preflight-blocker-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "runtime-start-apply-preflight-blocker-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "runtime-start-apply-preflight-blocker-v1.schema.json"


class RuntimeStartApplyPreflightBlockerTest(unittest.TestCase):
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
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertFalse(validation["apply_allowed"])
        self.assertFalse(validation["runtime_start_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["accepted_guard_decision_count"], 2)
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertEqual(validation["runtime_processes_started"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["apply_preflight_status"]["enum"][0], "blocked_no_real_signed_decision")
        self.assertEqual(report["blocker_reason"], "no_real_signed_operator_decision_artifact")


if __name__ == "__main__":
    unittest.main()
