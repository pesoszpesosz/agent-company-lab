import unittest
from pathlib import Path

from generated_artifact_helpers import (
    assert_clean_fixture_validation,
    assert_false_fields,
    assert_zero_fields,
    run_validator_load_artifacts,
)


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_local_a2a_egress_apply_command_contract.py"
VALIDATION = ROOT / "reports" / "local-a2a-egress-apply-command-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "local-a2a-egress-apply-command-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "local-a2a-egress-apply-command-contract-v1.schema.json"


class LocalA2AEgressApplyCommandContractTest(unittest.TestCase):
    def test_contract_rejects_live_local_a2a_apply_commands(self) -> None:
        validation, report, schema = run_validator_load_artifacts(
            self,
            root=ROOT,
            tool=TOOL,
            validation_path=VALIDATION,
            report_path=REPORT,
            schema_path=SCHEMA,
        )

        assert_clean_fixture_validation(self, validation, min_fixture_count=38)
        self.assertEqual(validation["target_route_id"], "local_agent_to_agent_report_only")
        self.assertEqual(validation["target_egress_type"], "agent_to_agent")
        assert_false_fields(
            self,
            validation,
            [
                "apply_command_allowed",
                "apply_allowed",
                "gateway_registration_allowed",
                "gateway_start_allowed",
                "live_egress_allowed",
                "agent_message_send_allowed",
                "worker_start_allowed",
                "model_api_calls",
                "mcp_tool_calls",
                "browser_sessions_started",
                "external_side_effects",
            ],
        )
        assert_zero_fields(
            self,
            validation,
            [
                "agent_messages_sent",
                "service_requests_assigned",
                "service_requests_updated",
                "apply_commands_written",
                "apply_commands_executed",
            ],
        )
        self.assertEqual(schema["properties"]["command_type"]["enum"][0], "deny_noop")
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "local_agent_to_agent_report_only")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "agent_to_agent")
        self.assertEqual(schema["properties"]["agent_message_send_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        accepted = [item for item in report["results"] if item["result"]["accepted_for_contract_only"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            self.assertEqual(item["result"]["target_route_id"], "local_agent_to_agent_report_only")
            self.assertFalse(item["result"]["apply_command_allowed"])
            self.assertFalse(item["result"]["agent_message_send_allowed"])
            self.assertEqual(item["result"]["agent_messages_sent"], 0)
            self.assertFalse(item["result"]["worker_start_allowed"])

        self.assertEqual(
            report["next_action"],
            "Build local A2A egress apply-command guard v1 only after a real signed operator decision and executable "
            "command preview exist; until then, keep local A2A egress blocked.",
        )


if __name__ == "__main__":
    unittest.main()
