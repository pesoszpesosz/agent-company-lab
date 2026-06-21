# YouTube Source Material Intake Routing Procedure V2

Generated UTC: 2026-06-21T12:16:04Z
Owner lane: `premium_customer_intake`
Target lane: `youtube_content_channels`
Owner agent: `premium-customer-intake-agent-20260620`
Target owner: `lane-manager-youtube_content_channels-20260620`
Status: `local_procedure_ready`
JSON mirror: `E:\agent-company-lab\reports\youtube-source-material-intake-routing-procedure-v2-20260621.json`

## Purpose

Route user-supplied YouTube videos, channels, transcripts, screenshots, creator notes, title lists, thumbnails, comments, trend links, or adjacent source materials into the YouTube lane without putting raw material in the CEO context window and without copying the source too closely.

## Intake Contract

Every source-material intake packet must include:

| Field | Requirement |
| --- | --- |
| `input_id` | Stable customer input id, preferably `customer-input-youtube-source-material-YYYYMMDD-NNN`. |
| `received_utc` | UTC timestamp when intake captured the material. |
| `raw_material_path_or_reference` | Local preserved file path or user-provided reference. Do not paste raw transcript into CEO context. |
| `source_type` | One of `youtube_video`, `youtube_channel`, `transcript`, `screenshot`, `thumbnail`, `title_bank`, `comment_thread`, `trend_reference`, `notes`, `mixed_sources`, or `other`. |
| `provided_by` | Usually `premium_customer`. |
| `why_it_might_help` | One to three sentences from the customer or intake agent. |
| `allowed_use` | One of `pattern_extraction`, `inspiration_only`, `fact_reference`, `needs_source_review`, or `do_not_use_until_reviewed`. |
| `raw_context_boundary` | Confirm raw material remains in `intake/customer/dropbox/` or referenced artifact only. |
| `compact_source_capsule` | Short summary for the lane and CEO surfaces. |
| `extractable_patterns` | Hook, structure, pacing, audience, topic angle, retention device, monetization clue, production pattern, or distribution clue. |
| `do_not_copy_notes` | Explicit notes on wording, persona, structure, visuals, music, title shape, thumbnail composition, or claim patterns not to reuse directly. |
| `target_artifact` | Smallest useful lane artifact: `script_brief`, `title_bank`, `thumbnail_brief`, `source_plan`, `content_gap_note`, `risk_review`, or `production_manifest_update`. |
| `human_action_needed` | True only when source rights, account access, paid data, KYC, billing, legal, or upload approval requires the user. |
| `revisit_condition` | Concrete condition for parked material, such as `source_review_complete`, `customer_confirms_allowed_use`, or `lane_owner_selects_target_episode`. |

## Procedure

1. Preserve raw material before interpretation.
   Store files, copied notes, transcripts, screenshots, or long pasted material in `E:\agent-company-lab\intake\customer\dropbox\` or record an existing referenced artifact. The CEO capsule may mention the source exists, but must not include raw transcripts, long copied notes, screenshots, or detailed source text.

2. Classify the source and allowed use.
   If the customer supplied ownership or permission details, record them. If rights are unclear, set `allowed_use` to `needs_source_review`; do not reject the input just because the source needs review.

3. Produce a compact source capsule.
   The capsule should fit in the CEO window and include only: intent, source type, usefulness hypothesis, target lane, target artifact, use boundary, status, next action, and whether human action is needed.

4. Route to the smallest YouTube lane artifact.
   Prefer a narrow artifact over a broad research task. A single video can become one script brief, a title-bank delta, a thumbnail pattern note, a production-risk note, or a source-plan update.

5. Apply the no-copy transform.
   Extract lessons rather than source material: audience promise, hook mechanism, pacing pattern, retention move, proof style, objection handled, monetization path, or production constraint. Do not copy wording, title structure, thumbnail layout, music, voice, creator persona, unique framing, or visual identity.

6. Synthesize lane follow-up.
   Use the existing premium customer follow-up flow so `youtube_content_channels` receives a lane-owned task or packet. Existing owner `lane-manager-youtube_content_channels-20260620` should acknowledge, start local work, park with a revisit condition, or request a CEO decision-batch item.

7. Update the customer.
   Emit a compact customer update that says where the material was preserved, which lane received the capsule, what artifact is next, and what gate or revisit condition applies.

## Compact Capsule Shape

```json
{
  "input_id": "customer-input-youtube-source-material-YYYYMMDD-NNN",
  "intent": "Use customer-provided source material to improve YouTube content production.",
  "source_type": "youtube_video",
  "raw_material_location": "preserved_outside_ceo_context",
  "target_lane_id": "youtube_content_channels",
  "target_owner_agent_id": "lane-manager-youtube_content_channels-20260620",
  "target_artifact": "script_brief",
  "summary": "Short usefulness hypothesis, not a transcript.",
  "allowed_use": "pattern_extraction",
  "do_not_copy": ["wording", "thumbnail_design", "creator_persona"],
  "status": "routed",
  "next_action": "Create one local script brief or park with source-review condition.",
  "human_action_needed": false
}
```

## Routing Outcomes

| Condition | Route |
| --- | --- |
| Clear YouTube content pattern | `youtube_content_channels` with target artifact `script_brief`, `title_bank`, or `thumbnail_brief`. |
| Useful but rights unclear | `youtube_content_channels` plus `needs_source_review`; park with `source_review_complete`. |
| Source implies account, upload, comment, channel creation, paid tool, or browser action | Create or reference a service-gated packet; do not execute the action. |
| Source is broad business research, not YouTube-specific | Route to the narrowest matching lane and include YouTube only as secondary if relevant. |
| Duplicate source with new angle | Route the new angle and link prior material; do not reject as duplicate if it adds information. |
| Unsafe, illegal, spammy, impossible, or out of scope | Record reason and stop; rejection remains exceptional. |

## Customer Update Template

```text
Received the YouTube/source material and preserved the raw context outside the CEO window.
Routed compact capsule to `youtube_content_channels`.
Next artifact: `<target_artifact>`.
Use boundary: `<allowed_use>`; no copying of source wording, visuals, persona, or protected material.
Human action needed: `<true|false>`.
Revisit condition: `<condition>`.
```

## Zero Side Effect Boundary

- Browser sessions started: 0
- Videos opened or downloaded: 0
- Transcripts scraped: 0
- Accounts or channels created: 0
- Uploads, comments, posts, or public actions: 0
- Model/API/MCP calls: 0
- Payments, trades, or paid tools: 0
- Worker/runtime/queue starts: 0
- External side effects: false

## Next Local Action

When the next user-supplied YouTube/source material arrives, create the preserved raw packet in `intake/customer/dropbox/`, run the premium customer router, synthesize the YouTube follow-up, and monitor acknowledgement. If the source cannot be used immediately, park it with a named revisit condition instead of rejecting it.
