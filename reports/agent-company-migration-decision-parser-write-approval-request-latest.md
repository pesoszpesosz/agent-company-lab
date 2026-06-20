# Agent Company Migration Decision Parser Write Approval Request

Generated UTC: 2026-06-16T13:33:42Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-request-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-write-approval-request-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_write_approval_request_ready_for_signed_operator_decision_or_hold`

Recommended default: `hold_without_signed_one_file_parser_write_approval`

Prepared the report-only one-file parser-write approval request packet with exact fields, paths, boundaries, refusal triggers, and evidence links.

## Approval Fields

- `decision_id`
- `operator_name`
- `decision_type`
- `target_path`
- `source_artifact_path`
- `source_review_path`
- `approval_scope`
- `expires_at`
- `signed_utc`

## Boundary Conditions

- one local file write only
- target path must match parser install preflight
- source artifact must match parser module file draft
- source review must match parser-write runner review
- no parser import
- no live decision parsing
- post-write static review and fixture rerun required
- no external service request browser account wallet payment public or security action

## Refusal Triggers

- missing signed decision id
- approval scope broader than one local file write
- target path differs from preflight
- source artifact differs from reviewed draft
- source review path differs from runner review
- approval includes import or live parsing
- approval includes SQL service-request worker API or browser action
- approval is expired or unsigned

## Operator Instructions

- Default to hold until an operator signs the exact one-file approval.
- Do not sign if any path differs from this packet.
- Do not bundle parser import, live parsing, SQL, service requests, browser, account, wallet, payment, public, security, or API actions.
- If approving, set decision_type to approve_one_parser_file_write_only.
- Set approval_scope to one_local_file_write_only.
- Require post-write static review and fixture rerun before any import question.
- Reject or request rework if the evidence chain is stale or failing.

## Boundary

This is a report-only approval request packet. It does not grant approval, write or import a parser module, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Hold for a signed operator approval matching this packet; do not write or import the parser without it.

