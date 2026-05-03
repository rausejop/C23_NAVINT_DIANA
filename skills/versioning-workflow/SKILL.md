---
name: versioning-workflow
description: Apply the C23 superset versioning rule — every change writes a new _vNNN.html, never deletes prior versions, never removes features, and ships a structured changelog comment.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    targetFile: "the unsuffixed file (e.g. C23_DIANA_NATO_WARFIGHTERS.html) currently mirroring the latest version"
    changeSummary: "list of additions / improvements / fixes for the changelog"
  outputSchema:
    newVersionedFile: "C23_DIANA_NATO_WARFIGHTERS_v(NNN+1).html with changelog header"
    unsuffixedMirror: "the unsuffixed file overwritten with the same content"
  errorHandling:
    versionConflict: "if _v(NNN+1).html already exists, abort and re-read the chain"
    missingChain:    "if no _vNNN.html exists, seed _v001.html as a copy of the unsuffixed file before writing the new version"
  stateless: true
tools: [Bash, Read, Edit, Write]
---

# versioning-workflow

## Purpose
Operationalise the project rule documented in `CLAUDE.md § "Versioning rule (mandatory)"`: every change to the SPA produces a new monotonically numbered file, the chain is never broken, no version is ever edited in place, and no feature is ever removed. This skill is what an agent runs **every time** a change to the SPA is requested.

## When to use
- Any time the SPA HTML is about to change.
- The user requests "a new version", "add feature X", "fix bug Y", "improve Z" against the SPA.
- Even apparently trivial fixes — typos, CSS tweaks — go through the chain.

## Inputs
- The unsuffixed `C23_DIANA_NATO_WARFIGHTERS.html` (treated as the current latest).
- The change summary (list of `+ / ~ / #` items).

## Outputs
- `C23_DIANA_NATO_WARFIGHTERS_v(NNN+1).html` with a structured changelog comment block at the very top.
- The unsuffixed file overwritten so existing references in `README.md`, `skills/*.md`, etc. keep resolving.
- The previous `_v(NNN).html` is **untouched** (verify with `md5sum` if doubt arises).

## Instructions

1. **Find the current version number:**
   ```bash
   ls C23_DIANA_NATO_WARFIGHTERS_v*.html 2>/dev/null \
     | sed 's/.*_v\([0-9]*\)\.html/\1/' | sort -n | tail -1
   ```
   If empty, seed the chain: `cp C23_DIANA_NATO_WARFIGHTERS.html C23_DIANA_NATO_WARFIGHTERS_v001.html`. The "current" is now 001.
2. **Compute the next number:** `printf "v%03d" $((current + 1))`.
3. **Apply changes to the unsuffixed file** with `Edit` (preferred — small diffs) or `Write` (only for full rewrites). Verify the SPA still passes the sanity checks of skill `react-babel-pitfalls` (one Babel block, one `ReactDOM.createRoot`).
4. **Snapshot to the new version**:
   ```bash
   cp C23_DIANA_NATO_WARFIGHTERS.html C23_DIANA_NATO_WARFIGHTERS_v<NNN+1>.html
   ```
5. **Insert the changelog comment** at the top of the new versioned file, **after `<!DOCTYPE html>`, before `<html lang="en">`**:
   ```html
   <!--
     C23_DIANA_NATO_WARFIGHTERS_vNNN.html
     Date: YYYY-MM-DD · Author: <handle>
     Previous: _v(NNN-1).html
     Source plan: <pointer to roadmap.md section or user request>

     Changes vs previous (additive only — superset rule per CLAUDE.md):
       + <added feature>      (with the AJP / spec citation when relevant)
       ~ <improved feature>
       # <bug fix>
     Removed: NONE  (per superset rule)
   -->
   ```
   Use `+` for additions, `~` for improvements / refactors that preserve behaviour, `#` for bug fixes. The `Removed:` line **must always read NONE**. If you are tempted to write anything else there, stop — see the superset clause below.
