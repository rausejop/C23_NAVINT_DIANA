---
name: cyber-domain
description: Add CYBER as the 5th operational domain alongside LAND / AIR / SEA / SUB across OOB, filters, tally, SIDC inference and editor selects.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    units: 'Unit[] possibly carrying domain:"CYBER"'
  outputSchema:
    enums: "domain enum extended; tally + filter chip + OOB <select> updated"
    units: "≥1 NATO + ≥1 OPFOR cyber units in the default mission"
  errorHandling:
    legacyImport: "OOB JSON without CYBER continues to load; CYBER tally cell renders 0"
  stateless: true
tools: [Read, Edit]
---

# cyber-domain

## Purpose
Recognise cyberspace as a distinct operational domain per **AJP-3.20**. Most NATO C2 platforms still treat CYBER as an event source rather than a domain — that's a doctrinal regression. v002 promotes CYBER to a peer of LAND/AIR/SEA/SUB.

## When to use
- The platform claims multi-domain awareness.
- A scenario involves DCO / OCO / DODIN-Ops actions, EW spillover, or red-team cyber activity.
- The user references AJP-3.20, "DCO", "OCO", "DODIN", "cyber as a domain".

## Inputs
- The OOB. Existing arrays continue to work; new units may carry `domain:"CYBER"`.
- The filter / tally / OOB-select code paths.

## Outputs
- `domain` enum extended to `LAND | AIR | SEA | SUB | CYBER` everywhere it appears.
- Filter chip `CYBER` on the LAYERS rail (default on).
- Tally row gains a `CYB` column (5-column grid).
- OOB editor `<select>` includes `CYBER`.
- Default mission ships ≥3 cyber units (in v002: NCIRC, CCDCOE Tallinn, GRU 26165).

## Instructions
1. **Extend the initial filter state**:
   ```js
   useState({ NATO:true, OPFOR:true, NEUTRAL:true,
              LAND:true, AIR:true, SEA:true, SUB:true, CYBER:true })
   ```
2. **Extend the tally factory** to include CYBER:
   ```js
   const blank = () => ({LAND:0, AIR:0, SEA:0, SUB:0, CYBER:0});
   ```
3. **Extend the tally render** to a 5-column grid (`tally-bars-5` CSS class):
   ```css
   .tally-bars-5 { grid-template-columns: repeat(5, 1fr); }
   ```
   Abbreviate the column header to `CYB` so the grid stays compact in the rail.
4. **Extend the filter chips array** to `["LAND","AIR","SEA","SUB","CYBER"]`.
5. **Extend the OOB-edit `<select>`** to include `<option>CYBER</option>`.
6. **Extend `getDomainFromSIDC`** with an informal char-2 mapping:
   ```js
   if (c === 'P') return 'CYBER';   // not in standard MIL-STD-2525B; chosen so legacy SIDCs still parse
   ```
   For real cyber units, set `domain:"CYBER"` explicitly in the OOB record; do not rely on SIDC inference.
7. **Seed cyber units** in the default mission. Use realistic names:
   - **NATO DCO**: NCIRC (Mons), CCDCOE Tallinn.
   - **OPFOR OCO**: GRU Unit 26165 (SPB).
8. **Document the DCO / OCO / DODIN acronyms** in the Acronyms tab.

## Examples

### Default cyber units (v002)
```js
{ id:"nc01", side:"NATO",  domain:"CYBER", designation:"NCIRC / NATO Cyber Defence Cell",
  type:"DCO", equipment:["Sensor grid","SIEM","DODIN-Ops"],
  mission:"Defensive Cyber Operations - Mons",
  status:"Operational", coordinates:{lat:50.45, lng:3.96}, echelon:"CELL", readiness:"R1",
  sidc:"SFGPUUS--------" }

{ id:"oc01", side:"OPFOR", domain:"CYBER", designation:"GRU Unit 26165 (OCO)",
  type:"OCO", equipment:["Spear-phish","Wiper malware","Supply-chain implants"],
  mission:"Offensive Cyber Operations - SPB",
  status:"Operational", coordinates:{lat:59.93, lng:30.32}, echelon:"CELL", readiness:"R1",
  sidc:"SHGPUUS--------" }
```

## Anti-patterns
- ❌ Storing cyber units with `domain:"LAND"` because "they're physically on land". Domain follows operational function, not the unit's physical location.
- ❌ Inventing a new SIDC scheme. Use the closest legitimate APP-6 symbol; the visual fidelity matters less than the discoverability of the unit through filters.
- ❌ Excluding CYBER from the tally because it's "not kinetic". Tally is force structure, not lethality.
- ❌ Treating any DDoS / spear-phish event as automatically CYBER-domain in the OOB. Events live in `intelEvents`; OOB units are persistent capabilities.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v002.html` — filter, tally, OOB-select extensions; default cyber units.
- `AJP/SUMMARIES/AJP-3.20.md` — doctrinal source.
- `roadmap.md § 2` — "CYBER as 5th domain".
- Skill `mil-symbology` — char-2 'P' → CYBER inference rule.
