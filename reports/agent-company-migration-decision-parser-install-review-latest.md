# Agent Company Migration Decision Parser Install Review

Generated UTC: 2026-06-16T12:40:56Z
JSON mirror: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-review-latest.json`
Validation: `E:\agent-company-lab\reports\agent-company-migration-decision-parser-install-review-validation-latest.json`

## Decision

`agent_company_migration_decision_parser_install_review_ready_for_signed_install_decision_or_hold`

Recommended default: `hold_without_signed_operator_file_write_approval`

Prepared a report-only operator review packet for the parser module install preflight, with hold as the default and one-file-write approval boundaries.

## Decision Options

- `hold` default: Do not write or install the parser module.
- `approve_one_file_write_only`: Permit one local file write to the declared target path only.
- `request_preflight_rework`: Return the install preflight for path, gate, or rollback edits.
- `reject_parser_install`: Close this parser install path and keep report-only artifacts only.

## Approval Conditions

- signed operator decision id is present
- decision names approve_one_file_write_only
- target path exactly matches the preflight target path
- source artifact exactly matches the parser module file draft artifact
- permission is limited to one local file write
- permission does not allow import or live parsing
- post-write static review and fixture runner remain required

## Refusal Conditions

- missing signed decision id
- decision includes import or live parsing permission
- decision changes target path
- decision bundles migration SQL or service request mutation
- decision bundles browser account wallet payment public or security actions
- source preflight validation is stale or failing
- rollback and post-write review are not accepted

## Operator Instructions

- Default to hold unless the one-file write is genuinely needed.
- Do not approve import or live decision parsing from this packet.
- If approving, include the exact target path and source artifact.
- Limit approval to one attempt and one local file.
- Require post-write static review before any import ask.
- Reject if any external or service-request side effect is included.

## Boundary

This is a report-only operator review packet. It does not apply an install decision, write an importable parser module, import code, parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.

## Next Action

Wait for a signed operator install decision or draft a report-only install-decision intake contract.

