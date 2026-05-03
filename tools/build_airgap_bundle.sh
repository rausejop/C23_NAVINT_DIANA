#!/usr/bin/env bash
# tools/build_airgap_bundle.sh — DP-01 (v005)
# Produces dist/airgap/ with every CDN dependency mirrored locally and the SPA
# rewritten to point at those mirrors. Verifiable with the browser set offline.
#
# Usage: bash tools/build_airgap_bundle.sh [SOURCE_HTML] [OUT_DIR]
# Defaults: SOURCE_HTML=C23_DIANA_NATO_WARFIGHTERS.html  OUT_DIR=dist/airgap
#
# Prerequisites: curl, sed, mkdir.  No pip/npm. No internet at runtime once built.

set -euo pipefail

SRC="${1:-C23_DIANA_NATO_WARFIGHTERS.html}"
OUT="${2:-dist/airgap}"

if [[ ! -f "$SRC" ]]; then
  echo "[!] Source HTML not found: $SRC" >&2
  exit 1
fi

echo "[*] Source : $SRC"
echo "[*] Output : $OUT"
mkdir -p "$OUT/vendor"

# ── 1. Fixed CDN dependencies (pinned versions — match the SPA <head>) ──────
declare -A DEPS=(
  ["leaflet@1.9.4/dist/leaflet.css"]="vendor/leaflet-1.9.4/leaflet.css"
  ["leaflet@1.9.4/dist/leaflet.js"]="vendor/leaflet-1.9.4/leaflet.js"
  ["milsymbol/dist/milsymbol.js"]="vendor/milsymbol/milsymbol.js"
  ["react@18.3.1/umd/react.development.js"]="vendor/react-18.3.1/react.development.js"
  ["react-dom@18.3.1/umd/react-dom.development.js"]="vendor/react-dom-18.3.1/react-dom.development.js"
  ["@babel/standalone@7.29.0/babel.min.js"]="vendor/babel-7.29.0/babel.min.js"
)

for k in "${!DEPS[@]}"; do
  url="https://unpkg.com/$k"
  dest="$OUT/${DEPS[$k]}"
  mkdir -p "$(dirname "$dest")"
  if [[ -f "$dest" ]]; then
    echo "  [.] $dest exists"
  else
    echo "  [+] $url → $dest"
    curl -L --fail --silent --show-error -o "$dest" "$url"
  fi
done

# Leaflet marker images (used by L.icon defaults; small but required)
mkdir -p "$OUT/vendor/leaflet-1.9.4/images"
for img in marker-icon.png marker-icon-2x.png marker-shadow.png; do
  dest="$OUT/vendor/leaflet-1.9.4/images/$img"
  if [[ ! -f "$dest" ]]; then
    echo "  [+] leaflet image: $img"
    curl -L --fail --silent --show-error -o "$dest" "https://unpkg.com/leaflet@1.9.4/dist/images/$img"
  fi
done

# ── 2. Fonts: download the CSS, rewrite the @font-face URLs, fetch each woff2 ──
mkdir -p "$OUT/vendor/fonts"
FONTS_CSS_URL='https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap'
RAW_CSS="$OUT/vendor/fonts/_raw.css"
echo "  [+] fonts.css from Google Fonts"
curl -L --fail --silent --show-error -A "Mozilla/5.0" -o "$RAW_CSS" "$FONTS_CSS_URL"

# Pull every .woff2 referenced by the CSS, mirror locally, rewrite the URL.
LOCAL_CSS="$OUT/vendor/fonts/fonts.css"
cp "$RAW_CSS" "$LOCAL_CSS"
grep -oE 'https://fonts\.gstatic\.com/[^)]+\.woff2' "$RAW_CSS" | sort -u | while read -r u; do
  fname="$(basename "$u")"
  if [[ ! -f "$OUT/vendor/fonts/$fname" ]]; then
    echo "    [+] font: $fname"
    curl -L --fail --silent --show-error -o "$OUT/vendor/fonts/$fname" "$u"
  fi
  # Rewrite reference in the local CSS to point at the local file
  sed -i.bak "s|$u|$fname|g" "$LOCAL_CSS"
done
rm -f "$LOCAL_CSS.bak" "$RAW_CSS"

