# Agent Company Report-Only Migration Draft

Generated UTC: 2026-06-16T11:27:18Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-report-only-migration-draft-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-report-only-migration-draft-validation-latest.json`

## Decision

`agent_company_report_only_migration_draft_ready_for_apply_preflight_packet`

Drafted a report-only migration packet from the department schema plan, including SQL text, validation queries, rollback SQL, and apply gates without executing migration SQL.

## Migration Inventory

- Tables: 10
- CREATE TABLE statements: 10
- CREATE INDEX statements: 20
- Validation queries: 10
- Rollback statements: 30

## Apply Gates

- `operator_approval_required_before_sql_execution`
- `backup_agent_company_sqlite_before_apply`
- `run_migration_against_throwaway_copy_first`
- `confirm_no_service_request_state_mutation`
- `confirm_no_worker_threads_started`
- `confirm_no_browser_account_wallet_payment_public_or_security_actions`
- `record_post_apply_integrity_report_before_next_layer`

## SQL Draft

### `agent_threads`

```sql
CREATE TABLE IF NOT EXISTS agent_threads (
  thread_id TEXT PRIMARY KEY NOT NULL,
  department_id TEXT,
  lane_id TEXT,
  role_id TEXT,
  owner_agent_id TEXT,
  state TEXT,
  current_task_id TEXT,
  service_request_id TEXT,
  handoff_status TEXT,
  last_report_path TEXT,
  created_at TEXT,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_agent_threads_department_state ON agent_threads (department_id, state);
CREATE INDEX IF NOT EXISTS idx_agent_threads_owner_state ON agent_threads (owner_agent_id, state);
SELECT COUNT(*) AS row_count FROM agent_threads;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_agent_threads_department_state;
DROP INDEX IF EXISTS idx_agent_threads_owner_state;
DROP TABLE IF EXISTS agent_threads;
```

### `departments`

```sql
CREATE TABLE IF NOT EXISTS departments (
  department_id TEXT PRIMARY KEY NOT NULL,
  manager_role_id TEXT,
  purpose TEXT,
  status TEXT,
  default_lane_id TEXT,
  approval_policy_id TEXT,
  queue_limit INTEGER,
  created_at TEXT,
  updated_at TEXT,
  last_reviewed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_departments_status_manager ON departments (status, manager_role_id);
CREATE INDEX IF NOT EXISTS idx_departments_default_lane ON departments (default_lane_id);
SELECT COUNT(*) AS row_count FROM departments;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_departments_status_manager;
DROP INDEX IF EXISTS idx_departments_default_lane;
DROP TABLE IF EXISTS departments;
```

### `money_paths`

```sql
CREATE TABLE IF NOT EXISTS money_paths (
  money_path_id TEXT PRIMARY KEY NOT NULL,
  department_id TEXT,
  name TEXT,
  category TEXT,
  payout_model REAL,
  expected_value_score REAL,
  legality_status TEXT,
  capital_required REAL,
  proofability_score REAL,
  gate_level TEXT,
  status TEXT,
  created_at TEXT,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_money_paths_department_status ON money_paths (department_id, status);
CREATE INDEX IF NOT EXISTS idx_money_paths_category_score ON money_paths (category, expected_value_score);
SELECT COUNT(*) AS row_count FROM money_paths;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_money_paths_department_status;
DROP INDEX IF EXISTS idx_money_paths_category_score;
DROP TABLE IF EXISTS money_paths;
```

### `opportunity_leads`

```sql
CREATE TABLE IF NOT EXISTS opportunity_leads (
  lead_id TEXT PRIMARY KEY NOT NULL,
  money_path_id TEXT,
  source_url TEXT,
  source_name TEXT,
  payout_min REAL,
  payout_max REAL,
  currency TEXT,
  account_required INTEGER,
  risk_score REAL,
  competition_score REAL,
  proof_artifact_path TEXT,
  next_action TEXT,
  status TEXT,
  created_at TEXT,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_opportunity_leads_money_path_status ON opportunity_leads (money_path_id, status);
CREATE INDEX IF NOT EXISTS idx_opportunity_leads_risk_payout ON opportunity_leads (risk_score, payout_max);
SELECT COUNT(*) AS row_count FROM opportunity_leads;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_opportunity_leads_money_path_status;
DROP INDEX IF EXISTS idx_opportunity_leads_risk_payout;
DROP TABLE IF EXISTS opportunity_leads;
```

### `worker_pool_interfaces`

```sql
CREATE TABLE IF NOT EXISTS worker_pool_interfaces (
  pool_id TEXT PRIMARY KEY NOT NULL,
  department_id TEXT,
  worker_role_id TEXT,
  allowed_actions TEXT,
  forbidden_actions TEXT,
  input_schema TEXT,
  output_schema TEXT,
  approval_required INTEGER,
  max_parallel_threads INTEGER,
  status TEXT,
  created_at TEXT,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_worker_pool_interfaces_department_status ON worker_pool_interfaces (department_id, status);
CREATE INDEX IF NOT EXISTS idx_worker_pool_interfaces_approval_status ON worker_pool_interfaces (approval_required, status);
SELECT COUNT(*) AS row_count FROM worker_pool_interfaces;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_worker_pool_interfaces_department_status;
DROP INDEX IF EXISTS idx_worker_pool_interfaces_approval_status;
DROP TABLE IF EXISTS worker_pool_interfaces;
```

### `approval_gates`

```sql
CREATE TABLE IF NOT EXISTS approval_gates (
  gate_id TEXT PRIMARY KEY NOT NULL,
  gate_type TEXT,
  department_id TEXT,
  requested_by_thread_id TEXT,
  service_request_id TEXT,
  scope TEXT,
  risk_summary TEXT,
  approval_state TEXT,
  approved_by TEXT,
  expires_at TEXT,
  rollback_plan TEXT,
  decision_note TEXT,
  created_at TEXT,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_approval_gates_state_type ON approval_gates (approval_state, gate_type);
CREATE INDEX IF NOT EXISTS idx_approval_gates_service_request_state ON approval_gates (service_request_id, approval_state);
SELECT COUNT(*) AS row_count FROM approval_gates;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_approval_gates_state_type;
DROP INDEX IF EXISTS idx_approval_gates_service_request_state;
DROP TABLE IF EXISTS approval_gates;
```

### `evidence_packets`

```sql
CREATE TABLE IF NOT EXISTS evidence_packets (
  packet_id TEXT PRIMARY KEY NOT NULL,
  lane_id TEXT,
  department_id TEXT,
  source_task_id TEXT,
  source_path TEXT,
  source_url TEXT,
  confidence TEXT,
  status TEXT,
  summary TEXT,
  next_action TEXT,
  reviewer_note TEXT,
  created_at TEXT,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_evidence_packets_department_status ON evidence_packets (department_id, status);
CREATE INDEX IF NOT EXISTS idx_evidence_packets_source_task ON evidence_packets (source_task_id);
SELECT COUNT(*) AS row_count FROM evidence_packets;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_evidence_packets_department_status;
DROP INDEX IF EXISTS idx_evidence_packets_source_task;
DROP TABLE IF EXISTS evidence_packets;
```

### `task_handoffs`

```sql
CREATE TABLE IF NOT EXISTS task_handoffs (
  handoff_id TEXT PRIMARY KEY NOT NULL,
  from_thread_id TEXT,
  to_thread_id TEXT,
  task_id TEXT,
  service_request_id TEXT,
  handoff_type TEXT,
  payload_path TEXT,
  status TEXT,
  response_path TEXT,
  created_at TEXT,
  updated_at TEXT,
  completed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_task_handoffs_to_thread_status ON task_handoffs (to_thread_id, status);
CREATE INDEX IF NOT EXISTS idx_task_handoffs_task_status ON task_handoffs (task_id, status);
SELECT COUNT(*) AS row_count FROM task_handoffs;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_task_handoffs_to_thread_status;
DROP INDEX IF EXISTS idx_task_handoffs_task_status;
DROP TABLE IF EXISTS task_handoffs;
```

### `experiment_runs`

```sql
CREATE TABLE IF NOT EXISTS experiment_runs (
  run_id TEXT PRIMARY KEY NOT NULL,
  money_path_id TEXT,
  department_id TEXT,
  experiment_type TEXT,
  hypothesis TEXT,
  input_path TEXT,
  output_path TEXT,
  metric_json TEXT,
  result_state TEXT,
  kill_reason TEXT,
  started_at TEXT,
  completed_at TEXT,
  created_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_experiment_runs_money_path_result ON experiment_runs (money_path_id, result_state);
CREATE INDEX IF NOT EXISTS idx_experiment_runs_department_started ON experiment_runs (department_id, started_at);
SELECT COUNT(*) AS row_count FROM experiment_runs;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_experiment_runs_money_path_result;
DROP INDEX IF EXISTS idx_experiment_runs_department_started;
DROP TABLE IF EXISTS experiment_runs;
```

### `roi_ledger`

```sql
CREATE TABLE IF NOT EXISTS roi_ledger (
  roi_entry_id TEXT PRIMARY KEY NOT NULL,
  money_path_id TEXT,
  lead_id TEXT,
  task_id TEXT,
  expected_value_usd REAL,
  realized_value_usd REAL,
  cost_usd REAL,
  minutes_spent INTEGER,
  payout_probability REAL,
  status TEXT,
  decision_reason TEXT,
  created_at TEXT,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_roi_ledger_money_path_status ON roi_ledger (money_path_id, status);
CREATE INDEX IF NOT EXISTS idx_roi_ledger_value_probability ON roi_ledger (expected_value_usd, payout_probability);
SELECT COUNT(*) AS row_count FROM roi_ledger;
```

Rollback:

```sql
DROP INDEX IF EXISTS idx_roi_ledger_money_path_status;
DROP INDEX IF EXISTS idx_roi_ledger_value_probability;
DROP TABLE IF EXISTS roi_ledger;
```

## Boundary

This command writes a migration draft only. It does not execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Draft the apply-preflight packet next; do not execute migration SQL until the operator explicitly approves an apply step.

