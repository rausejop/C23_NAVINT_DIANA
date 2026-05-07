# SESSION_STATE.md — Resumable execution log

**Purpose:** if the current Claude session runs out of tokens, crashes, or is closed,
this file lets the next session pick up exactly where it stopped. Update after every
material operation (file written, version bumped, batch closed).

**Current task (root user request):** "ejecuta todos los cubos pero ve guardando el
estado de la sesión donde te has quedado" — i.e. work through the four cubos A/B/C/D
listed in the previous turn's reply, producing a new `_vNNN.html` per cubo, and
keep this file current.

**Started:** 2026-05-03

---

## Plan — versions and cubos

| Bump | Cubo | Items | Status |
|------|------|-------|:------:|
| **v005** | **A** — 6 prioritarios del roadmap §11.7 | WF-01+02 (ROE-gated CoA + C-UAS workflow) · LD-03 (Weather feed) · WF-03 (OPORD generator) · AN-04 (Auto-suggest ACH scores) · CO-01 (Tactical→op→strategic roll-up) · DP-01 (Air-gap bundle script) | ✅ DONE |
| **v006** | **C** — 8 mejoras UX/QoL | localStorage persistence · hotkeys · OOB search-and-highlight · undo/redo · multi-mission selector · print/PDF view · i18n stub · MEDEVAC/IED/EOD event-source enums | ✅ DONE |
| **v007** | **D** — 5 mejoras visuales/branding | NATO logo on transparent halo · light-theme alt · slide-down rail animation · real tooltips · persistent active-faction indicator | ✅ DONE |
| **v008** | **B easy** — 4 ítems manejables del roadmap §11 | AN-02 (anomaly det. generalizada) · LD-02 (adversary-behaviour replay) · WF-05 (AAR formaliser) · CO-02 (multi-HQ views) | ✅ DONE |
| **v009** | **B hard** — 4 ítems pesados | AN-01 (correlation engine) · AN-03 (2º/3er order cascades) · LD-01 (live-feed adapter ISR) · WF-04 (Ops Assessment MoP/MoE) | ✅ DONE |

The 5 ★ FM-01..FM-05 items (foundation-model swap) stay out of scope per checklist disclaimers.

---

## Procedure for every bump (from `skills/versioning-workflow/SKILL.md`)

1. Find current latest version number (`ls C23_DIANA_NATO_WARFIGHTERS_v*.html | sort -n | tail -1`).
2. Apply additive edits to the unsuffixed `C23_DIANA_NATO_WARFIGHTERS.html`.
3. After every group of edits, append a one-line note under the current bump's section in this file.
4. When the bump is complete, `cp` to `_v(NNN+1).html` and add the changelog comment at top.
5. Verify: `grep -c 'type="text/babel"'` = 1 · `grep -c 'ReactDOM.createRoot'` = 1 · prior `_vNNN.html` md5 unchanged.
6. Update this file: flip ⏳ → ✅, record any deferred items, update "Where I am" section.

---

## Where I am right now (2026-05-03, end of session)

**Last action:** Submission package COMPLETE end-to-end. v011 sealed; NewDraft.md
char-budgeted across all 9 sections; 5 PNG screenshots produced; 4-min narrated
MP4 video produced (with TTS voice + visible cursor + burned subtitles); 2 new
skills authored (`playwright-spa-screenshots`, `narrated-demo-video`).
Unsuffixed `C23_DIANA_NATO_WARFIGHTERS.html` re-synced to match `_v011.html`
exactly (md5 `e317294837f1455d086267509e7b34ce`).

**Next action:** Submit to DIANA portal. Nothing pending in this repo other than
the 5 ★ FM-01..FM-05 backlog (foundation-model swap, deliberately deferred).

**Live SPA chain after v011 (current):**
```
C23_DIANA_NATO_WARFIGHTERS.html        (= v011, 279816 B, md5 e317294...)
C23_DIANA_NATO_WARFIGHTERS_v001.html  (135 KB)
C23_DIANA_NATO_WARFIGHTERS_v002.html  (173)
C23_DIANA_NATO_WARFIGHTERS_v003.html  (178)
C23_DIANA_NATO_WARFIGHTERS_v004.html  (186)
C23_DIANA_NATO_WARFIGHTERS_v005.html  (210)
C23_DIANA_NATO_WARFIGHTERS_v006.html  (222)
C23_DIANA_NATO_WARFIGHTERS_v007.html  (226)
C23_DIANA_NATO_WARFIGHTERS_v008.html  (235)
C23_DIANA_NATO_WARFIGHTERS_v009.html  (246)
C23_DIANA_NATO_WARFIGHTERS_v010.html  (269)
C23_DIANA_NATO_WARFIGHTERS_v011.html  (280) ← latest sealed
tools/build_airgap_bundle.sh
tools/capture_diana_screenshots.py
tools/capture_diana_video.py
tools/generate_narration.py
```

