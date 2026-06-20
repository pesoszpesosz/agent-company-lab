import unittest
from pathlib import Path

from generated_artifact_helpers import (
    assert_clean_fixture_validation,
    assert_false_fields,
    assert_zero_fields,
    run_validator_load_artifacts,
)


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_runtime_process_egress_apply_command_contract.py"
VALIDATION = ROOT / "reports" / "runtime-process-egress-apply-command-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "runtime-process-egress-apply-command-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "runtime-process-egress-apply-command-contract-v1.schema.json"


class RuntimeProcessEgressApplyCommandContractTest(unittest.TestCase):
    def test_contract_rejects_live_runtime_process_apply_commands(self) -> None:
        validation, report, schema = run_validator_load_artifacts(
            self,
            root=ROOT,
            tool=TOOL,
            validation_path=VALIDATION,
            report_path=REPORT,
            schema_path=SCHEMA,
        )

        assert_clean_fixture_validation(self, validation, min_fixture_count=40)
        self.assertEqual(validation["target_route_id"], "runtime_process_gateway")
        self.assertEqual(validation["target_egress_type"], "runtime_start")
        assert_false_fields(
            self,
            validation,
            [
                "apply_command_allowed",
                "apply_allowed",
                "gateway_registration_allowed",
                "gateway_start_allowed",
                "live_egress_allowed",
                "runtime_start_allowed",
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
                "runtime_starts",
                "dependency_installs",
                "queue_mutations",
                "worker_starts",
                "service_requests_assigned",
                "service_requests_updated",
                "apply_commands_written",
                "apply_commands_executed",
            ],
        )

        self.assertEqual(schema["properties"]["command_type"]["enum"][0], "deny_noop")
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "runtime_process_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "runtime_start")
        self.assertEqual(schema["properties"]["runtime_start_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        accepted = [item for item in report["results"] if item["result"]["accepted_for_contract_only"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            payload = item["result"]
            self.assertEqual(payload["target_route_id"], "runtime_process_gateway")
            self.assertFalse(payload["apply_command_allowed"])
            self.assertFalse(payload["runtime_start_allowed"])
            self.assertEqual(payload["runtime_starts"], 0)
            self.assertEqual(payload["dependency_installs"], 0)
            self.assertEqual(payload["queue_mutations"], 0)

        self.assertEqual(
            report["next_action"],
            "Build runtime process egress apply-command guard v1 only after a real signed operator decision and "
            "executable command preview exist; until then, keep runtime process egress blocked.",
        )


if __name__ == "__main__":
    unittest.main()
