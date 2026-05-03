# C23 DIANA — Agent Skills Catalogue

This directory contains every reusable capability exercised while building the C23 DIANA NATO Warfighters platform, packaged as **Agent Skills** that any Claude / agentic harness can pick up and apply.

## Skill format

Every skill is a directory with a single `SKILL.md` file. The file starts with YAML frontmatter and is then organised into the same sections so callers can locate inputs, instructions and references without parsing prose.

```yaml
---
name: skill-name                  # kebab-case, matches the directory
description: One-sentence trigger # surfaced to model selectors
version: 1.0.0
author: CONFIANZA23
slo:                              # SLO Agent-Skills annotations (Master Prompt ANNEX)
  inputSchema:  …
  outputSchema: …
  errorHandling: …
  stateless: true|false
tools:                            # tools the skill expects to have available
  - Read
  - Write
  - Edit
---
```

All skills are designed to be **modular and stateless**. The defining authority is `make-skill/SKILL.md` — start there if you want to author a new skill in the same style.

## Index

### Foundations & process

| # | Skill | Purpose |
|---|---|---|
| 0 | [`make-skill`](make-skill/SKILL.md) | Meta-skill: how to author a new skill in this catalogue. |
| 1 | [`build-single-file-spa`](build-single-file-spa/SKILL.md) | Build a self-contained HTML SPA with React + Babel-standalone, no bundler. |
| 2 | [`react-babel-pitfalls`](react-babel-pitfalls/SKILL.md) | Avoid the recurring traps of multi-block Babel-standalone setups (e.g. `const` redeclaration). |
| 3 | [`versioning-workflow`](versioning-workflow/SKILL.md) | **v002** — apply the C23 superset versioning rule (every change → new `_vNNN.html`, never delete, never remove features). |
| 4 | [`roadmap-driven-release`](roadmap-driven-release/SKILL.md) | **v002** — pick a prioritised batch from `roadmap.md` and ship it as the next version bump. |
| 4b | [`resumable-execution-state`](resumable-execution-state/SKILL.md) | **v005-09** — persist mid-execution state to `SESSION_STATE.md` so any future session can resume mid-bump. The save-net for multi-version batches. |
| 4c | [`react-hotkeys`](react-hotkeys/SKILL.md) | **v006** — global keyboard shortcuts with input-guarding and a single keydown listener. |
| 4d | [`spa-persistence`](spa-persistence/SKILL.md) | **v006** — localStorage hydration + write-through, named-slot snapshots, undo/redo, clear-all escape hatch. |
| 4e | [`char-budget-respect`](char-budget-respect/SKILL.md) | **NewDraft** — author multi-section text under per-section char limits with per-block live counts and a deterministic 5-pass trim protocol. |

### Mission-editor capabilities

| # | Skill | Purpose |
|---|---|---|
| 5 | [`mission-editor`](mission-editor/SKILL.md) | Un-hardcode mission parameters into a CRUD editor (**19 tabs as of v009**) with JSON import/export. |
| 6 | [`ach-matrix`](ach-matrix/SKILL.md) | ACH matrix (CoA × Evidence). **v003 5-level scale** CC/C/N/I/II. NEUTRAL side admissible since v002. |
| 6b | [`ach-auto-suggest`](ach-auto-suggest/SKILL.md) | **v005** — heuristic auto-scoring of empty ACH cells via keyword overlap; preserves analyst values. |
| 7 | [`joint-targeting-jtc`](joint-targeting-jtc/SKILL.md) | **v002** — implement the AJP-3.9 Joint Targeting Cycle: 6-phase JTC, JPTL CRUD, F2T2EA, CDE, RTL, NSL. |
| 7b | [`roe-gated-execution`](roe-gated-execution/SKILL.md) | **v005** — gate every CoA execution behind a ROE-authorisation modal that surfaces JPTL TST hits + RTL/NSL + CDE. |
| 8 | [`movement-entities`](movement-entities/SKILL.md) | **v002** — MSR / ASR polylines + APOD / SPOD point CRUD per AJP-3.13 / AJP-4.4. |
| 9 | [`posture-indicators`](posture-indicators/SKILL.md) | **v002** — FPCON / CBRN / PNT / CIS-PACE colour-coded top-bar tiles per AJP-3.14 / 3.23 / 3.3 / 6. WX (v005) follows the same pattern. |
| 9b | [`echelon-rollup-and-scoping`](echelon-rollup-and-scoping/SKILL.md) | **v005-08** — tactical/operational/strategic roll-up + per-HQ AOR bbox scoping (CO-01 + CO-02). |
| 9c | [`event-analytics`](event-analytics/SKILL.md) | **v008-09** — three companion analytics over event streams: anomaly detection (rules), correlation (clusters), 2nd/3rd-order cascades. |
| 9d | [`live-feed-adapter`](live-feed-adapter/SKILL.md) | **v009** — poll a remote endpoint for fresh intel events on a configurable interval; merge with provenance tagging. |
| 9e | [`doctrine-document-generator`](doctrine-document-generator/SKILL.md) | **v005, v008** — generate STANAG-2014 OPORD/FRAGO and AAR Markdown from current mission state + turn history. |

