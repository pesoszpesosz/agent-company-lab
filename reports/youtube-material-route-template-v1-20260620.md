# YouTube Material Route Template V1

Generated UTC: 2026-06-20T17:18:00Z
Owner lane: `premium_customer_intake`
Target lane: `youtube_content_channels`
Status: local intake template
JSON mirror: `E:\agent-company-lab\reports\youtube-material-route-template-v1-20260620.json`

## Purpose

Route customer-provided YouTube videos, references, notes, screenshots, transcripts, or other materials into the YouTube lane without poisoning CEO context or copying source material too closely.

## Required Fields

- `input_id`
- `received_utc`
- `raw_material_path_or_url`
- `provided_by`
- `why_it_might_help`
- `target_channel_experiment`
- `allowed_use`
- `summary_not_transcript`
- `extractable_patterns`
- `do_not_copy_notes`
- `target_artifact`
- `human_action_needed`
- `revisit_condition`

## Transformation Rules

- Summarize the useful pattern; do not paste full transcripts into CEO context.
- Extract structure, audience, hook type, pacing, production pattern, or monetization clue.
- Do not copy wording, title structure, thumbnail design, music, visual identity, or creator persona.
- Route to the smallest target artifact: script brief, title bank, thumbnail brief, source plan, or AR evaluation.
- If source use is unclear, mark `needs_source_review` rather than rejecting.

## Default Route

Customer-provided YouTube material should route:

1. `premium_customer_intake` captures the raw material reference.
2. `youtube_content_channels` receives a context capsule.
3. `knowledge_application_loop_v1` requires an applied artifact or revisit condition.
4. CEO receives only the capsule and applied-knowledge delta.

## Boundary

This template does not open the video, download content, scrape transcripts, copy material, upload, comment, or perform public actions.
