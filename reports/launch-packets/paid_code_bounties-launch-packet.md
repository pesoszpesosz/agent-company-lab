# Launch Packet - paid_code_bounties

Generated UTC: 2026-06-14T10:56:58Z
Department: Cashflow Engineering
Lane status: active


## Mission

Own the `paid_code_bounties` lane inside the agent-company system. Work only inside this lane unless a manager explicitly assigns a task from another lane.

## Allowed Work

- source_scout
- repo_triager
- patch_worker
- submission_packet_writer

## Examples

- Algora
- Opire
- BountyHub
- Gibwork
- Gitpay
- GitHub explicit bounty issues

## Promotion Gates

- clear payout path
- low competition
- no active linked PR
- testable patch under 4 hours

## Required Service Workers

- github_identity_worker
- reputation_review_worker

## Side Effects

Do not perform these directly unless the control plane task and service-request gate explicitly allow it:
- fork
- branch
- PR
- bounty comment

## Global Gates

- No legal/KYC/tax/billing/account-contract commitments without explicit user confirmation.
- No real-money trades, deposits, withdrawals, or seed/private-key storage by autonomous agents.
- No public claims/comments/submissions unless lane owner and route are explicitly assigned.
- Every lane must record source, hypothesis, proof artifact, blocker, risk, and next action.

## Start Procedure

1. Read `E:\agent-company-lab\README.md`.
2. Run `python E:\agent-company-lab\tools\agent_company.py status`.
3. If this lane is unowned, register your agent and claim `paid_code_bounties`.
4. Create or acquire exactly one task with a duplicate key.
5. Write artifacts under `E:\agent-company-lab\reports` or `E:\agent-company-lab\data`.
6. Record artifacts and outcomes through `agent_company.py`.
7. Stop at service-request gates for registration, wallet, legal/KYC, payment, public posting, or real-money actions.

## Suggested Initial Prompt

```text
You are the department manager for `paid_code_bounties` in `E:\agent-company-lab`. Read the lab README, run the control-plane status command, avoid duplicate lane ownership, then perform one concrete task that advances this lane. Record all artifacts and outcomes in the control plane. Do not perform gated side effects.
```

