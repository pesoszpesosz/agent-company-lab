# Security Program Rules/Scope Ranker v1

Generated UTC: 2026-06-17T21:50:00Z
Task: `task-security-program-rules-scope-ranker-v1-20260618`
Dataset: `E:\agent-company-lab\data\security-program-rules-scope-ranker-v1-20260618.json`
CSV: `E:\agent-company-lab\data\security-program-rules-scope-ranker-v1-20260618.csv`
Validation: `E:\agent-company-lab\reports\security-program-rules-scope-ranker-v1-validation-20260618.json`

## Purpose

This packet turns the top-ranked security money path into a local rules/scope ranker. It does not perform security testing, register accounts, start browsers, submit reports, contact programs, touch wallets, or post anything publicly. Its job is to tell the security lane manager where local rules reading and public-code review should start.

## Ranked Routes

| Rank | Program | Type | Value | Verdict | Next Proof |
| ---: | --- | --- | ---: | --- | --- |
| `1` | [Immunefi directory](https://immunefi.com/bug-bounty/) | Web3 bounty directory | `10` | `promote_for_rules_shortlist` | `immunefi_directory_scope_shortlist_v1` |
| `2` | [Lido on Immunefi](https://immunefi.com/bug-bounty/lido/information/) | Web3 protocol bounty | `9` | `watch_high_reward_rules_first` | `lido_scope_rules_extraction_packet_v1` |
| `3` | [Optimism on Immunefi](https://immunefi.com/bug-bounty/optimism/information/) | Web3 protocol bounty | `9` | `watch_high_reward_recent_update` | `optimism_scope_rules_extraction_packet_v1` |
| `4` | [Immutable on Immunefi](https://immunefi.com/bug-bounty/immutable/information/) | Web3 protocol bounty | `8` | `watch_after_top_two` | `immutable_scope_rules_extraction_packet_v1` |
| `5` | [Disclose platform directory](https://github.com/disclose/bug-bounty-platforms) | VDP/platform directory | `8` | `promote_for_source_discovery` | `vdp_platform_catalog_router_v1` |
| `6` | [bugbounty-companion](https://github.com/tintinweb/bugbounty-companion) | Research tooling reference | `7` | `study_tooling_pattern_only` | `bug_bounty_source_manifest_fields_v1` |
| `7` | [OSS AI-slop quality risk](https://www.itpro.com/software/open-source/curl-open-source-bug-bounty-program-scrapped) | Quality risk signal | `10` | `mandatory_quality_gate_for_all_security_paths` | `security_report_quality_gate_v1` |

## Quality Gate

Minimum before any submission:

- Program scope and safe-harbor terms captured.
- In-scope asset and impact row identified.
- Local reproduction or static proof artifact exists.
- False-positive and duplicate checks complete.
- Report explains exact impact and affected version/asset.
- CRO/user approval explicitly grants the submission route.

Automatic kill conditions:

- Impact is out of scope.
- Proof depends on live testing without approval.
- Claim is AI-generated without local verification.
- Finding is only best-practice hardening with no eligible impact.
- Program prohibits the test or report route.
- Payout route requires wallet/payment details not approved by the user.

## Decision

Promote rules/scope research only. No target-specific testing, report drafting, private submission, wallet/payment action, or public action is ready.

## Boundary

- Browser sessions started: `0`
- Accounts registered: `0`
- Service requests assigned/updated: `0` / `0`
- Worker/runtime starts: `0` / `0`
- Security tests: `False`
- Private reports submitted: `0`
- Public actions: `False`
- Wallet/payment actions: `False` / `False`
- External side effects: `False`