---

## v005 — Cubo A — execution log

(updated as I work)

- [x] **LD-03 — Weather feed.** `mission.weather { overall, forecast[] }`; WX tile on top bar; WEATHER tab with full CRUD; default mission seeds 4 regions.
- [x] **WF-01 + WF-02 — ROE-gated CoA + C-UAS workflow.** `roePending` state, `RoEModal` showing JPTL TST + RTL + NSL with ✓/✕; auto C-UAS log on intel RADAR + UAS regex.
- [x] **WF-03 — OPORD / FRAGO generator.** ORDERS tab; STANAG-2014 Markdown export from mission + coaHistory.
- [x] **AN-04 — Auto-suggest ACH scores.** ⚛ AUTO-SCORE button; keyword overlap → CC/C/N/I/II; preserves analyst scores.
- [x] **CO-01 — Tactical→operational→strategic roll-up.** ROLL-UP tab with `ECHELON_TIER` mapping and per-tier counts + lists.
- [x] **DP-01 — Air-gap bundle.** `tools/build_airgap_bundle.sh` mirrors CDN deps + Carto tiles + fonts; rewrites SPA `<head>`.

Progress notes:
- All six items shipped in a single bump. Mission Editor catalogue grew from 13 → 16 tabs.
- Top bar got the WX tile (now 7 status tiles total: DTG/THREAT/PHASE/MODE/FPCON/CBRN/PNT/CIS PACE/JTC PHASE/WX/OP TYPE).
- v005 sealed. md5 of v001-v004 confirmed unchanged.

---

## v006 — Cubo C — execution log

- [x] localStorage persistence (`c23.mission`, `c23.units`).
- [x] Hotkeys (I/?/C/T/A/R/Esc/1-9/+/-/Ctrl-Z/Ctrl-Shift-Z/Ctrl-Y).
- [x] OOB search-and-fly (clic en designation → fly + dossier + pulso dorado).
- [x] Undo/Redo stack (in-memory, cap 30, bound a Ctrl-Z / Shift+Z / Y).
- [x] Multi-mission slots (5 slots persistidos en `c23.slots`).
- [x] Print one-pager (`@media print` + botón en WORKSPACE).
- [x] i18n stub EN/ES/FR (persistido en `c23.lang`).
- [x] MEDEVAC/IED/EOD enums via `<datalist id="c23-event-sources">`.

Notes:
- All 8 items shipped in a single bump. Mission Editor: 16 → 17 tabs.

---

## v007 — Cubo D — execution log

- [x] NATO logo halo (no card; double drop-shadow).
- [x] Theme switcher dark / light / high-contrast con `data-theme` en `<html>`.
- [x] Slide-down animation 180 ms al expandir secciones del rail.
- [x] Tooltips ricos via `[data-tip]:hover:after` (FPCON/CBRN/PNT/CIS-PACE wired).
- [x] Indicador persistente de facción (3-px coloured strip atop rail, `data-faction` en `<html>`).

---

## v008 — Cubo B easy — execution log

- [x] AN-02 — `detectAnomalies()` rule set: AIS dark + loitering, OOB disrupted/R4, JPTL CDE≥4 TST, posture interactions.
- [x] LD-02 — Adversary-behaviour replay (load JSON of intel events, append).
- [x] WF-05 — AAR Markdown formaliser exportable.
- [x] CO-02 — Multi-HQ scoping (SHAPE / JFC-BAL / TCC-N / TCC-S) bbox per-HQ.
- [x] All four landing on a single new INTEL OPS tab.

---

## v009 — Cubo B hard — execution log

- [x] AN-01 — `correlateEvents()` por (source × top-keyword), clusters ≥ 2, severidad agregada.
- [x] AN-03 — `cascadeEffects()` heurístico por CoA (SEA/LOG/HNS/INFRA/STRATCOM/LAND/NEUTRAL/CIS/C2).
- [x] LD-01 — Adapter live-feed con polling configurable, persisted en `c23.live`, log en canal [LIVE].
- [x] WF-04 — Ops Assessment MoP/MoE per-CoA en tabla.
- [x] Todo en nuevo tab ANALYTICS (complementa INTEL OPS).

---

## v010 — DIANA-evaluator-priority batch (post-decision)

**Decision basis:** user chose to prioritise what a DIANA evaluator values most, keep single-HTML, exclude FM-01 (LLM call). Items ordered by evaluator impact, not by alphabetical roadmap order.

