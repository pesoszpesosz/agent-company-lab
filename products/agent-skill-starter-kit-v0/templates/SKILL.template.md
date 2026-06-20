---
name: "{{skill_name}}"
description: "{{one_sentence_trigger_and_value}}"
---

# {{Skill Name}}

## Purpose

Describe the repeatable job this skill helps an agent do. Keep it narrow enough that a future agent can tell when to use it and when to leave it alone.

Good scope:

- one domain;
- one artifact family;
- one clear set of allowed actions;
- explicit stop gates.

Avoid:

- vague "do everything" skills;
- unreviewed account, payment, marketplace, or public-action steps;
- workflows that require private data without a handling rule.

## Use When

- {{trigger_condition_1}}
- {{trigger_condition_2}}
- {{trigger_condition_3}}

## Do Not Use When

- The task belongs to another lane or owner.
- The task requires account creation, seller setup, payment setup, public submission, outreach, posting, commenting, browser side effects, credentials, private data, or paid API/model execution without approval.
- The user asks for legal, tax, financial, medical, security submission, or regulated advice beyond local drafting and review support.

## Inputs

Required:

- `{{input_name}}`: {{input_description}}
- `{{artifact_destination}}`: local path where outputs should be saved

Optional:

- `{{optional_input}}`: {{optional_input_description}}

## Allowed Actions

- Read local files relevant to the task.
- Create or edit local draft artifacts.
- Summarize local source material.
- Produce checklists, templates, examples, reports, and acceptance notes.
- Ask for approval if the next step would cross a stop gate.

## Forbidden Actions

- Do not create accounts, accept terms, submit forms, upload files, publish listings, send messages, post publicly, buy, sell, trade, set up payments, handle credentials, or use private data unless a scoped approval exists.
- Do not claim revenue, acceptance, listing approval, compliance, or payout from a draft.
- Do not use copyrighted, trademarked, or restricted assets unless license status is documented.

## Workflow

1. Read the newest user request and lane/task context.
2. Confirm the work fits this skill and does not belong to another owner.
3. Gather only local or explicitly approved sources.
4. Build the requested local artifact.
5. Run the acceptance checklist.
6. Record blockers and exact next gates.
7. Save the final artifact and report.

## Output Contract

Save:

- a primary artifact at `{{primary_artifact_path}}`;
- a short report at `{{report_path}}`;
- a gate checklist if any external, account, payment, public, API, or credential step remains.

The report must include:

- what was built;
- source material used;
- acceptance check result;
- unresolved gates;
- next local-only action.

## Acceptance Checks

- [ ] The output is local and reproducible.
- [ ] No external side effects occurred.
- [ ] All gates are named.
- [ ] Examples avoid real private data.
- [ ] The artifact can be reviewed without marketplace or account access.
- [ ] The next action is either local-only or explicitly approval-gated.
