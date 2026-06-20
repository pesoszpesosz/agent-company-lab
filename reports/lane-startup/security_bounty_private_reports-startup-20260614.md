# security_bounty_private_reports startup memo - 2026-06-14

Agent: `lane-manager-security_bounty_private_reports-019ec612`
Thread: `019ec612-4cf1-7601-8818-ddd3028a06f4`
Lane: `security_bounty_private_reports`
Task: `task-security_bounty_private_reports-startup-20260614`

## Scope and gates

This manager owns only `security_bounty_private_reports` in `E:\agent-company-lab`.
It does not own `submitted_bounty_payouts`, RustChain, Charles, GitHub payout chasing, or any public submission lane.

Allowed for this startup:

- Local report review.
- Public-source and local-clone static review already present on disk.
- Local ranking, memo, artifact, outcome, and trace records.

Hard stops:

- No live target testing.
- No report submission, disclosure email, PR, issue, public comment, bounty claim, or account action.
- No legal, KYC, tax, billing, payout, or payment action.
- No browser public action.
- No model/API execution or external worker action without an approved service request for the exact scope.

Prompt/eval guidance used:

- `E:\agent-company-lab\reports\prompt-eval-review-latest.md` marks `lane-manager-startup-v2-20260614` active.
- The active manager prompt passed the local static safety evaluator with score `1.0` across 6 safety cases.
- This memo follows the active prompt's one-lane, one-task, local-artifact, service-gated workflow.

## Sources read

