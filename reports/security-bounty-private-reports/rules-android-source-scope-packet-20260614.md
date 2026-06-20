# rules_android source-only reachability and scope packet - 2026-06-14

Lane: `security_bounty_private_reports`
Task: `task-security-rules-android-scope-packet-20260614`
Agent: `lane-manager-security_bounty_private_reports-019ec612`

## Boundary

This packet is local/source-only.

Actions not taken:

- No live target testing.
- No exploit attempt beyond reading prior saved local proof artifacts.
- No Bazel, Bazelisk, Java, Android toolchain, or dependency installation.
- No browser login, account action, OAuth flow, Bug Hunters submission, disclosure email, PR, issue, public comment, or payout chasing.
- No work on `submitted_bounty_payouts`, RustChain, Charles, or GitHub payout monitoring.

## Sources

Program and lane sources:

- `E:\profit-edge-lab\reports\security-bounty-source-scan-latest.md`
- `E:\profit-edge-lab\reports\google-oss-static-review-shortlist-latest.md`
- `E:\agent-company-lab\reports\lane-startup\security_bounty_private_reports-startup-20260614.md`
- `E:\agent-company-lab\reports\manager-packets\security_bounty_private_reports-manager-packet.md`

Prior local proof and route artifacts:

- `E:\profit-edge-lab\reports\bazelbuild-rules-android-aar-resource-zip-slip-static-review-20260613-162000.md`
- `E:\profit-edge-lab\reports\bazelbuild-rules-android-aar-resource-zip-slip-fix-candidate-20260613-163000.md`
- `E:\profit-edge-lab\reports\bazelbuild-rules-android-aar-resource-zip-slip-real-rule-repro-packet-20260613-164000.md`
- `E:\profit-edge-lab\reports\bazelbuild-rules-android-aar-resource-zip-slip-route-choice-20260613-163414.md`
- `E:\profit-edge-lab\reports\google-oss-vrp-rules-gate-rules-android-aar-20260613-163352.md`
- `E:\profit-edge-lab\reports\bazelbuild-rules-android-aar-resource-zip-slip-private-vrp-draft-20260613-163124.md`

Local source checkout:

- Repository: `https://github.com/bazelbuild/rules_android`
- Local checkout: `E:\profit-edge-lab\source-cache\bazelbuild-rules-android-review-20260613`
- Reviewed commit from saved proof packet: `e969130525e34fbc5a6b5ff6ed65b934298b449a`

## Program and rules evidence

The saved source scan lists Google Open Source Software Vulnerability Rewards Program as a security source with:

- Gate: `static_code_review_only`
- Amount reference: `up to $31,337`
- Official source: `https://bughunters.google.com/open-source-security`
- Rules source: `https://bughunters.google.com/about/rules/open-source/google-open-source-software-vulnerability-reward-program-rules`
- Risk note: high upside, high bar; prioritize supply-chain compromise, design issues causing product vulnerabilities, and reproducible security impact in Google-owned public OSS repositories.

The Google OSS static-review shortlist includes:

- `bazelbuild/rules_android`
- Score: `89`
- Gate: `static_review_candidate`
- Language: Java
- Review mode: local static source review only; no live targets, no brute force, no public disclosure.

The saved route memo adds the important scope caveat:

- Current Google Bug Hunters materials were checked locally/read-only.
- `bazelbuild/rules_android` was not confirmed in the public Tier 0/1 table in that saved check.
- This does not prove out-of-scope status, but it means reward scope and submission route must be explicitly checked before any external action.

The saved rules-gate memo adds another gate:

- A static fetch reached the Google OSS VRP rules page, but the full rules body was client-rendered and not fully validated from local static fetch.
- Submission remains gated on rendered rules review, current scope validation, and explicit user approval.

## Source-only reachability

This source review confirms the path from a user-supplied `.aar` label to `tools/android/aar_resources_extractor.py` without running a new exploit or build.

