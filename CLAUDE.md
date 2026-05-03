# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is **not** a conventional codebase with a build system. It is the working directory for the **C23 DIANA NATO Warfighters** submission to the DIANA Challenge "Decision Superiority for NATO Warfighters". The deliverable is a single self-contained HTML Single Page Application (`C23_DIANA_NATO_WARFIGHTERS.html`) that runs offline on a tactical laptop. Surrounding files are doctrinal sources, requirement specifications, and a reference template that the SPA must be derived from.

There is no package manager, no test runner, no lint config, and no git repository. Edits land directly on the HTML file; the only way to "run" the platform is to open the HTML in a browser.

## Versioning rule (mandatory — applies to every change of the SPA)

**Every change to `C23_DIANA_NATO_WARFIGHTERS.html` must produce a new numbered file. Old versions are never deleted, never edited in place. New versions are strict supersets of the previous — features only get added or improved, never removed.**

### Mechanics

1. **File-naming convention**: `C23_DIANA_NATO_WARFIGHTERS_vNNN.html`, where `NNN` is a zero-padded three-digit version number. The chain begins at `_v001.html` (already seeded as a copy of the initial release) and grows monotonically: `_v002.html`, `_v003.html`, `_v004.html`, …
2. **The unsuffixed `C23_DIANA_NATO_WARFIGHTERS.html` always points to the latest version.** On every change, write the new versioned file *and* overwrite the unsuffixed file with the same content. README, skills and other docs reference the unsuffixed name; do not break those references.
3. **Find the next version number** before writing:
   ```bash
   ls C23_DIANA_NATO_WARFIGHTERS_v*.html | sed 's/.*_v\([0-9]*\)\.html/\1/' | sort -n | tail -1
   ```
   Increment by 1 and zero-pad to 3 digits.
4. **Never delete** any `_vNNN.html` file. Never `git rm`, never `mv` over an existing version. The full chain is the audit trail.
5. **Never edit `_vNNN.html` in place** once written. If a fix is needed, it goes into `_v(NNN+1).html`.

### Superset rule (no regressions)

Each new version must keep **every** feature, tab, button, schema field, doctrinal binding, classification element and integration seam present in the previous version. Allowed deltas are **additive** (new features), **corrective** (bug fixes that preserve behaviour), or **improvements** (better UX / performance / clarity for an existing feature). If a change appears to require removing a feature, do not perform it — surface the trade-off to the user first.

The Master Prompt deliverables A–K are the **floor**, not the ceiling. Anything from `roadmap.md` that gets implemented is added on top.

### Changelog block (mandatory at top of each new file)

The first comment block of every new versioned HTML file lists the changes versus the immediately previous version:

```html
<!--
  C23_DIANA_NATO_WARFIGHTERS_vNNN.html
  Date: YYYY-MM-DD · Author: <handle>
  Previous: _v(NNN-1).html
  Changes vs previous:
    + <added feature>
    ~ <improved feature>
    # <bug fix>
  Removed: NONE  (per superset rule)
-->
```

Use prefixes `+` (added), `~` (improved/refactored without behaviour change), `#` (bug fix). The `Removed:` line must always read `NONE`. If you are tempted to write anything else there, stop and re-read the superset rule.

### Workflow on every change

1. Read the latest `_vNNN.html` to know the current state.
2. Apply the change with `Edit` against the unsuffixed file (or write a new full file if the change is large).
3. `cp` the unsuffixed file to `C23_DIANA_NATO_WARFIGHTERS_v(NNN+1).html`.
4. Add the changelog comment block at the top of the new versioned file.
5. Verify both files exist and old versions are untouched:
   ```bash
   ls -la C23_DIANA_NATO_WARFIGHTERS*.html
   ```
6. Report to the user: the new version number, what changed, and the file paths.

## Authoritative inputs (read these before changing anything)

The work is governed by `MasterPrompt.txt` at the repo root. It defines the deliverables (A–K) and the **mandatory ingestion order** before any change is made:

1. `Specifications/20260502 DIANA FAQ.txt`
2. `Specifications/20260502 Welcome to DIANAs Challenge Portal.txt`
3. `Specifications/20260502 Decision Superiority for NATO Warfighters.txt` — primary requirements source

Any new functionality must be checked back against the Decision Superiority spec (deliverable F). The `MasterPrompt.txt` ANNEX defines coding standards (TypeScript strict / no `any`, SLO Agent Skills framework, AIS JSON schema for vessel data). The `AIS` schema in the ANNEX is the canonical shape for any commercial maritime ingestion code.

