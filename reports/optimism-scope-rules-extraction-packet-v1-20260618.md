# Optimism Scope Rules Extraction Packet v1

Generated UTC: 2026-06-17T21:42:00Z
Task: `task-optimism-scope-rules-extraction-packet-v1-20260618`
Lane: `security_bounty_private_reports`

## Purpose

Turn Optimism's Immunefi program into a local rules packet before any target-specific security work. This packet does not test, run, clone, submit, log in, probe, or contact anything.

## Program Snapshot

| Field | Value |
| --- | --- |
| Platform | Immunefi |
| Program | Optimism |
| Last updated | 2026-06-16 |
| Maximum bounty | $2,000,042 |
| Triaged by Immunefi | True |
| PoC required | True |
| KYC required | True |
| Observed assets in scope | 33 |
| Observed impacts in scope | 27 |
| Submission-ready rows | 0 |

## Reward Surface

| Category | Critical | High | Medium | Primacy |
| --- | --- | --- | --- | --- |
| Blockchain/DLT | Up to $2,000,042 | Max $50,000 Min $15,000 | Max $15,000 Min $1,000 | Primacy of Impact |
| Smart Contract | Up to $2,000,042 | Max $50,000 Min $15,000 | Max $15,000 Min $1,000 | Primacy of Impact |
| Web & App | Max $50,000 Min $5,000 | Flat $5,000 |  | Primacy of Rules |

## Scope Notes

Examples from the public scope page include `OptimismPortal`, `ProxyAdmin`, `DisputeGameFactory`, `L2OutputOracle`, `OptimismMintableERC20Factory`, `L1CrossDomainMessenger`, `PermissionedDisputeGame`, `op-dispute-mon`, and the Optimism specs. The resources page points at program smart contracts, Optimism Docs, and previous audits/monorepo material.

The program also says smart-contract proxy implementations are in scope when the proxy is in scope, but only assets listed in the scope table are considered in scope. This makes the next local packet clear: normalize all 33 assets before reviewing any code path.

## Impact Notes

Critical impact classes include protocol insolvency, user-fund theft, direct loss or permanent freezing of funds, arbitrary command execution, sensitive running-server data retrieval, unauthorized authenticated user actions, subdomain takeover with connected-wallet interaction, direct user-fund theft in web/app context, malicious connected-wallet interactions, and XSS through metadata. High web/app impact includes subdomain takeover without connected-wallet interaction.

## Duplicate and Out-of-Scope Controls

- Check Optimism smart-contract known issues dated 2025-06-12.
- Check Optimism Blockchain/DLT known issues dated 2025-06-12.
- Do not replay publicly disclosed upstream reth or Ethereum Foundation vulnerabilities against Optimism unless disclosed to Optimism at the same time.
- Check devp2p known issues before any networking claim.
- Exclude chain-operator best-practice violations, user-exposed JSON-RPC/Beacon API requirements, Alt-DA for op-node/op-batcher, end-of-service execution clients, and listed bridge foot guns.
- Do not inspect or probe listed out-of-scope web properties. Agora-operated `vote.optimism.io` and `atlas.optimism.io` route to Agora unless there is direct OP Stack or Optimism protocol financial impact.

## Allowed Next Local Work

| Proof | Gate Needed Now | Description |
| --- | --- | --- |
| `optimism_asset_scope_table_v1` | No | Normalize 33 scope assets into local CSV/JSON with category, date, and duplicate-risk notes. |
| `optimism_known_issue_duplicate_matrix_v1` | No | Extract known issues, upstream reth/devp2p exclusions, and bridge-footgun exclusions into a mandatory checklist. |
| `security_report_quality_gate_v1` | No | Create report-quality checklist for scope, PoC, duplicate, impact, local-only evidence, KYC/payment, and disclosure gates. |
| `optimism_local_harness_plan_v1` | Yes | Design a local-only proof path using official dockerized services and integration tests; no clone/build/run/test until runtime gate exists. |

## Blocked Actions

- No mainnet or public testnet testing.
- No live web/app probing, DNS probing, node start, Docker start, integration-test run, local fork, transaction, bridge, oracle, third-party, or automated traffic testing.
- No account login, KYC, W-9/W-8, payout, wallet, or payment action.
- No Immunefi submission, public disclosure, or public action.

## Decision

Optimism remains the top Immunefi candidate, but only local rules extraction and quality gates are ready. Target-specific local proof work is not ready until `optimism_asset_scope_table_v1`, `optimism_known_issue_duplicate_matrix_v1`, and `security_report_quality_gate_v1` exist.

## Boundary

- Browser sessions started: `0`
- Accounts registered: `0`
- Service requests assigned/updated: `0` / `0`
- Worker starts/runtime starts: `0` / `0`
- Security tests: `False`
- Private reports submitted: `0`
- Public actions: `False`
- Wallet/payment actions: `False` / `False`
- External side effects: `False`
