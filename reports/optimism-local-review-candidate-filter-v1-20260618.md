# Optimism Local Review Candidate Filter v1

Generated UTC: 2026-06-17T21:56:43Z

Lane: `security_bounty_private_reports`

Task: `task-optimism-local-review-candidate-filter-v1-20260618`

## Purpose

This filter converts the Optimism scope table, duplicate matrix, and security report quality gate into an operational pre-review router. It tells a future security agent which candidate classes can be studied locally and which classes must stop before code review.

## Best Local Route

The best next local route is `olf-001`: Optimism smart-contract invariant review.

Why: source mapping, invariant analysis, duplicate comparison, and local PoC planning can be done without touching mainnet, public testnet, browser sessions, accounts, wallets, payment flows, private reports, or public disclosure.

Good example asset families:

- `OptimismPortal`
- `DisputeGameFactory`
- `FaultDisputeGame`
- `PreimageOracle`
- `SystemConfig`
- `MIPS`

## Hard Stops And Low-Value Routes

- Public RPC/Beacon API exposure and chain-operator topology issues are hard stops.
- Alt-DA feature claims must stop unless the exclusion is clearly cleared.
- Bridge/token foot-gun claims must stop unless there is a new protocol bypass beyond documented exclusions.
- op-reth issues require upstream reth and Ethereum Foundation route checks before promotion.
- Web/App issues require route and browser gates before any browser work.
- Economic/governance/Sybil/centralization/lack-of-liquidity claims must stop unless there is a direct code bug.

## Candidate Packet Requirements

A future `optimism_single_asset_candidate_packet_v1` must include:

1. Selected asset ID.
2. Selected filter ID.
3. Asset scope evidence.
4. Impact scope evidence.
5. Duplicate matrix notes.
6. Security report quality gate notes.
7. Runnable local PoC plan.
8. Side-effect audit.
9. Operator submission-gate status.

## Boundary

This packet is report-only. It does not authorize code execution against Optimism targets, local fork testing, browser work, account registration, private report submission, public disclosure, wallet action, payment action, service-request assignment, worker start, runtime start, or any external side effect.

## Next Action

Select exactly one Optimism smart-contract asset and create a local candidate packet. Do not run code, fork chains, test targets, or submit reports.
