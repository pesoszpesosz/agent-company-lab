"""Bootstrap CEO-facing AI Resources workers and durable goals."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR
from .premium_customer_intake_router import ZERO_SIDE_EFFECT_BOUNDARY
from .utils import md_cell, sha256_file


SCHEMA_VERSION = "ceo_worker_bootstrap.v1"
DEFAULT_JSON = REPORTS_DIR / "ceo-worker-roster-v1-20260621.json"
DEFAULT_MD = REPORTS_DIR / "ceo-worker-roster-v1-20260621.md"
AI_RESOURCES_LANE = "ai_resources_lab"
AI_RESOURCES_DEPARTMENT = "ai_resources"
AI_RESOURCES_MANAGER = "lane-manager-ai_resources_lab-20260620"
BOOTSTRAP_TASK_ID = "task-ceo-worker-bootstrap-v1-20260621"


ROLES: list[dict[str, Any]] = [
    {
        "role_id": "ai_resources_manager",
        "level": "manager",
        "responsibilities": [
            "own the AI Resources queue",
            "hire evolve park or retire AI workers based on evidence",
            "enforce capability non-overlap before new agents are created",
            "report compact AR state to the CEO packet",
        ],
        "must_not_do": [
            "create duplicate agents for capabilities already owned",
            "start external worker runtimes without a gated service request",
            "hide failed evaluations",
        ],
    },
    {
        "role_id": "capability_overlap_mapper",
        "level": "worker",
        "responsibilities": [
            "map every requested capability to existing lanes roles agents tools and packets",
            "prove whether an existing worker can evolve before recommending a hire",
            "maintain the no-overlap map for AR decisions",
        ],
        "must_not_do": ["recommend a new agent without overlap evidence", "retire agents directly"],
    },
    {
        "role_id": "candidate_registry_curator",
        "level": "worker",
        "responsibilities": [
            "collect AI-agent frameworks tools and worker candidates",
            "normalize candidate evidence into local registry packets",
            "queue candidates for local-only evaluation",
        ],
        "must_not_do": ["install untrusted tools", "call external APIs", "promote candidates without evaluation"],
    },
    {
        "role_id": "local_evaluation_harness_builder",
        "level": "worker",
        "responsibilities": [
            "build local fixture tests for AI resources and worker candidates",
            "define pass fail watch and reject gates",
            "record reproducible evidence for AR decisions",
        ],
        "must_not_do": ["start untrusted runtimes", "perform networked tests without approval"],
    },
    {
        "role_id": "adoption_retirement_reviewer",
        "level": "worker",
        "responsibilities": [
            "write adopt evolve watch reject and retire recommendations",
            "identify stale or overlapping agents",
            "propose smaller context capsules for existing agents",
        ],
        "must_not_do": ["delete agents directly", "change lane ownership without manager decision"],
    },
    {
        "role_id": "continuity_watchdog_worker",
        "level": "worker",
        "responsibilities": [
            "check stale offline ownerless overlapping or goal-less work",
            "use parallel checker agents when available",
            "write restore or escalation packets every cadence",
        ],
        "must_not_do": ["mutate external state", "auto-approve service requests", "duplicate lane workers"],
    },
    {
        "role_id": "premium_customer_context_router",
        "level": "manager",
        "responsibilities": [
            "receive premium customer requests and materials",
            "preserve raw context outside the CEO window",
            "route compact capsules to the right lanes and update the customer",
        ],
        "must_not_do": ["dump raw materials into CEO context", "reject usable input without a revisit branch"],
    },
    {
        "role_id": "browser_account_ops_worker",
        "level": "service_worker",
        "responsibilities": [
            "prepare browser and account-operation packets",
            "separate AI-doable account work from human KYC tax billing or legal gates",
            "keep exact human-action asks rare and scoped",
        ],
        "must_not_do": ["create accounts without approval", "accept terms", "submit KYC", "change billing"],
    },
]


AGENTS: list[dict[str, Any]] = [
    {
        "agent_id": AI_RESOURCES_MANAGER,
        "role_id": "ai_resources_manager",
        "department_id": AI_RESOURCES_DEPARTMENT,
        "thread_arg": "ar_thread_id",
        "goal": "Lead the AI Resources operating cell: hire, evolve, park, or retire agents only after capability-overlap review and local evidence.",
    },
    {
        "agent_id": "capability-overlap-mapper-20260621",
        "role_id": "capability_overlap_mapper",
        "department_id": AI_RESOURCES_DEPARTMENT,
        "thread_arg": "overlap_thread_id",
        "goal": "Maintain the capability overlap map so new AI hires happen only when existing owners cannot evolve to cover the need.",
    },
    {
        "agent_id": "candidate-registry-curator-20260621",
        "role_id": "candidate_registry_curator",
        "department_id": AI_RESOURCES_DEPARTMENT,
        "thread_arg": "candidate_thread_id",
        "goal": "Curate external AI worker frameworks and money-making agent candidates into a local candidate registry with source evidence.",
    },
    {
        "agent_id": "local-evaluation-harness-builder-20260621",
        "role_id": "local_evaluation_harness_builder",
        "department_id": AI_RESOURCES_DEPARTMENT,
        "thread_arg": "evaluation_thread_id",
        "goal": "Build local-only eval packets that prove whether candidate agents or tools improve the company before adoption.",
    },
    {
        "agent_id": "adoption-retirement-reviewer-20260621",
        "role_id": "adoption_retirement_reviewer",
        "department_id": AI_RESOURCES_DEPARTMENT,
        "thread_arg": "retirement_thread_id",
        "goal": "Recommend evolve, watch, reject, merge, or retire decisions for stale, overlapping, or under-specified agents.",
    },
    {
        "agent_id": "continuity-watchdog-worker-20260621",
        "role_id": "continuity_watchdog_worker",
        "department_id": AI_RESOURCES_DEPARTMENT,
        "thread_arg": "continuity_thread_id",
        "goal": "Run the continuity loop: check active lanes for stale, offline, ownerless, overlapping, or goal-less work and write restore packets.",
    },
    {
        "agent_id": "premium-customer-context-router-20260621",
        "role_id": "premium_customer_context_router",
        "department_id": "premium_customer_intake",
        "thread_arg": "premium_router_thread_id",
        "goal": "Accept premium customer input, preserve raw material outside CEO context, route compact capsules to lanes, and update the customer.",
    },
    {
        "agent_id": "browser-account-ops-worker-20260621",
        "role_id": "browser_account_ops_worker",
        "department_id": "ceo_control_room",
        "thread_arg": "browser_ops_thread_id",
        "goal": "Prepare browser/account operation packets and surface exact human KYC, tax, billing, terms, or legal gates without taking side effects.",
    },
]


DEPARTMENTS: list[dict[str, str]] = [
    {"department_id": AI_RESOURCES_DEPARTMENT, "name": "Artificial Resources", "manager_agent_id": AI_RESOURCES_MANAGER},
    {"department_id": "premium_customer_intake", "name": "Premium Customer Intake", "manager_agent_id": "premium-customer-context-router-20260621"},
    {"department_id": "ceo_control_room", "name": "CEO Control Room", "manager_agent_id": AI_RESOURCES_MANAGER},
]


def _thread_id_for(agent: dict[str, Any], args: argparse.Namespace) -> str | None:
    arg_name = agent.get("thread_arg")
    if not arg_name:
        return None
    return getattr(args, arg_name, None)


def _goal_task(agent: dict[str, Any], md_path: Path, generated_utc: str) -> dict[str, Any]:
    agent_id = agent["agent_id"]
    return {
        "task_id": f"task-{agent_id}-active-goal-20260621",
        "lane_id": AI_RESOURCES_LANE,
        "title": f"Active goal for {agent_id}",
        "status": "in_progress",
        "priority": 96 if agent_id == AI_RESOURCES_MANAGER else 90,
        "owner_agent_id": agent_id,
        "duplicate_key": f"ceo-worker-bootstrap:{agent_id}:active-goal",
        "evidence_required": str(md_path),
        "next_action": agent["goal"],
        "created_at": generated_utc,
        "updated_at": generated_utc,
        "started_at": generated_utc,
    }


def _payload(args: argparse.Namespace, json_path: Path, md_path: Path) -> dict[str, Any]:
    generated = getattr(args, "now_utc", None) or now_utc()
    agents: list[dict[str, Any]] = []
    goals: list[dict[str, Any]] = []
    for agent in AGENTS:
        item = dict(agent)
        item["thread_id"] = _thread_id_for(agent, args)
        item["status"] = "active"
        item["permissions"] = [
            "local_db_read_write",
            "local_report_write",
            "local_artifact_register",
            "no_external_side_effects_without_service_gate",
        ]
        agents.append(item)
        goals.append(_goal_task(item, md_path, generated))
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated,
        "status": "ceo_workers_bootstrapped",
        "lane_id": AI_RESOURCES_LANE,
        "departments": DEPARTMENTS,
        "roles": ROLES,
        "agents": agents,
        "goals": goals,
        "counts": {
            "agents": len(agents),
            "departments": len(DEPARTMENTS),
            "goals": len(goals),
            "roles": len(ROLES),
        },
        "operating_rules": [
            "Keep ai_resources_lab as the single AR lane; evolve existing owners before creating duplicates.",
            "New AI hires require capability-overlap evidence and a local evaluation or explicit CEO decision.",
            "Retirement is evidence-driven: park, merge, evolve, or retire with a written revisit condition.",
            "Premium customer raw materials stay in intake artifacts; CEO receives compact capsules.",
            "Continuity watchdog produces local restore/escalation packets before any worker restart or external action.",
        ],
        "next_action": "Run continuity watchdog snapshots on cadence, then route restore packets to AI Resources or CEO decision batch.",
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        "json_path": str(json_path),
        "md_path": str(md_path),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# CEO Worker Roster V1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Status: `{payload['status']}`",
        f"Lane: `{payload['lane_id']}`",
        f"JSON mirror: `{payload['json_path']}`",
        "",
        "## Operating Rules",
        "",
    ]
    for rule in payload["operating_rules"]:
        lines.append(f"- {rule}")
    lines.extend(
        [
            "",
            "## Agents",
            "",
            "| Agent | Role | Department | Thread | Active Goal |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for agent in payload["agents"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{agent['agent_id']}`",
                    f"`{agent['role_id']}`",
                    f"`{agent['department_id']}`",
                    md_cell(agent.get("thread_id") or "pending_attachment", 110),
                    md_cell(agent["goal"], 220),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Goals",
            "",
            "| Task | Owner | Priority | Next Action |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for goal in payload["goals"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{goal['task_id']}`",
                    f"`{goal['owner_agent_id']}`",
                    str(goal["priority"]),
                    md_cell(goal["next_action"], 260),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This bootstrap creates local control-plane records, reports, tasks, trace, artifacts, and outcomes only. It does not open browsers, create accounts, start runtimes, approve service requests, publish, submit, trade, spend, call APIs, or contact anyone.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _upsert_role(conn: sqlite3.Connection, role: dict[str, Any], ts: str) -> None:
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
            role["role_id"],
            role["level"],
            json.dumps(role["responsibilities"], sort_keys=True),
            json.dumps(role["must_not_do"], sort_keys=True),
            ts,
            ts,
        ),
    )


def _upsert_department(conn: sqlite3.Connection, department: dict[str, str], ts: str) -> None:
    conn.execute(
        """
        INSERT INTO departments(department_id, name, manager_agent_id, status, created_at, updated_at)
        VALUES(?, ?, ?, 'active', ?, ?)
        ON CONFLICT(department_id) DO UPDATE SET
          name=excluded.name,
          manager_agent_id=excluded.manager_agent_id,
          status=excluded.status,
          updated_at=excluded.updated_at
        """,
        (
            department["department_id"],
            department["name"],
            department["manager_agent_id"],
            ts,
            ts,
        ),
    )


def _ensure_ai_resources_lane(conn: sqlite3.Connection, ar_thread_id: str | None, ts: str) -> None:
    existing = conn.execute("SELECT lane_id FROM lanes WHERE lane_id = ?", (AI_RESOURCES_LANE,)).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE lanes
            SET department = 'Artificial Resources',
                status = 'active',
                owner_agent_id = ?,
                owner_thread_id = COALESCE(?, owner_thread_id),
                updated_at = ?
            WHERE lane_id = ?
            """,
            (AI_RESOURCES_MANAGER, ar_thread_id, ts, AI_RESOURCES_LANE),
        )
        return
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
          examples_json, promotion_gates_json, service_workers_required_json,
          side_effects_json, global_gates_json, notes, created_at, updated_at
        )
        VALUES(?, 'Artificial Resources', 'active', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            AI_RESOURCES_LANE,
            AI_RESOURCES_MANAGER,
            ar_thread_id,
            json.dumps(["ai_resources_manager", "ai_resource_evaluator", "continuity_watchdog_worker"]),
            json.dumps(["hire/evolve/retire AI agents", "route premium customer materials", "restore stale goals"]),
            json.dumps(["no-overlap evidence", "local eval artifact", "CEO decision batch when gated"]),
            json.dumps(["human_action_desk", "browser_account_ops_worker"]),
            json.dumps(["local_reports_only_without_service_request"]),
            json.dumps(["no external side effects without explicit gate"]),
            "Artificial Resources operating lane.",
            ts,
            ts,
        ),
    )


