---
name: mil-symbology
description: Render MIL-STD-2525B / APP-6 unit symbols with the milsymbol library, derive domain from SIDC, and embed SIDC previews in editor forms.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    sidc: 15-character MIL-STD-2525B Symbol Identification Code
    size: int (default 30)
  outputSchema:
    svg: SVG markup
    domain: "LAND | AIR | SEA | SUB"
  errorHandling:
    invalidSidc: "return divIcon with grey 24x24 placeholder; never throw"
  stateless: true
tools: [Read, Edit]
---

# mil-symbology

## Purpose
Render correct, hover-scalable, drop-shadowed unit icons using the **milsymbol** library and the 15-char SIDC convention.

## When to use
- The COP / OOB needs APP-6-compliant icons.
- The user types a SIDC and wants a live preview while editing a unit.
- Domain (LAND / AIR / SEA / SUB) must be inferred from the SIDC if not stored separately.

## Inputs
- `sidc` — 15-character string (e.g. `SFGPUCA----E---`).
- `size` — pixel size of the rendered glyph (default 30, range 20–48).

## Outputs
- `buildSidcIcon(unit, size)` returns a Leaflet `divIcon` with the milsymbol SVG inside.
- `getDomainFromSIDC(sidc)` returns one of `"LAND" | "AIR" | "SEA" | "SUB"`.

## Instructions

1. **Pin milsymbol from a CDN** in the `<head>`: `<script src="https://unpkg.com/milsymbol/dist/milsymbol.js"></script>`.
2. **Wrap the construction in try/catch** — invalid SIDCs are common in user input and must never break the map:
   ```js
   function buildSidcIcon(unit, size) {
     try {
       const sym = new ms.Symbol(unit.sidc, { size, strokeWidth:4, fillOpacity:1, infoColor:"white" });
       const a   = sym.getAnchor();
       return L.divIcon({
         className: `unit-marker-app6 side-${unit.side}`,
         html: `<div style="width:${sym.width}px; height:${sym.height}px;">${sym.asSVG()}</div>`,
         iconSize:  [sym.width, sym.height],
         iconAnchor:[a.x, a.y]
       });
     } catch {
       return L.divIcon({ className:"unit-marker-app6",
         html:"<div style='width:24px;height:24px;background:#888'></div>" });
     }
   }
   ```
3. **Derive domain from SIDC char index 2** (the "battle dimension"):
   ```js
   const getDomainFromSIDC = (sidc) => {
     if (!sidc || sidc.length < 3) return 'LAND';
     const c = sidc.charAt(2).toUpperCase();
     if (c === 'A') return 'AIR';   if (c === 'G') return 'LAND';
     if (c === 'S') return 'SEA';   if (c === 'U') return 'SUB';
     /* v002 — informal extension: char-2 'P' → CYBER (no standard APP-6 dimension yet) */
     if (c === 'P') return 'CYBER';
     return 'LAND';
   };
   ```
   For real cyber units, set `domain:"CYBER"` explicitly in the OOB record — see skill `cyber-domain`.
4. **Live SIDC preview in the editor** — use `useMemo` so the SVG re-builds only on SIDC change:
   ```js
   const sidcPreview = useMemo(() => {
     try { return new ms.Symbol(form.sidc,{size:38,strokeWidth:4,fillOpacity:1}).asSVG(); }
     catch { return null; }
   }, [form.sidc]);
   ```
5. **Constrain editor input** to 15 chars and uppercase: `<input maxLength={15} onChange={e => set(e.target.value.toUpperCase())}/>`.
6. **Add hover scale + drop-shadow via CSS:**
   ```css
   .unit-marker-app6 { filter: drop-shadow(0px 0px 5px rgba(0,0,0,0.8));
                       transition: transform .2s; }
   .unit-marker-app6:hover { transform: scale(1.2); z-index:1000 !important; }
   ```

## Examples

### NATO Battle Group (eFP Estonia)
```
SFGPUCA----E---
│└─ identity affiliation: F = Friend
│   ┌── battle dimension: G = LAND
│   │┌─ status: P = Present
│   ││ ┌── unit indicator
│   ││ │
S F G P U C A----E---
                ↑↑↑
                echelon: E = Battalion
```

### OPFOR Submarine
```
SHUPSL---------
   ↑
   battle dimension U = Underwater (SUB)
```

### NEUTRAL Civil Airliner (v002)
```
SNAPCF---------
 ↑↑
 ││ battle dimension A = AIR
 │  affiliation N = Neutral (renders as APP-6 neutral-green diamond)
```

## Anti-patterns
- ❌ Generating raster (PNG) icons. Use the milsymbol SVG output.
- ❌ Storing `domain` only — keep both `sidc` and a derived `domain`. Imports may have one without the other.
- ❌ Skipping the try/catch — bad SIDCs from user input are guaranteed to occur.

## References
- `C23_DIANA_NATO_WARFIGHTERS.html` — `buildSidcIcon`, `getDomainFromSIDC`, `OOBTab` SIDC preview.
- milsymbol: <https://github.com/spatialillusions/milsymbol>
- MIL-STD-2525B and APP-6 (NATO).
