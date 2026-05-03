---
name: neutral-side
description: Add NEUTRAL as a third faction (alongside NATO / OPFOR) for civilians, NGOs, IOs and infrastructure providers per AJP-3.19 CIMIC.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    units: 'Unit[] possibly carrying side:"NEUTRAL"'
  outputSchema:
    enums: "side enum extended; tally row + filter chip + OOB <select> + ACH side updated"
    units: "≥1 NEUTRAL units (civil airliner, NGO liaison, civil ferry) in default mission"
  errorHandling:
    legacyImport: "OOB JSON without NEUTRAL continues to load; NEUTRAL row renders empty"
  stateless: true
tools: [Read, Edit]
---

# neutral-side

## Purpose
Represent the actors that are neither friendly nor hostile but whose presence shapes targeting, ROE, FPCON and StratCom: civil populations, civilian infrastructure operators, IOs and NGOs (ICRC, OSCE, UN), commercial maritime / aviation, host-nation civil authorities. Without this third faction, CIMIC (AJP-3.19), Stability (AJP-3.28), HumAss (AJP-3.26), NEO (AJP-3.25) and PSO (AJP-3.24) cannot be modelled honestly.

## When to use
- The platform models any operation where civilians or NGOs are present in the AOR (i.e., any real operation).
- A scenario must show that engaging would risk RTL/NSL violations.
- The user references AJP-3.19 / 3.24 / 3.25 / 3.26 / 3.28, "CIMIC", "civilian", "NGO", "neutral".

## Inputs
- The OOB. Existing arrays continue to work; new units may carry `side:"NEUTRAL"`.
- The filter / tally / OOB-select / ACH-side code paths.

## Outputs
- `side` enum extended to `NATO | OPFOR | NEUTRAL` everywhere it appears.
- Filter chip `NEUTRAL` (NATO neutral-green palette).
- Tally row for NEUTRAL with the same five domain columns.
- OOB editor `<select>` includes `NEUTRAL`.
- ACH-CoA `<select>` includes `NEUTRAL` (so neutral-actor courses of action — e.g., evacuation, declaration of safe zone — are first-class).
- Default mission ships ≥3 NEUTRAL units (in v002: airBaltic civil airliner, ICRC Vilnius liaison, M/V Stena Baltica ferry).

## Instructions
1. **Extend the initial filter state** to include `NEUTRAL:true`.
2. **Extend the tally factory** with a third side:
   ```js
   const t = { NATO:blank(), OPFOR:blank(), NEUTRAL:blank() };
   ```
3. **Extend the tally render** to map over `["NATO","OPFOR","NEUTRAL"]`.
4. **Extend filter chips** with NEUTRAL; map the label so `NEUTRAL` displays as `NEUTRAL` (not `HOSTILE`).
5. **Extend the OOB-edit `<select>`** with `<option>NEUTRAL</option>`.
6. **Extend the ACH `<select>`** with `<option>NEUTRAL</option>` so analysts can record neutral-actor CoAs.
7. **Add NATO-neutral-green palette** for NEUTRAL borders / chips:
   ```css
   .tally-row.side-NEUTRAL { border-left: 3px solid var(--neutral); }
   .side-NEUTRAL .tally-side { color: var(--neutral); }
   .chip.side-NEUTRAL.on { border-color: var(--neutral); color: var(--neutral); background:#0c2418; }
   .d-card.side-NEUTRAL { border-left: 3px solid var(--neutral); }
   .pill.side-NEUTRAL { color: var(--neutral); border-color: rgba(116,216,95,0.5);
     background: rgba(116,216,95,0.08); }
   ```
8. **Use APP-6 neutral SIDCs** in seeded units. Char-1 `S` (status: simulation), char-2 `N` (affiliation: neutral). E.g., `SNAPCF---------` (civil air), `SNGPUC---------` (civil land), `SNSPCLCC-------` (civil sea).
9. **Add to Acronyms.** CIMIC, ICRC, NGO, IO already exist; verify they are present.

## Examples

### Default neutral units (v002)
```js
{ id:"x01", side:"NEUTRAL", domain:"AIR",
  designation:"airBaltic BT-643 (civil)", type:"Civil Airliner",
  equipment:["Airbus A220-300"],
  mission:"Scheduled passenger flight RIX → TLL",
  status:"Operational", coordinates:{lat:58.20,lng:24.50}, echelon:"FLT", readiness:"R1",
  sidc:"SNAPCF---------" }

{ id:"x02", side:"NEUTRAL", domain:"LAND",
  designation:"ICRC Liaison (Vilnius)", type:"NGO Liaison",
  equipment:["Soft-skin vehicles"],
  mission:"Humanitarian liaison and evacuation routes",
  status:"Operational", coordinates:{lat:54.69,lng:25.28}, echelon:"CELL", readiness:"R2",
  sidc:"SNGPUC---------" }
```

## Anti-patterns
- ❌ Treating NEUTRAL units as "OPFOR-with-low-priority". They are not lower priority; they are *not on a side*. Engagement of neutrals is unlawful unless ROE explicitly allows it.
- ❌ Letting NEUTRAL inherit OPFOR red colouring. Use NATO neutral green per APP-6 convention.
- ❌ Excluding NEUTRAL from filters. Operators must be able to declutter the COP, but NEUTRAL must default *on*.
- ❌ Forcing NEUTRAL units into the ACH matrix. Allow it (some neutral CoAs matter — e.g., civil evacuation routes), but don't require it.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v002.html` — filter, tally, chip CSS, OOB / ACH select extensions; default neutral units.
- `AJP/SUMMARIES/AJP-3.19.md` — doctrinal source (CIMIC).
- `roadmap.md § 6` — "NEUTRAL side".
- Skill `mil-symbology` — APP-6 affiliation char-2 `N` for neutral.
