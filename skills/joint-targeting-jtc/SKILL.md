---
name: joint-targeting-jtc
description: Implement the AJP-3.9 Joint Targeting Cycle in a single-file SPA — six-phase JTC indicator, JPTL CRUD, FIVE-O / F2T2EA stage tracking, CDE rating, RTL and NSL.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    jptl:  "Target[]    # { id, name, side, coords, category:'HVT|HPT|TST|NSL', priority:1..9, intent, f2t2ea, restrictions, cde:'1..5' }"
    rtl:   "[{ id, name, reason }]"
    nsl:   "[{ id, name }]"
    jtcPhase: "1..6 — current cycle phase"
  outputSchema:
    tab:    "JOINT TARGETING modal tab in the Mission Editor"
    overlay: "Concentric ring + dot per JPTL target on the COP map"
    tile:    "JTC PHASE n/6 tile in the top bar"
  errorHandling:
    invalidCoords: "skip the target on the map; keep it in the table for editing"
    deleteTarget:  "no cascade — target IDs are not referenced from other state"
  stateless: true
tools: [Read, Edit]
---

# joint-targeting-jtc

## Purpose
Add a doctrine-faithful Joint Targeting capability per **AJP-3.9 Edition B Version 1**: the six-phase Joint Targeting Cycle (JTC), the Joint Prioritised Target List (JPTL), the FIVE-O / F2T2EA execution sequence, Collateral Damage Estimation (CDE), the Restricted Target List (RTL) and the No-Strike List (NSL). This is the highest-leverage doctrinal item per `roadmap.md § 9` and shipped as the centrepiece of v002.

## When to use
- The platform must surface targeting decisions, not only force movement.
- A scenario requires HVT / HPT / TST classification, dynamic vs deliberate targeting distinction, or a CDE step before engagement.
- The user references AJP-3.9, "JPTL", "F2T2EA", "FIVE-O", "no-strike list", "collateral damage estimation".

## Inputs
- A list of `jptl` targets shaped per the input schema above.
- Two reference lists: `rtl` (restricted — engagement permitted only with extra authority) and `nsl` (no-strike — protected status).
- The current `jtcPhase` (1..6) and the six-phase definition table (`JTC_PHASES`).

## Outputs
- A `JOINT TARGETING` tab in the Mission Editor with:
  - Six numbered phase buttons (1–6); selecting one writes back to `mission.jointTargeting.jtcPhase`.
  - JPTL table with full CRUD (12 columns: ID · CAT · PRI · NAME · SIDE · LAT · LON · F2T2EA · CDE · RESTRICTIONS · INTENT · DEL).
  - Side-by-side RTL / NSL CRUD lists.
- A `JTC PHASE n/6` tile on the top bar.
- A map overlay (toggleable) drawing one dashed ring + one filled dot per target, coloured by category:
  - **HVT** = NATO Gold (`#FFC72C`)
  - **HPT** = amber (`#f59e0b`)
  - **TST** = hostile red (`#e85d50`)
  - other / NSL = allied blue (`#9bc7ff`)

## Instructions
1. **Define the six JTC phases as a constant** so naming is identical across the UI:
   ```js
   const JTC_PHASES = [
     { id:1, name:"Commander's End-state & Objectives" },
     { id:2, name:"Target Development & Prioritisation (JPTL)" },
     { id:3, name:"Capabilities Analysis" },
     { id:4, name:"Commander's Decision & Force Assignment" },
     { id:5, name:"Mission Planning & Force Execution" },
     { id:6, name:"Combat Assessment (BDA + MEA + Re-attack)" }
   ];
   ```
2. **Add `jointTargeting` to the default mission** with seeded JPTL (≥4 targets demonstrating each category), RTL (≥2 entries), NSL (≥2 entries), and an initial `jtcPhase`.
3. **Render JPTL on the map in its own `useEffect`** keyed `[tweaks.showJPTL, mission.jointTargeting]`. Always remove the previous layer set first; store layers in a dedicated ref (`jptlLayerRef`).
4. **Tooltip every target** with category, priority, F2T2EA stage, intent, CDE rating and restrictions — analysts must see the gating data before deciding.
5. **Wire the tile** in the top bar so the JTC phase is visible without opening the modal.
6. **Cascade is unnecessary** — JPTL/RTL/NSL IDs are not referenced from other tables. Delete is local.
7. **Provide a layer toggle** on the LAYERS rail so the JPTL ring overlay can be hidden during pure-COP review.
8. **Document in the Acronyms tab** every term the module introduces: JTC, JPTL, RTL, NSL, HVT, HPT, TST, F2T2EA, FIVE-O, CDE, BDA, MEA, VBSS.

## Examples

### Default seeded JPTL entry (TST against a dark vessel)
```js
{ id:"t04", name:"Suspect dark-AIS vessel (DARK ECHO 2)", side:"OPFOR",
  coords:[55.65,18.95],
  category:"TST", priority:1,
  intent:"Prevent second subsea cable severance",
  f2t2ea:"Target",
  restrictions:"VBSS preferred; engagement only on confirmed hostile intent",
  cde:"1" }
```

### JPTL ring overlay
```js
const ring = L.circleMarker(t.coords, {
  radius:11, color:cat(t.category), fillColor:cat(t.category),
  fillOpacity:0.0, weight:2, dashArray:"3,3"
}).bindTooltip(`<b>${t.category} · ${t.name}</b><br/>` +
  `Priority ${t.priority} · F2T2EA ${t.f2t2ea}<br/>` +
  `${t.intent}<br/>CDE ${t.cde} · ${t.restrictions}`,
  {direction:"top",offset:[0,-12]}).addTo(m);
```

## Anti-patterns
- ❌ Treating "engage" as a one-click action. AJP-3.9 demands CDE and RTL/NSL checks first; the UI must surface them before any state change tagged `Engage`.
- ❌ Letting CDE be free-text. Use a `<select>` of 1–5 so the cell is always parseable for downstream weighting.
- ❌ Mixing JPTL targets with OOB units. Targets are *attribution* (what / where / why), units are *force* (who / what they have / where they are). Keep separate tables; allow targets to reference unit IDs in `intent` if useful.
- ❌ Hiding RTL / NSL inside the JPTL table. Both are reference lists with their own life-cycle; they must be CRUD-able independently.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v002.html` — `JointTargetingTab`, `JTC_PHASES`, `jptlLayerRef`.
- `AJP/SUMMARIES/AJP-3.9.md` — doctrinal source.
- AJP-3.9 Edition B Version 1, 2021 (NATO Standardization Office).
- `roadmap.md § 3` — Joint Targeting tracking.
