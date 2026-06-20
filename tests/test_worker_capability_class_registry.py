import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_worker_capability_class_registry.py"
VALIDATION = ROOT / "reports" / "worker-capability-class-registry-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "worker-capability-class-registry-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "worker-capability-class-registry-v1.schema.json"


class WorkerCapabilityClassRegistryTest(unittest.TestCase):
    def test_registry_maps_docket_worker_classes_to_gated_capabilities(self) -> None:
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
        self.assertEqual(validation["source_docket_item_count"], 27)
        self.assertGreaterEqual(validation["capability_class_count"], 8)
        self.assertEqual(validation["unmapped_docket_item_count"], 0)
        self.assertFalse(validation["worker_registration_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertFalse(validation["runtime_start_allowed"])
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["worker_registration_allowed"]["const"], False)

        classes = {item["capability_class_id"]: item for item in report["capability_classes"]}
        for required in [
            "browser_worker",
            "durable_runtime",
            "durable_workflow",
            "gateway_or_mcp",
            "agent_framework",
            "model_backed_agent_framework",
            "workflow_platform",
            "observability",
        ]:
            self.assertIn(required, classes)
            self.assertFalse(classes[required]["worker_registration_allowed"])
            self.assertFalse(classes[required]["worker_start_allowed"])
            self.assertGreaterEqual(len(classes[required]["required_gates"]), 2)

        self.assertIn("browser_worker_adapter_contract_v1", classes["browser_worker"]["required_gates"])
        self.assertIn("runtime_start_preflight_v1", classes["durable_runtime"]["required_gates"])
        self.assertIn("mcp_tool_registry_gate_v1", classes["gateway_or_mcp"]["required_gates"])
        self.assertIn("model_api_execution_gate", classes["model_backed_agent_framework"]["required_gates"])
        self.assertEqual(report["next_action"], "Build unified_agent_egress_gateway_docket_v1 before registering or starting any worker capability class.")


if __name__ == "__main__":
    unittest.main()
