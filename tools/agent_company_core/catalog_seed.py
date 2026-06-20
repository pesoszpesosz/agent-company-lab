from __future__ import annotations

import json
import sqlite3
from typing import Any

"""Catalog seed and upsert operations."""

from .io import load_json, now_utc
from .paths import LANE_TAXONOMY_PATH, ROLE_REGISTRY_PATH, SERVICE_CATALOG_PATH, SOURCE_SPECS_PATH
from .schema import init_db

def upsert_role(conn: sqlite3.Connection, role: dict[str, Any]) -> None:
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES(?, ?, ?, ?, ?, ?)
        ON CONFLICT(role_id) DO UPDATE SET
          level=excluded.level,
          responsibilities_json=excluded.responsibilities_json,
          must_not_do_json=excluded.must_not_do_json,
          updated_at=excluded.updated_at
        """,
        (
            role["id"],
            role["level"],
            json.dumps(role.get("responsibilities", []), sort_keys=True),
            json.dumps(role.get("must_not_do", []), sort_keys=True),
            ts,
            ts,
        ),
    )


def department_id(name: str) -> str:
    return (
        name.lower()
        .replace("/", "_")
        .replace("&", "and")
        .replace(" ", "_")
        .replace("-", "_")
    )


def upsert_department(conn: sqlite3.Connection, name: str) -> str:
    dep_id = department_id(name)
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO departments(department_id, name, status, created_at, updated_at)
        VALUES(?, ?, 'planned', ?, ?)
        ON CONFLICT(department_id) DO UPDATE SET
          name=excluded.name,
          updated_at=excluded.updated_at
        """,
        (dep_id, name, ts, ts),
    )
    return dep_id


def upsert_lane(conn: sqlite3.Connection, lane: dict[str, Any], global_gates: list[str]) -> None:
    ts = now_utc()
    upsert_department(conn, lane["department"])
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_thread_id, agent_types_json, examples_json,
          promotion_gates_json, service_workers_required_json, side_effects_json,
          global_gates_json, notes, created_at, updated_at
        )
        VALUES(?, ?, 'active', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(lane_id) DO UPDATE SET
          department=excluded.department,
          agent_types_json=excluded.agent_types_json,
          examples_json=excluded.examples_json,
          promotion_gates_json=excluded.promotion_gates_json,
          service_workers_required_json=excluded.service_workers_required_json,
          side_effects_json=excluded.side_effects_json,
          global_gates_json=excluded.global_gates_json,
          notes=excluded.notes,
          updated_at=excluded.updated_at
        """,
        (
            lane["id"],
            lane["department"],
            lane.get("owner_thread"),
            json.dumps(lane.get("agent_types", []), sort_keys=True),
            json.dumps(lane.get("examples", []), sort_keys=True),
            json.dumps(lane.get("promotion_gates", []), sort_keys=True),
            json.dumps(lane.get("service_workers_required", []), sort_keys=True),
            json.dumps(lane.get("side_effects", []), sort_keys=True),
            json.dumps(global_gates, sort_keys=True),
            lane.get("owner_thread"),
            ts,
            ts,
        ),
    )


def upsert_source_spec(conn: sqlite3.Connection, spec: dict[str, Any]) -> None:
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO source_specs(
          spec_id, lane_id, name, source_type, source_paths_json, refresh_command,
          cadence, risk_gate, outputs_json, status, notes, created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?, ?)
        ON CONFLICT(spec_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          name=excluded.name,
          source_type=excluded.source_type,
          source_paths_json=excluded.source_paths_json,
          refresh_command=excluded.refresh_command,
          cadence=excluded.cadence,
          risk_gate=excluded.risk_gate,
          outputs_json=excluded.outputs_json,
          status=excluded.status,
          notes=excluded.notes,
          updated_at=excluded.updated_at
        """,
        (
            spec["id"],
            spec["lane_id"],
            spec["name"],
            spec["source_type"],
            json.dumps(spec.get("source_paths", []), sort_keys=True),
            spec.get("refresh_command"),
            spec["cadence"],
            spec["risk_gate"],
            json.dumps(spec.get("outputs", []), sort_keys=True),
            spec.get("notes"),
            ts,
            ts,
        ),
    )


def upsert_service_definition(conn: sqlite3.Connection, service: dict[str, Any]) -> None:
    ts = now_utc()
    dep_id = upsert_department(conn, service.get("department", "Service Bureau"))
    conn.execute(
        """
        INSERT INTO service_catalog(
          service_id, department_id, name, request_type, owner_role_id, purpose,
          allowed_actions_json, hard_gates_json, required_intake_json,
          approval_required_by_json, output_artifacts_json, default_status,
          notes, created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(service_id) DO UPDATE SET
          department_id=excluded.department_id,
          name=excluded.name,
          request_type=excluded.request_type,
          owner_role_id=excluded.owner_role_id,
          purpose=excluded.purpose,
          allowed_actions_json=excluded.allowed_actions_json,
          hard_gates_json=excluded.hard_gates_json,
          required_intake_json=excluded.required_intake_json,
          approval_required_by_json=excluded.approval_required_by_json,
          output_artifacts_json=excluded.output_artifacts_json,
          default_status=excluded.default_status,
          notes=excluded.notes,
          updated_at=excluded.updated_at
        """,
        (
            service["id"],
            dep_id,
            service["name"],
            service["request_type"],
            service["owner_role_id"],
            service["purpose"],
            json.dumps(service.get("allowed_actions", []), sort_keys=True),
            json.dumps(service.get("hard_gates", []), sort_keys=True),
            json.dumps(service.get("required_intake", []), sort_keys=True),
            json.dumps(service.get("approval_required_by", []), sort_keys=True),
            json.dumps(service.get("output_artifacts", []), sort_keys=True),
            service.get("default_status", "available"),
            service.get("notes"),
            ts,
            ts,
        ),
    )


def seed_source_specs(conn: sqlite3.Connection) -> None:
    if not SOURCE_SPECS_PATH.exists():
        return
    payload = load_json(SOURCE_SPECS_PATH)
    for spec in payload.get("specs", []):
        upsert_source_spec(conn, spec)


def seed_service_catalog(conn: sqlite3.Connection) -> None:
    if not SERVICE_CATALOG_PATH.exists():
        return
    roles = load_json(ROLE_REGISTRY_PATH)
    for role in roles["roles"]:
        upsert_role(conn, role)
    payload = load_json(SERVICE_CATALOG_PATH)
    for service in payload.get("services", []):
        upsert_service_definition(conn, service)


def seed(conn: sqlite3.Connection) -> None:
    init_db(conn)
    roles = load_json(ROLE_REGISTRY_PATH)
    lanes = load_json(LANE_TAXONOMY_PATH)
    for role in roles["roles"]:
        upsert_role(conn, role)
    for lane in lanes["lanes"]:
        upsert_lane(conn, lane, lanes.get("global_gates", []))
    seed_source_specs(conn)
    seed_service_catalog(conn)
    conn.commit()
