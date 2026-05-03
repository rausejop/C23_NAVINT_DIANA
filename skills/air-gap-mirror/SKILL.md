---
name: air-gap-mirror
description: Convert a CDN-loaded single-file SPA into an air-gapped local-mirror build for use on tactical workstations without Internet access.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    htmlFile:    path to the SPA
    aor:         "{ minLat, minLng, maxLat, maxLng, minZoom, maxZoom }"  # for tile pre-fetch
    targetDir:   directory where mirrored assets will live
  outputSchema:
    bundleDir:   self-contained directory ready to ship to the workstation
    rewrittenHtml: path to the SPA with src=/href= rewritten to local paths
  errorHandling:
    networkFailure: "abort with the URL that failed; never partial-mirror silently"
  stateless: true
tools: [Read, Edit, Bash]
---

# air-gap-mirror

## Purpose
Take a working CDN-based single-file SPA (Leaflet, milsymbol, React, ReactDOM, Babel-standalone, fonts, basemap tiles) and produce a directory tree that runs **with zero outbound traffic**.

## When to use
- The platform must be deployed to a NATO restricted network or a tactical workstation.
- The user says "air-gapped", "offline", "no Internet", "STANAG environment", "TEMPEST".
- A demo will be shown in a SCIF or on an aircraft.

## Inputs
- The SPA HTML file (e.g. `C23_DIANA_NATO_WARFIGHTERS.html`).
- The Area of Responsibility (AOR) bounding box and required zoom range for tile pre-fetch.
- A target directory (e.g. `dist/airgap/`).

## Outputs
A directory like:
```
dist/airgap/
├── index.html                     ← rewritten SPA
├── vendor/
│   ├── leaflet-1.9.4/{leaflet.css, leaflet.js, images/…}
│   ├── milsymbol/milsymbol.js
│   ├── react-18.3.1/react.development.js
│   ├── react-dom-18.3.1/react-dom.development.js
│   ├── babel-7.29.0/babel.min.js
│   └── fonts/{IBM-Plex-Sans, JetBrains-Mono}/{*.woff2, fonts.css}
└── tiles/{z}/{x}/{y}.png          ← pre-fetched basemap tiles for the AOR
```

## Instructions

1. **Audit external references** in the SPA:
   ```bash
   grep -nE 'https?://' "$htmlFile"
   ```
2. **Mirror the JavaScript and CSS dependencies:**
   ```bash
   mkdir -p dist/airgap/vendor/{leaflet-1.9.4,milsymbol,react-18.3.1,react-dom-18.3.1,babel-7.29.0}
   curl -L -o dist/airgap/vendor/leaflet-1.9.4/leaflet.css   https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
   curl -L -o dist/airgap/vendor/leaflet-1.9.4/leaflet.js    https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
   curl -L -o dist/airgap/vendor/milsymbol/milsymbol.js      https://unpkg.com/milsymbol/dist/milsymbol.js
   curl -L -o dist/airgap/vendor/react-18.3.1/react.development.js          https://unpkg.com/react@18.3.1/umd/react.development.js
   curl -L -o dist/airgap/vendor/react-dom-18.3.1/react-dom.development.js  https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js
   curl -L -o dist/airgap/vendor/babel-7.29.0/babel.min.js                  https://unpkg.com/@babel/standalone@7.29.0/babel.min.js
   ```
   Also pull `leaflet/dist/images/` (marker shadow PNGs etc.).
3. **Mirror fonts.** Save the `fonts.googleapis.com/css2?family=…` response, rewrite each `src: url(...)` to a local path, then download every referenced `.woff2`.
4. **Pre-fetch basemap tiles** for the AOR / zoom range. Example for Carto Voyager:
   ```bash
   for z in 4 5 6 7; do
     for x in $(seq $minX $maxX); do
       for y in $(seq $minY $maxY); do
         mkdir -p dist/airgap/tiles/$z/$x
         curl -s -o dist/airgap/tiles/$z/$x/$y.png "https://a.basemaps.cartocdn.com/rastertiles/voyager_nolabels/$z/$x/$y.png"
       done
     done
   done
   ```
   (Use `tilebelt` / `slippy_tile` to compute `minX/maxX/minY/maxY` from the AOR.)
5. **Rewrite `<head>` references** in the HTML to point at the mirror:
   ```html
   <link rel="stylesheet" href="vendor/leaflet-1.9.4/leaflet.css"/>
   <script src="vendor/leaflet-1.9.4/leaflet.js"></script>
   <script src="vendor/milsymbol/milsymbol.js"></script>
   <script src="vendor/react-18.3.1/react.development.js"></script>
   <script src="vendor/react-dom-18.3.1/react-dom.development.js"></script>
   <script src="vendor/babel-7.29.0/babel.min.js"></script>
   <link href="vendor/fonts/fonts.css" rel="stylesheet"/>
   ```
6. **Rewrite the BASEMAPS table** in the JS to point at local tiles:
   ```js
   const BASEMAPS = {
     "carto-voyager": { url:"tiles/{z}/{x}/{y}.png", attr:"© OSM © CARTO (mirror)" }
   };
   ```
7. **Drop any `crossorigin=` and `integrity=` attributes** on the rewritten tags — these are CDN-only.
8. **Verify** with the browser offline:
   - Open DevTools → Network → throttle to "Offline".
   - Reload the page. **Zero requests should fail.**
9. **Lock the bundle:** `chmod -R a-w dist/airgap/` (or NTFS read-only) and ship.

## Examples

### One-shot dependency mirror
```bash
cat > mirror.sh <<'SH'
set -e
HTML="$1"; OUT="${2:-dist/airgap}"
mkdir -p "$OUT/vendor"
grep -oE 'https://[^"]+' "$HTML" | sort -u | while read u; do
  rel="vendor/$(basename "$u")"
  mkdir -p "$OUT/$(dirname "$rel")"
  curl -L --fail -o "$OUT/$rel" "$u"
done
SH
```

## Anti-patterns
- ❌ Mirror only the JS and assume tiles will work — they won't, and the COP renders blank water.
- ❌ Use `latest` URLs in the original SPA. They invalidate the mirror as soon as the upstream pushes.
- ❌ Skip the offline DevTools verification. "It works on my laptop" is not an attestation.
- ❌ Forget the Leaflet marker shadow / icon PNGs under `leaflet/dist/images/`.

## References
- `C23_DIANA_NATO_WARFIGHTERS.html` — every CDN URL that needs mirroring.
- **`tools/build_airgap_bundle.sh` (v005)** — reference implementation of this skill, runnable. Mirrors the six pinned CDN deps, fonts, Leaflet marker images, and pre-fetches Carto Voyager tiles for the 53–60°N · 17–31°E AOR at zoom 4..7. Produces `dist/airgap/`. Usage: `bash tools/build_airgap_bundle.sh [SOURCE_HTML] [OUT_DIR]`.
- DIANA Master Prompt deliverable K (Connectivity).
- Carto basemap usage: <https://carto.com/help/working-with-data/basemaps/>
- Skill `nato-classification` — banner / TEMPEST badging usually paired with air-gap.
