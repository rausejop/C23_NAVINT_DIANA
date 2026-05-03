---
name: echelon-rollup-and-scoping
description: Aggregate units by echelon tier (tactical / operational / strategic) and scope counts to a HQ AOR via bbox filtering.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    units: "OOB units carrying { side, echelon, coordinates }"
    hqs:   "[{ id, name, bbox?:[s,w,n,e] }]"
  outputSchema:
    rollup: "{ Tactical|Operational|Strategic: { NATO, OPFOR, NEUTRAL } }"
    scoped: "units inside the active HQ's bbox (or all if bbox null)"
  errorHandling:
    unknownEchelon: "default to Tactical tier"
  stateless: true
tools: [Read, Edit]
---

# echelon-rollup-and-scoping

## Purpose
Tactical / operational / strategic is the canonical NATO echelon split (AJP-3 / AJP-5). A C2 platform that only shows raw unit counts misses the point: commanders care about *what gets aggregated up* and *whose AOR it lives in*. This skill is the two patterns combined — the per-tier roll-up (CO-01) and the per-HQ bbox filter (CO-02).

## When to use
- The OOB has units across multiple echelons (BG / BCT / BDE / DIV / CORPS / ARMY / etc).
- Multiple HQs share the AOR and each has its own area of responsibility.
- The user references "tactical/operational/strategic", "echelon", "JFC", "TCC", "SHAPE".

## Inputs
- The full OOB.
- A list of HQs, each optionally carrying a bounding box `[south, west, north, east]`. A null bbox means the whole AOR (e.g. SHAPE).

## Outputs
- A roll-up grid: `{ Tactical, Operational, Strategic } × { NATO, OPFOR, NEUTRAL }` with counts.
- A per-HQ scoped list of units (filter by bbox).

## Instructions

1. **Define the echelon → tier mapping centrally.** A pure helper that doesn't reach into React state:
   ```js
   const ECHELON_TIER = (e) => {
     const tac = ["BG","BCT","BDE","DET","REGT","FFG","SSK","MCM","FSG","CELL","FLT","FERRY","LHD"];
     const opn = ["DIV"];
     const str = ["CORPS","ARMY"];
     const x = (e||"").toUpperCase();
     if (str.includes(x)) return "Strategic";
     if (opn.includes(x)) return "Operational";
     if (tac.includes(x)) return "Tactical";
     return "Tactical";
   };
   ```
2. **Default to Tactical** for unknown echelons rather than emitting a `?` row. The grid column shape stays clean.
3. **Roll up with `useMemo([units])`** — the grid is pure-derived, no state.
4. **Bbox filter is a one-liner**:
   ```js
   const inBox = (u, bbox) => {
     if (!bbox) return true;
     const [s,w,n,e] = bbox;
     return u.coordinates && u.coordinates.lat>=s && u.coordinates.lat<=n
                          && u.coordinates.lng>=w && u.coordinates.lng<=e;
   };
   ```
5. **Render the grid as a small 4-column table** (TIER · NATO · OPFOR · NEUTRAL) with totals. Then list units per tier in collapsible/scrollable sub-tables.
6. **HQ presets matter.** Ship a few canonical HQs in code (SHAPE = whole AOR, JFC-BAL = Baltic AOR, TCC-N / TCC-S = sub-areas) so the analyst doesn't have to type bboxes.
7. **Keep bbox in `[s,w,n,e]` order**, not `[lat,lng,lat,lng]`. Match the GeoJSON bbox convention so a future migration to GeoJSON is trivial.

## Examples

### HQ presets (paste-ready, from v008)
```js
const C23_HQS = [
  { id:"shape",   name:"SHAPE",   bbox:null /* whole AOR */ },
  { id:"jfc-bal", name:"JFC-BAL", bbox:[53,17,60,31] },
  { id:"tcc-n",   name:"TCC-N (Estonia/Latvia/Finland)", bbox:[57,21,60.5,29] },
  { id:"tcc-s",   name:"TCC-S (Lithuania/Poland)",       bbox:[52,17,57,26] }
];
```

### Roll-up grid render
```jsx
{tiers.map(t => (
  <tr key={t}>
    <td><b>{t}</b></td>
    <td className="mono" style={{color:"var(--allied)"}}>{grid[t].NATO.length}</td>
    <td className="mono" style={{color:"var(--hostile)"}}>{grid[t].OPFOR.length}</td>
    <td className="mono" style={{color:"var(--neutral)"}}>{grid[t].NEUTRAL.length}</td>
    <td className="mono">{grid[t].NATO.length + grid[t].OPFOR.length + grid[t].NEUTRAL.length}</td>
  </tr>
))}
```

## Anti-patterns
- ❌ Inferring tier from SIDC echelon code at render time. The platform's `echelon` field is the truth; SIDC is a sibling representation.
- ❌ Letting the analyst freely type tier names. The three-tier vocabulary is doctrinal — don't open it up.
- ❌ A bbox per unit. Units have a single coord; HQs have AORs. Don't mix.
- ❌ No SHAPE-equivalent (whole-AOR) preset. Forces the user to compute the union manually.
- ❌ Storing the rollup as state. It's a pure function of `units`.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v005.html` — `RollUpTab` (CO-01).
- `C23_DIANA_NATO_WARFIGHTERS_v008.html` — `IntelOpsTab` HQ scoping (CO-02).
- AJP-3 (Conduct of Operations) — tactical/operational/strategic split.