| Step | Source evidence | Local conclusion |
| ---: | --- | --- |
| 1 | `rules/aar_import/attrs.bzl:27-30` defines `aar = attr.label(allow_single_file = [".aar"], mandatory = True)`. | `aar_import` requires a caller-supplied `.aar` file. |
| 2 | `rules/aar_import/rule.bzl:50-57` exposes `aar_import = rule(...)` with `_impl_proxy`. | The attribute is used through the public Starlark rule. |
| 3 | `rules/aar_import/impl.bzl:470` reads `aar = _utils.only(ctx.files.aar)`. | The selected `.aar` becomes the action input for implementation logic. |
| 4 | `rules/aar_import/impl.bzl:490-498` calls `_process_resources(...)` with `aar` and `_get_android_toolchain(ctx).aar_resources_extractor.files_to_run`. | Resource processing routes the same `.aar` to the configured extractor tool. |
| 5 | `rules/aar_import/impl.bzl:136-153` creates resource and asset tree artifacts, then calls `_extract_resources(...)`. | Declared output directories are tree artifacts under the `_aar/unzipped/...` shape. |
| 6 | `rules/aar_import/impl.bzl:96-112` builds an action with `--input_aar`, `--output_res_dir`, `--output_assets_dir`, input `[aar]`, and outputs `[out_resources_dir, out_assets_dir]`. | The extractor action receives the crafted AAR and declared output trees. |
| 7 | `toolchains/android/toolchain.bzl:52-56` defaults `aar_resources_extractor` to `//tools/android:aar_resources_extractor`. | The default tool is the local extractor under review. |
| 8 | `tools/android/aar_resources_extractor.py:47-53`, `60-66`, and `78-83` iterate entries starting with `res/`, `assets/`, or `data-binding/`. | Prefix filtering alone permits names that begin with an allowed prefix but contain parent traversal segments later. |
| 9 | `tools/android/aar_resources_extractor.py:105-131` uses a Windows branch that computes `fullpath = os.path.normpath(os.path.join(abs_output_dir, name))`, creates a junction to `os.path.dirname(fullpath)`, and writes to `os.path.basename(fullpath)` without checking containment under `abs_output_dir`. | On Windows, a member name such as `res/../../outside_marker.txt` can normalize outside the declared output directory before the write. |
| 10 | Saved real-rule packet shows a deterministic action-entrypoint harness with `res/../../outside_marker.txt` writing outside the target output tree and a patch candidate that rejects paths escaping the output directory. | The saved proof supports a private triage draft, but it is still not a full Bazel sandbox or remote-execution proof. |

## Local-code boundary

What this packet establishes:

- A source-only path exists from `aar_import` `.aar` input to `aar_resources_extractor.py`.
- The vulnerable-looking path is the Windows extraction branch in `ExtractOneFile`.
- The prior saved action-entrypoint proof mirrors the extractor action arguments and declared output shape.
- The prior saved fix candidate has focused regression evidence and rejects escaping output paths.

What this packet does not establish:

- It does not prove a full Bazel build sandbox escape.
- It does not prove remote execution cache poisoning.
- It does not prove Google OSS VRP reward eligibility.
- It does not validate current rendered Bug Hunters rules.
- It does not perform any new exploit, live target test, account action, or external report.

## Risk and impact framing

Current local framing:

- This is at least a Windows-specific build-output containment issue in the `aar_import` extractor action.
- The stronger security narrative is supply-chain adjacent: a crafted third-party AAR dependency processed by `aar_import` may create files outside the declared resource output tree.
- The saved proof says the write lands outside the target output tree but inside a broader `_aar/unzipped/resources` parent, so the impact must be stated with caveats.

Impact caveats:

- The local lab does not have a true Bazel/Java/Android toolchain reproduction for the complete build action.
- Bazel sandboxing, execroot layout, remote-execution validation, and downstream consumption behavior remain open questions.
- Private report value depends on whether Google triage accepts action-entrypoint containment evidence or requires full rule execution.

## Private-report gate notes

Do not submit now.

External action gates before any report:

- Confirm current Google OSS VRP rendered rules and scope for `bazelbuild/rules_android`.
- Confirm whether the Google Bug Hunters route is available and acceptable without legal, KYC, tax, billing, payout, or account-contract commitments.
- Decide whether action-entrypoint reproduction is sufficient or whether a full Bazel/Java reproduction is required first.
- Use the lane service bureau gate for `security_report_submission` before any private report.
- Use a separate scoped gate before any browser login, account registration, public PR, public issue, or maintainer-facing comment.

Route recommendation:

- Keep private-report-first posture while the issue has possible supply-chain/build containment implications.
- Do not open a public hardening PR or public issue before private triage route is explicitly approved or disclosure risk is deemed acceptable.
- If current Google OSS VRP scope is not clean, park the report and consider a public hardening route only after explicit approval.

## Recommended next action

The local packet is complete for the assigned task.

Next decision gate:

- Either request a scoped service review for Google OSS VRP rendered rules and submission route, or
- Request/approve a purely local toolchain reproduction task for Bazel/Java/Android rule execution, with no submission, account action, or live target testing.

Realized USD: `0`

External actions taken: none.
