"""SQLite schema and compatibility migrations for Agent Company."""

from __future__ import annotations

import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS roles (
    role_id TEXT PRIMARY KEY,
    level TEXT NOT NULL,
    responsibilities_json TEXT NOT NULL,
    must_not_do_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS departments (
    department_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    manager_agent_id TEXT,
    status TEXT NOT NULL DEFAULT 'planned',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS agents (
    agent_id TEXT PRIMARY KEY,
    role_id TEXT NOT NULL,
    thread_id TEXT,
    department_id TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    permissions_json TEXT NOT NULL DEFAULT '[]',
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(role_id) REFERENCES roles(role_id),
    FOREIGN KEY(department_id) REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS lanes (
    lane_id TEXT PRIMARY KEY,
    department TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    owner_agent_id TEXT,
    owner_thread_id TEXT,
    agent_types_json TEXT NOT NULL,
    examples_json TEXT NOT NULL,
    promotion_gates_json TEXT NOT NULL,
    service_workers_required_json TEXT NOT NULL,
    side_effects_json TEXT NOT NULL,
    global_gates_json TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(owner_agent_id) REFERENCES agents(agent_id)
);

CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    lane_id TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    priority INTEGER NOT NULL DEFAULT 50,
    owner_agent_id TEXT,
    duplicate_key TEXT,
    evidence_required TEXT,
    next_action TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id),
    FOREIGN KEY(owner_agent_id) REFERENCES agents(agent_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_tasks_duplicate_key
ON tasks(duplicate_key)
WHERE duplicate_key IS NOT NULL AND duplicate_key != '';

CREATE INDEX IF NOT EXISTS idx_tasks_lane_created
ON tasks(lane_id, created_at);

CREATE INDEX IF NOT EXISTS idx_tasks_status_priority_created
ON tasks(status, priority, created_at);

CREATE TABLE IF NOT EXISTS service_requests (
    request_id TEXT PRIMARY KEY,
    service_id TEXT,
    request_type TEXT NOT NULL,
    lane_id TEXT,
    requester_agent_id TEXT,
    status TEXT NOT NULL DEFAULT 'needs_review',
    risk_gate TEXT NOT NULL,
    requested_action TEXT NOT NULL,
    intake_json TEXT NOT NULL DEFAULT '{}',
    approval_scope TEXT,
    artifact_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(service_id) REFERENCES service_catalog(service_id),
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id),
    FOREIGN KEY(requester_agent_id) REFERENCES agents(agent_id)
);

CREATE INDEX IF NOT EXISTS idx_service_requests_status_created
ON service_requests(status, created_at);

CREATE INDEX IF NOT EXISTS idx_service_requests_lane_status
ON service_requests(lane_id, status);

CREATE TABLE IF NOT EXISTS approvals (
    approval_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    status TEXT NOT NULL,
    approved_by TEXT NOT NULL,
    exact_scope TEXT NOT NULL,
    expires_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(request_id) REFERENCES service_requests(request_id)
);

CREATE TABLE IF NOT EXISTS artifacts (
    artifact_id TEXT PRIMARY KEY,
    lane_id TEXT,
    task_id TEXT,
    kind TEXT NOT NULL,
    path_or_url TEXT NOT NULL,
    sha256 TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id),
    FOREIGN KEY(task_id) REFERENCES tasks(task_id)
);

CREATE INDEX IF NOT EXISTS idx_artifacts_lane_created
ON artifacts(lane_id, created_at);

CREATE INDEX IF NOT EXISTS idx_artifacts_task_created
ON artifacts(task_id, created_at);

CREATE TABLE IF NOT EXISTS outcomes (
    outcome_id TEXT PRIMARY KEY,
    lane_id TEXT NOT NULL,
    task_id TEXT,
    outcome_type TEXT NOT NULL,
    status TEXT NOT NULL,
    realized_usd REAL NOT NULL DEFAULT 0,
    evidence TEXT,
    next_action TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id),
    FOREIGN KEY(task_id) REFERENCES tasks(task_id)
);

CREATE INDEX IF NOT EXISTS idx_outcomes_lane_created
ON outcomes(lane_id, created_at);

CREATE INDEX IF NOT EXISTS idx_outcomes_task_created
ON outcomes(task_id, created_at);

CREATE TABLE IF NOT EXISTS lane_evidence (
    evidence_id TEXT PRIMARY KEY,
    lane_id TEXT NOT NULL,
    source_path TEXT,
    source_url TEXT,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    summary TEXT,
    next_action TEXT,
    ownership_note TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id)
);

CREATE INDEX IF NOT EXISTS idx_lane_evidence_lane_status
ON lane_evidence(lane_id, status);

CREATE INDEX IF NOT EXISTS idx_lane_evidence_source_path
ON lane_evidence(source_path);

CREATE TABLE IF NOT EXISTS source_specs (
    spec_id TEXT PRIMARY KEY,
    lane_id TEXT NOT NULL,
    name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_paths_json TEXT NOT NULL,
    refresh_command TEXT,
    cadence TEXT NOT NULL,
    risk_gate TEXT NOT NULL,
    outputs_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id)
);

CREATE INDEX IF NOT EXISTS idx_source_specs_lane
ON source_specs(lane_id, status);

CREATE TABLE IF NOT EXISTS service_catalog (
    service_id TEXT PRIMARY KEY,
    department_id TEXT,
    name TEXT NOT NULL,
    request_type TEXT NOT NULL,
    owner_role_id TEXT NOT NULL,
    purpose TEXT NOT NULL,
    allowed_actions_json TEXT NOT NULL,
    hard_gates_json TEXT NOT NULL,
    required_intake_json TEXT NOT NULL,
    approval_required_by_json TEXT NOT NULL,
    output_artifacts_json TEXT NOT NULL,
    default_status TEXT NOT NULL DEFAULT 'available',
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(department_id) REFERENCES departments(department_id),
    FOREIGN KEY(owner_role_id) REFERENCES roles(role_id)
);