- [x] Cascade rules as doctrinal table (Camino B). `mission.cascadeRules[]` seeded with 10 rules (each cites its AJP). `cascadeEffects()` iterates the table; legacy fallback preserved. CRUD editor in ANALYTICS tab.
- [x] Branches & Sequels per phase (AJP-5). 4 phases seeded with branches + sequels. PHASES tab has per-phase editor.
- [x] JPRC tab (AJP-3.7). 5-task sequence Reported→Located→Supported→Recovered→Reintegrated. Default mission ships 2 IPs (REAPER-04, BLUE-LINE-12). Per-stage tally tiles + advance button.
- [x] MoP/MoE per LOO/LOE (AJP-3 extension). `coa.loo[]` / `coa.loe[]` seeded on c1/c2/c3. Ops Assessment table now buckets per LOO with subtotals.
- [x] CTF/CTG/CTU + JLSG echelons (AJP-3.1 / 4.6) via `<datalist id="c23-echelons">`.
- [x] CIMIC Liaison + MSU unit types via `<datalist id="c23-unit-types">`.
- [x] C-IED pillar tag on CoAs (`coa.ciedPillar` enum: Defeat-Device / Attack-Network / Prepare-Force).
- [x] Air-gap bundle script validated in sandbox: all 6 CDN URLs HTTP 200 with expected sizes (leaflet.css 14.8KB, leaflet.js 147KB, milsymbol 862KB, react 110KB, react-dom 1.08MB, babel 3.14MB). `bash -n` passes. Tile XY computation verified.

v010 sealed.

---

## v011 — DIANA-evaluator priority batch (post-v010)

**Decision:** user repeated "prioritise DIANA evaluator value, single HTML, no LLM, do everything else". Items selected by visibility in the spec ("wargaming" appears literal) and by completing the doctrinal data→map integration story.

- [x] Wargaming subtab — pairwise NATO×OPFOR matrix with colour-coded net score and best/worst summary per NATO CoA. `simulatedOutcome()` deterministic.
- [x] COP overlay — PR isolated personnel (stage-coloured ring + cross + tooltip). Toggle in LAYERS rail.
- [x] COP overlay — Naval Interdiction Zone polygon. Toggle inherits from Movement layer.
- [x] navalInterdict CRUD on MOVEMENT tab with reseed-from-default button.
- [x] ATO cycle phase property on AIR CoAs (column on ACH MATRIX).
- [x] Air-gap bundle generated under dist/airgap/ (5.5 MB without tiles) + dist/airgap/cdax.json CycloneDX 1.7 attestation skeleton.

v011 sealed.

---

## ✅ EJECUCIÓN COMPLETA (v005-v009)

Todos los cubos (A · B · C · D) ejecutados. La cadena de versiones queda:

```
v001 (135 KB) v002 (173) v003 (178) v004 (186) v005 (210) v006 (222) v007 (226) v008 (235) v009 (244)
```

**Mission Editor:** 13 → 19 tabs.
**Skills shipped:** se podrían crear para v005-v009 si el usuario lo pide.
**Roadmap status:** sólo quedan los 5 ★ FM-01..FM-05 (foundation-model swap, fuera de TRL 6+).

---

## Submission-package work (post-v011, 2026-05-03)

After v011 sealed, the user requested the full DIANA submission package. Each
subsection captures what was produced and where; the next session can verify
deliverables exist and re-run any tool from these notes alone.

### NewDraft.md (DIANA "New Draft Proposal" form)

- **File:** `NewDraft.md` (31 764 B at repo root).
- **Form text source:** `Specifications/20260503 New Draft Proposal.txt`.
- **Char limits enforced:** SF1-4 = 1500 each · LF1 Abstract = 750 · LF2 Technical Merit = 12 000 · LF3-5 = 3500 each.
- **Section 5 (Company and Commercial)** populated from `Pitch Deck_NAVINT v20260501v2.pdf` (financial plan 2027/2028/2029, team, advisory board, certifications, TAM/SAM/SOM, pricing tiers, GTM).
- **Final state:** all 9 sections within budget (margin 8 – 1506 chars).
- **Verification helper:** Perl one-liner inside `skills/diana-proposal-draft/SKILL.md` § "Char-budget verification helper".
- **Skill applied:** `diana-proposal-draft` + `char-budget-respect` (5-pass trim protocol).

### Screenshots (DIANA short-form + long-form images)

- **Files (5):** `dist/screenshots/`
  - `short_1_global_cop.png` (1.99 MB) — global multi-domain COP with all overlays
  - `short_2_wargaming.png` (181 KB) — pairwise NATO×OPFOR matrix
  - `long_1_joint_targeting.png` (227 KB) — JTC + JPTL
  - `long_2_analytics_cascades.png` (304 KB) — cascade rules editor
  - `long_3_jprc.png` (158 KB) — Personnel Recovery / JPRC