def _upsert_agent(conn: sqlite3.Connection, agent: dict[str, Any], ts: str) -> None:
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, notes, created_at, updated_at)
        VALUES(?, ?, ?, ?, 'active', ?, ?, ?, ?)
        ON CONFLICT(agent_id) DO UPDATE SET
          role_id=excluded.role_id,
          thread_id=COALESCE(excluded.thread_id, agents.thread_id),
          department_id=excluded.department_id,
          status=excluded.status,
          permissions_json=excluded.permissions_json,
          notes=excluded.notes,
          updated_at=excluded.updated_at
        """,
        (
            agent["agent_id"],
            agent["role_id"],
            agent.get("thread_id"),
            agent["department_id"],
            json.dumps(agent["permissions"], sort_keys=True),
            agent["goal"],
            ts,
            ts,
        ),
    )


def _upsert_goal(conn: sqlite3.Connection, goal: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          title=excluded.title,
          status=excluded.status,
          priority=excluded.priority,
          owner_agent_id=excluded.owner_agent_id,
          duplicate_key=excluded.duplicate_key,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          started_at=COALESCE(tasks.started_at, excluded.started_at)
        """,
        (
            goal["task_id"],
            goal["lane_id"],
            goal["title"],
            goal["status"],
            goal["priority"],
            goal["owner_agent_id"],
            goal["duplicate_key"],
            goal["evidence_required"],
            goal["next_action"],
            goal["created_at"],
            goal["updated_at"],
            goal["started_at"],
        ),
    )


