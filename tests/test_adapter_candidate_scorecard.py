import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_adapter_candidate_scorecard.py"
REPORT = ROOT / "reports" / "adapter-candidate-scorecard-v1-20260617.json"
VALIDATION = ROOT / "reports" / "adapter-candidate-scorecard-v1-validation-20260617.json"
SCHEMA = ROOT / "architecture" / "adapter-candidate-scorecard-v1.schema.json"


class AdapterCandidateScorecardTest(unittest.TestCase):
    def test_scorecard_ranks_candidates_without_runtime_adoption(self) -> None:
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
        self.assertEqual(validation["candidate_count"], 7)
        self.assertEqual(validation["selected_for_runtime_adoption_count"], 0)
        self.assertFalse(validation["runtime_adoption_allowed"])
        self.assertFalse(validation["dependency_install_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["dependency_installs"], 0)
        self.assertEqual(validation["dependency_imports"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["selected_for_runtime_adoption_count"]["const"], 0)

        rows = report["candidate_rows"]
        self.assertEqual(len(rows), 7)
        self.assertEqual([row["rank"] for row in rows], list(range(1, 8)))
        self.assertTrue(all("checkpoint_interrupt_contract_v1" in row["required_gates"] for row in rows))
        self.assertTrue(all(not row["runtime_adoption_allowed"] for row in rows))
        self.assertIn(report["recommended_next_candidate"], {row["repo"] for row in rows})


if __name__ == "__main__":
    unittest.main()
