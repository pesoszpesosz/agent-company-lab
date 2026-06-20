import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_checkpoint_interrupt_bridge_fixture.py"
VALIDATION = ROOT / "reports" / "checkpoint-interrupt-bridge-fixture-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "checkpoint-interrupt-bridge-fixture-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "checkpoint-interrupt-bridge-fixture-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "checkpoint-interrupt-bridge-fixture-v1-fixtures"


class CheckpointInterruptBridgeFixtureTest(unittest.TestCase):
    def test_langgraph_bridge_fixture_is_local_only_and_non_executable(self) -> None:
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
        self.assertEqual(validation["accepted_count"], 1)
        self.assertGreaterEqual(validation["rejected_count"], 16)
        self.assertFalse(validation["runtime_adoption_allowed"])
        self.assertFalse(validation["dependency_install_allowed"])
        self.assertFalse(validation["dependency_import_allowed"])
        self.assertFalse(validation["resume_allowed"])
        self.assertFalse(validation["apply_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["external_framework_imports"], 0)
        self.assertEqual(validation["dependency_installs"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["graph_nodes_executed"], 0)
        self.assertEqual(validation["checkpoint_resumes"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 17)
        self.assertEqual(schema["properties"]["source_candidate"]["const"], "langchain-ai/langgraph")
        self.assertTrue(report["source_state"]["scorecard_top_candidate_langgraph"])


if __name__ == "__main__":
    unittest.main()
