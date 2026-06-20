---
name: local-research-memo
description: Draft a source-backed local research memo from files already present in the workspace, with explicit stop gates and next actions.
---

# Local Research Memo

## Purpose

Use this skill when a user asks for a concise research memo based on local files or explicitly approved local sources. The output is a saved Markdown memo with sources, findings, blockers, and next action.

## Use When

- The task asks for a local memo, summary, or decision packet.
- The relevant sources are local files or already-provided text.
- The next action can remain local-only or approval-gated.

## Do Not Use When

- The user asks for browser research, marketplace inspection, account work, payment setup, public posting, outreach, or API/model execution without approval.
- The task belongs to another lane owner.
- The requested memo would include private data, regulated advice, or unsupported revenue claims.

## Inputs

Required:

- source paths;
- memo destination path;
- decision or question to answer.

Optional:

- required headings;
- gate list;
- acceptance criteria.

## Allowed Actions

- Read local files named by the user or task packet.
- Summarize findings.
- Write a local Markdown memo.
- Record blockers and service-request gates.

## Forbidden Actions

- Do not browse.
- Do not create accounts.
- Do not submit, upload, post, message, purchase, sell, or promote.
- Do not handle credentials, tokens, cookies, private files, or payment details.
- Do not claim realized money unless actual received funds are documented.

## Workflow

1. Confirm the lane and task.
2. Read only the named local sources.
3. Extract the relevant facts and unresolved questions.
4. Draft the memo with sources and gates.
5. Run the acceptance checklist.
6. Save the memo and report the path.

## Output Contract

Save one Markdown memo with:

- summary;
- source list;
- findings;
- blockers;
- stop gates;
- next local action.

## Acceptance Checks

- [ ] The memo cites local source paths.
- [ ] No external side effects occurred.
- [ ] Every blocker has a named gate.
- [ ] The next action is local-only or approval-gated.
