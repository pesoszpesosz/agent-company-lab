import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


def run_validator_load_artifacts(
    test_case: unittest.TestCase,
    *,
    root: Path,
    tool: Path,
    validation_path: Path,
    report_path: Path,
    schema_path: Path,
    timeout: int = 30,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    result = subprocess.run(
        [sys.executable, str(tool)],
        cwd=str(root),
        text=True,
        capture_output=True,
        timeout=timeout,
    )

    test_case.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return validation, report, schema


def assert_clean_fixture_validation(
    test_case: unittest.TestCase,
    validation: dict[str, Any],
    *,
    min_fixture_count: int,
) -> None:
    test_case.assertTrue(validation["all_checks_passed"])
    test_case.assertEqual(validation["failure_count"], 0)
    test_case.assertGreaterEqual(validation["fixture_count"], min_fixture_count)
    test_case.assertEqual(validation["accepted_count"], validation["expected_accepted_count"])
    test_case.assertEqual(validation["rejected_count"], validation["expected_rejected_count"])
    if "fixture_expectation_mismatch_count" in validation:
        test_case.assertEqual(validation["fixture_expectation_mismatch_count"], 0)


def assert_false_fields(
    test_case: unittest.TestCase,
    payload: dict[str, Any],
    fields: list[str],
) -> None:
    for field in fields:
        test_case.assertFalse(payload[field])


def assert_zero_fields(
    test_case: unittest.TestCase,
    payload: dict[str, Any],
    fields: list[str],
) -> None:
    for field in fields:
        test_case.assertEqual(payload[field], 0)