CREATE INDEX IF NOT EXISTS idx_service_catalog_type
ON service_catalog(request_type, default_status);

CREATE INDEX IF NOT EXISTS idx_service_catalog_owner
ON service_catalog(owner_role_id, default_status);

CREATE TABLE IF NOT EXISTS trace_events (
    event_id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    lane_id TEXT,
    task_id TEXT,
    agent_id TEXT,
    event_type TEXT NOT NULL,
    event_time TEXT NOT NULL,
    source TEXT,
    summary TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    artifact_path TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id),
    FOREIGN KEY(task_id) REFERENCES tasks(task_id),
    FOREIGN KEY(agent_id) REFERENCES agents(agent_id)
);

CREATE INDEX IF NOT EXISTS idx_trace_events_trace_time
ON trace_events(trace_id, event_time);

CREATE INDEX IF NOT EXISTS idx_trace_events_lane_time
ON trace_events(lane_id, event_time);

CREATE INDEX IF NOT EXISTS idx_trace_events_task_time
ON trace_events(task_id, event_time);

CREATE TABLE IF NOT EXISTS prompt_templates (
    template_id TEXT PRIMARY KEY,
    lane_id TEXT,
    name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner_agent_id TEXT,
    default_stop_gates_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id)
);

CREATE INDEX IF NOT EXISTS idx_prompt_templates_lane
ON prompt_templates(lane_id);

CREATE TABLE IF NOT EXISTS prompt_versions (
    prompt_version_id TEXT PRIMARY KEY,
    template_id TEXT NOT NULL,
    version_label TEXT NOT NULL,
    prompt_text TEXT NOT NULL,
    source_artifact_path TEXT,
    sha256 TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL,
    FOREIGN KEY(template_id) REFERENCES prompt_templates(template_id)
);

CREATE INDEX IF NOT EXISTS idx_prompt_versions_template
ON prompt_versions(template_id, status);

CREATE TABLE IF NOT EXISTS eval_datasets (
    dataset_id TEXT PRIMARY KEY,
    lane_id TEXT,
    name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    cases_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id)
);

CREATE INDEX IF NOT EXISTS idx_eval_datasets_lane
ON eval_datasets(lane_id);

CREATE TABLE IF NOT EXISTS eval_runs (
    eval_run_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    prompt_version_id TEXT,
    lane_id TEXT,
    runner_agent_id TEXT,
    runtime TEXT NOT NULL,
    status TEXT NOT NULL,
    score REAL,
    results_json TEXT NOT NULL DEFAULT '{}',
    artifact_path TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(dataset_id) REFERENCES eval_datasets(dataset_id),
    FOREIGN KEY(prompt_version_id) REFERENCES prompt_versions(prompt_version_id),
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id)
);

CREATE INDEX IF NOT EXISTS idx_eval_runs_dataset_time
ON eval_runs(dataset_id, created_at);

CREATE INDEX IF NOT EXISTS idx_eval_runs_prompt_time
ON eval_runs(prompt_version_id, created_at);

CREATE TABLE IF NOT EXISTS human_reviews (
    review_id TEXT PRIMARY KEY,
    lane_id TEXT,
    artifact_id TEXT,
    trace_id TEXT,
    prompt_version_id TEXT,
    reviewer_agent_id TEXT,
    status TEXT NOT NULL,
    decision TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(lane_id) REFERENCES lanes(lane_id),
    FOREIGN KEY(artifact_id) REFERENCES artifacts(artifact_id),
    FOREIGN KEY(prompt_version_id) REFERENCES prompt_versions(prompt_version_id)
);

CREATE INDEX IF NOT EXISTS idx_human_reviews_lane_time
ON human_reviews(lane_id, created_at);

CREATE INDEX IF NOT EXISTS idx_human_reviews_prompt_time
ON human_reviews(prompt_version_id, created_at);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    ensure_columns(conn)
    conn.commit()


def ensure_columns(conn: sqlite3.Connection) -> None:
    task_columns = {row["name"] for row in conn.execute("PRAGMA table_info(tasks)")}
    if "lease_owner_agent_id" not in task_columns:
        conn.execute("ALTER TABLE tasks ADD COLUMN lease_owner_agent_id TEXT")
    if "lease_expires_at" not in task_columns:
        conn.execute("ALTER TABLE tasks ADD COLUMN lease_expires_at TEXT")
    if "started_at" not in task_columns:
        conn.execute("ALTER TABLE tasks ADD COLUMN started_at TEXT")
    if "completed_at" not in task_columns:
        conn.execute("ALTER TABLE tasks ADD COLUMN completed_at TEXT")
    request_columns = {row["name"] for row in conn.execute("PRAGMA table_info(service_requests)")}
    if "service_id" not in request_columns:
        conn.execute("ALTER TABLE service_requests ADD COLUMN service_id TEXT")
    if "intake_json" not in request_columns:
        conn.execute("ALTER TABLE service_requests ADD COLUMN intake_json TEXT NOT NULL DEFAULT '{}'")
    if "assigned_agent_id" not in request_columns:
        conn.execute("ALTER TABLE service_requests ADD COLUMN assigned_agent_id TEXT")
    if "started_at" not in request_columns:
        conn.execute("ALTER TABLE service_requests ADD COLUMN started_at TEXT")
    if "completed_at" not in request_columns:
        conn.execute("ALTER TABLE service_requests ADD COLUMN completed_at TEXT")
    if "decision_note" not in request_columns:
        conn.execute("ALTER TABLE service_requests ADD COLUMN decision_note TEXT")
