---
name: ais-fusion
description: Ingest AIS commercial-vessel feeds (Master Prompt ANNEX schema), render them on a Leaflet COP, and flag dark-AIS / suspect tracks.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    feed: '{ DATA: AisRecord[], METADATA: {...} }   # see Master Prompt ANNEX'
  outputSchema:
    layer: a Leaflet layer group with one triangular marker per vessel
    flags: list of vessels marked dark-AIS / suspect
  errorHandling:
    badLatLng: "skip the record with one warn-tone log line"
    schemaDrift: "tolerate missing optional fields; require MMSI, LAT, LON"
  stateless: true
tools: [Read, Edit]
---

# ais-fusion

## Purpose
Add a maritime situational-awareness layer to a multi-domain COP using the AIS schema fixed in the C23 Master Prompt ANNEX (`SHIPNAME, MMSI, IMO, LAT, LON, SPEED, HEADING, FLAG, TYPE_NAME, DESTINATION, LAST_PORT, …`). Suspect tracks (dark-AIS, FLAG-of-convenience near CUI) get visually distinguished.

## When to use
- The platform claims maritime / Baltic / SLOC awareness.
- The user provides AIS JSON or asks for "dark-vessel detection" or "commercial maritime fusion".
- AJP-3.1 (Maritime) features are in scope.

## Inputs
- A JSON object with the canonical shape:
  ```jsonc
  { "DATA": [ { "MMSI":"…", "LAT":"…", "LON":"…", "SHIPNAME":"…", "FLAG":"…",
                "DESTINATION":"…", "LAST_PORT":"…", "SPEED":"…", "HEADING":"…",
                "TYPE_NAME":"…", … } ],
    "METADATA": { "DATE_FROM":"…", "DATE_TO":"…", "CURSOR":"…" } }
  ```
- The list of `cuiNodes` (so proximity heuristics can flag suspect tracks).

## Outputs
- A Leaflet layer with one triangular `L.polygon` per vessel (heading-rotated optional).
- Tooltip: `<b>SHIPNAME</b><br/>TYPE_NAME · FLAG<br/>MMSI … · SPEED kn HEADING°<br/>Last port: …`.
- Per-vessel `dark` flag for visual styling and downstream alerting.

## Instructions

1. **Parse `LAT/LON` as floats** and skip records where either is `NaN` (data drift is common).
2. **Detect dark-AIS / suspect tracks.** Initial heuristics (extend per OPINTEL):
   - `DESTINATION` contains `"AIS OFF"` or empty + `LAST_PORT` non-empty.
   - `FLAG = "RU"` AND `SHIPNAME` starts with `"DARK ECHO"` (synthetic test pattern).
   - Optional: distance(vessel, nearest CUI) < 5 nm + speed < 4 kn → loitering near cable.
3. **Render as a triangle** so vessels never collide visually with land-unit MIL-STD-2525B icons:
   ```js
   const tri = L.polygon([[lat+0.06,lng],[lat-0.04,lng-0.06],[lat-0.04,lng+0.06]],
     { color, fillColor:color, fillOpacity:0.55, weight:1 })
     .bindTooltip(tooltipHtml, {direction:"top",offset:[0,-6]}).addTo(map);
   ```
   - `color = dark ? "#e85d50" : "#7cd8a8"` (red for suspect, mint for clean).
4. **Manage the layer life-cycle in a `useEffect`** keyed on `[tweaks.showAIS, mission.aisFeed]`. Always remove the previous layer set before re-rendering.
5. **Expose a CRUD editor** (one row per vessel) so analysts can append observed tracks without leaving the platform.
6. **Provide JSON file import** with a strict check: `Array.isArray(data.DATA)`. Reject otherwise with a readable error.
7. **Log every load** through the same Command-log channel (`AIS` prefix) so audit is consistent.

## Examples

### One vessel record (default mission, dark-AIS test pattern)
```json
{
  "MMSI":"273450910", "IMO":"9300012",
  "LAT":"59.42", "LON":"24.55", "SPEED":"11", "HEADING":"265",
  "STATUS":"0", "TIMESTAMP":"2026-04-29T11:35:00.000Z", "DSRC":"TER",
  "MARKET":"TANKER", "SHIPNAME":"DARK ECHO 1", "FLAG":"RU",
  "TYPE_NAME":"Crude Oil Tanker", "DESTINATION":"FOR ORDERS",
  "LAST_PORT":"PRIMORSK", "LAST_PORT_TIME":"2026-04-28T18:00:00.000Z"
}
```
Renders red because `FLAG=RU` and `SHIPNAME` begins with `DARK ECHO`.

### Suspect detector (compact)
```js
function isSuspect(v) {
  const dest = (v.DESTINATION||"").toUpperCase();
  if (dest.includes("AIS OFF")) return true;
  if (v.FLAG==="RU" && (v.SHIPNAME||"").startsWith("DARK")) return true;
  return false;
}
```

## Anti-patterns
- ❌ Drawing AIS vessels as MIL-STD-2525B icons. They are commercial; a separate visual class avoids confusion with combatants.
- ❌ Hard-coding a single suspect heuristic. Make `isSuspect()` swappable so OPINTEL can extend it.
- ❌ Ingesting feeds without metadata (`DATE_FROM`, `DATE_TO`). Time-bound staleness is part of the source-of-truth.

## References
- `C23_DIANA_NATO_WARFIGHTERS.html` — `AISTab`, AIS layer effect.
- Master Prompt ANNEX `§ 4` — AIS Format.
- AJP-3.1 — Allied Joint Doctrine for Maritime Operations.
