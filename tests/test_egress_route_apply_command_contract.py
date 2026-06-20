import unittest
from pathlib import Path

from generated_artifact_helpers import (
    assert_clean_fixture_validation,
    assert_false_fields,
    assert_zero_fields,
    run_validator_load_artifacts,
)


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_egress_route_apply_command_contract.py"
VALIDATION = ROOT / "reports" / "egress-route-apply-command-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "egress-route-apply-command-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "egress-route-apply-command-contract-v1.schema.json"


class EgressRouteApplyCommandContractTest(unittest.TestCase):
    def test_contract_rejects_live_browser_egress_apply_commands(self) -> None:
        validation, report, schema = run_validator_load_artifacts(
            self,
            root=ROOT,
            tool=TOOL,
            validation_path=VALIDATION,
            report_path=REPORT,
            schema_path=SCHEMA,
        )

        assert_clean_fixture_validation(self, validation, min_fixture_count=35)
        self.assertEqual(validation["target_route_id"], "browser_read_only_gateway")
        assert_false_fields(
            self,
            validation,
            [
                "apply_command_allowed",
                "apply_allowed",
                "gateway_registration_allowed",
                "gateway_start_allowed",
                "live_egress_allowed",
                "browser_session_start_allowed",
                "worker_start_allowed",
                "external_side_effects",
            ],
        )
        assert_zero_fields(
            self,
            validation,
            [
                "service_requests_assigned",
                "service_requests_updated",
                "apply_commands_written",
                "apply_commands_executed",
            ],
        )
        self.assertEqual(schema["properties"]["command_type"]["enum"][0], "deny_noop")
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "browser_read_only_gateway")
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        accepted = [item for item in report["results"] if item["result"]["accepted_for_contract_only"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            self.assertEqual(item["result"]["target_route_id"], "browser_read_only_gateway")
            self.assertFalse(item["result"]["apply_command_allowed"])
            self.assertFalse(item["result"]["gateway_start_allowed"])
            self.assertFalse(item["result"]["browser_session_start_allowed"])

        self.assertEqual(
            report["next_action"],
            "Build egress route apply-command guard v1 only after a real signed operator decision and executable "
            "command preview exist; until then, keep browser egress blocked.",
        )


if __name__ == "__main__":
    unittest.main()
