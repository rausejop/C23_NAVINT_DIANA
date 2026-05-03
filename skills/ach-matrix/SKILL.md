---
name: ach-matrix
description: Implement an Analysis-of-Competing-Hypotheses matrix (CoA × Evidence with Consistent / Neutral / Inconsistent scoring) and roll-up ranking.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    coas:    "Course[]"     # { id, side, name, description, weight }
    events:  "Evidence[]"   # geopolitical + intel events
  outputSchema:
    matrix:  "{ scores: { '<eid>::<coaId>': 'C'|'N'|'I' } }"
    ranking: "[{ id, name, side, score, evCount }]  sorted desc"
  errorHandling:
    missingCoa: "ignore the score key silently; never throw"
    deleteCoa:  "cascade — strip every '<eid>::<coaId>' key from scores"
  stateless: true
tools: [Read, Edit]
---

# ach-matrix

## Purpose
Score each Course of Action (CoA) against each Evidence item using the classic **Analysis of Competing Hypotheses** convention (Heuer). v003 expanded the scale from 3 to 5 levels, fully backward-compatible:

- **CC · 1** Most Consistent &nbsp;⇒ +2 (v003)
- **C  · 2** Consistent &nbsp;⇒ +1
- **N  · 3** Neutral &nbsp;⇒ 0
- **I  · 4** Inconsistent &nbsp;⇒ −1
- **II · 5** Most Inconsistent &nbsp;⇒ −2 (v003)

Then surface a per-CoA total and a global ranking. The lowest-inconsistency CoA wins; in this codebase we add the +X for completeness so tie-breaks are visible. v005 added an **AUTO-SCORE** button (skill `ach-auto-suggest`) that fills empty cells via a keyword-overlap heuristic without overwriting analyst-set values.

## When to use
- A wargame or planning UI needs a structured CoA-comparison view (AJP-5).
- An analyst needs to defend a recommendation against multiple competing explanations.
- The user asks for "ACH", "competing hypotheses" or a "CoA scoring matrix".

## Inputs
- An array of CoAs, each with `{ id, side, name, description, weight? }`. `side ∈ {NATO, OPFOR, NEUTRAL}` (NEUTRAL added in v002 for civil-actor courses of action — e.g., civilian evacuation, declaration of safe zone — see skill `neutral-side`).
- An array of Evidence items (the union of geopolitical + intel events): `{ id, phase, dtg, source, title, narrative, severity }`.

## Outputs
- A persistent `scores` object keyed `"<evidenceId>::<coaId>"` with values in `"C" | "N" | "I" | ""`.
- A pure ranking helper:
  ```js
  function scoreCoas(achMatrix) {
    const v = { C:+1, N:0, I:-1 };
    return achMatrix.coas.map(c => {
      let score = 0, n = 0;
      Object.entries(achMatrix.scores||{}).forEach(([k,val])=>{
        const [, coaId] = k.split("::");
        if (coaId === c.id) { score += v[val]||0; n++; }
      });
      return { id:c.id, name:c.name, side:c.side, score, evCount:n };
    }).sort((a,b)=>b.score-a.score);
  }
  ```

## Instructions
1. **Store scores in a flat object** keyed `"<evidenceId>::<coaId>"`. Don't nest — flat keys make import/export and partial updates trivial.
2. **Render two tables:** a CoA list (CRUD; columns `ID · SIDE · NAME · DESCRIPTION · SCORE`) and a CoA × Evidence grid where every cell is a `<select>` of `—/C/N/I`.
3. **Mirror NATO/OPFOR colour conventions** on the CoA-side cells (allied blue, hostile red).
4. **Cascade-delete cleanly.** When a CoA is deleted, walk `scores` and strip every key ending in `::<coaId>`.
5. **Provide one purpose-built export** (`{ schema:"…/ACH/1.0", achMatrix }`) so analysts can move just the matrix between missions.
6. **Document the convention** in the platform's Acronyms tab so users know `C/N/I = +1/0/−1`.

## Examples

### A CoA × Evidence cell
```jsx
<select className="ach-cell-edit" value={ach.scores[`${e.id}::${c.id}`]||""}
        onChange={ev=>setScore(e.id, c.id, ev.target.value)}>
  <option value="">—</option>
  <option value="C">C</option>
  <option value="N">N</option>
  <option value="I">I</option>
</select>
```

### Auto-mode CoA pick (TRL-6 stub for foundation-model integration)
```js
const eligible = mission.achMatrix.coas.filter(c => c.side === activeFaction);
const pick = eligible[Math.floor(Math.random()*eligible.length)];
selectCoA(pick.id, "auto");
```

## Anti-patterns
- ❌ Weighting cells silently. Heuer's convention is per-cell; weighting belongs at the CoA roll-up, not in cell semantics.
- ❌ Storing per-evidence subtotals as state — derive on render.
- ❌ Allowing "I" to be entered as a free-text field. Use `<select>`; no other values are legal.
- ❌ Treating the highest score as "the answer". Surface the ranking and let the human decide; this is decision *support*, not decision *automation*.

## References
- `C23_DIANA_NATO_WARFIGHTERS.html` — `ACHTab`, `scoreCoas()`.
- AJP-5 — Allied Joint Doctrine for the Planning of Operations.
- Heuer, R.J. (1999), *Psychology of Intelligence Analysis*, Ch. 8 — Analysis of Competing Hypotheses.
