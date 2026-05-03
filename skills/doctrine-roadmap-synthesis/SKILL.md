---
name: doctrine-roadmap-synthesis
description: Consolidate per-doctrine summaries into a prioritised platform roadmap with shipped vs scheduled status and a v1.x priority list.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    summariesDir: directory of <AJP-ID>.md files (the output of skill ajp-doctrine-summary)
  outputSchema:
    file: roadmap.md at repo root
  errorHandling:
    duplicateItems: "deduplicate by item title; cite both source AJPs"
  stateless: true
tools: [Read, Write, Edit]
---

# doctrine-roadmap-synthesis

## Purpose
Take every "Platform improvements" bullet from the per-AJP summaries and produce one prioritised, status-tagged roadmap that the team can work against. Source-trace every item so disagreements can be re-litigated against the doctrine.

## When to use
- After a batch of new or updated AJP summaries is committed.
- Before planning a v1.x iteration of the platform.
- The user asks for "roadmap", "prioritise doctrine items", "what's next".

## Inputs
- All `AJP/SUMMARIES/AJP-*.md` files (the output of `ajp-doctrine-summary`).
- The current platform's shipped feature list (read from the SPA or from previous `roadmap.md`).

## Outputs
- `roadmap.md` at repo root with the structure below.

## Instructions

1. **Read each `AJP/SUMMARIES/AJP-*.md`** and pull the bullets under `## Platform improvements`.
2. **Normalise the status flag** on each item to one of:
   - ✅ Shipped in v1.0
   - 🚧 Scheduled
   - ★ Deep-dive needed (PDF re-read required)
3. **Group by theme**, not by AJP number. Themes proven useful in this repo:
   - Capstone & Conduct (AJP-01, 3, 5)
   - Maritime / Land / Air / Cyber (AJP-3.1, 3.2, 3.3, 3.3.5, 3.20)
   - Joint Targeting (AJP-3.9 — its own theme; it's that load-bearing)
   - Movement & Sustainment (AJP-3.13, 4, 4.3, 4.4, 4.6, 4.10)
   - Force Protection / C-IED / EOD / CWMD (AJP-3.14, 3.15, 3.18, 3.23)
   - Stability / COIN / NEO / HumAss / SFA (AJP-3.7, 3.10.1, 3.16, 3.19, 3.22, 3.24, 3.25, 3.26, 3.27, 3.28)
   - StratCom / InfoOps / MILPA (AJP-6, 10, 10.1, 10.3)
4. **Always source-trace** each item back to one or more AJPs (`| Item | AJP | Status | Notes |`).
5. **List shipped items separately** so reviewers immediately see what's done.
6. **Emit a "next iteration" priority list** of 5–7 items with reasoning. The bar: highest leverage × lowest cost × unlocks downstream.
7. **Carry forward the methodology disclosure** from `AJP/SUMMARIES/README.md` near the top of the roadmap so consumers know which items rest on PDF deep-reads vs structural inference.

## Roadmap skeleton

```markdown
# roadmap.md — Doctrine-Driven Platform Update Plan

**Source:** AJP/SUMMARIES/*  · **Target:** C23_DIANA_NATO_WARFIGHTERS.html
**Methodology disclosure:** <one paragraph; copy from SUMMARIES/README.md>

## 0. Status legend
- ✅ Shipped in v1.0
- 🚧 Scheduled
- ★ Deep-dive needed

## 1. Capstone & Conduct (AJP-01, AJP-3, AJP-5)
| Item | AJP | Status | Notes |
| --- | --- | --- | --- |
| … | … | … | … |

## 2. … (one section per theme) …

## N. Cross-cutting platform improvements (already shipped)
- bullet list of ✅ items, plain prose for the executive summary

## N+1. Implementation priority for the next iteration (v1.1)
1. <highest-leverage item>
2. …
```

## Examples
- See `roadmap.md` at the repo root for a working synthesis of the 33 AJP summaries.

## Anti-patterns
- ❌ A flat unordered list. Themes + a status column are the whole point.
- ❌ Items without a citation. If you can't say which AJP demanded it, the item is your opinion, not doctrine.
- ❌ Burying shipped items inside the scheduled list. Reviewers must see "done" instantly.
- ❌ A roadmap that doesn't end in a priority list. "Everything matters" is no plan.

## References
- `roadmap.md` (output exemplar).
- Skill `ajp-doctrine-summary` (upstream).
