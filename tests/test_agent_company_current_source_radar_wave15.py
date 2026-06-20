import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_agent_company_current_source_radar_wave15.py"
VALIDATION = ROOT / "reports" / "agent-company-current-source-radar-wave15-validation-20260617.json"
REPORT_JSON = ROOT / "reports" / "agent-company-current-source-radar-wave15-20260617.json"
DATA_JSON = ROOT / "data" / "agent-company-current-source-radar-wave15-20260617.json"


class AgentCompanyCurrentSourceRadarWave15Test(unittest.TestCase):
    def test_wave15_current_source_radar_is_read_only_and_mapped(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            timeout=30,
        )

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
        report = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
        dataset = json.loads(DATA_JSON.read_text(encoding="utf-8"))

        self.assertTrue(validation["all_checks_passed"])
        self.assertEqual(validation["failure_count"], 0)
        self.assertEqual(validation["repo_count"], 7)
        self.assertGreaterEqual(validation["doc_source_count"], 10)
        self.assertEqual(validation["public_github_metadata_reads"], 7)
        self.assertFalse(validation["execution_api_calls"])
        self.assertFalse(validation["model_api_calls"])
        self.assertEqual(validation["dependency_installs"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(len(dataset["repos"]), 7)
        self.assertTrue(all(row["local_decision"] and row["gate"] for row in dataset["repos"]))
        self.assertTrue(any(row["repo"] == "langchain-ai/langgraph" for row in report["ranked_repos"]))
        self.assertTrue(any(src["source_id"] == "microsoft_hitl_sample" for src in report["doc_sources"]))


if __name__ == "__main__":
    unittest.main()