def _record_run(conn: sqlite3.Connection, payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    ts = payload["generated_utc"]
    for role in payload["roles"]:
        _upsert_role(conn, role, ts)
    for department in payload["departments"]:
        _upsert_department(conn, department, ts)
    for agent in payload["agents"]:
        _upsert_agent(conn, agent, ts)
    _ensure_ai_resources_lane(conn, next((agent.get("thread_id") for agent in payload["agents"] if agent["agent_id"] == AI_RESOURCES_MANAGER), None), ts)
    for goal in payload["goals"]:
        _upsert_goal(conn, goal)
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, 'Bootstrap CEO worker constellation', 'complete', 99, ?, 'ceo-worker-roster-bootstrap:v1', ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          status=excluded.status,
          priority=excluded.priority,
          owner_agent_id=excluded.owner_agent_id,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            BOOTSTRAP_TASK_ID,
            AI_RESOURCES_LANE,
            AI_RESOURCES_MANAGER,
            str(md_path),
            payload["next_action"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    for artifact_id, kind, path, notes in [
        ("artifact-ceo-worker-roster-v1-json-20260621", "ceo_worker_roster_json", json_path, "Machine-readable CEO worker roster."),
        ("artifact-ceo-worker-roster-v1-md-20260621", "ceo_worker_roster_markdown", md_path, "Human-readable CEO worker roster."),
    ]:
        conn.execute(
            """
            INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
              lane_id=excluded.lane_id,
              task_id=excluded.task_id,
              kind=excluded.kind,
              path_or_url=excluded.path_or_url,
              sha256=excluded.sha256,
              notes=excluded.notes
            """,
            (artifact_id, AI_RESOURCES_LANE, BOOTSTRAP_TASK_ID, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "counts": payload["counts"],
        "agent_ids": [agent["agent_id"] for agent in payload["agents"]],
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, 'ceo_worker_constellation_bootstrapped', ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          trace_id=excluded.trace_id,
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          agent_id=excluded.agent_id,
          event_time=excluded.event_time,
          source=excluded.source,
          summary=excluded.summary,
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path
        """,
        (
            "trace-event-ceo-worker-bootstrap-v1-20260621",
            "trace-ceo-worker-bootstrap-v1-20260621",
            AI_RESOURCES_LANE,
            BOOTSTRAP_TASK_ID,
            AI_RESOURCES_MANAGER,
            ts,
            "ceo_worker_bootstrap_v1",
            f"Bootstrapped {payload['counts']['agents']} CEO/AR workers with active goals.",
            json.dumps(metadata, sort_keys=True),
            str(md_path),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES('outcome-ceo-worker-bootstrap-v1-20260621', ?, ?, 'ceo_worker_bootstrap', 'active', 0, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (AI_RESOURCES_LANE, BOOTSTRAP_TASK_ID, str(md_path), payload["next_action"], ts),
    )
    conn.commit()


def bootstrap_ceo_workers(conn: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    json_path = Path(getattr(args, "json_path", None) or DEFAULT_JSON)
    md_path = Path(getattr(args, "path", None) or DEFAULT_MD)
    payload = _payload(args, json_path, md_path)
    _write_json(json_path, payload)
    _write_md(md_path, payload)
    if not getattr(args, "no_db_record", False):
        _record_run(conn, payload, json_path, md_path)
    return payload


def write_ceo_worker_bootstrap(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    payload = bootstrap_ceo_workers(conn, args)
    print(
        json.dumps(
            {
                "ok": True,
                "status": payload["status"],
                "counts": payload["counts"],
                "agent_ids": [agent["agent_id"] for agent in payload["agents"]],
                "json_path": payload["json_path"],
                "md_path": payload["md_path"],
                "zero_side_effect_boundary": payload["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
