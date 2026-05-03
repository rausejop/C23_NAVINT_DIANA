---
name: movement-entities
description: Add MSR / ASR polylines and APOD / SPOD point entities to a NATO COP, with status-coloured rendering and CRUD per AJP-3.13 / AJP-4.4.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    msrs:  "[{ id, name, status:'Open|Contested|Cut', coords:[[lat,lng], ...] }]"
    asrs:  "[{ id, name, status, coords:[[lat,lng], ...] }]"
    apods: "[{ id, name, nation, status, coords:[lat,lng] }]"
    spods: "[{ id, name, nation, status, coords:[lat,lng] }]"
  outputSchema:
    tab:    "MOVEMENT modal tab in the Mission Editor"
    overlay: "Polylines (MSR solid, ASR dashed) + circle markers (APOD blue, SPOD green)"
    toggle:  "MSR / ASR / APOD / SPOD layer toggle on the LAYERS rail"
  errorHandling:
    badPolyline: "the parser tolerates trailing semicolons and whitespace; rejects pairs with NaN"
  stateless: true
tools: [Read, Edit]
---

# movement-entities

## Purpose
Surface deployment / movement infrastructure as first-class entities on the COP per **AJP-3.13** (Deployment & Redeployment) and **AJP-4.4** (Movement). MSR (Main Supply Routes) and ASR (Alternate Supply Routes) carry status colour; APOD / SPOD carry status + nation. Closing the loop with the existing Phase-3 `locCut` polyline: that legacy overlay is still drawn for the wargame, but real-world supply routing now lives in `mission.movement` and is editable.

## When to use
- The platform must show how a force gets to and through theatre, not only where units sit.
- A scenario involves theatre opening, RSOM, MSR/ASR cut, or deployment from APOD/SPOD.
- The user references AJP-3.13 / AJP-4.4, "MSR", "ASR", "APOD", "SPOD", "RSOM", "MOVCON".

## Inputs
A `mission.movement` object with four arrays (see schema). Default mission seeds two MSRs (one Open, one Contested), one ASR, three APODs (Riga / Šiauliai / Ämari) and two SPODs (Gdańsk / Klaipėda).

## Outputs
- A `MOVEMENT` tab in the Mission Editor with four sub-tables (RouteTable for MSR/ASR, PortTable for APOD/SPOD).
- A map overlay (toggleable) drawing:
  - MSR as solid polylines, weight 4, status-coloured.
  - ASR as dashed polylines (`dashArray:"4,6"`), weight 3, status-coloured.
  - APOD as blue ringed dots; SPOD as green ringed dots.
- A `MSR / ASR / APOD / SPOD` toggle on the LAYERS rail (default on).

## Instructions
1. **Add `mission.movement`** with four arrays. Polylines are arrays of `[lat,lng]` pairs.
2. **Render in a dedicated `useEffect`** keyed `[tweaks.showMovement, mission.movement]`. Always clear the previous layer set via `movementLayerRef`.
3. **Status colour helper** — map status → colour once, use everywhere:
   ```js
   const statusColor = (s) => s==="Cut" ? "#e85d50"
                            : s==="Contested" ? "#f59e0b"
                            : "#7cd8a8";
   ```
4. **Polyline editor accepts a flat string** like `"54.40,18.66; 54.10,20.10; 55.08,24.19"`. Parse with `split(";").map(s=>s.trim().split(",").map(parseFloat))` and reject pairs with `NaN` so a half-typed entry doesn't blow up the layer.
5. **APOD vs SPOD distinction** is visual (blue vs green ring) and semantic (`status:"Open|Contested|Closed"`). Both are point geometry; do not give them polyline schemas.
6. **Tooltip every layer.** Operators must see `name · status · nation` without clicking.
7. **Add the layer toggle** on the LAYERS rail with default `true` (use `tweaks.showMovement!==false` so the toggle treats unset as on).
8. **Add the acronyms** APOD, SPOD, ASR, RSOM, MOVCON, MCCE to the Acronyms tab (RSOM and MSR already existed).
9. **Default the legacy `phase3Polygons.locCut` polyline alone**: MSR rendering is additive and persistent; the wargame's `locCut` is still a Phase-3-only overlay.

## Examples

### MSR seed (Contested)
```js
{ id:"msr02", name:"MSR BALTIC (Riga→Tapa)", status:"Contested",
  coords:[[56.92,23.97],[57.82,24.40],[59.26,25.97]] }
```

### Movement layer effect (abbreviated)
```js
useEffect(() => {
  const m = mapRef.current; if (!m) return;
  movementLayerRef.current.forEach(l => m.removeLayer(l));
  movementLayerRef.current = [];
  if (tweaks.showMovement===false) return;
  (mission.movement?.msrs||[]).forEach(r => {
    const ln = L.polyline(r.coords, { color:statusColor(r.status), weight:4, opacity:0.85 })
      .bindTooltip(`<b>${r.name}</b><br/>MSR · ${r.status}`, {direction:"top"}).addTo(m);
    movementLayerRef.current.push(ln);
  });
  /* …same for asrs (dashed), apods (blue ring), spods (green ring) */
}, [tweaks.showMovement, mission.movement]);
```

## Anti-patterns
- ❌ Treating MSR/ASR as decorations. Their `status` is operationally meaningful (Cut MSR triggers FPCON / sustainment alarms).
- ❌ Storing polylines as comma-separated strings. The on-disk representation must be `[[lat,lng], …]`. The string form is only for the inline editor cell.
- ❌ Putting APOD/SPOD inside the OOB. They are infrastructure, not units; mixing them breaks tally and side filters.
- ❌ Hard-coding the Phase-3 `locCut` MSR severance. v002 keeps the legacy `locCut` overlay *and* exposes editable MSRs — both are valid; do not collapse.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v002.html` — `MovementTab`, `movementLayerRef`, `mission.movement` seed.
- `AJP/SUMMARIES/AJP-3.13.md`, `AJP/SUMMARIES/AJP-4.4.md`.
- `roadmap.md § 4` — Movement & Sustainment tracking.
