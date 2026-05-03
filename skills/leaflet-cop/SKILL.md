---
name: leaflet-cop
description: Build a NATO-styled Common Operating Picture on Leaflet — multi-layer toggles, animated phases, A2/AD bastions, CUI / AIS overlays.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    units:        "Unit[] with sidc + coordinates"
    a2adZones:    "[{ name, center, radiusKm, color }]"
    cuiNodes:     "[{ name, coords, kind }]"
    phaseVectors: "{ phaseN_<domain>: { unitId: [lat,lng] } }"
  outputSchema:
    component: "<App/> mounting Leaflet into a ref'd div"
  errorHandling:
    leafletMissing: "fail loudly with a single error in #root"
    badSidc:        "fall back to a grey 24x24 square divIcon"
  stateless: true
tools: [Read, Edit]
---

# leaflet-cop

## Purpose
Provide the recurring scaffolding for a NATO Common Operating Picture: dark theme, gold/blue accents, classification banner, layer toggles, phase ladder, animated unit movement, and the standard intel/dossier side panels.

## When to use
- Any Allied / OPFOR map view that needs MIL-STD-2525B symbology.
- A wargame UI requiring sequential phase execution with overlays.
- A maritime / multi-domain situational-awareness panel.

## Inputs
- `units[]`: each `{ id, sidc, side, domain, designation, type, coordinates:{lat,lng}, ... }`.
- `a2adZones[]`, `cuiNodes[]`, `phaseVectors{}`, `phase3Polygons{}`.
- `phaseLogs{}`: `{ phaseId: [[delayMs, prefix, msg, tone], …] }`.

## Outputs
- A React component that mounts Leaflet (`L.map`) on a `mapEl` ref.
- One marker per visible unit, rendered as a milsymbol SVG `divIcon`.
- One filtered set of overlays (A2/AD circles, CUI dots, AIS triangles).

## Instructions

1. **Mount Leaflet once** in a `useEffect` keyed `[]`:
   ```js
   useEffect(() => {
     if (mapRef.current) return;
     const m = L.map(mapEl.current, { center:[58,22], zoom:5, zoomControl:false, attributionControl:false });
     L.control.zoom({position:"bottomright"}).addTo(m);
     mapRef.current = m;
   }, []);
   ```
2. **Swap the basemap in its own effect** keyed `[tweaks.basemap]`. Always remove the previous tile layer first.
3. **Re-render unit markers** in an effect keyed `[units, filter, tweaks.symbolSize]`. Always clear the prior set:
   ```js
   Object.values(markersRef.current).forEach(m => map.removeLayer(m));
   markersRef.current = {};
   ```
4. **Use `L.divIcon` with milsymbol SVG** — never raster icons. See skill `mil-symbology`.
5. **Animate movement with `requestAnimationFrame`** (ease-out cubic) and store frame ids in a ref so `Reset Op` can `cancelAnimationFrame` them.
6. **Phase overlays:** A2/AD = pulsing `L.circle`, vectors = dashed `L.polyline` + arrowhead `L.circleMarker`, occupation polygons = `L.polygon`, LOC cuts = thick dashed polyline.
7. **Persistent overlays (v002+):** AIS triangles, CUI dots, Movement (MSR/ASR polylines + APOD/SPOD ringed dots — see skill `movement-entities`), JPTL target rings (see skill `joint-targeting-jtc`). Each lives in its own `useEffect` keyed on `[tweaks.show<X>, mission.<key>]` and its own dedicated layer ref so toggles and re-renders are independent of phase execution.
8. **Track every *phase-driven* layer** in `dynamicLayerRef.current` so Reset is one loop. Persistent overlays use their own refs and are *not* cleared on Reset.
9. **HUD pills** for AOR / Fusion / Units / Dossier go in absolutely-positioned `<div className="hud hud-tl|tr|bl">` overlays *outside* the Leaflet pane (zIndex ≥ 500).
10. **Click handlers must `L.DomEvent.stopPropagation`** the click event before invoking React state setters.
11. **Map container styling:** use `position:absolute; inset:0` on the map; the parent `.stage` gets `position:relative`. This is what makes Leaflet fill its grid cell properly.

## Examples

### Animate a unit to a target lat/lng
```js
const animateUnit = (unitId, target, duration) => {
  const marker = markersRef.current[unitId]; if (!marker) return;
  const start = marker.getLatLng();
  const dLat = target[0]-start.lat, dLng = target[1]-start.lng;
  let t0 = null;
  const step = (ts) => {
    if (!t0) t0 = ts;
    const pct  = Math.min((ts-t0)/duration, 1);
    const ease = 1 - Math.pow(1-pct, 2.4);
    marker.setLatLng([start.lat + dLat*ease, start.lng + dLng*ease]);
    if (pct < 1) animFramesRef.current.push(requestAnimationFrame(step));
    else setUnits(us => us.map(u => u.id===unitId
      ? {...u, coordinates:{lat:start.lat+dLat,lng:start.lng+dLng}} : u));
  };
  animFramesRef.current.push(requestAnimationFrame(step));
};
```

## Anti-patterns
- ❌ Re-creating `L.map` on every render. Init exactly once via `useEffect([])`.
- ❌ Storing markers in React state. They are imperative DOM objects — use a ref.
- ❌ Tying overlays to React render loops. Use Leaflet layers + a tracking ref.
- ❌ Forgetting to clear animation frames on Reset → ghost units keep moving.
- ❌ Hard-coding the basemap URL inside the JSX — keep `BASEMAPS` as a tweak.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v009.html` — `App`, `MapHud`, `PhaseGate`, the persistent layer effects (AIS / CUI / Movement / JPTL), and the **v006 `flyToUnit()` helper** exposed as `window.__c23_flyTo(unit)` so any tab (notably the OOB CRUD table) can fly the map to a unit and pulse a transient gold ring.
- Leaflet 1.9 docs: <https://leafletjs.com/reference.html>
- Skill `mil-symbology` — for the divIcon contents.
