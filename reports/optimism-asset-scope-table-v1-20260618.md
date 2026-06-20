# Optimism Asset Scope Table v1

Generated UTC: 2026-06-17T21:53:00Z
Task: `task-optimism-asset-scope-table-v1-20260618`
Lane: `security_bounty_private_reports`

## Purpose

Normalize Optimism's Immunefi in-scope assets into a local table before any target-specific code review, proof planning, runtime work, security testing, or report drafting.

## Extraction Note

The public Immunefi scope page advertised `33` total assets. Static HTML exposed the default table, then a public read-only headless Edge extraction clicked the category controls and Smart Contract `Show all` control to reconcile all rows. This was text extraction only: no login, form, account, probing, testing, submission, wallet, payment, or mutation.

## Counts

| Category | Rows |
| --- | ---: |
| Blockchain/DLT | 4 |
| Smart Contract | 19 |
| Web & App | 10 |
| Total | 33 |

## Asset Rows

| ID | Category | Name | Added | Target |
| --- | --- | --- | --- | --- |
| `optimism-bdl-001` | Blockchain/DLT | op-reth | 2026-06-12 | https://github.com/ethereum-optimism/optimism/tree/develop/rust/op-reth |
| `optimism-bdl-002` | Blockchain/DLT | Primacy of Impact placeholder | 2026-03-11 | Primacy Of Impact |
| `optimism-bdl-003` | Blockchain/DLT | op-dispute-mon | 2024-05-29 | https://github.com/ethereum-optimism/optimism/tree/develop/op-dispute-mon |
| `optimism-bdl-004` | Blockchain/DLT | op-node | 2024-05-29 | https://github.com/ethereum-optimism/optimism/tree/develop/op-node |
| `optimism-sc-001` | Smart Contract | L1StandardBridge | 2024-03-11 | https://etherscan.io/address/0x99C9fc46f92E8a1c0deC1b1747d010903E884bE1 |
| `optimism-sc-002` | Smart Contract | L2OutputOracle | 2024-03-11 | https://etherscan.io/address/0xdfe97868233d1aa22e815a266982f2cf17685a27 |
| `optimism-sc-003` | Smart Contract | DelayedWETH | 2025-10-03 | https://etherscan.io/address/0xE497B094d6DbB3D5E4CaAc9a14696D7572588d14 |
| `optimism-sc-004` | Smart Contract | L1ERC721Bridge | 2024-03-11 | https://etherscan.io/address/0x5a7749f83b81B301cAb5f48EB8516B986DAef23D |
| `optimism-sc-005` | Smart Contract | OptimismPortal | 2024-03-11 | https://etherscan.io/address/0xbEb5Fc579115071764c7423A4f12eDde41f106Ed |
| `optimism-sc-006` | Smart Contract | L1CrossDomainMessenger | 2024-03-11 | https://etherscan.io/address/0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1 |
| `optimism-sc-007` | Smart Contract | DisputeGameFactory | 2024-05-29 | https://etherscan.io/address/0xe5965Ab5962eDc7477C8520243A95517CD252fA9 |
| `optimism-sc-008` | Smart Contract | AddressManager | 2024-03-11 | https://etherscan.io/address/0xdE1FCfB0851916CA5101820A69b13a4E276bd81F |
| `optimism-sc-009` | Smart Contract | ProxyAdmin | 2024-03-11 | https://etherscan.io/address/0x543bA4AADBAb8f9025686Bd03993043599c6fB04 |
| `optimism-sc-010` | Smart Contract | OptimismMintableERC20Factory | 2024-03-11 | https://etherscan.io/address/0x75505a97BD334E7BD3C476893285569C4136Fa0F |
| `optimism-sc-011` | Smart Contract | PermissionedDisputeGame | 2025-10-03 | https://etherscan.io/address/0xE9daD167EF4DE8812C1abD013Ac9570C616599A0 |
| `optimism-sc-012` | Smart Contract | AnchorStateRegistry | 2025-10-03 | https://etherscan.io/address/0x18DAc71c228D1C32c99489B7323d441E1175e443 |
| `optimism-sc-013` | Smart Contract | OptimismPortal Implementation | 2024-05-29 | https://etherscan.io/address/0xe2F826324b2faf99E513D16D266c3F80aE87832B |
| `optimism-sc-014` | Smart Contract | FaultDisputeGame | 2025-10-03 | https://etherscan.io/address/0x4146DF64D83acB0DcB0c1a4884a16f090165e122 |
| `optimism-sc-015` | Smart Contract | PreimageOracle | 2025-10-03 | https://etherscan.io/address/0xD326E10B8186e90F4E2adc5c13a2d0C137ee8b34 |
| `optimism-sc-016` | Smart Contract | SystemConfig | 2024-03-11 | https://etherscan.io/address/0x229047fed2591dbec1eF1118d64F7aF3dB9EB290 |
| `optimism-sc-017` | Smart Contract | MIPS | 2025-10-03 | https://etherscan.io/address/0x0f8EdFbDdD3c0256A80AD8C0F2560B1807873C9c |
| `optimism-sc-018` | Smart Contract | Primacy of Impact placeholder | 2026-03-11 | Primacy Of Impact |
| `optimism-sc-019` | Smart Contract | PolicyEngineStaking | 2026-05-21 | https://optimistic.etherscan.io/address/0xb5CB7a05DD1311195982A26DFC8222477f9D8179 |
| `optimism-web-001` | Web & App | Main OP Labs blog | 2025-10-03 | https://blog.oplabs.co/ |
| `optimism-web-002` | Web & App | Main OP Labs website | 2025-10-03 | https://www.oplabs.co/ |
| `optimism-web-003` | Web & App | Optimism's Careers page | 2025-10-03 | http://jobs.optimism.io/ |
| `optimism-web-004` | Web & App | Optimism's Community page | 2025-10-03 | https://community.optimism.io/ |
| `optimism-web-005` | Web & App | Optimism's Console | 2025-10-03 | https://console.optimism.io/ |
| `optimism-web-006` | Web & App | Optimism's Specs | 2025-10-03 | https://specs.optimism.io/ |
| `optimism-web-007` | Web & App | Optimism's Docs | 2025-10-03 | https://docs.optimism.io/ |
| `optimism-web-008` | Web & App | Optimism's App | 2025-10-03 | https://app.optimism.io/ |
| `optimism-web-009` | Web & App | Optimism's Gateway | 2025-10-03 | http://gateway.optimism.io/ |
| `optimism-web-010` | Web & App | Main Optimism website | 2025-10-03 | https://www.optimism.io/ |

## Decision

The full observed asset table is now normalized. The next useful local work is `optimism_known_issue_duplicate_matrix_v1` and `security_report_quality_gate_v1`. This table does not make any row submission-ready and does not authorize runtime work, code execution, node starts, probing, fork tests, or Immunefi submission.

## Boundary

- Public read-only headless page extraction sessions: `1`
- Service-worker browser sessions started: `0`
- Accounts registered: `0`
- Service requests assigned/updated: `0` / `0`
- Worker starts/runtime starts: `0` / `0`
- Security tests: `False`
- Private reports submitted: `0`
- Public actions: `False`
- Wallet/payment actions: `False` / `False`
- External side effects: `False`
