# Service Request Checklist Template

Use this when a local artifact is ready but the next step requires a service worker or explicit approval.

## Request Identity

- Request ID: `{{request_id}}`
- Lane: `{{lane_id}}`
- Task: `{{task_id}}`
- Requester agent: `{{agent_id}}`
- Service needed: `{{service_id}}`
- Request type: `{{request_type}}`
- Risk gate: `{{risk_gate}}`

## Exact Requested Action

{{one_sentence_exact_action}}

The service request must be narrow. It should name one target surface, one allowed action class, one evidence output, and the forbidden actions.

## Required Intake

| Field | Value |
| --- | --- |
| target URL or platform | {{target}} |
| allowed read/action scope | {{allowed_scope}} |
| forbidden actions | {{forbidden_actions}} |
| evidence needed | {{evidence_needed}} |
| session sensitivity | {{public_read_only_or_private}} |
| max cost | {{zero_or_budget}} |
| account/payment impact | {{none_or_described}} |
| artifact path | {{artifact_path}} |

## Hard Stops

- No account creation or login unless explicitly approved.
- No terms acceptance unless explicitly approved.
- No payment, purchase, payout, seller setup, or tax/KYC action unless explicitly approved.
- No upload, listing, submission, post, comment, message, review, or promotion unless explicitly approved.
- No credentials, OTPs, cookies, private files, private customer data, or wallet actions unless explicitly approved.

## Completion Evidence

- Local capture/report path: `{{completion_artifact}}`
- Decision note: `{{decision_note}}`
- Remaining gates: `{{remaining_gates}}`
