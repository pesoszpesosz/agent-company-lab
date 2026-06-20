import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_egress_route_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "egress-route-apply-preflight-blocker-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "egress-route-apply-preflight-blocker-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "egress-route-apply-preflight-blocker-v1.schema.json"


class EgressRouteApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_prevents_apply_after_signed_guard_until_apply_contract_exists(self) -> None:
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
        self.assertEqual(validation["target_route_id"], "browser_read_only_gateway")
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_egress_route_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertTrue(validation["apply_command_contract_present"])
        self.assertFalse(validation["apply_allowed"])
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "browser_read_only_gateway")
        self.assertEqual(schema["properties"]["apply_allowed"]["const"], False)

        checks = {item["check_id"]: item for item in report["checks"]}
        for required in [
            "gateway_docket_validation_passes",
            "signed_decision_intake_validation_passes",
            "signed_decision_guard_passes_for_target_route",
            "real_signed_decision_absent",
            "apply_command_contract_observed_without_apply",
        ]:
            self.assertIn(required, checks)
            self.assertTrue(checks[required]["passed"])

        self.assertEqual(
            report["next_action"],
            "Provide a real signed operator egress-route decision artifact, then build an apply-command guard before any browser gateway registration, service request mutation, browser session, worker start, or live egress can be considered.",
        )


if __name__ == "__main__":
    unittest.main()