# ── 3. Carto basemap tiles for the Baltic AOR (zoom 4..7, ~1500 tiles) ──────
echo "[*] Pre-fetching Carto basemap tiles for the Baltic AOR (zoom 4..7) …"
mkdir -p "$OUT/tiles"
# Tile XY for lat/lon at zoom z (slippy-map convention, computed inline)
tilexy() {
  awk -v lat="$1" -v lon="$2" -v z="$3" 'BEGIN{
    n = 2 ^ z;
    x = int((lon + 180.0) / 360.0 * n);
    rad = lat * 3.141592653589793 / 180.0;
    y = int((1 - log(sin(rad)/cos(rad) + 1/cos(rad)) / 3.141592653589793) / 2 * n);
    print x, y;
  }'
}
# AOR bbox: 53–60°N · 17–31°E (matches mission.aor in the SPA)
LAT_N=60; LAT_S=53; LON_W=17; LON_E=31
for z in 4 5 6 7; do
  read -r XW YN < <(tilexy "$LAT_N" "$LON_W" "$z")
  read -r XE YS < <(tilexy "$LAT_S" "$LON_E" "$z")
  for x in $(seq "$XW" "$XE"); do
    for y in $(seq "$YN" "$YS"); do
      dest="$OUT/tiles/$z/$x/$y.png"
      [[ -f "$dest" ]] && continue
      mkdir -p "$(dirname "$dest")"
      curl -L --fail --silent -o "$dest" \
        "https://a.basemaps.cartocdn.com/rastertiles/voyager_nolabels/$z/$x/$y.png" || true
    done
  done
done

# ── 4. Copy the SPA and rewrite <head> URLs ────────────────────────────────
cp "$SRC" "$OUT/index.html"
echo "[*] Rewriting <head> URLs in $OUT/index.html …"
sed -i.bak \
  -e 's|https://unpkg.com/leaflet@1.9.4/dist/leaflet.css|vendor/leaflet-1.9.4/leaflet.css|g' \
  -e 's|https://unpkg.com/leaflet@1.9.4/dist/leaflet.js|vendor/leaflet-1.9.4/leaflet.js|g' \
  -e 's|https://unpkg.com/milsymbol/dist/milsymbol.js|vendor/milsymbol/milsymbol.js|g' \
  -e 's|https://unpkg.com/react@18.3.1/umd/react.development.js|vendor/react-18.3.1/react.development.js|g' \
  -e 's|https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js|vendor/react-dom-18.3.1/react-dom.development.js|g' \
  -e 's|https://unpkg.com/@babel/standalone@7.29.0/babel.min.js|vendor/babel-7.29.0/babel.min.js|g' \
  -e 's|https://fonts.googleapis.com/css2[^"]*|vendor/fonts/fonts.css|g' \
  -e 's|https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png|tiles/{z}/{x}/{y}.png|g' \
  -e 's|https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png|tiles/{z}/{x}/{y}.png|g' \
  -e 's|https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png|tiles/{z}/{x}/{y}.png|g' \
  "$OUT/index.html"
rm -f "$OUT/index.html.bak"

# Drop crossorigin/integrity attributes that don't apply offline
sed -i.bak \
  -e 's| crossorigin="anonymous"||g' \
  -e 's| crossorigin=""||g' \
  -e 's| integrity="[^"]*"||g' \
  "$OUT/index.html"
rm -f "$OUT/index.html.bak"

# ── 5. Verification artefact ───────────────────────────────────────────────
cat > "$OUT/README.md" <<EOF
# C23 DIANA NATO Warfighters — Air-gap bundle

Built from \`$(basename "$SRC")\` on $(date -u +%Y-%m-%dT%H:%M:%SZ).

## How to verify
1. Open \`index.html\` directly in a browser.
2. DevTools → Network → throttle to "Offline".
3. Reload. Zero requests should fail (other than tiles outside the pre-fetched AOR).

## Contents
- \`index.html\` — the SPA with rewritten <head> URLs.
- \`vendor/\` — pinned mirrored dependencies.
- \`tiles/\` — Carto Voyager basemap tiles for 53–60°N · 17–31°E, zoom 4..7.

## Re-run
\`\`\`bash
bash tools/build_airgap_bundle.sh [SOURCE_HTML] [OUT_DIR]
\`\`\`
EOF

echo ""
echo "[*] Done. Bundle at: $OUT/"
echo "    Open $OUT/index.html with the browser offline to verify."
