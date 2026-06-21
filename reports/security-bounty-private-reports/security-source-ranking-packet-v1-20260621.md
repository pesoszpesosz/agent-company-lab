# Security Source Ranking Packet v1

Generated UTC: 2026-06-21T13:34:00Z
Lane: `security_bounty_private_reports`
Task: `task-continuity-lane-next-task-20260621-security_bounty_private_reports-002`
Owner: `lane-manager-security_bounty_private_reports-019ec612`
Evidence: `E:\agent-company-lab\reports\security-bounty-private-reports\security-bounty-local-readiness-proof-v1-20260621.md`
Commit context: `085a03a Continue lane proof followups`

## Boundary

This packet uses local control-plane evidence only. It does not access live targets, scan, exploit, submit reports, contact programs, open browsers, call APIs, approve route gates, spend, trade, create accounts, create duplicate workers, or mutate lane ownership.

## Ranking Method

Candidates are ranked for the next local proof step, not for submission. Scores use only local evidence already imported into the lane.

| Factor | Weight | Local meaning |
| --- | ---: | --- |
| Proof maturity | 30 | Existing local proof, patch candidate, or concrete invariant direction |
| Scope route clarity | 20 | Whether local evidence names a plausible program/disclosure route without needing a live lookup |
| Local-only executable next step | 20 | Whether the next step can be a report-only fixture, regression design, or local test packet |
| Security impact plausibility | 20 | Whether the candidate describes a credible boundary, traversal, validation, parser, or release risk |
| Duplicate/staleness risk | 10 | Lower score when local evidence already says killed, rejected, stale, or route-only |

## Ranked Imported Evidence

