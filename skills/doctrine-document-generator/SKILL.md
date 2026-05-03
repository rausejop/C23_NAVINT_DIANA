---
name: doctrine-document-generator
description: Generate doctrinally-shaped Markdown documents (OPORD/FRAGO STANAG-2014, AAR After-Action Review) from current mission state + turn history.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    documentKind: "OPORD | FRAGO | AAR"
    mission:      "the live mission object"
    units:        "current OOB"
    coaHistory:   "executed turns (newest first)"
  outputSchema:
    markdown: "string ready to render or download"
  errorHandling:
    emptyHistory:  "render document with explicit '(no turns played yet)' lines"
    missingFields: "use '—' as placeholder; never throw"
  stateless: true
tools: [Read, Edit]
---

# doctrine-document-generator

## Purpose
Stop hand-writing OPORDs and AARs. Both follow well-known doctrinal shapes (STANAG 2014 for OPORD/FRAGO; the standard "what was the mission / what happened / what worked / what didn't / recommendations" for AAR). The platform already has every input — mission identity, phases, OOB, posture, JPTL, weather, turn history — so the document is a `useMemo` away.

## When to use
- The user asks for "OPORD", "FRAGO", "operations order", "AAR", "after-action review", "after-action report", "lessons learned export".
- The platform reaches a transition point (phase complete, exercise end) and a paper artefact is needed.
- A briefing requires a one-pager that summarises the current state.

## Inputs
- `mission` (live editor state).
- `units` (current OOB).
- `coaHistory` (executed turns, newest first).
- The document kind (OPORD / FRAGO / AAR).

## Outputs
- A Markdown string built deterministically from inputs (no hidden state, no fetch).
- Re-generated on every render — what the user sees is what downloads.

## Instructions

1. **Compose with `useMemo`** keyed on every input that affects the output. The point is a faithful mirror of state, not a snapshot.
2. **Reuse helpers, don't duplicate.** `dtgFmt` for date-time groups, `mission.posture.*` for posture lines, etc.
3. **Always include "Annex JPTL" and "Annex Turn History"** for OPORD/FRAGO. They are what makes the order auditable.
4. **AAR template is open-ended** — fill the `## What went well`, `## What did not go well`, `## Recommendations` sections with `(analyst input)` placeholders so the editor knows where to type.
5. **Download via Blob:** `new Blob([text], {type:"text/markdown"})` → URL → `<a download>`. Filename includes operation code + date.
6. **Render the live preview as `<pre>`** so the user sees what they will get — not a "click to generate" dialog.
7. **Don't try to be clever.** Do not parse the user's free-text intent and try to summarise it; reproduce it verbatim. The agent that *consumes* the document does the parsing.

## Examples

### OPORD shape (used in v005 `OrdersTab`)
```
# OPORD <code> — <name>
Issued by: <commander>
DTG: <ZULU>

## 1. SITUATION       (AOR · Operation Type · Mission Type · CoG · Weather)
## 2. MISSION         (commander's intent)
## 3. EXECUTION       (3.a Concept · 3.b Tasks per OOB unit · 3.c Coord — FPCON/CBRN/PNT/CIS PACE)
## 4. SUSTAINMENT     (APOD / SPOD / MSR / ASR)
## 5. COMMAND & SIGNAL (Commander · Master Narrative)
## ANNEX A — JOINT TARGETING (AJP-3.9, JPTL)
## ANNEX B — TURN HISTORY
```

### AAR shape (used in v008 `IntelOpsTab.generateAAR`)
```
# AFTER-ACTION REVIEW
Mission · Operation · AAR DTG

## What was the mission?            > <intent>
## What actually happened?          (one bullet per executed CoA, oldest first)
## What went well? (sustain)        (analyst input)
## What did not go well? (improve)  (analyst input)
## Anomalies detected at AAR time   (auto, from detectAnomalies())
## Recommendations                  (analyst input)
```

### Download helper
```js
const download = (text, filename) => {
  const blob = new Blob([text], {type:"text/markdown"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a"); a.href = url; a.download = filename;
  a.click(); URL.revokeObjectURL(url);
};
```

## Anti-patterns
- ❌ Generating once on a button click and stashing the string in state. Use `useMemo` so the document is always live.
- ❌ Hiding sections that have no data ("## SUSTAINMENT" with no APOD/SPOD/MSR/ASR). Render the heading; doctrine consumers expect the skeleton.
- ❌ Trying to make the OPORD pretty (HTML, tables, headings styled in CSS). Plain Markdown survives every downstream pipeline; styling does not.
- ❌ A "DOWNLOAD AAR" button that doesn't have a "GENERATE" companion. The analyst must edit before exporting.
- ❌ Emitting Markdown with surprise tokens (em-dash inside code blocks, smart quotes). Stick to ASCII for portability.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v005.html` — `OrdersTab` (OPORD).
- `C23_DIANA_NATO_WARFIGHTERS_v008.html` — `IntelOpsTab.generateAAR()` (AAR).
- STANAG 2014 — Allied Operations Order format reference.
- Skill `mission-editor` (provides the host tab); skill `joint-targeting-jtc` (provides the JPTL annex).
