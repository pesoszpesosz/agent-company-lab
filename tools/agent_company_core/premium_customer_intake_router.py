"""Context-safe premium customer intake router."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
from pathlib import Path
from typing import Any

from .io import now_utc
from .paths import REPORTS_DIR, ROOT
from .utils import md_cell, safe_id_fragment, sha256_file


OWNER_AGENT_ID = "premium-customer-intake-agent-20260620"
INTAKE_ROOT = ROOT / "intake" / "customer"
DROPBOX_DIR = INTAKE_ROOT / "dropbox"
ROUTES_DIR = INTAKE_ROOT / "routes"
PROCESSED_DIR = INTAKE_ROOT / "processed"
LEDGER_JSON = REPORTS_DIR / "customer-request-routing-ledger-v1-20260620.json"
LEDGER_MD = REPORTS_DIR / "customer-request-routing-ledger-v1-20260620.md"
UPDATE_FEED_JSON = REPORTS_DIR / "customer-update-feed-v3-20260620.json"
UPDATE_FEED_MD = REPORTS_DIR / "customer-update-feed-v3-20260620.md"
SCHEMA_VERSION = "customer_input_route_packet.v2"

ZERO_SIDE_EFFECT_BOUNDARY = {
    "browser_sessions_started": 0,
    "accounts_created_or_modified": 0,
    "public_actions_taken": 0,
    "wallet_payment_trading_actions": 0,
    "model_api_mcp_calls": 0,
    "worker_runtime_queue_starts": 0,
    "service_requests_approved_assigned_or_started": 0,
    "external_side_effects": False,
}

LANE_PATTERNS: list[tuple[str, tuple[str, ...], str]] = [
    (
        "youtube_content_channels",
        ("youtube", "youtu.be", "video", "channel", "thumbnail", "shorts", "script", "storyboard"),
        "Matches YouTube/content-channel material or production work.",
    ),
    (
        "paid_code_bounties",
        ("github", "pull request", "pr ", "bounty", "algora", "code task", "issue", "repo"),
        "Matches paid coding bounty, GitHub, repo, or PR work.",
    ),
    (
        "prediction_market_research",
        ("prediction market", "predictive market", "kalshi", "polymarket", "manifold", "market odds"),
        "Matches prediction-market research or settlement work.",
    ),
    (
        "ai_ml_competitions",
        ("kaggle", "competition", "benchmark", "arc-prize", "arc agi", "prize"),
        "Matches AI/ML competition or benchmark opportunities.",
    ),
    (
        "ai_resources_lab",
        ("agent", "ai resource", "framework", "multi-agent", "worker", "infrastructure", "tooling"),
        "Matches AI Resources evaluation or worker-capability infrastructure.",
    ),
    (
        "digital_products_templates_plugins",
        ("template", "plugin", "digital product", "gumroad", "notion pack", "asset pack"),
        "Matches product-studio packaging or sellable digital asset work.",
    ),
    (
        "content_and_social_growth",
        ("x/twitter", "twitter", "social", "post", "audience", "creator", "growth"),
        "Matches audience, social growth, or distribution work.",
    ),
    (
        "money_source_discovery",
        ("money", "profitable", "opportunity", "lead", "revenue", "cashflow", "strategy"),
        "Matches broad money-source discovery when no narrower lane owns it.",
    ),
]

SURFACE_PATTERNS: list[tuple[str, tuple[str, ...], str]] = [
    (
        "human_action_desk",
        ("kyc", "tax", "billing", "login", "manual", "approval", "account creation", "i will make", "human"),
        "Requires or describes rare human-only action.",
    ),
    (
        "goal_evolver_review",
        ("goal", "ceo", "company brain", "evolve", "strategy", "whole personality"),
        "May affect the CEO operating goal or goal-evolver queue.",
    ),
    (
        "ceo_state_packet",
        ("priority", "newest request", "status", "update me", "head of the company", "context"),
        "CEO should receive only the compact context capsule.",
    ),
]

CLASS_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("status_request", ("status", "what happened", "update me", "latest update")),
    ("human_capability_update", ("i made", "i created", "i can make", "i will make", "manual", "kyc")),
    ("correction", ("correction", "actually", "wrong", "instead", "update that")),
    ("constraint_or_preference", ("do not", "don't", "avoid", "must", "never", "prefer", "important")),
    ("opportunity_lead", ("opportunity", "lead", "bounty", "market", "competition", "profitable")),
    ("new_request", ("i want", "please", "add", "build", "create", "make", "need", "your task")),
]


def _getattr(args: argparse.Namespace, name: str, default: Any = None) -> Any:
    return getattr(args, name, default)


def _compact(value: str, limit: int = 420) -> str:
    cleaned = " ".join(value.replace("\r", "\n").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit].rstrip() + "..."


def _summary_from_input(value: str, limit: int = 360) -> str:
    lines = [line.strip() for line in value.replace("\r", "\n").split("\n") if line.strip()]
    if lines:
        return _compact(" ".join(lines[:2]), limit)
    return _compact(value, limit)


def _read_limited(path: Path, limit: int = 200_000) -> str:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return handle.read(limit)


def _source_text(args: argparse.Namespace) -> tuple[str, Path | None]:
    if _getattr(args, "text_file"):
        path = Path(args.text_file)
        return _read_limited(path), path
    if _getattr(args, "input_path"):
        path = Path(args.input_path)
        return _read_limited(path), path
    if _getattr(args, "text"):
        return str(args.text), None
    raise SystemExit("route-premium-customer-input requires --input-path, --text-file, or --text.")


def _extract_urls(text: str) -> list[str]:
    urls = re.findall(r"https?://[^\s)>\"]+", text)
    return [url.rstrip(".,;]") for url in urls]


def _derive_input_id(text: str, source_path: Path | None, title: str | None, received_utc: str) -> str:
    if title:
        basis = title
    elif source_path:
        basis = source_path.stem
    else:
        basis = _compact(text, 80)
    day = received_utc[:10].replace("-", "")
    digest = hashlib.sha1(f"{basis}|{text}".encode("utf-8", errors="replace")).hexdigest()[:10]
    return f"customer-input-{safe_id_fragment(basis, 54)}-{day}-{digest}"


def _preserve_raw_input(
    text: str,
    source_path: Path | None,
    input_id: str,
    dropbox_dir: Path,
    overwrite: bool,
) -> dict[str, Any]:
    dropbox_dir.mkdir(parents=True, exist_ok=True)
    if source_path:
        suffix = source_path.suffix or ".txt"
        preserved_path = dropbox_dir / f"{input_id}{suffix}"
        same_file = False
        try:
            same_file = source_path.resolve() == preserved_path.resolve()
        except FileNotFoundError:
            same_file = False
        if not same_file:
            if preserved_path.exists() and not overwrite:
                raise SystemExit(f"Preserved raw input already exists: {preserved_path}. Use --overwrite.")
            shutil.copyfile(source_path, preserved_path)
    else:
        preserved_path = dropbox_dir / f"{input_id}.md"
        if preserved_path.exists() and not overwrite:
            raise SystemExit(f"Preserved raw input already exists: {preserved_path}. Use --overwrite.")
        preserved_path.write_text(text, encoding="utf-8")
    return {
        "source_path": str(source_path) if source_path else None,
        "preserved_raw_path": str(preserved_path),
        "sha256": sha256_file(preserved_path),
        "bytes": preserved_path.stat().st_size,
    }


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    haystack = text.lower()
    return any(needle in haystack for needle in needles)


def _classify(text: str, urls: list[str], source_path: Path | None) -> tuple[str, list[str]]:
    lowered = text.lower()
    secondary: list[str] = []
    primary = "lane_material" if urls or source_path else "new_request"
    for class_name, needles in CLASS_PATTERNS:
        if _contains_any(lowered, needles):
            if primary == "lane_material" and class_name in {"new_request", "constraint_or_preference"}:
                secondary.append(class_name)
            elif primary == "new_request" and class_name == "constraint_or_preference":
                secondary.append(class_name)
            elif primary == "lane_material" and class_name == "opportunity_lead":
                secondary.append(class_name)
            else:
                primary = class_name
    if primary == "new_request" and urls:
        secondary.append("lane_material")
    return primary, sorted(set(secondary))


def _route_matches(text: str, urls: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    searchable = f"{text}\n{' '.join(urls)}".lower()
    target_lanes: list[str] = []
    routes: list[dict[str, str]] = [
        {
            "lane_or_surface": "premium_customer_intake",
            "reason": "Owns customer input capture, routing, compact updates, and raw-context separation.",
            "status": "applied",
        }
    ]
    for lane_id, needles, reason in LANE_PATTERNS:
        if _contains_any(searchable, needles):
            if lane_id not in target_lanes:
                target_lanes.append(lane_id)
                routes.append({"lane_or_surface": lane_id, "reason": reason, "status": "routed"})
    for surface, needles, reason in SURFACE_PATTERNS:
        if _contains_any(searchable, needles):
            routes.append({"lane_or_surface": surface, "reason": reason, "status": "referenced"})
    if not target_lanes:
        target_lanes.append("money_source_discovery")
        routes.append(
            {
                "lane_or_surface": "money_source_discovery",
                "reason": "Fallback lane for broad or ambiguous money-making inputs with a concrete revisit condition.",
                "status": "parked_with_revisit_condition",
            }
        )
    if "ceo_state_packet" not in {route["lane_or_surface"] for route in routes}:
        routes.append(
            {
                "lane_or_surface": "ceo_state_packet",
                "reason": "CEO receives compact routing state only, not raw customer material.",
                "status": "referenced",
            }
        )
    return routes, target_lanes


def _context_check(conn: sqlite3.Connection | None, target_lanes: list[str]) -> dict[str, Any]:
    if conn is None:
        return {"status": "not_recorded", "target_lanes": target_lanes}
    context: dict[str, Any] = {"checked_utc": now_utc(), "target_lanes": []}
    for table in ("lanes", "tasks", "artifacts", "outcomes", "trace_events", "service_requests"):
        try:
            context[f"{table}_total"] = int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        except sqlite3.Error:
            context[f"{table}_total"] = None
    for lane_id in target_lanes:
        lane = conn.execute(
            "SELECT lane_id, status, owner_agent_id, department FROM lanes WHERE lane_id = ?",
            (lane_id,),
        ).fetchone()
        status_counts = [
            dict(row)
            for row in conn.execute(
                """
                SELECT status, COUNT(*) AS count
                FROM tasks
                WHERE lane_id = ?
                GROUP BY status
                ORDER BY status
                """,
                (lane_id,),
            )
        ]
        recent_open = [
            dict(row)
            for row in conn.execute(
                """
                SELECT task_id, status, priority, next_action
                FROM tasks
                WHERE lane_id = ? AND status != 'complete'
                ORDER BY priority DESC, created_at DESC
                LIMIT 5
                """,
                (lane_id,),
            )
        ]
        context["target_lanes"].append(
            {
                "lane_id": lane_id,
                "known": bool(lane),
                "lane": dict(lane) if lane else None,
                "task_status_counts": status_counts,
                "recent_open_tasks": recent_open,
            }
        )
    service_statuses = [
        dict(row)
        for row in conn.execute(
            "SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status ORDER BY status"
        )
    ]
    context["service_request_status_counts"] = service_statuses
    return context


def _primary_route(routes: list[dict[str, str]]) -> str:
    route_names = {route["lane_or_surface"] for route in routes}
    routed_names = [route["lane_or_surface"] for route in routes if route["status"] == "routed"]
    if "goal_evolver_review" in route_names and "ai_resources_lab" in routed_names:
        return "ai_resources_lab"
    if "premium_customer_intake" in route_names and "ceo_state_packet" in route_names and "ai_resources_lab" in routed_names:
        return "ai_resources_lab"
    for route in routes:
        if route["lane_or_surface"] != "premium_customer_intake" and route["status"] == "routed":
            return route["lane_or_surface"]
    return "premium_customer_intake"


def _packet_paths(input_id: str, routes_dir: Path) -> tuple[Path, Path]:
    routes_dir.mkdir(parents=True, exist_ok=True)
    return routes_dir / f"{input_id}.json", routes_dir / f"{input_id}.md"


def _build_packet(
    text: str,
    args: argparse.Namespace,
    raw_input: dict[str, Any],
    conn: sqlite3.Connection | None,
) -> dict[str, Any]:
    received_utc = _getattr(args, "received_utc") or now_utc()
    source_path = Path(args.text_file or args.input_path) if (_getattr(args, "text_file") or _getattr(args, "input_path")) else None
    input_id = _getattr(args, "input_id") or _derive_input_id(text, source_path, _getattr(args, "title"), received_utc)
    urls = _extract_urls(text)
    input_class, secondary_classes = _classify(text, urls, source_path)
    routes, target_lanes = _route_matches(text, urls)
    context = _context_check(conn, target_lanes)
    primary = _primary_route(routes)
    human_action_needed = any(route["lane_or_surface"] == "human_action_desk" for route in routes)
    ceo_attention_needed = input_class in {"new_request", "constraint_or_preference", "correction", "status_request"} or any(
        route["lane_or_surface"] in {"goal_evolver_review", "ceo_state_packet"} for route in routes
    )
    summary = _summary_from_input(text, 360)
    packet = {
        "schema_version": SCHEMA_VERSION,
        "input_id": input_id,
        "received_utc": received_utc,
        "status": "routed",
        "owner_agent_id": _getattr(args, "owner_agent_id") or OWNER_AGENT_ID,
        "customer_intent": summary,
        "input_class": input_class,
        "secondary_classes": secondary_classes,
        "target_lane_ids": target_lanes,
        "urls": urls,
        "raw_material_paths": {
            "source_path": raw_input["source_path"],
            "preserved_raw_path": raw_input["preserved_raw_path"],
            "sha256": raw_input["sha256"],
            "bytes": raw_input["bytes"],
        },
        "routes": routes,
        "company_context_check": context,
        "ceo_context_capsule": {
            "short_summary": summary,
            "why_this_route": f"Primary route `{primary}` selected from deterministic local lane/surface matching plus current DB context.",
            "application_path": "raw_input_preserved_compact_capsule_route_packet_ledger_customer_update_db_trace",
            "status": "routed",
            "next_artifact": f"route packet `{input_id}` and lane-specific follow-up by `{primary}`",
            "human_action_needed": human_action_needed,
            "ceo_attention_needed": ceo_attention_needed,
        },
        "knowledge_application": {
            "rule": "Useful knowledge must be routed, applied, blocked by a named gate, or parked with a revisit condition.",
            "current_application": "routed_to_lane_packet_and_customer_ledger",
            "revisit_condition": "If target lane has no owner or no follow-up artifact after next CEO packet, escalate to AI Resources or CEO decision batch.",
        },
        "next_artifact": f"{primary}_followup_packet_or_task",
        "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
    }
    return packet


def _write_packet_json(path: Path, packet: dict[str, Any]) -> None:
    path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")


def _write_packet_md(path: Path, packet: dict[str, Any]) -> None:
    lines = [
        "# Customer Input Route Packet",
        "",
        f"Input id: `{packet['input_id']}`",
        f"Received UTC: {packet['received_utc']}",
        f"Status: `{packet['status']}`",
        f"Owner: `{packet['owner_agent_id']}`",
        "",
        "## Customer Intent",
        "",
        packet["customer_intent"],
        "",
        "## Input Class",
        "",
        f"`{packet['input_class']}`",
    ]
    if packet["secondary_classes"]:
        lines.extend(["", "Secondary classes:", ""])
        for item in packet["secondary_classes"]:
            lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Routes",
            "",
            "| Route | Reason | Status |",
            "| --- | --- | --- |",
        ]
    )
    for route in packet["routes"]:
        lines.append(
            f"| `{route['lane_or_surface']}` | {md_cell(route['reason'], 180)} | {md_cell(route['status'], 80)} |"
        )
    lines.extend(
        [
            "",
            "## Raw Material",
            "",
            f"- Preserved raw path: `{packet['raw_material_paths']['preserved_raw_path']}`",
            f"- SHA256: `{packet['raw_material_paths']['sha256']}`",
            f"- Bytes: `{packet['raw_material_paths']['bytes']}`",
            "",
            "## CEO Context Capsule",
            "",
            packet["ceo_context_capsule"]["short_summary"],
            "",
            "## Application Path",
            "",
            f"`{packet['ceo_context_capsule']['application_path']}`",
            "",
            "## Human Action Needed",
            "",
            "Yes." if packet["ceo_context_capsule"]["human_action_needed"] else "None.",
            "",
            "## Next Artifact",
            "",
            f"`{packet['next_artifact']}`",
            "",
            "## Boundary",
            "",
            "No browser, account, public, payment, wallet, trading, model/API/MCP, worker start, runtime start, queue start, or service-request approval occurred.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _load_json_or_default(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _update_ledger(packet: dict[str, Any], route_md_path: Path, ledger_json: Path, ledger_md: Path) -> None:
    ledger_json.parent.mkdir(parents=True, exist_ok=True)
    now = now_utc()
    ledger = _load_json_or_default(
        ledger_json,
        {
            "schema_version": "customer_request_routing_ledger.v1",
            "generated_utc": now,
            "owner_agent_id": OWNER_AGENT_ID,
            "status": "active_local_ledger",
            "ledger_rule": "Every customer input should become routed, synthesized, applied, parked with a revisit condition, blocked by an explicit gate, or rejected with a safer alternative when rejection is truly necessary.",
            "entries": [],
            "zero_side_effect_boundary": ZERO_SIDE_EFFECT_BOUNDARY,
        },
    )
    entry = {
        "input_id": packet["input_id"],
        "input_class": packet["input_class"],
        "primary_route": _primary_route(packet["routes"]),
        "secondary_routes": [
            route["lane_or_surface"]
            for route in packet["routes"]
            if route["lane_or_surface"] not in {"premium_customer_intake", _primary_route(packet["routes"])}
        ],
        "status": packet["status"],
        "route_packet_path": str(route_md_path),
        "raw_material_path": packet["raw_material_paths"]["preserved_raw_path"],
        "next_artifact": packet["next_artifact"],
    }
    entries = [item for item in ledger.get("entries", []) if item.get("input_id") != packet["input_id"]]
    ledger["entries"] = [entry] + entries
    ledger["generated_utc"] = now
    ledger["zero_side_effect_boundary"] = ZERO_SIDE_EFFECT_BOUNDARY
    ledger_json.write_text(json.dumps(ledger, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Customer Request Routing Ledger V1",
        "",
        f"Generated UTC: {ledger['generated_utc']}",
        f"Owner: `{ledger['owner_agent_id']}`",
        f"Status: {ledger['status']}",
        f"JSON mirror: `{ledger_json}`",
        "",
        "## Ledger Rule",
        "",
        ledger["ledger_rule"],
        "",
        "## Entries",
        "",
        "| Input | Class | Primary Route | Status | Next Artifact |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in ledger["entries"]:
        lines.append(
            f"| `{item['input_id']}` | `{item['input_class']}` | `{item['primary_route']}` | {md_cell(item['status'], 80)} | `{item['next_artifact']}` |"
        )
    lines.extend(
        [
            "",
            "## Current Route Packet",
            "",
            f"`{route_md_path}`",
            "",
            "## Boundary",
            "",
            "This ledger is local routing memory only. It does not approve gates, start workers, open browsers, create accounts, publish, upload, trade, spend, call APIs, or perform external actions.",
            "",
        ]
    )
    ledger_md.write_text("\n".join(lines), encoding="utf-8")


def _load_prior_update_feed() -> dict[str, Any]:
    if UPDATE_FEED_JSON.exists():
        return _load_json_or_default(UPDATE_FEED_JSON, {})
    prior = REPORTS_DIR / "customer-update-feed-v2-20260620.json"
    if prior.exists():
        data = _load_json_or_default(prior, {})
        data["schema_version"] = "customer_update_feed.v3"
        return data
    return {}


def _update_customer_feed(packet: dict[str, Any], route_md_path: Path, feed_json: Path, feed_md: Path) -> None:
    now = now_utc()
    feed = _load_prior_update_feed()
    if not feed:
        feed = {
            "schema_version": "customer_update_feed.v3",
            "generated_utc": now,
            "owner_agent_id": OWNER_AGENT_ID,
            "status": "active_local_update_feed",
            "updates": [],
            "zero_side_effect_boundary": {"external_side_effects": False},
        }
    update = {
        "update_id": f"customer-update-{packet['input_id']}",
        "generated_utc": now,
        "summary": f"Customer input `{packet['input_id']}` routed to `{_primary_route(packet['routes'])}`.",
        "applied": [
            "raw_input_preserved",
            "compact_route_packet_written",
            "routing_ledger_updated",
            "customer_update_feed_updated",
        ],
        "route_packet_path": str(route_md_path),
        "human_action_needed": packet["ceo_context_capsule"]["human_action_needed"],
        "next": packet["next_artifact"],
    }
    updates = [item for item in feed.get("updates", []) if item.get("update_id") != update["update_id"]]
    feed["updates"] = [update] + updates
    feed["schema_version"] = "customer_update_feed.v3"
    feed["generated_utc"] = now
    feed["owner_agent_id"] = OWNER_AGENT_ID
    feed["status"] = "active_local_update_feed"
    feed["zero_side_effect_boundary"] = {"external_side_effects": False}
    feed_json.parent.mkdir(parents=True, exist_ok=True)
    feed_json.write_text(json.dumps(feed, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Customer Update Feed V3",
        "",
        f"Generated UTC: {feed['generated_utc']}",
        f"Owner: `{feed['owner_agent_id']}`",
        f"Status: {feed['status']}",
        f"JSON mirror: `{feed_json}`",
        "",
        "## Updates",
        "",
    ]
    for item in feed["updates"]:
        lines.extend(
            [
                f"### {item['generated_utc']} - {item['summary']}",
                "",
                f"Route packet: `{item.get('route_packet_path', '')}`",
                "",
                f"Human action needed: {'yes' if item.get('human_action_needed') else 'none'}.",
                "",
                f"Next: {item.get('next', '')}",
                "",
            ]
        )
    feed_md.write_text("\n".join(lines), encoding="utf-8")


def _record_db(conn: sqlite3.Connection, packet: dict[str, Any], paths: dict[str, Path]) -> None:
    ts = now_utc()
    input_id = packet["input_id"]
    task_id = f"task-{input_id}"
    lane_id = "premium_customer_intake"
    owner = packet["owner_agent_id"]
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, started_at, completed_at
        )
        VALUES(?, ?, ?, 'complete', ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(task_id) DO UPDATE SET
          title=excluded.title,
          status=excluded.status,
          priority=excluded.priority,
          owner_agent_id=excluded.owner_agent_id,
          duplicate_key=excluded.duplicate_key,
          evidence_required=excluded.evidence_required,
          next_action=excluded.next_action,
          updated_at=excluded.updated_at,
          completed_at=excluded.completed_at
        """,
        (
            task_id,
            lane_id,
            f"Route premium customer input {input_id}",
            88,
            owner,
            input_id,
            str(paths["route_md"]),
            packet["next_artifact"],
            ts,
            ts,
            ts,
            ts,
        ),
    )
    artifacts = [
        (f"artifact-{input_id}-route-json", "customer_input_route_packet_json", paths["route_json"], "Machine-readable customer route packet."),
        (f"artifact-{input_id}-route-md", "customer_input_route_packet", paths["route_md"], "Human-readable compact customer route packet."),
        (f"artifact-{input_id}-raw", "customer_input_raw_material", Path(packet["raw_material_paths"]["preserved_raw_path"]), "Preserved raw customer input outside CEO context."),
        (f"artifact-{input_id}-routing-ledger", "customer_routing_ledger", paths["ledger_json"], "Updated customer request routing ledger."),
        (f"artifact-{input_id}-customer-update-feed", "customer_update_feed", paths["update_feed_json"], "Updated premium customer update feed."),
    ]
    for artifact_id, kind, path, notes in artifacts:
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
            (artifact_id, lane_id, task_id, kind, str(path), sha256_file(path), notes, ts),
        )
    metadata = {
        "input_id": input_id,
        "input_class": packet["input_class"],
        "target_lane_ids": packet["target_lane_ids"],
        "routes": packet["routes"],
        "zero_side_effect_boundary": packet["zero_side_effect_boundary"],
        "route_packet_path": str(paths["route_md"]),
    }
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          trace_id=excluded.trace_id,
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          agent_id=excluded.agent_id,
          event_type=excluded.event_type,
          event_time=excluded.event_time,
          source=excluded.source,
          summary=excluded.summary,
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path
        """,
        (
            f"trace-event-{input_id}",
            f"trace-{input_id}",
            lane_id,
            task_id,
            owner,
            "premium_customer_input_routed",
            ts,
            "premium_customer_intake_router_v1",
            f"Routed premium customer input {input_id} to {_primary_route(packet['routes'])}.",
            json.dumps(metadata, sort_keys=True),
            str(paths["route_md"]),
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(outcome_id) DO UPDATE SET
          status=excluded.status,
          realized_usd=excluded.realized_usd,
          evidence=excluded.evidence,
          next_action=excluded.next_action
        """,
        (
            f"outcome-{input_id}",
            lane_id,
            task_id,
            "customer_input_routing",
            "routed",
            0.0,
            str(paths["route_md"]),
            packet["next_artifact"],
            ts,
        ),
    )
    conn.commit()


