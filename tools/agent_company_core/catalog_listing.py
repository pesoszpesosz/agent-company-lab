from __future__ import annotations

import argparse
import json
import sqlite3
from typing import Any

"""Catalog list and filter operations."""

from .utils import decode_json_list

def list_evidence(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    params: list[Any] = []
    where = ""
    if args.lane_id:
        where = "WHERE lane_id = ?"
        params.append(args.lane_id)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT evidence_id, lane_id, status, title, source_path, source_url, next_action, ownership_note, updated_at
            FROM lane_evidence
            {where}
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            params,
        )
    ]
    print(json.dumps({"count": len(rows), "evidence": rows}, indent=2))


def list_source_specs(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    params: list[Any] = []
    where = ""
    if args.lane_id:
        where = "WHERE lane_id = ?"
        params.append(args.lane_id)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT spec_id, lane_id, name, source_type, cadence, risk_gate, refresh_command, source_paths_json, outputs_json, notes
            FROM source_specs
            {where}
            ORDER BY lane_id, spec_id
            LIMIT ?
            """,
            params,
        )
    ]
    for row in rows:
        row["source_paths"] = decode_json_list(row.pop("source_paths_json"))
        row["outputs"] = decode_json_list(row.pop("outputs_json"))
    print(json.dumps({"count": len(rows), "source_specs": rows}, indent=2))


def service_catalog_where(args: argparse.Namespace) -> tuple[str, list[Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if getattr(args, "service_id", None):
        clauses.append("service_id = ?")
        params.append(args.service_id)
    if getattr(args, "request_type", None):
        clauses.append("request_type = ?")
        params.append(args.request_type)
    if getattr(args, "owner_role_id", None):
        clauses.append("owner_role_id = ?")
        params.append(args.owner_role_id)
    if getattr(args, "status", None):
        clauses.append("default_status = ?")
        params.append(args.status)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    return where, params


def list_service_catalog(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    where, params = service_catalog_where(args)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT service_id, department_id, name, request_type, owner_role_id, purpose,
                   allowed_actions_json, hard_gates_json, required_intake_json,
                   approval_required_by_json, output_artifacts_json, default_status, notes
            FROM service_catalog
            {where}
            ORDER BY request_type, service_id
            LIMIT ?
            """,
            params,
        )
    ]
    for row in rows:
        row["allowed_actions"] = decode_json_list(row.pop("allowed_actions_json"))
        row["hard_gates"] = decode_json_list(row.pop("hard_gates_json"))
        row["required_intake"] = decode_json_list(row.pop("required_intake_json"))
        row["approval_required_by"] = decode_json_list(row.pop("approval_required_by_json"))
        row["output_artifacts"] = decode_json_list(row.pop("output_artifacts_json"))
    print(json.dumps({"count": len(rows), "service_catalog": rows}, indent=2))
