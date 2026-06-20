# Agent Task DAG Contract v1

Generated UTC: 2026-06-17T18:37:28Z
DAG: `dag-agent-company-scaleout-v1-20260617`
Task: `task-agent-task-dag-contract-v1-20260617`
Schema: `E:\agent-company-lab\architecture\agent-task-dag-contract-v1.schema.json`
JSON: `E:\agent-company-lab\reports\agent-task-dag-contract-v1-20260617.json`
Validation: `E:\agent-company-lab\reports\agent-task-dag-contract-v1-validation-20260617.json`

## Purpose

Create a report-only dispatch DAG for scaling the agent company across money lanes and gated workers.

## Validation

- Nodes: `10`
- Edges: `12`
- Gates: `3`
- Evidence requirements: `3`
- Failures: `0`
- Topological order: `node-ceo-intake`, `node-source-radar`, `node-dag-contract`, `node-money-lane-refresh`, `node-paid-code-proof`, `node-security-proof`, `node-digital-product-proof`, `node-browser-service-request`, `node-worker-pool-preflight`, `node-ceo-synthesis`

## Nodes

| Node | Lane | Role | Type | Status | Gate | Output |
| --- | --- | --- | --- | --- | --- | --- |
| `node-ceo-intake` | `platform_engineering` | `ceo` | `synthesis` | `ready_local_only` | `local_only` | requirements map, lane dispatch criteria |
| `node-source-radar` | `platform_engineering` | `infrastructure_scout` | `research` | `ready_local_only` | `public_read_only` | ranked infrastructure source set, recommended local builds |
| `node-dag-contract` | `platform_engineering` | `control_plane_builder` | `implementation_contract` | `ready_local_only` | `local_only` | agent_task_dag_contract_v1 schema, validated sample DAG |
| `node-money-lane-refresh` | `money_source_discovery` | `source_mapper` | `research` | `blocked_by_gate` | `browser_read_only_or_current_source_gate` | source family matrix, refresh request packet |
| `node-paid-code-proof` | `paid_code_bounties` | `repo_triager` | `local_proof` | `blocked_by_gate` | `public_read_only_or_github_public_action_gate` | candidate proof packet, claim/PR gate decision |
| `node-security-proof` | `security_bounty_private_reports` | `program_rules_reader` | `local_proof` | `blocked_by_gate` | `security_testing_and_report_submission_gate` | rules-safe proof packet, submission decision packet |
| `node-digital-product-proof` | `digital_products_templates_plugins` | `market_gap_scout` | `local_proof` | `ready_local_only` | `local_only_until_marketplace_gate` | private review packet, post-approval simulation plan |
| `node-browser-service-request` | `platform_engineering` | `browser_action_worker` | `service_request` | `blocked_by_gate` | `human_cro_approval_gate_required` | service-worker request packet, exact-scope template |
| `node-worker-pool-preflight` | `platform_engineering` | `control_plane_builder` | `review` | `ready_local_only` | `local_only` | assignment preflight result |
| `node-ceo-synthesis` | `platform_engineering` | `ceo` | `synthesis` | `ready_local_only` | `local_only` | CEO dispatch board, next DAG revision |

## Edges

| From | To | Reason |
| --- | --- | --- |
| `node-ceo-intake` | `node-source-radar` | Requirements define what sources matter |
| `node-source-radar` | `node-dag-contract` | Fresh orchestration signals inform DAG structure |
| `node-dag-contract` | `node-money-lane-refresh` | Lane refresh becomes a typed DAG node |
| `node-dag-contract` | `node-paid-code-proof` | Paid-code proof follows dispatch contract |
| `node-dag-contract` | `node-security-proof` | Security proof follows dispatch contract |
| `node-dag-contract` | `node-digital-product-proof` | Product proof follows dispatch contract |
| `node-money-lane-refresh` | `node-browser-service-request` | Blocked source refresh needs exact browser scope |
| `node-paid-code-proof` | `node-browser-service-request` | Live issue verification needs browser/GitHub read-only gate |
| `node-security-proof` | `node-browser-service-request` | Rendered program rules may need browser read-only gate |
| `node-browser-service-request` | `node-worker-pool-preflight` | Worker pools are checked only after exact request scope exists |
| `node-digital-product-proof` | `node-ceo-synthesis` | Local proof can be synthesized immediately |
| `node-worker-pool-preflight` | `node-ceo-synthesis` | Gated work reports readiness or hold reason |

## Gates

| Gate | Type | Blocks | Required Approval |
| --- | --- | --- | --- |
| `gate-browser-readonly` | `browser_read_only_session` | `node-money-lane-refresh`, `node-paid-code-proof`, `node-security-proof`, `node-browser-service-request` | `human_user`, `chief_risk_officer` |
| `gate-security-submission` | `security_report_submission` | `node-security-proof` | `human_user`, `chief_risk_officer` |
| `gate-public-action` | `public_action_execution` | `node-paid-code-proof`, `node-digital-product-proof` | `human_user`, `reputation_review_worker` |

## Evidence Requirements

| Evidence | Required For | Kind | Fields |
| --- | --- | --- | --- |
| `evidence-node-status` | `every_node` | `json_or_markdown` | `node_id`, `lane_id`, `owner_role`, `status`, `gate`, `next_action` |
| `evidence-gate-decision` | `blocked_by_gate_node` | `decision_packet` | `requested_action`, `allowed_actions`, `prohibited_actions`, `approval_required_by`, `do_not_execute_clause` |
| `evidence-proof-output` | `local_proof_node` | `proof_packet` | `source`, `method`, `result`, `confidence`, `next_action` |

## Boundary

- This contract is report-only.
- It approves no actions, starts no workers, updates no service requests, calls no APIs, and performs no external side effects.
- External browser/account/wallet/payment/public/security/trading actions remain blocked until separate exact-scope approval and readiness checks pass.
