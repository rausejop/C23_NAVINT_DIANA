---
name: posture-indicators
description: Surface FPCON / CBRN / PNT / CIS-PACE as colour-coded top-bar tiles backed by a CRUD POSTURE tab.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    posture: "{ fpcon:'Alpha|Bravo|Charlie|Delta', cbrn:'Green|Yellow|Red', pnt:'Nominal|Degraded|Denied', cisPace:'P|A|C|E' }"
  outputSchema:
    tiles: "Four meta-blocks on the top bar, status-coloured"
    tab:   "POSTURE modal tab in the Mission Editor"
  errorHandling:
    unknownValue: "fall back to lowest-severity tone; do not throw"
  stateless: true
tools: [Read, Edit]
---

# posture-indicators

## Purpose
Make the operational posture of the force visible at all times — without needing to open a modal. Four discrete indicators implement four distinct AJPs:

- **FPCON** (AJP-3.14 Force Protection) — Alpha → Bravo → Charlie → Delta.
- **CBRN ALERT** (AJP-3.23 CWMD) — Green → Yellow → Red.
- **PNT STATUS** (AJP-3.3 Air & Space Ops, EW context) — Nominal → Degraded → Denied.
- **CIS PACE** (AJP-6 CIS) — Primary → Alternate → Contingency → Emergency.

## When to use
- The platform claims multi-domain situational awareness.
- A scenario can degrade GPS / comms / put forces under chemical threat — those degradations must be visible above the fold.
- The user references AJP-3.14 / 3.23 / 3.3 / 6 or "FPCON", "CBRN ALERT", "PNT denied", "PACE plan".

## Inputs
A `mission.posture` object with the four enum values.

## Outputs
- Four meta-blocks on the top bar (between MODE and OP TYPE) with semantic colour:
  - **Green / Mint** for the lowest severity (Alpha / Green / Nominal / P).
  - **Yellow** for the next (Bravo / Yellow / — / A).
  - **Orange** for Charlie / — / — / C.
  - **Red** for Delta / Red / Denied / E.
- A `POSTURE` tab in the Mission Editor with four `<select>` controls.

## Instructions
1. **Add `mission.posture`** with the four keys (default Alpha / Green / Nominal / P).
2. **Render each tile** with a className that drives the colour:
   ```jsx
   <div className={`meta-block posture-fpcon-${(p.fpcon||"alpha").toLowerCase()}`}>
     <div className="meta-label">FPCON</div>
     <div className="meta-val mono">{(p.fpcon||"—").toUpperCase()}</div>
   </div>
   ```
3. **Define one CSS rule per (indicator, value)** rather than computing colour in JSX:
   ```css
   .meta-block.posture-fpcon-alpha   .meta-val{color:var(--mint);}
   .meta-block.posture-fpcon-bravo   .meta-val{color:#f5d65e;}
   .meta-block.posture-fpcon-charlie .meta-val{color:#ff9b3a;}
   .meta-block.posture-fpcon-delta   .meta-val{color:var(--hostile);}
   ```
   Repeat for cbrn / pnt / pace. This keeps colour theming centralised and printable.
4. **Edit via the POSTURE tab.** Each indicator is a single `<select>`; on change, write back to `mission.posture[<key>]` and re-render.
5. **Persist in mission JSON.** An exported mission carries its posture; an imported mission applies it on first paint (no extra plumbing needed because `mission.posture` is a plain key).
6. **Add to Acronyms.** FPCON, CBRN, PNT, CIS PACE must each appear in the in-platform Acronyms tab.

## Examples

### Mission seed
```js
posture: { fpcon:"Bravo", cbrn:"Green", pnt:"Degraded", cisPace:"P" }
```
This produces: amber FPCON tile, mint CBRN tile, amber PNT tile, mint CIS PACE tile.

### Where the colour comes from
A simple class concatenation. No JS branching for colour:
```jsx
<div className={`meta-block posture-pnt-${p.pnt.toLowerCase()}`}>
```

## Anti-patterns
- ❌ Coupling posture to phase. Operators must be able to crank FPCON to Charlie regardless of the wargame phase.
- ❌ Picking colours in JSX with ternaries. The CSS-class approach scales (adding a fifth FPCON value is one CSS line).
- ❌ Hiding posture inside CONFIG only. The whole point is constant visibility on the top bar.
- ❌ Using "DEFCON" instead of "FPCON". DEFCON is a US national alert level; FPCON is the NATO/US force-protection condition. AJP-3.14 uses FPCON.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v002.html` — top-bar tiles, `PostureTab`, `mission.posture` seed.
- `AJP/SUMMARIES/AJP-3.14.md`, `AJP/SUMMARIES/AJP-3.23.md`, `AJP/SUMMARIES/AJP-3.3.md`, `AJP/SUMMARIES/AJP-6.md`.
- `roadmap.md § 5` — Force Protection / CBRN tracking.
- `roadmap.md § 1` — CIS posture tracking.
