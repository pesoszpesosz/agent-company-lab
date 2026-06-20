# Wave 7 Agent-Company Operating Model - 2026-06-15

Generated at: 2026-06-14T21:51:53Z

## Company Org

CEO/control plane: owns the ledger, lanes, approvals, tasks, artifacts, outcomes, trace events, and final go/no-go decisions.

Departments: one lane per money path family: paid code bounties, security bounties, prediction markets, AI/ML competitions, digital products, content/growth, lead generation, web3 grants/airdrops/hackathons, trading research, and money-source discovery.

Managers: lane-specific agents that convert broad money paths into ranked work packets, service requests, and proof artifacts.

Seekers: scouts that search current sources and produce evidence-backed candidates. They do not perform gated external actions.

Service workers: specialized workers for browser sessions, account registration, wallet operations, legal/KYC/tax/payment review, public submissions, and model/API execution. They act only from approved service_worker_request.v1 packets.

Reviewers: CRO/legal/safety/human reviewers that can approve, reject, or request narrowing of service requests.

## Non-Negotiable Invariant

Lane agents may request risky capabilities, but they do not receive them directly. Every external side effect goes through a service desk with scope, approval, result artifact, and trace event.

## Near-Term Build Order

1. service_worker_request.v1 schema and one converted browser-readonly request.
2. Local service desk queue report grouped by worker_type and risk_gate.
3. OpenInference-shaped trace export plan for local trace_events.
4. DBOS durable adapter spike on one local work_packet.v1.
5. Hatchet queue comparison after DBOS evidence exists.

## Gated Worker Boundaries

- Browser workers: public read-only browsing unless a later request explicitly permits sign-in or form submission.
- Registration workers: no signup, identity, email, phone, payment method, or terms acceptance without explicit approval.
- Wallet workers: no key generation/import, signing, transaction, funding, claim, bridge, staking, or token approval without explicit approval.
- Submission workers: no public post, issue, PR, marketplace listing, bounty report, or private security report without explicit approval.
- Model/API workers: no paid model/API call without provider, model, max cost, and artifact scope.
