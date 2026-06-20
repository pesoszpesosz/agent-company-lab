import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_agent_company_runtime_adoption_docket.py"
VALIDATION = ROOT / "reports" / "agent-company-runtime-adoption-docket-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "agent-company-runtime-adoption-docket-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "agent-company-runtime-adoption-docket-v1.schema.json"


class AgentCompanyRuntimeAdoptionDocketTest(unittest.TestCase):
    def test_docket_classifies_wave19_candidates_without_runtime_adoption(self) -> None:
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
        self.assertEqual(validation["source_candidate_count"], 27)
        self.assertEqual(validation["docket_item_count"], 27)
        self.assertGreaterEqual(validation["reference_only_count"], 10)
        self.assertGreaterEqual(validation["adapter_candidate_count"], 3)
        self.assertGreaterEqual(validation["blocked_dependency_count"], 8)
        self.assertGreaterEqual(validation["future_runtime_candidate_count"], 3)
        self.assertFalse(validation["adoption_allowed"])
        self.assertEqual(validation["dependency_installs"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["adoption_allowed"]["const"], False)
        self.assertIn("browser-use/browser-use", report["top_adapter_candidates"])
        self.assertIn("temporalio/temporal", report["future_runtime_candidates"])
        self.assertIn("agentgateway/agentgateway", report["gateway_candidates"])
        self.assertEqual(report["next_action"], "Build worker_capability_class_registry_v1 before any dependency install or runtime adoption.")


if __name__ == "__main__":
    unittest.main()