def route_premium_customer_input(conn: sqlite3.Connection | None, args: argparse.Namespace) -> dict[str, Any]:
    text, source_path = _source_text(args)
    received_utc = _getattr(args, "received_utc") or now_utc()
    input_id = _getattr(args, "input_id") or _derive_input_id(text, source_path, _getattr(args, "title"), received_utc)
    dropbox_dir = Path(_getattr(args, "dropbox_dir") or DROPBOX_DIR)
    routes_dir = Path(_getattr(args, "routes_dir") or ROUTES_DIR)
    ledger_json = Path(_getattr(args, "ledger_json") or LEDGER_JSON)
    ledger_md = Path(_getattr(args, "ledger_md") or LEDGER_MD)
    update_feed_json = Path(_getattr(args, "update_feed_json") or UPDATE_FEED_JSON)
    update_feed_md = Path(_getattr(args, "update_feed_md") or UPDATE_FEED_MD)
    raw_input = _preserve_raw_input(text, source_path, input_id, dropbox_dir, bool(_getattr(args, "overwrite", False)))
    args.input_id = input_id
    args.received_utc = received_utc
    packet = _build_packet(text, args, raw_input, conn)
    route_json, route_md = _packet_paths(input_id, routes_dir)
    if (route_json.exists() or route_md.exists()) and not _getattr(args, "overwrite", False):
        raise SystemExit(f"Route packet already exists for {input_id}. Use --overwrite.")
    _write_packet_json(route_json, packet)
    _write_packet_md(route_md, packet)
    _update_ledger(packet, route_md, ledger_json, ledger_md)
    _update_customer_feed(packet, route_md, update_feed_json, update_feed_md)
    paths = {
        "route_json": route_json,
        "route_md": route_md,
        "ledger_json": ledger_json,
        "ledger_md": ledger_md,
        "update_feed_json": update_feed_json,
        "update_feed_md": update_feed_md,
    }
    if not _getattr(args, "no_db_record", False) and conn is not None:
        _record_db(conn, packet, paths)
    return {
        "packet": packet,
        "route_json": str(route_json),
        "route_md": str(route_md),
        "preserved_raw_path": raw_input["preserved_raw_path"],
        "ledger_json": str(ledger_json),
        "update_feed_json": str(update_feed_json),
    }


def write_premium_customer_input_route(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    result = route_premium_customer_input(conn, args)
    packet = result["packet"]
    print(
        json.dumps(
            {
                "ok": True,
                "input_id": packet["input_id"],
                "input_class": packet["input_class"],
                "target_lane_ids": packet["target_lane_ids"],
                "route_json": result["route_json"],
                "route_md": result["route_md"],
                "preserved_raw_path": result["preserved_raw_path"],
                "ledger_json": result["ledger_json"],
                "update_feed_json": result["update_feed_json"],
                "zero_side_effect_boundary": packet["zero_side_effect_boundary"],
            },
            indent=2,
        )
    )
