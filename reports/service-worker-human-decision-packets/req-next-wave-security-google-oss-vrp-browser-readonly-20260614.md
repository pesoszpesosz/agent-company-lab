# Service Worker Human Decision Packet

Generated UTC: 2026-06-17T20:41:28Z
Request: `req-next-wave-security-google-oss-vrp-browser-readonly-20260614`
Lane: `security_bounty_private_reports`
Worker type: `browser_read_only`
Risk gate: `catalog_required_approval_no_external_action`

## Operating Rule

This packet is for human/CRO decision support only. It does not approve, reject, register, assign, update, start, browse, call APIs, post, submit, pay, trade, or contact anyone.

## Gate State

- Current blocking gate: `human_cro_approval_required`
- Review route: `ready_for_human_cro_review`
- Scope diff route: `missing_exact_scope`
- Scope compatible with packet: `False`
- Recommended worker pool: `service-worker-browser-read-only-pool`
- Pool status: `missing_service_worker_pool`

## Preconditions

| Check | Passed |
| --- | --- |
| `chain_integrity_all_checks_passed` | `True` |
| `service_status_needs_review` | `True` |
| `packet_valid` | `True` |
| `current_gate_human_cro_approval_required` | `True` |
| `manual_review_required` | `True` |
| `approve_preview_present` | `True` |
| `reject_preview_present` | `True` |

## Suggested Exact Scope

DRAFT ONLY - NOT APPROVED. For source service request `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` and worker request `swr-next-wave-security-google-oss-vrp-browser-readonly-20260614`, allow `browser_read_only` worker activity only after separate explicit user/CRO approval. Objective: After explicit approval only, run a public read-only browser research worker for req-next-wave-security-google-oss-vrp-browser-readonly-20260614; capture evidence and stop before any login, form submission, account, public, payment, wallet, or real-money action. Allowed actions: read public allowed pages after approval; capture source URLs, page titles, short compliant excerpts, summaries, and local evidence artifacts; stop at login, account, payment, public action, or private-data boundaries Allowed hosts: scope_defined_in_source_packet Starting URLs: scope_defined_in_source_packet Allowed data: local artifact references; public source URLs; page titles; short factual excerpts within copyright limits; local notes; approval and risk metadata Required outputs: E:\agent-company-lab\reports\service-worker-requests\req-next-wave-security-google-oss-vrp-browser-readonly-20260614-result-placeholder.md Hard denials: no credentials, OTPs, secrets, private files, private data, payment details, tax/KYC data, or wallet data; no login, signup, account creation, account settings changes, or terms/legal acceptance; no payments, purchases, deposits, withdrawals, trades, wallet connections, wallet signatures, or real-money action; no public posts, comments, replies, messages, listings, uploads, form submissions, issue/PR actions, or external contact; no external side effects, API/provider/model calls, paid cost, worker start, or queue mutation unless separately approved in an exact scope; no bypassing paywalls, rate limits, access controls, platform rules, or the packet stop conditions; execute without explicit approval; login unless explicitly approved; signup or account creation; accept terms or legal agreements; enter credentials, OTPs, personal data, private files, payment details, tax/KYC data, or wallet information; submit forms; publish, post, reply, comment, message, list, upload, or contact external parties; purchase, deposit, withdraw, trade, connect wallet, sign wallet messages, or perform real-money actions; change account settings; bypass paywalls, rate limits, access controls, or platform rules Stop conditions: service request status is not approved or assigned; requested action exceeds approval scope; required artifact/source is missing or ambiguous; page requires unapproved login, signup, consent, payment, private data, credentials, OTP, wallet action, file upload, or public submission; worker would need to leave allowed host/scope Max cost USD: 0. This draft expires unless separately approved with `approve-service-request`; this report grants no approval, assignment, start authority, browser action, API call, public action, payment, trade, submission, or external side effect.

## Approve Preview

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "approve-service-request",
  "--request-id",
  "req-next-wave-security-google-oss-vrp-browser-readonly-20260614",
  "--approved-by",
  "USER_OR_CRO",
  "--exact-scope",
  "REPLACE_WITH_MANUALLY_REVIEWED_EXACT_SCOPE_FROM_SUGGESTED_SCOPE",
  "--decision-note",
  "Manual approval after reviewing packet, risk gate, exact scope, and stop conditions."
]
```

## Reject Preview

```json
[
  "python",
  "E:\\agent-company-lab\\tools\\agent_company.py",
  "reject-service-request",
  "--request-id",
  "req-next-wave-security-google-oss-vrp-browser-readonly-20260614",
  "--rejected-by",
  "USER_OR_CRO",
  "--reason",
  "Manual rejection after reviewing packet, risk gate, exact scope, and stop conditions."
]
```

## Next Action

Human/CRO must review the packet, risk gate, exact scope, gate map, and current external context before running any approve/reject command manually.

