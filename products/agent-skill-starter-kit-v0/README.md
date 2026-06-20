# Agent Skill Starter Kit v0

Status: local product proof bundle  
Lane: `digital_products_templates_plugins`  
Built for: `task-digital-products-agent-skill-starter-kit-v0-20260614`  

## What This Is

Agent Skill Starter Kit v0 is a Markdown bundle for builders who want to package repeatable AI-agent workflows with clear instructions, stop gates, artifacts, and acceptance checks.

The kit is designed for local adaptation. It is not a marketplace listing, not a seller account asset, and not a revenue claim.

## Buyer Problem

Many builders can write one-off prompts, but they struggle to turn a workflow into a reusable agent skill or operating packet:

- the skill description is too vague;
- examples do not show the expected artifact;
- stop gates for accounts, payments, browser actions, credentials, public posts, and APIs are missing;
- acceptance checks are implicit;
- reusable handoff and review formats are absent.

## Contents

```text
agent-skill-starter-kit-v0/
  README.md
  templates/
    SKILL.template.md
    gate-checklist.template.md
    service-request-checklist.template.md
    artifact-contract.template.md
    acceptance-review.template.md
  examples/
    local-research-skill/
      SKILL.md
      sample-output.md
  docs/
    buyer-guide.md
    license-and-ip-note.md
    screenshot-plan.md
    listing-draft.md
```

## Quick Start

1. Copy `templates/SKILL.template.md` into a new skill folder as `SKILL.md`.
2. Fill in the skill name, description, trigger rules, inputs, allowed actions, forbidden actions, workflow, and output contract.
3. Copy `templates/gate-checklist.template.md` beside the skill and mark every gate as allowed, blocked, or approval required.
4. Use `templates/artifact-contract.template.md` to define exactly what the skill must save.
5. Use `templates/acceptance-review.template.md` to verify the output before reuse or publication.

## Stop Gates

Do not use this kit to bypass platform, legal, financial, account, credential, or public-action review. Any workflow that touches the following requires an explicit approved service request or human approval:

- account creation, login, settings changes, seller profiles, or terms acceptance;
- marketplace listings, uploads, submissions, messages, reviews, comments, or public promotion;
- payment, payout, tax, KYC, billing, wallet, purchase, deposit, or withdrawal activity;
- credential, token, cookie, OTP, private file, or secret handling;
- paid APIs, model calls, premium data, scraping against terms, or rate-limit bypass;
- bounty claims, GitHub public actions, outreach, or anything in another lane.

## Acceptance Standard

The v0 bundle is complete when:

- every required file exists;
- examples are fictional or local-only;
- all template fields are fillable without external accounts;
- the gate checklist includes account, payment, legal/KYC/tax, public action, browser, model/API, data/API, outreach, secrets, IP/license, and lane-boundary gates;
- the listing draft avoids guaranteed earnings, unsupported claims, and platform endorsement;
- the screenshot plan names only local screenshots until marketplace review is approved.

## Local Distribution Readiness

This folder can be zipped for internal review only. Before any sale, listing, upload, or public promotion, the lane needs:

- approved browser-read-only marketplace terms research;
- legal/KYC/tax/payment review;
- public listing/action approval;
- IP/license review;
- final human approval of price, refund language, seller identity, and platform route.