### COP rendering & domains

| # | Skill | Purpose |
|---|---|---|
| 10 | [`leaflet-cop`](leaflet-cop/SKILL.md) | NATO-styled COP on Leaflet, multi-layer toggles, animated phases, **v006 `window.__c23_flyTo()` cross-tab fly helper**. |
| 11 | [`mil-symbology`](mil-symbology/SKILL.md) | Render APP-6 / MIL-STD-2525B units with milsymbol; derive domain from SIDC (incl. v002 'P' → CYBER). |
| 12 | [`cyber-domain`](cyber-domain/SKILL.md) | **v002** — promote CYBER to a 5th operational domain (filter chip, tally column, OOB enum) per AJP-3.20. |
| 13 | [`neutral-side`](neutral-side/SKILL.md) | **v002** — add NEUTRAL faction (civilians, NGOs, IOs, infrastructure) per AJP-3.19 CIMIC. |
| 14 | [`ais-fusion`](ais-fusion/SKILL.md) | Ingest AIS commercial-vessel feeds (Master Prompt ANNEX schema) and flag dark-AIS tracks. |
| 15 | [`nato-classification`](nato-classification/SKILL.md) | NATO classification banners, STANAG 4774/4778 metadata, TEMPEST badging. |
| 15b | [`css-affordances`](css-affordances/SKILL.md) | **v007** — five small CSS patterns: themes via `[data-theme]`, CSS-only tooltips via `[data-tip]:hover:after`, persistent state indicators via `[data-…]`, slide-down animations, NATO logo halo. |

### Deployment & data

| # | Skill | Purpose |
|---|---|---|
| 16 | [`air-gap-mirror`](air-gap-mirror/SKILL.md) | Convert a CDN-loaded SPA into an air-gapped local-mirror build. **v005 reference impl: `tools/build_airgap_bundle.sh`**. |
| 17 | [`cyclonedx-unified-bom`](cyclonedx-unified-bom/SKILL.md) | Single CycloneDX 1.7 / ECMA-424 envelope covering S/SaaS/C/H/ML/O/M-BOM, VDR, VEX, BOV, CDAX, BOM-Link, CRNF. |

### Submissions & proposals

| # | Skill | Purpose |
|---|---|---|
| 17b | [`diana-proposal-draft`](diana-proposal-draft/SKILL.md) | **NewDraft** — generate a copy-paste-ready DIANA "New Draft Proposal" mapping every form field to a self-verifying char-budgeted answer; cites the live C23 NAVINT artefact and the pitch deck financial / team / market figures. |

### Doctrine ingestion

| # | Skill | Purpose |
|---|---|---|
| 18 | [`ajp-doctrine-summary`](ajp-doctrine-summary/SKILL.md) | Produce a consistent per-AJP Markdown summary suitable for indexing and roadmap synthesis. |
| 19 | [`doctrine-roadmap-synthesis`](doctrine-roadmap-synthesis/SKILL.md) | Consolidate per-doctrine summaries into a prioritised platform roadmap. |
| 20 | [`nato-ajp-sync`](nato-ajp-sync/SKILL.md) | Sync the local mirror of NATO Allied Joint Publications from gov.uk (wraps `AJP/update_ajp_doctrines.py`). |

## How a harness should use this

1. Read `skills/README.md` to get the index.
2. Match the user request against each `description:` line in the frontmatter.
3. Read only the matching `SKILL.md` (the rest stay cold).
4. Follow the **Instructions** section step by step; consult **Examples** for template output and **References** for source-of-truth pointers.