| Rank | Evidence ID | Candidate | Local status | Score | Decision | Next local action |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-017e0cb02622` | `bazelbuild/rules_android` Windows AAR resource path traversal | `action_entrypoint_repro_ready_bazel_runtime_gated` | 86 | **promote: `local_proof_needed`** | Write a local proof packet that defines the minimal `aar_import` reproduction, expected containment invariant, path cases, and helper-hardening regression tests. Do not install toolchains or run Bazel unless separately approved. |
| 2 | `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-60f499367ecf` | `bazelbuild/rules_android` Windows AAR resource path traversal | `verified_patch_candidate_unsubmitted` | 82 | hold as same-family backup | Reuse only if rank 1 is killed; avoid promoting two candidates from the same family. |
| 3 | `pe-ledger-bazelbuild-rules_android-aar-resource-zip-slip-win-de60afb752e0` | `bazelbuild/rules_android` AAR resource zip-slip Windows extraction | `partial_verified_patch_candidate_unsubmitted` | 78 | hold | Complete helper-hardening proof design after the promoted path-traversal packet, if still distinct. |
| 4 | `pe-ledger-google-certificate-transparency-go-get-entries-res-29e093c10c2a` | `google/certificate-transparency-go` get-entries response cardinality validation | `verified_patch_candidate_unsubmitted` | 74 | hold | Needs a local regression packet and scope/route clarity before private-report drafting. |
| 5 | `pe-ledger-bazelbuild-buildtools-buildozer-label-traversal-wo-0426669d4438` | `bazelbuild/buildtools` buildozer label traversal workspace escape | `verified_patch_candidate_unsubmitted` | 73 | hold | Needs first-party untrusted-label automation evidence from local sources before promotion. |
| 6 | `pe-ledger-bazelbuild_rules_android_aar_resource_zip_slip_sta-b2eae39b165b` | `bazelbuild_rules_android` AAR resource zip-slip static review | `draft_hypothesis_not_submission_ready` | 68 | hold | Lower confidence duplicate/same-family row; keep as supporting evidence only. |
| 7 | `pe-ledger-google-certificate-transparency-go-get-entries-ove-7f64f49eed42` | `google/certificate-transparency-go` get-entries overcount validation gap | `draft_hypothesis_not_submission_ready` | 63 | hold | Build a cleaner local regression patch plan before promotion. |
| 8 | `pe-ledger-bazelbuild-buildtools-buildozer-label-traversal-wo-e0e7682d2503` | `bazelbuild/buildtools` buildozer label traversal workspace escape | `draft_hypothesis_not_submission_ready` | 61 | hold | Same-family lower maturity row; use as context only. |
| 9 | `pe-ledger-golang_crypto_static_review_scout_20260613_1548-77ce36c4f6ee` | `golang_crypto` oversized-agent-frame scout | `fresh_lane_recorded_not_promoted` | 54 | hold | Needs a local oversized-frame probe and exposure-path evidence. |
| 10 | `pe-report-google-oss-static-review-shortlist-dbeac8a17965` | Google OSS static review shortlist | `imported` | 52 | source pool | Useful for future sourcing, not a single proof candidate. |
| 11 | `pe-report-security-bounty-source-scan-032255bc416b` | Security bounty source scan | `imported` | 49 | source pool | Broad scout artifact; not promoted until narrowed to one target class. |
| 12 | `pe-report-issuehunt-security-program-scan-eaea569f83ac` | IssueHunt security program scan | `imported` | 42 | scope blocked | Needs program-page scope review through approved route before candidate work. |
| 13 | `pe-report-sherlock-contest-detail-c507970e8545` | Sherlock contest detail | `imported` | 38 | scope blocked | Contest-specific route and timing are not locally proven for this lane step. |
| 14 | `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-28880407640f` | `bazelbuild/rules_android` Windows AAR resource path traversal | `submission_rules_gate_not_cleared` | 35 | gate evidence only | Use only as a reminder that submission rules are blocked. |
| 15 | `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-0fe9bce52771` | `bazelbuild/rules_android` Windows AAR resource path traversal | `private_report_draft_gated_user_approval` | 34 | gate evidence only | Do not draft for delivery; route remains gated. |
| 16 | `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-65a966d00227` | `bazelbuild/rules_android` Windows AAR resource path traversal | `private_report_route_gated_no_external_action` | 33 | gate evidence only | Do not submit externally; route remains gated. |
| 17 | `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-d02caa323f08` | `bazelbuild/rules_android` Windows AAR resource path traversal | `record_reachability_boundary_unsubmitted` | 32 | gate evidence only | Toolchain/runtime enablement is not approved. |
| 18 | `pe-report-submitted-security-advisory-monitor-391de16b380f` | Submitted security advisory monitor | `rejected` | 10 | exclude | Not an active proof candidate for this lane refresh. |
| 19 | `pe-ledger-google-go-github-request-and-redirect-handling-rev-b5058cae0c0d` | `google/go-github` request/redirect handling review | `kill_hypothesis_already_mitigated` | 0 | kill | Local evidence says do not submit; keep killed. |
| 20 | `evidence-agent-company-atlas-scope-run-v1-20260617` | Scope Run Atlas minigame validation | `complete` | 0 | non-security-lane artifact | Ignore for source promotion; not a bounty/private-report candidate. |

## Promoted Candidate

Promoted evidence ID: `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-017e0cb02622`

Promoted status: `local_proof_needed`

Reason: it has the strongest local maturity signal in the imported evidence set (`action_entrypoint_repro_ready_bazel_runtime_gated`), a credible traversal/security-boundary theme, and a concrete local-only next step that can be written as a proof packet without touching a live target or submitting a report.

Required next local proof packet:

| Field | Requirement |
| --- | --- |
| Candidate | `bazelbuild/rules_android` Windows AAR resource path traversal |
| Local proof goal | Define the minimal `aar_import` or helper-level reproduction design and the path-containment invariant |
| Test cases | Absolute paths, drive-qualified paths, backslash separators, empty segments, `.`, `..`, nested traversal, and normal resource paths |
| Expected safe behavior | Reject or normalize any AAR resource entry that escapes the intended extraction/resource root |
| Evidence source | Local ledger/control-plane evidence only; no live repository lookup in this step |
| Blockers | Bazel/Java runtime execution, current program scope, duplicate review, private route, and user/report-submission approval remain blocked |

## Non-Promoted Candidate Handling

All other candidates are held, source-pooled, scope-blocked, gate-only, excluded, or killed as listed above. No second candidate is promoted in this packet.

## Gate Posture

The promoted candidate is not submission-ready. It remains blocked from any private report, public issue/PR, advisory, or program contact until:

1. A local proof packet exists and passes the readiness evidence standard.
2. Scope and allowed testing are verified through approved evidence.
3. Duplicate/known-issue review is complete or explicitly accepted as incomplete by the gate owner.
4. The user approves the exact route and report text.
5. `security_report_submission_gate` is reviewed and cleared.
6. Any browser/account/API step has a separately approved service request.

## Next Action

Write `security-rules-android-aar-traversal-local-proof-plan-v1-20260621.md` as a local-only proof packet for `pe-ledger-bazelbuild-rules_android-windows-aar-resource-path-017e0cb02622`. The packet should describe fixtures, expected behavior, rejection criteria, and gate blockers; it should not run Bazel, fetch code, contact programs, submit reports, or approve any route.