- `E:\agent-company-lab\README.md`
- `E:\agent-company-lab\reports\manager-packets\security_bounty_private_reports-manager-packet.md`
- `E:\agent-company-lab\reports\lane-manager-thread-launch-manifest-latest.md`
- `E:\agent-company-lab\reports\prompt-eval-review-latest.md`
- `E:\profit-edge-lab\reports\security-bounty-source-scan-latest.md`
- `E:\profit-edge-lab\reports\google-oss-static-review-shortlist-latest.md`
- `E:\profit-edge-lab\reports\issuehunt-security-program-scan-latest.md`
- `E:\profit-edge-lab\reports\sherlock-contest-1259-detail-latest.md`
- `E:\profit-edge-lab\reports\submitted-security-advisory-monitor-latest.md`
- Selected local proof packets and ledger rows under `E:\profit-edge-lab\reports\` and `E:\profit-edge-lab\opportunities\opportunity-ledger.jsonl`.

## Ranking method

Ranking weights are qualitative and local-only:

- Program scope: Is the target clearly within a known program or source directory?
- Evidence quality: Is there a saved local proof, reviewed commit, patch, tests, and route memo?
- Payout path: Is there a plausible reward venue and amount, without assuming payout?
- Disclosure route: Is the private reporting route clear enough to use after explicit approval?
- Gate load: How many blockers remain before any external action could even be considered?

## Imported source ranking

| Rank | Source | Program scope | Evidence quality | Payout path | Disclosure route | Gate status | Decision |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | Google OSS VRP - `bazelbuild/rules_android` AAR resource traversal | Google OSS style scope is plausible, but `rules_android` was not confirmed in the public Tier 0/1 table in the saved route memo. | Strongest local bundle: Windows extractor proof, action-entrypoint repro packet, patch candidate, route memo, private draft, reviewed commit `e969130525e34fbc5a6b5ff6ed65b934298b449a`. | Plausible Google OSS VRP path, public source scan lists Google OSS max up to `$31,337`, but reward eligibility is unconfirmed. | Private Google Bug Hunters route only after rendered rules/account review and explicit user approval. Public PR/issue deferred to avoid premature disclosure. | Full Bazel/Java repro unavailable locally; scope and report route not cleared. | Top local proof candidate. Next work should be source-only reachability consolidation or true Bazel repro only if the local toolchain gate is explicitly approved. |
| 2 | Google OSS VRP - `google/certificate-transparency-go` get-entries cardinality | Google-owned public OSS repo from the static-review lane. | Strong local patch candidate: client and scanner tests passed at reviewed commit `257bdb3be3bbbf838a3c199fb38e11f08b9fa7c6`. | Possible Google OSS VRP, but payout depends on accepting malicious/compromised CT log response handling as reportable security impact. | Private Google Bug Hunters versus public hardening route remains undecided and approval-gated. | Impact framing needs a concrete Google-owned consumer or accepted threat model. | Best low-friction local follow-up if the lane wants cleaner tests before route work. |
| 3 | Google OSS VRP - `bazelbuild/buildtools` buildozer label traversal | Bazelbuild repo appears in the Google OSS static-review set; specific reward tier not confirmed here. | Strong local patch candidate: focused and full edit tests passed; CLI proof no longer rewrites outside `BUILD` file at commit `84fa6c32aee6964c1d71ec7db96755ca6b6287f2`. | Possible Google OSS VRP if a supply-chain automation path with untrusted labels is proven; otherwise public hardening only. | Private report or public hardening route both gated on explicit user approval. | Needs first-party automation exposure evidence. | Keep as third proof candidate; do not submit without stronger impact framing. |
| 4 | Google OSS VRP - legacy `buildtools` symlink write-through packet | Current upstream commit was checked in saved addendum; public duplicate search found no obvious issue/PR. | Private packet, fix patch, and WSL proof exist, but later generic buildtools review warns not to reopen weak/generic buildtools rows without a clean private route. | Possible Google OSS VRP, but collision and route risk remain. | Private Google route only; no public issue/PR first. | Conflicting triage history makes this less clean than the newer buildozer row. | Park behind the current top three unless a route owner wants to reconcile the packet. |
| 5 | IssueHunt programs - SORACOM first | Scope is comparatively clear for SORACOM API/domain/SPA targets; source scan flags small scope and English-readable rules. | Directory/rules evidence only; no local code proof or non-invasive hypothesis yet. | Max JPY 300,000 for top practical candidates; bitFlyer/bitbank show higher rewards but heavy account/KYC risk. | IssueHunt account/report route required; user approval needed before account setup or testing. | No live testing allowed; no account route cleared. | Good source for future rules-reading task, not first proof task. |
| 6 | Intersect/Cardano OSS bounty and existing submitted advisories | Source scan reports 45 in-scope Intersect repos and high/critical rewards; submitted advisory monitor shows two GHSA items in triage. | Existing advisory monitor is history only for this startup; no new local proof assessed here. | Public source scan lists critical `10,000-20,000` and high `5,000-10,000`; actual path depends on program terms and maintainer handling. | Private advisory route exists historically, but this manager must not submit or chase anything without approval. | Submitted advisory monitoring is not this first task and can drift into payout chasing. | Park. Use only as background until a scoped local static-review task is approved. |
| 7 | Google OSS VRP - `golang/crypto` scout | Google-owned public OSS repo from shortlist. | Scout found no submission-ready issue; only an SSH agent oversized-frame research edge remains. | Possible Google OSS VRP only if untrusted exposure and impact are proven. | No route until proof exists. | Needs local probe plus first-party untrusted boundary evidence. | Research backlog, not current proof candidate. |
| 8 | Sherlock DRE App - dreUSD contest | Contest scope is specific to dreUSD contracts and reward is visible. | No local public repo access; saved detail says contest repo access is not public or requires auth. | `60,000 USDC` contest reward pool, but KYC is required. | Sherlock registration/KYC/repo access required. | Blocked by registration/KYC/repo access and contest account gates. | Do not work now. High headline value, poor lane fit under current hard stop. |
| 9 | Immunefi directory and audit competitions | Directory has many programs and high visible max bounty, but no selected program scope. | Directory-level evidence only. | Very high theoretical max, but no selected local proof. | Program-specific private route required. | Needs program selection, terms review, and often account/KYC-style gates. | Monitor/source discovery only. |
| 10 | Google OSS VRP - `google/go-github` request/redirect review | Google-owned public OSS repo. | Focused local review and tests found existing mitigations. | No payout path because the hypothesis is killed. | No disclosure route needed. | N/A. | Do not submit or reopen this hypothesis. |

## Concrete hypothesis ranking

| Rank | Hypothesis | Local artifact | Why it ranks here | Next local-only action |
| ---: | --- | --- | --- | --- |
| 1 | `bazelbuild/rules_android` Windows AAR resource traversal | `E:\profit-edge-lab\reports\bazelbuild-rules-android-aar-resource-zip-slip-real-rule-repro-packet-20260613-164000.md` | Best evidence bundle and most supply-chain-shaped impact, but still route/toolchain gated. | Produce a source-only reachability checklist from the local clone and saved packet; stop before installing Bazel/Java or submitting. |
| 2 | `google/certificate-transparency-go` get-entries cardinality validation | `E:\profit-edge-lab\reports\google-ct-go-getentries-cardinality-fix-candidate-20260613-161725.md` | Clean tests and patch; impact is real but needs threat-model framing. | Draft a local impact-routing note comparing private VRP versus public hardening, using only saved tests and source. |
| 3 | `bazelbuild/buildtools` buildozer label traversal | `E:\profit-edge-lab\reports\bazelbuild-buildtools-buildozer-label-traversal-fix-candidate-20260613-162139.md` | Clean patch and proof; reportability depends on an automation exposure path. | Search local clone/docs for first-party automation that accepts untrusted labels; no GitHub issue/PR. |
| 4 | `buildtools` symlink write-through private packet | `E:\profit-edge-lab\reports\google-oss-buildtools-symlink-write-freshness-addendum-20260612-1359.md` | Packet appears mature but has older/conflicting triage and route risk. | Keep parked until the newer buildtools row is resolved. |
| 5 | `golang/crypto` SSH agent oversized frame edge | `E:\profit-edge-lab\reports\golang-crypto-static-review-scout-20260613-154800.md` | Fresh scout, no vulnerability yet. | Local-only probe plus first-party exposure search if top candidates stall. |
| 6 | `google/go-github` request/redirect handling | `E:\profit-edge-lab\reports\google-go-github-request-redirect-static-review-kill-20260613-165049.md` | Killed by existing mitigations. | Do not reopen. |

## First proof task recommendation

Recommended next task after startup:

`rules_android` source-only reachability and scope packet.

Goal:

- Consolidate the saved Windows extractor proof, action-entrypoint repro packet, private draft, rules gate, and route memo into one local decision packet.
- Verify from local source only that the crafted AAR path reaches `aar_resources_extractor.py` through `aar_import`.
- List exactly what would be needed for a true Bazel/Java repro without performing installation, account action, submission, PR, issue, or live target testing.

Stop condition:

- If the next step requires installing/enabling Bazel, Bazelisk, Java, Android toolchains, browser login, Bug Hunters account review, or external submission, stop and create/request an approved service request for that exact scope.

Fallback if the lane wants lower gate load:

- Use the `certificate-transparency-go` patch candidate to write a local impact-routing note because the saved Go tests already pass and no extra toolchain appears necessary.

## Outcome

Startup complete with local ranking artifact only.

Realized USD: `0`

No external action was taken.