- **Tool:** `tools/capture_diana_screenshots.py` (Playwright headless, `device_scale_factor: 2`).
- **Key learning:** for modal captures use `page.locator('.modal').screenshot()` not `page.screenshot()` so the dim backdrop does not bleed into the frame. Codified in skill `playwright-spa-screenshots`.

### Video (DIANA "Upload a Video")

- **File:** `dist/video/diana_demo.mp4` (10.83 MB / 4:00.00 / 1920×1080 H.264 + AAC stereo 48 kHz).
- **DIANA limits:** ≤ 4 min OK · ≤ 100 MB OK · MP4 OK · English voice + English subtitles OK · screen capture + audio commentary OK.
- **Pipeline (two-step, re-runnable):**
  1. `python tools/generate_narration.py` — synthesises 10 per-scene MP3s via `edge-tts` (`en-GB-RyanNeural`, `+8%` rate); per-scene padding/atempo to fit each storyboard window; concatenates to `dist/video/narration/narration.wav` (238.5 s + 1.5 s tail silence).
  2. `python tools/capture_diana_video.py` — drives Playwright through 10 scenes with a yellow-on-NATO-blue **visible cursor overlay** (`#__c23_cursor` + click pulse-ring `#__c23_ring`) injected after each `goto()`; mouse motion before every click via `move_cursor(steps=22, ease-in-out)`; ffmpeg muxes `webm + narration.wav`, burns subtitles with `force_style='PrimaryColour=&H00FFFFFF,...,BorderStyle=3,BackColour=&HB0000000,MarginV=60,Bold=1'`, caps to `-t 240`.
- **Inputs (kept editable):** `dist/video/storyboard.md` (10 scenes, 595 words at 150 wpm) · `dist/video/subtitles.srt` (28 cues).
- **Backups:** `dist/video/raw/<random>.webm` (silent Playwright capture).
- **Recurring trap encountered + fixed:** ASS `PrimaryColour=&HFFFFFFFF` = alpha-FF in libass = TRANSPARENT text → invisible subtitles. Fix is `&H00FFFFFF`. Documented as anti-pattern in skill `narrated-demo-video`.

### Skills authored or updated

- **NEW** `skills/playwright-spa-screenshots/SKILL.md` — packages the screenshot pattern.
- **NEW** `skills/narrated-demo-video/SKILL.md` — packages the TTS + cursor + burn-in pattern; includes voice table, DIANA compliance checklist, and the exact ffmpeg command.
- **UPDATED** `skills/README.md` — index rows 17c, 17d added under "Submissions & proposals" (catalogue grew 33 → 35 skills).
- **UPDATED** `skills/diana-proposal-draft/SKILL.md` — References section now cross-links the two new sibling skills.

### Tools added this session

- `tools/capture_diana_screenshots.py` — earlier session.
- `tools/generate_narration.py` — TTS step (Edge `en-GB-RyanNeural`).
- `tools/capture_diana_video.py` — Playwright recorder + cursor overlay + ffmpeg mux + subtitle burn-in.

### Inventory check command (run at start of next session to verify state)

```bash
md5sum C23_DIANA_NATO_WARFIGHTERS_v011.html C23_DIANA_NATO_WARFIGHTERS.html  # must match
ls -la dist/screenshots/ dist/video/diana_demo.mp4 NewDraft.md
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=0 dist/video/diana_demo.mp4
ls skills/ | wc -l   # expect 36 (35 skills + README)
```

---

## How to resume from this file (for the next Claude / session)

1. `cat SESSION_STATE.md` — read this file end-to-end.
2. Find the row marked ⏳ with the lowest version number — that's the next bump.
3. Look at "Where I am right now" for the exact mid-bump checkpoint.
4. If the unsuffixed `C23_DIANA_NATO_WARFIGHTERS.html` differs from the latest
   `_vNNN.html`, the previous session was mid-bump. Inspect with
   `diff <(sed '1,/<!--$/d;/^-->/,$d' C23_DIANA_NATO_WARFIGHTERS_vNNN.html) C23_DIANA_NATO_WARFIGHTERS.html`
   (strips the changelog header from the versioned file).
5. Continue from the next [ ] checkbox in the active bump's execution log.
6. After every Edit/Write, update the relevant checkbox + "Last action" line and
   re-save this file.
7. When a bump completes (all checkboxes ✅, file snapshotted, verified),
   bump the table at the top, clear "Where I am", move on to the next ⏳ row.
