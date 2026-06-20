import unittest
from pathlib import Path

from generated_artifact_helpers import (
    assert_clean_fixture_validation,
    assert_false_fields,
    assert_zero_fields,
    run_validator_load_artifacts,
)


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_public_action_egress_apply_command_contract.py"
VALIDATION = ROOT / "reports" / "public-action-egress-apply-command-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "public-action-egress-apply-command-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "public-action-egress-apply-command-contract-v1.schema.json"


class PublicActionEgressApplyCommandContractTest(unittest.TestCase):
    def test_contract_rejects_live_public_action_apply_commands(self) -> None:
        validation, report, schema = run_validator_load_artifacts(
            self,
            root=ROOT,
            tool=TOOL,
            validation_path=VALIDATION,
            report_path=REPORT,
            schema_path=SCHEMA,
        )

        assert_clean_fixture_validation(self, validation, min_fixture_count=40)
        self.assertEqual(validation["target_route_id"], "public_action_gateway")
        self.assertEqual(validation["target_egress_type"], "public_submission")
        assert_false_fields(
            self,
            validation,
            [
                "apply_command_allowed",
                "apply_allowed",
                "gateway_registration_allowed",
                "gateway_start_allowed",
                "live_egress_allowed",
                "public_action_allowed",
                "public_actions",
                "browser_session_start_allowed",
                "account_actions",
                "mcp_tool_calls",
                "model_api_calls",
                "external_side_effects",
            ],
        )
        assert_zero_fields(
            self,
            validation,
            [
                "posts_created",
                "forms_submitted",
                "prs_opened",
                "bounty_claims",
                "messages_sent",
                "browser_sessions_started",
                "service_requests_assigned",
                "service_requests_updated",
                "apply_commands_written",
                "apply_commands_executed",
            ],
        )
        self.assertEqual(schema["properties"]["command_type"]["enum"][0], "deny_noop")
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "public_action_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "public_submission")
        self.assertEqual(schema["properties"]["public_action_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        accepted = [item for item in report["results"] if item["result"]["accepted_for_contract_only"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            payload = item["result"]
            self.assertEqual(payload["target_route_id"], "public_action_gateway")
            self.assertFalse(payload["apply_command_allowed"])
            self.assertFalse(payload["public_action_allowed"])
            self.assertFalse(payload["public_actions"])
            self.assertFalse(payload["browser_session_start_allowed"])

        self.assertEqual(
            report["next_action"],
            "Build public action egress apply-command guard v1 only after a real signed operator decision, exact "
            "action-body approval, and executable command preview exist; until then, keep public egress blocked.",
        )


if __name__ == "__main__":
    unittest.main()
