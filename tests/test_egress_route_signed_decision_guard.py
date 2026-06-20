import unittest
from pathlib import Path

from generated_artifact_helpers import (
    assert_clean_fixture_validation,
    assert_false_fields,
    assert_zero_fields,
    run_validator_load_artifacts,
)


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_egress_route_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "egress-route-signed-decision-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "egress-route-signed-decision-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "egress-route-signed-decision-guard-v1.schema.json"


class EgressRouteSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_exact_browser_route_preflight_decisions(self) -> None:
        validation, report, schema = run_validator_load_artifacts(
            self,
            root=ROOT,
            tool=TOOL,
            validation_path=VALIDATION,
            report_path=REPORT,
            schema_path=SCHEMA,
        )

        assert_clean_fixture_validation(self, validation, min_fixture_count=30)
        self.assertEqual(validation["target_route_id"], "browser_read_only_gateway")
        self.assertEqual(validation["target_egress_type"], "browser_read_only")
        assert_zero_fields(
            self,
            validation,
            [
                "gateway_registrations",
                "gateway_starts",
                "live_egress_events",
                "browser_sessions_started",
                "worker_starts",
                "decisions_applied",
            ],
        )
        assert_false_fields(self, validation, ["model_api_calls", "mcp_tool_calls", "external_side_effects"])
        self.assertEqual(schema["properties"]["route_id"]["const"], "browser_read_only_gateway")
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        self.assertIn("browser_read_only_apply_command_contract_v1", report["target_route_required_gates"])
        self.assertIn("agent_egress_event_ledger_v1", report["target_route_required_gates"])
        accepted = [item for item in report["results"] if item["result"]["accepted_for_apply_preflight"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            self.assertEqual(item["result"]["route_id"], "browser_read_only_gateway")
            self.assertFalse(item["result"]["gateway_start_allowed"])
            self.assertFalse(item["result"]["live_egress_allowed"])
            self.assertFalse(item["result"]["browser_session_start_allowed"])

        self.assertEqual(
            report["next_action"],
            "Build egress route apply preflight blocker for the accepted browser_read_only_gateway decision before "
            "any gateway registration, browser session, worker start, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
