"""Durable-adapter fixture validation helpers."""

from __future__ import annotations

import json
from typing import Any

from .constants import (
    DURABLE_ADAPTER_ACTION_FIELDS,
    DURABLE_ADAPTER_ALLOWED_OUTPUT_STATES,
    DURABLE_ADAPTER_REQUIRED_FIXTURE_FIELDS,
    DURABLE_ADAPTER_REQUIRED_INPUT_FIELDS,
)


def add_durable_adapter_validation_error(
    errors: list[dict[str, Any]],
    fixture_index: int | None,
    fixture_id: Any,
    field: str,
    message: str,
    actual: Any = None,
) -> None:
    errors.append(
        {
            "fixture_index": fixture_index,
            "fixture_id": fixture_id,
            "field": field,
            "message": message,
            "actual": actual,
        }
    )


def require_durable_adapter_nonempty_string(
    errors: list[dict[str, Any]],
    fixture_index: int,
    fixture_id: Any,
    field: str,
    value: Any,
) -> None:
    if not isinstance(value, str) or not value.strip():
        add_durable_adapter_validation_error(
            errors,
            fixture_index,
            fixture_id,
            field,
            "must be a non-empty string",
            value,
        )


def validate_durable_adapter_fixture_doc(fixture_doc: dict[str, Any], fixtures: list[Any]) -> None:
    errors: list[dict[str, Any]] = []
    fixture_count = fixture_doc.get("fixture_count")
    if fixture_count is not None and fixture_count != len(fixtures):
        add_durable_adapter_validation_error(
            errors,
            None,
            None,
            "fixture_count",
            f"must equal len(fixtures), expected {len(fixtures)}",
            fixture_count,
        )

    seen_fixture_ids: set[str] = set()
    seen_request_ids: set[str] = set()
    seen_idempotency_keys: set[str] = set()
    for index, fixture in enumerate(fixtures):
        fixture_id = fixture.get("fixture_id") if isinstance(fixture, dict) else None
        if not isinstance(fixture, dict):
            add_durable_adapter_validation_error(
                errors,
                index,
                fixture_id,
                "fixture",
                "must be an object",
                fixture,
            )
            continue

        for field in DURABLE_ADAPTER_REQUIRED_FIXTURE_FIELDS:
            if field not in fixture:
                add_durable_adapter_validation_error(
                    errors,
                    index,
                    fixture_id,
                    field,
                    "required top-level fixture field is missing",
                )

        request_id = fixture.get("request_id")
        require_durable_adapter_nonempty_string(errors, index, fixture_id, "fixture_id", fixture_id)
        require_durable_adapter_nonempty_string(errors, index, fixture_id, "request_id", request_id)

        for field, value, seen in [
            ("fixture_id", fixture_id, seen_fixture_ids),
            ("request_id", request_id, seen_request_ids),
        ]:
            if isinstance(value, str) and value.strip():
                if value in seen:
                    add_durable_adapter_validation_error(
                        errors,
                        index,
                        fixture_id,
                        field,
                        "must be unique within the fixture packet",
                        value,
                    )
                seen.add(value)

        fixture_input = fixture.get("input")
        expected = fixture.get("expected_output")
        expected_exit = fixture.get("expected_exit")
        if not isinstance(fixture_input, dict):
            add_durable_adapter_validation_error(
                errors,
                index,
                fixture_id,
                "input",
                "must be an object",
                fixture_input,
            )
            fixture_input = {}
        if not isinstance(expected, dict):
            add_durable_adapter_validation_error(
                errors,
                index,
                fixture_id,
                "expected_output",
                "must be an object",
                expected,
            )
            expected = {}
        if not isinstance(expected_exit, dict):
            add_durable_adapter_validation_error(
                errors,
                index,
                fixture_id,
                "expected_exit",
                "must be an object",
                expected_exit,
            )
            expected_exit = {}

        for field in DURABLE_ADAPTER_REQUIRED_INPUT_FIELDS:
            require_durable_adapter_nonempty_string(
                errors,
                index,
                fixture_id,
                f"input.{field}",
                fixture_input.get(field),
            )

        idempotency_key = fixture_input.get("idempotency_key")
        if isinstance(idempotency_key, str) and idempotency_key.strip():
            if idempotency_key in seen_idempotency_keys:
                add_durable_adapter_validation_error(
                    errors,
                    index,
                    fixture_id,
                    "input.idempotency_key",
                    "must be unique within the fixture packet",
                    idempotency_key,
                )
            seen_idempotency_keys.add(idempotency_key)

        output_state = expected.get("output_state")
        if output_state not in DURABLE_ADAPTER_ALLOWED_OUTPUT_STATES:
            add_durable_adapter_validation_error(
                errors,
                index,
                fixture_id,
                "expected_output.output_state",
                "must be one of the allowed durable adapter output states",
                output_state,
            )

        for field in ["parked", "terminal"]:
            if not isinstance(expected.get(field), bool):
                add_durable_adapter_validation_error(
                    errors,
                    index,
                    fixture_id,
                    f"expected_output.{field}",
                    "must be a boolean",
                    expected.get(field),
                )

        for field in DURABLE_ADAPTER_ACTION_FIELDS:
            if expected.get(field) is not False:
                add_durable_adapter_validation_error(
                    errors,
                    index,
                    fixture_id,
                    f"expected_output.{field}",
                    "must be explicitly false for dry-run safety",
                    expected.get(field),
                )

        resume_requirements = expected.get("resume_requirements")
        if not isinstance(resume_requirements, list) or not all(
            isinstance(item, str) and item.strip() for item in resume_requirements
        ):
            add_durable_adapter_validation_error(
                errors,
                index,
                fixture_id,
                "expected_output.resume_requirements",
                "must be a list of non-empty strings",
                resume_requirements,
            )
        elif output_state == "parked.awaiting_human_review" and not resume_requirements:
            add_durable_adapter_validation_error(
                errors,
                index,
                fixture_id,
                "expected_output.resume_requirements",
                "must be non-empty for parked states",
                resume_requirements,
            )

        if expected_exit.get("exit_code") != 0:
            add_durable_adapter_validation_error(
                errors,
                index,
                fixture_id,
                "expected_exit.exit_code",
                "must be 0 in the positive reducer fixture packet",
                expected_exit.get("exit_code"),
            )

    if errors:
        raise SystemExit(
            json.dumps(
                {
                    "ok": False,
                    "error": "durable_adapter_fixture_validation_failed",
                    "failure_count": len(errors),
                    "failures": errors,
                },
                indent=2,
                sort_keys=True,
            )
        )

__all__ = [
    "add_durable_adapter_validation_error",
    "require_durable_adapter_nonempty_string",
    "validate_durable_adapter_fixture_doc",
]
