---
name: ach-auto-suggest
description: Heuristic auto-scoring of ACH cells via keyword overlap between events and CoAs. Preserves analyst-set scores; only fills empty cells.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    achMatrix: "{ coas, scores }"
    events:    "geopolitical + intel events"
  outputSchema:
    scoresUpdated: "merged scores object — analyst values untouched"
  errorHandling:
    noEvents: "noop; report 0 added / 0 preserved"
  stateless: true
tools: [Read, Edit]
---

# ach-auto-suggest

## Purpose
Filling an empty ACH matrix is tedious. A keyword-overlap heuristic produces an 80%-good first pass that the analyst then refines. The analyst's existing edits are NEVER overwritten, so the function is safe to re-run.

## When to use
- A new mission is loaded with a populated CoA list and event list but mostly-empty ACH scores.
- The analyst added a batch of new events and wants a starting point for re-scoring.
- The user asks for "auto-score", "suggest scores", "fill ACH".

## Inputs
- `mission.achMatrix.coas`, `mission.achMatrix.scores`.
- The combined geopolitical + intel events list.

## Outputs
- A new `scores` object where empty cells got CC / C / N / I / II suggestions; non-empty cells passed through unchanged.
- A summary alert: "Auto-score: X cells filled, Y cells preserved as set by analyst."

## Instructions

1. **Tokenise both sides** of the comparison: event title + narrative on one side, CoA name + description on the other. Drop tokens shorter than 4 chars (too noisy).
2. **Count overlap** between the two token sets per (event, CoA) cell.
3. **Map overlap to the 5-level scale** (skill `ach-matrix` defines CC/C/N/I/II = +2/+1/0/−1/−2):
   - overlap ≥ 3 → CC
   - overlap == 2 → C
   - overlap == 1 → N
   - overlap == 0 → leave empty (no signal)
4. **Side-flip on hostile evidence:** if the CoA side is NATO and the event severity is `warn`/`alert` (interpreted as OPFOR-favourable), flip CC→II and C→I. The same heuristic the platform uses for the default mission.
5. **Skip already-set cells** with `if (next[k]) { kept++; return; }`. Honouring analyst input is the contract.
6. **Surface the result** with a `window.alert` so the user knows what changed; the live legend will already show the new colours.
7. **Make the function pure.** No side effects beyond producing the new `scores` object. The caller (the ACH tab button) does the `setMission`.

## Examples

### The exact heuristic from v005
```js
const tokenize = (s) => (s||"").toLowerCase().split(/[^a-z0-9]+/).filter(w=>w.length>3);
const autoScore = () => {
  const next = {...(ach.scores||{})};
  let added = 0, kept = 0;
  events.forEach(ev => {
    const evTokens = new Set([...tokenize(ev.title), ...tokenize(ev.narrative)]);
    (ach.coas||[]).forEach(c => {
      const k = `${ev.id}::${c.id}`;
      if (next[k]) { kept++; return; }
      const coaTokens = new Set([...tokenize(c.name), ...tokenize(c.description)]);
      let overlap = 0; coaTokens.forEach(t => { if (evTokens.has(t)) overlap++; });
      let val = "";
      if (overlap >= 3)      val = "CC";
      else if (overlap === 2) val = "C";
      else if (overlap === 1) val = "N";
      if (val && c.side === "NATO" && (ev.severity==="alert"||ev.severity==="warn")) {
        if (overlap >= 3) val = "II";
        else if (overlap === 2) val = "I";
      }
      if (val) { next[k] = val; added++; }
    });
  });
  setMission(m => ({...m, achMatrix:{...m.achMatrix, scores:next}}));
  window.alert(`Auto-score: ${added} cells filled, ${kept} cells preserved as set by analyst.`);
};
```

## Anti-patterns
- ❌ Using a more complex weight (TF-IDF, embeddings) before showing the analyst what the simple heuristic already gives. Most missions don't need it.
- ❌ Overwriting analyst-set cells. Breaks trust permanently.
- ❌ Auto-applying without a button click ("auto-score on every event add"). The analyst loses agency.
- ❌ Putting the heuristic inside `scoreCoas`. `scoreCoas` *reads* scores; this function *writes*. Keep them separate.
- ❌ Ignoring side flips. CC against a NATO defensive CoA from an OPFOR-warning event is wrong.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v005.html` — `ACHTab.autoScore()`.
- Skill `ach-matrix` — defines the 5-level scale and `ACH_VAL_MAP`.
