# Agent Company Migration Operator Review

Generated UTC: 2026-06-16T11:42:41Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-operator-review-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-operator-review-validation-latest.json`

## Decision

`agent_company_migration_operator_review_packet_ready_for_signed_decision_or_hold`

Recommended default: `hold_without_signed_operator_approval`

Prepared a human operator review packet for the migration preflight, with decision options, approval/refusal conditions, evidence links, and a default hold posture.

## Decision Options

- `hold` default: No apply command is enabled; continue report-only planning.
- `approve_sandbox_dry_run_only`: Allow a future command to copy the DB and test migration SQL on a throwaway copy only.
- `request_rework`: Send the migration packet back for table, rollback, or gate revisions.
- `reject_migration_path`: Close this schema path and keep the current control-plane tables unchanged.

## Approval Conditions

- operator supplies an explicit signed decision id
- decision scope names sandbox dry-run only unless separately approved
- backup path is specified and outside the live DB file
- migration draft and preflight validation both pass
- service request counts are snapshotted before any sandbox action
- rollback drill is required on the sandbox copy
- post-dry-run integrity report is required before any next ask
- approval expires unless used for the named command and artifact set

## Refusal Conditions

- missing signed decision id
- approval tries to include live SQL apply
- backup path is missing or points to the live DB
- preflight or migration validation is stale or failing
- service request state drift is detected
- worker start, browser, account, wallet, payment, public, or security action is requested
- rollback drill is omitted
- artifact paths do not match this review packet

## Human Instructions

1. Review the migration draft markdown before approving anything.
2. Prefer hold unless a sandbox dry-run is genuinely needed.
3. Do not approve live migration SQL from this packet.
4. If approving, write the exact option and artifact paths into the decision.
5. Limit any approval to one command run and one timestamped sandbox copy.
6. Require a post-run validation report before considering schema apply.
7. Reject or request rework if any gate language is ambiguous.

## Evidence Links

- `E:\agent-company-lab\reports\agent-company-report-only-migration-draft-latest.md`
- `E:\agent-company-lab\reports\agent-company-report-only-migration-draft-validation-latest.json`
- `E:\agent-company-lab\reports\agent-company-migration-apply-preflight-latest.md`
- `E:\agent-company-lab\reports\agent-company-migration-apply-preflight-validation-latest.json`

## Boundary

This packet does not apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Wait for a signed operator decision or prepare a report-only decision-intake parser; do not enable or run the apply command.