6. **Verify:**
   ```bash
   ls -la C23_DIANA_NATO_WARFIGHTERS*.html        # ≥ 3 files: unsuffixed + every _vNNN
   wc -l C23_DIANA_NATO_WARFIGHTERS*.html         # new version line count ≥ previous
   md5sum C23_DIANA_NATO_WARFIGHTERS_v(NNN-1).html # previous unchanged from when it was written
   grep -c 'type="text/babel"'  C23_DIANA_NATO_WARFIGHTERS_vNNN.html   # = 1
   grep -c 'ReactDOM.createRoot' C23_DIANA_NATO_WARFIGHTERS_vNNN.html  # = 1
   ```
7. **Report to the user**: new version number, what changed (mirror the changelog `+/~/#` items), the file paths, and confirm the previous version is byte-identical to its prior state.

## Superset clause (no regressions, ever)

A new version must keep **every** feature, tab, button, schema field, doctrinal binding, classification element and integration seam present in the previous version. Allowed deltas are strictly:

- **+ Additive** (new features, new fields, new tabs).
- **~ Improvements** (better UX / performance / clarity / refactors that preserve behaviour).
- **# Fixes** (bug repairs that restore intended behaviour).

If a requested change appears to require *removing* a feature, do not perform it. Surface the trade-off to the user first; if removal is genuinely required, that is a deliberate decision that needs to be acknowledged outside the rule.

## Examples

### A typical session that ended in v002
```bash
ls *_v*.html | sed 's/.*_v\([0-9]*\)\.html/\1/' | sort -n | tail -1   # → 001
# … apply edits to the unsuffixed file …
cp C23_DIANA_NATO_WARFIGHTERS.html C23_DIANA_NATO_WARFIGHTERS_v002.html
# Edit the top of _v002.html to insert the changelog comment block
md5sum C23_DIANA_NATO_WARFIGHTERS_v001.html   # confirms v001 still byte-identical
```

### Changelog header that v002 actually shipped (abbreviated)
```html
<!--
  C23_DIANA_NATO_WARFIGHTERS_v002.html
  Date: 2026-05-02 · Author: CONFIANZA23
  Previous: C23_DIANA_NATO_WARFIGHTERS_v001.html
  Source plan: roadmap.md § 9 — Implementation priority for the next iteration (v1.1)

  Changes vs previous (additive only — superset rule per CLAUDE.md):
    + JOINT TARGETING module (AJP-3.9) — ...
    + MOVEMENT module (AJP-3.13 / 4.4) — ...
    + POSTURE module (AJP-3.14 / 3.23 / 3.3 / 6) — ...
    + CYBER as the 5th operational domain (AJP-3.20).
    + NEUTRAL side (AJP-3.19 CIMIC).
    + Operation Type and Mission Type on Mission tab.
    + Master Narrative, CoG, End-state criteria.
    + 23 acronyms.
  ~ Tally rail: 5-column grid (added CYBER) with NEUTRAL row.
  ~ Filter chips rail: NEUTRAL chip + CYBER chip.
  Removed: NONE  (per superset rule)
-->
```

## Anti-patterns
- ❌ `git rm`-ing or `mv`-ing over a `_vNNN.html`. The chain is the audit trail.
- ❌ "Just patching" the existing `_vNNN.html` with a small fix instead of bumping. That breaks the chain integrity guarantee.
- ❌ Writing `Removed: <feature>` in the changelog. Never. If a feature truly must go, it does so in a deliberate negotiated step that exits the superset rule explicitly.
- ❌ Letting the unsuffixed file diverge from the latest `_vNNN.html` (other than the changelog header). They must be functionally identical.
- ❌ Forgetting the `data-presets="react"` and one-Babel-block sanity check before snapshotting. Don't ship a black-screen version.

## References
- `CLAUDE.md § "Versioning rule (mandatory)"` — authoritative source.
- `C23_DIANA_NATO_WARFIGHTERS_v002.html` — first non-seed version, full worked example.
- Skill `react-babel-pitfalls` — pre-snapshot sanity checks.
- Skill `roadmap-driven-release` — companion skill for picking *what* goes into the next bump.