## Building the SPA

The platform is generated from a template, not written from scratch:

- **HTML template:** `Format/EasternFlankv003.html` — contains the COP scaffold, NATO chrome (NATO Reflex Blue `#004990`, NATO Gold `#FFC72C`), classification banner, and the React/Babel/Leaflet/milsymbol stack loaded via CDN tags.
- **Mission parameters:** `Format/EasternFlank_v003.json` — OOB (Order of Battle), `phaseVectors` (per-phase movement targets keyed by unit id), and `mapSettings`.

The output is `C23_DIANA_NATO_WARFIGHTERS.html` at repo root. Per deliverable B, parameters that ship hardcoded in the template **must be exposed through a Mission Editor with full CRUD** over: mission name, phase ladders (relative + absolute dates), ladder names/descriptions, geopolitical events, intel events, the full OOB. JSON import/export must support full mission, OOB-only, or both.

## Hard architectural constraints (deliverable K)

These are non-negotiable and shape every implementation choice:

- **Single HTML file.** No build step, no bundler, no separate JS/CSS files. The SPA is one `.html` blob.
- **Air-gapped.** All third-party assets (Tailwind, React, Babel, Leaflet, milsymbol, fonts, basemap tiles, images) must work without internet. The current template loads from `unpkg.com` and `fonts.googleapis.com`; for a final air-gapped build these must be inlined or mirrored locally.
- **16 GB RAM laptop, Windows.** Avoid heavy in-browser ML; AI/ML behavior is **simulated** at this TRL (deliverable D — random-choice stub stands in for the future LangChain + Ollama integration).
- **Security by Design.** NATO Secured Environment Standards (STANAGs, TEMPEST considerations, restricted-network data integrity). Source data must remain open-source and publicly released NATO doctrine only.

## Doctrinal corpus (`AJP/`)

`AJP/` is a local mirror of all 33 NATO Allied Joint Publications, indexed `01 …` through `33 …`. The order matters — deliverable H requires reading **every** AJP directory in numeric order, producing a per-doctrine Markdown summary, and consolidating findings into `roadmap.md` for platform updates (deliverable I).

Maintenance:

```powershell
python AJP/update_ajp_doctrines.py
```

This scrapes <https://www.gov.uk/government/collections/allied-joint-publication-ajp>, creates/updates numbered folders, and downloads any new PDFs. Re-run if PDFs land in `AJP/` root instead of subfolders. Only stdlib (`urllib`, `html.parser`) — no pip install needed. See `AJP/update_ajp_skill.md` for the agent-skill wrapper.

The platform's doctrine bindings are explicit: AJP-3.9 (Joint Targeting — 6-phase JTC, JPTL, FIVE-O taxonomy), AJP-4.4 (Movement — RSOM, MSR), AJP-3 (Conduct of Operations — multi-domain synchronization). Treat these as the source of truth for terminology and workflow shape, not invented UX.

## Required platform features beyond the template

From `MasterPrompt.txt` deliverables, the SPA must include (at minimum):

- **Mission Editor** with CRUD on every hardcoded parameter + JSON import/export (B).
- **ACH Matrix** (Analysis of Competing Hypotheses) with CoA × Evidence CRUD; CoAs are per-turn decisions for Allied or Hostile, manual or automatic (C).
- **Automatic mode** simulated by random selection (D); leave the integration seam clearly named so the LangChain+Ollama swap-in is obvious.
- **Turn button** that displays and toggles the active faction (Allied/Hostile), letting the user play either side (E).
- **Info button** next to CONFIG with two tabs: Instructions (walks through every parameter in configuration order) and Acronyms (every term used in the platform) (G).
- **Unified data model** in `Datamodel.md` based on CycloneDX BOM JSON 1.7 covering SBOM, SaaSBOM, CBOM, HBOM, ML-BOM, OBOM, MBOM, VDR, VEX, BOV, CDAX, BOM-Link, CRNF (J).

## Working in this repo

- The Format/ template, Specifications/ texts, and AJP/ PDFs are read-only source material. Do not modify them; derive outputs at the repo root.
- When adding a feature, name the AJP doctrine it implements in a brief code comment — that traceability is the whole point of the deliverable.
- Use `python` (stdlib only) for any tooling. No Node toolchain is set up.
- Forward slashes in shell paths; this is bash on Windows. The working directory contains spaces — quote it.
