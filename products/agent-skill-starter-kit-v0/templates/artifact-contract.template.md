# Artifact Contract Template

Artifact name: `{{artifact_name}}`  
Owner lane: `{{lane_id}}`  
Task: `{{task_id}}`  
Primary path: `{{primary_path}}`  
Status: `draft | ready_for_review | complete | blocked`  

## Purpose

{{artifact_purpose}}

## Inputs Used

| Input | Source | Gate status |
| --- | --- | --- |
| {{input_1}} | {{local_or_approved_source}} | {{status}} |
| {{input_2}} | {{local_or_approved_source}} | {{status}} |

## Required Sections

- [ ] Summary
- [ ] Buyer/user problem or operational problem
- [ ] Build artifact or deliverable description
- [ ] Source list
- [ ] Stop gates
- [ ] Acceptance checks
- [ ] Next action

## Quality Bar

- specific enough for another agent to continue;
- no hidden external action;
- no unsupported revenue, compliance, performance, or acceptance claims;
- no private data or credentials;
- exact blockers and next approvals are named.

## Trace Fields

- `api_calls`: `false` unless approved and recorded
- `external_side_effects`: `false` unless explicitly approved and recorded
- `realized_usd`: `0` unless actual received money exists
- `service_request_status`: `needs_review | approved | complete | none`
