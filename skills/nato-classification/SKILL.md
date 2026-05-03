---
name: nato-classification
description: Apply the standard NATO classification banner, NATO Reflex Blue / NATO Gold chrome, STANAG 4774/4778 metadata, and TEMPEST badging to a UI.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    classification: e.g. "UNCLASSIFIED // FOR OFFICIAL USE ONLY — TRAINING / WARGAME"
    showStanag: bool
    tempestLevel: "SDIP-27 Level B" | …
  outputSchema:
    bannerHtml: classification banner block (top of viewport)
    cssVars: NATO Blue / Gold CSS variables
    badgesHtml: standards badges block (Settings tab footer)
  errorHandling:
    invalidClassification: "render UNCLASSIFIED with a warn log line"
  stateless: true
tools: [Edit]
---

# nato-classification

## Purpose
Provide a consistent, non-spoofable look-and-feel that signals NATO operational provenance: classification banner top + bottom of viewport, NATO Reflex Blue (`#004990`) and NATO Gold (`#FFC72C`) chrome, STANAG metadata, and TEMPEST badge.

## When to use
- Any UI delivered to a NATO end-user, even at TRAINING / WARGAME classification.
- DIANA submissions that must visually pass for a tactical workstation.
- Any platform with the constraints "NATO Secured Environment Standards", "STANAG", "TEMPEST".

## Inputs
- A classification string. Must include the level (e.g. `UNCLASSIFIED`) and any caveats.
- The current platform identity (mission name, TRL, faction).

## Outputs
- A `.classif` banner block at the top of the viewport showing classification on the left, mission name centre, standards (`STANAG 4774/4778 · TEMPEST SDIP-27 · AIR-GAPPED`) on the right.
- CSS variables for NATO Blue (`--nato-blue: #004990`), NATO Gold (`--nato-gold: #FFC72C`), allied (`--allied: #3895FF`), hostile (`--hostile: #E63946`), neutral (`--neutral: #74D85F`), unknown (`--unknown: #FFD24A`).
- A standards badges block (rendered in the Settings tab) listing every applicable standard.

## Instructions

1. **Pin the classification banner at the top of the viewport,** above any other chrome, in NATO Green (`#0b8a4a`):
   ```jsx
   <div className="classif">
     <span>{classification}</span>
     <span className="classif-mid">{mission} · TRL-{trl}</span>
     <span>STANAG 4774/4778 · TEMPEST SDIP-27 · AIR-GAPPED</span>
   </div>
   ```
2. **Use the official NATO palette in the top bar:** gradient from `#004990` to `#0b3e7c` to `#061a36`, with a 3-px repeating blue/gold stripe at top.
3. **Echo the classification at the bottom of the viewport** when feasible (most NATO platforms repeat it top + bottom; for SPAs the bottom Command Log substitutes).
4. **Use `--allied` for friendly markers and `--hostile` for hostile**. Default to APP-6 spirit colours (cyan-blue + red).
5. **Surface a standards badge cluster** in the SETTINGS tab listing what the platform conforms to. Minimum: `STANAG 4774`, `STANAG 4778`, `TEMPEST SDIP-27`, `MIL-STD-2525B`, `APP-6`, `AJP-3`, `AJP-3.9`, `AJP-4.4`, `CycloneDX 1.7`, `Air-Gapped`.
6. **Never use red as primary chrome.** Red is reserved for hostile units and alert tones. NATO chrome is blue + gold.
7. **Tone the alert colours separately:** `tone-warn` = amber, `tone-alert` = red, `tone-success` = mint. Apply to log lines, not to chrome.

## Examples

### Banner styles
```css
.classif{display:flex;justify-content:space-between;align-items:center;
  background:#0b8a4a;color:#fff;font-weight:700;font-size:11px;
  letter-spacing:0.2em;padding:0 14px;text-transform:uppercase;
  font-family:"JetBrains Mono",monospace;border-bottom:1px solid #0a6b3a;}
.topbar{background:linear-gradient(90deg,#004990 0%,#0b3e7c 50%,#061a36 100%);
  border-bottom:2px solid #1b7be0;}
.topbar:before{content:"";position:absolute;left:0;right:0;top:0;height:3px;
  background:repeating-linear-gradient(90deg,#004990 0 64px,#FFC72C 64px 80px);opacity:0.65;}
```

### Classification strings (legitimate NATO)
- `UNCLASSIFIED // FOR OFFICIAL USE ONLY — TRAINING / WARGAME SCENARIO`
- `NATO UNCLASSIFIED — RELEASABLE TO PFP`
- `NATO RESTRICTED`
- `NATO CONFIDENTIAL` (do **not** use this in any demo unless authorised)

## Anti-patterns
- ❌ Showing only "DEMO" in the banner. Always include a classification level word.
- ❌ Using red as the banner colour to signal alarm — that is the wrong language. Banner colour = classification, not threat.
- ❌ Black-on-yellow military aesthetics borrowed from civilian dashboards. Use NATO Blue / Gold.
- ❌ Faking caveats (`SECRET // NOFORN`) on a public demo. Stick to UNCLASSIFIED variants for unclassified work.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v002.html` — banner, CSS vars, badges in Settings tab.
- STANAG 4774 (Confidentiality Metadata Label Syntax), STANAG 4778 (Metadata Binding).
- TEMPEST SDIP-27 (NATO).
- Companion skill `posture-indicators` — the FPCON / CBRN / PNT / CIS-PACE top-bar tiles complement the banner with operational-state colour coding (different concept from classification, never collapse them visually).
