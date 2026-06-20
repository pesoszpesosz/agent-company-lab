import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_egress_route_signed_decision_intake_contract.py"
VALIDATION = ROOT / "reports" / "egress-route-signed-decision-intake-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "egress-route-signed-decision-intake-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "egress-route-signed-decision-intake-contract-v1.schema.json"


class EgressRouteSignedDecisionIntakeContractTest(unittest.TestCase):
    def test_intake_contract_covers_gateway_routes_without_live_egress(self) -> None:
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
        self.assertGreaterEqual(validation["route_count"], 8)
        self.assertEqual(validation["template_count"], validation["route_count"])
        self.assertGreaterEqual(validation["fixture_count"], 25)
        self.assertGreaterEqual(validation["accepted_count"], 3)
        self.assertGreaterEqual(validation["rejected_count"], 20)
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertEqual(validation["gateway_registrations"], 0)
        self.assertEqual(validation["gateway_starts"], 0)
        self.assertEqual(validation["live_egress_events"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        templates = {item["route_id"]: item for item in report["decision_templates"]}
        for route_id in [
            "local_agent_to_agent_report_only",
            "browser_read_only_gateway",
            "mcp_tool_gateway",
            "model_api_gateway",
            "runtime_process_gateway",
            "public_action_gateway",
            "account_wallet_payment_gateway",
            "telemetry_export_gateway",
        ]:
            self.assertIn(route_id, templates)
            self.assertIn("deny", templates[route_id]["allowed_decisions"])
            self.assertIn("approve_route_preflight_only", templates[route_id]["allowed_decisions"])
            self.assertIn("agent_egress_event_ledger_v1", templates[route_id]["required_gates"])
            self.assertTrue(templates[route_id]["approval_is_not_apply"])
            self.assertFalse(templates[route_id]["approval_granted_by_contract"])
            self.assertFalse(templates[route_id]["apply_allowed"])

        self.assertIn("browser_read_only_apply_command_contract_v1", templates["browser_read_only_gateway"]["required_gates"])
        self.assertIn("mcp_tool_registry_gate_v1", templates["mcp_tool_gateway"]["required_gates"])
        self.assertIn("model_api_execution_gate", templates["model_api_gateway"]["required_gates"])
        self.assertIn("runtime_start_preflight_v1", templates["runtime_process_gateway"]["required_gates"])
        self.assertIn("legal_kyc_tax_payment_gate", templates["account_wallet_payment_gateway"]["required_gates"])
        self.assertEqual(
            report["next_action"],
            "Build egress route signed-decision guard for one exact route decision before any apply preflight, gateway registration, gateway start, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
