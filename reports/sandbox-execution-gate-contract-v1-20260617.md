# Sandbox Execution Gate Contract v1

Generated UTC: 2026-06-17T18:20:06Z
Task: `task-sandbox-execution-gate-contract-v1-20260617`
Source matrix: `E:\agent-company-lab\reports\agent-platform-capability-matrix-v1-20260617.json`
Contract JSON: `E:\agent-company-lab\reports\sandbox-execution-gate-contract-v1-20260617.json`
Validation: `E:\agent-company-lab\reports\sandbox-execution-gate-contract-v1-validation-20260617.json`
Schema: `E:\agent-company-lab\architecture\sandbox-execution-gate-contract-v1.schema.json`

## Summary

- Candidate patterns: `2`
- Required approval fields: `18`
- Hard denies: `10`
- Negative probes rejected: `10` of `10`
- Validation failures: `0`

## Candidate Patterns

| Candidate | Category | Contract Use |
| --- | --- | --- |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | `coding_agent_harness` | High-adoption autonomous coding agent harness; relevant for future code-worker lanes, but only inside strict workspace/sandbox and public-action gates. |
| [e2b-dev/E2B](https://github.com/e2b-dev/E2B) | `sandbox_execution` | Agent sandboxing is a likely missing department primitive for untrusted code, generated tools, and reproducible worker runs. |

## Required Approval Fields

- `decision_id`
- `approver`
- `signed_utc`
- `expires_utc`
- `lane_id`
- `task_id`
- `sandbox_provider`
- `workspace_root`
- `allowed_commands`
- `allowed_file_roots`
- `network_policy`
- `secret_policy`
- `dependency_policy`
- `time_limit_seconds`
- `cost_limit_usd`
- `artifact_capture_paths`
- `teardown_plan`
- `rollback_plan`

## Hard Denies

- `unbounded_network_access`
- `wildcard_filesystem_write`
- `ambient_secrets_or_environment_dump`
- `unbounded_dependency_install`
- `public_pr_issue_comment_or_submission`
- `browser_or_account_action`
- `wallet_payment_real_money_action`
- `live_security_testing_or_exploitation`
- `service_request_mutation_without_separate_approval`
- `cloud_sandbox_start_without_cost_cap`

## Negative Probes

| Probe | Result | Reason |
| --- | --- | --- |
| `network_any` | `reject` | `unbounded_network_access` |
| `workspace_any_write` | `reject` | `wildcard_filesystem_write` |
| `ambient_secrets` | `reject` | `ambient_secrets_or_environment_dump` |
| `pip_latest` | `reject` | `unbounded_dependency_install` |
| `public_pr` | `reject` | `public_pr_issue_comment_or_submission` |
| `browser_login` | `reject` | `browser_or_account_action` |
| `wallet_action` | `reject` | `wallet_payment_real_money_action` |
| `security_scan_live` | `reject` | `live_security_testing_or_exploitation` |
| `service_mutation` | `reject` | `service_request_mutation_without_separate_approval` |
| `cloud_no_cost_cap` | `reject` | `cloud_sandbox_start_without_cost_cap` |

## Boundary

- No sandbox session, process, command, dependency install/import, network access, secret use, API key use, cloud sandbox, service-request mutation, worker start, browser session, model/API call, public/account/wallet/payment/security/real-money action, or external side effect occurred.
