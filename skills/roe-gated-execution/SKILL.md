---
name: roe-gated-execution
description: Gate every CoA execution behind a ROE-authorisation modal that surfaces JPTL TST hits, RTL/NSL conflicts and CDE rating before allowing commit.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    coa: "{ id, side, name, description, requiresROE?:bool, ... }"
    jointTargeting: "{ jptl[], rtl[], nsl[] }"
  outputSchema:
    modal: "RoEModal — surfaces gating data + ✓ AUTHORISE / ✕ DENY"
    log: "[ROE] entries on open / authorise / deny"
  errorHandling:
    noJointTargeting: "fall back to commit immediately if `jointTargeting` is absent"
    autoModeWithROE:  "auto-mode CoAs still gate; modal opens, log says CMDR decision required"
  stateless: true
tools: [Read, Edit]
---

# roe-gated-execution

## Purpose
NATO Joint Targeting (AJP-3.9) and Airspace Control (AJP-3.3.5) require explicit **Rules of Engagement** authorisation before kinetic execution. A C2 platform that lets an analyst one-click "execute CoA" against a TST without surfacing CDE / RTL / NSL is doctrinally unsafe. This skill captures the gating pattern.

## When to use
- Any UI that lets the user commit a CoA, attack, engagement, or order with potential collateral consequences.
- A scenario involves TSTs (Time-Sensitive Targets), C-UAS engagements, or CoAs that the analyst marked `requiresROE: true`.
- The user references AJP-3.9 / 3.3.5 / "ROE" / "rules of engagement" / "authorisation".

## Inputs
- The CoA being executed.
- `mission.jointTargeting` (JPTL + RTL + NSL).

## Outputs
- A `roePending` state that holds the CoA waiting for authorisation.
- A `RoEModal` component rendered conditionally that:
  - Lists matching TSTs with CDE rating, F2T2EA stage and restrictions.
  - Shows the full RTL and NSL.
  - Offers `✓ AUTHORISE & EXECUTE` (commits the CoA) or `✕ DENY` (cancels).
- Three log channels: `[ROE]` open · `[ROE]` authorised · `[ROE]` denied.

## Instructions

1. **Two-stage commit.** Split your existing single-stage CoA selector into:
   - A public `selectCoA(coaId, mode)` that decides whether ROE is needed.
   - A private `_executeCoaCommitted(coa, mode)` that actually mutates state.
2. **Decide the gate.** ROE is required if **either**:
   - `coa.requiresROE === true` (analyst-flagged), OR
   - The mission JPTL contains at least one TST whose `side` differs from the CoA's side (the CoA could engage a hostile TST).
3. **Open the modal** by setting a `roePending` state object: `{ coa, mode, reason, tstHits }`. Push a `[ROE]` warn-tone log line: "Authorisation required for «X» — awaiting CMDR decision."
4. **Render the modal in NATO red chrome** (this is hostile/danger semantics, not classification semantics — see skill `nato-classification` for the distinction):
   - Modal head: gradient `#5a1418 → #3a0e10`, gold border.
   - Section: TST list with CDE / F2T2EA / restrictions per row.
   - Section: full RTL.
   - Section: full NSL.
   - Footer: green AUTHORISE button + red DENY button.
5. **Confirm path:** `confirmRoE()` clears `roePending`, calls `_executeCoaCommitted(coa, mode)`, logs `[ROE] AUTHORISED`.
6. **Cancel path:** `cancelRoE()` clears `roePending`, logs `[ROE] DENIED`. **Do not** flip the active faction (the CoA never committed).
7. **Auto-mode is not a bypass.** If `mode === "auto"`, the modal still opens. Auto-mode picks the CoA, but a human still confirms the kinetic action.
8. **Pair with C-UAS auto-trigger:** when an intel event with `source === "RADAR"` and title/narrative matching `/\b(uas|uav|drone)\b/` is injected, log `[C-UAS]` citing AJP-3.3.5 so the operator knows ROE confirmation is incoming.

## Examples

### The two-stage commit (paste-ready, abbreviated)
```js
const _executeCoaCommitted = useCallback((coa, mode) => {
  setCoaHistory(h => [{...turn}, ...h]);
  pushLog("COA", `${activeFaction} executes "${coa.name}" — ${coa.description}`, "info");
  executeTurnKineticMovement(coa);
  setActiveFaction(f => f==="NATO" ? "OPFOR" : "NATO");
}, [activeFaction, pushLog, executeTurnKineticMovement]);

const selectCoA = useCallback((coaId, mode="manual") => {
  const coa = (mission.achMatrix?.coas||[]).find(c=>c.id===coaId); if (!coa) return;
  const tstHits = (mission.jointTargeting?.jptl||[])
    .filter(t => t.category==="TST" && t.side !== coa.side);
  const needsRoE = coa.requiresROE === true || tstHits.length > 0;
  if (needsRoE) {
    setRoePending({ coa, mode, reason: coa.requiresROE
      ? "CoA flagged requiresROE"
      : `TST in JPTL: ${tstHits.map(t=>t.name).join(", ")}`, tstHits });
    pushLog("ROE", `Authorisation required for "${coa.name}" — awaiting CMDR decision.`, "warn");
    return;
  }
  _executeCoaCommitted(coa, mode);
}, [mission.achMatrix, mission.jointTargeting, _executeCoaCommitted, pushLog]);
```

### C-UAS auto-trigger inside phase event injection
```js
if ((e.source||"").toUpperCase()==="RADAR" &&
    /\b(uas|uav|drone)\b/.test(`${e.title} ${e.narrative}`.toLowerCase())) {
  setTimeout(()=>pushLog("C-UAS",
    `[AJP-3.3.5] C-UAS workflow opened — ROE confirmation required for "${e.title}".`, "alert"), 200);
}
```

## Anti-patterns
- ❌ Committing first and showing the ROE info "for the record" afterwards. The point of ROE is to gate, not to log.
- ❌ A single boolean prop `requiresROE` without the JPTL-derived check. Analysts forget to set the flag; the JPTL signal catches them.
- ❌ Auto-mode that bypasses the modal. ROE bypass would defeat ROE.
- ❌ Reusing the classification banner colour (NATO Green) for the ROE modal. Use the danger palette (red/dark-red) — they're different concepts.
- ❌ Not flipping the active faction on DENY (correct) **and** not flipping on AUTHORISE (wrong — AUTHORISE commits, so the turn ends).

## References
- `C23_DIANA_NATO_WARFIGHTERS_v005.html` — `selectCoA`, `_executeCoaCommitted`, `confirmRoE`, `cancelRoE`, `RoEModal`.
- AJP-3.9 (Joint Targeting) and AJP-3.3.5 (Airspace Control / C-UAS).
- Skill `joint-targeting-jtc` (provides the JPTL/RTL/NSL the modal surfaces).
- Skill `ach-matrix` (the CoA is fed from there).
