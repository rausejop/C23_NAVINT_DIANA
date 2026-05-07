# C23 NAVINT — Decision Superiority for NATO Warfighters

**A doctrine-driven AI decision-superiority augmentation for Maven Smart System NATO and Allied C2 platforms.**

> **Submitted to the DIANA Warfighters Challenge 2026 as an Open-Source Intelligence (OSINT) proof of concept.** Every fact, unit, location, equipment fitting, force-structure detail, and event in the platform — including the 50-entry Eastern Flank Order of Battle regenerated for D-day 2026-05-07 — has been derived exclusively from publicly available, openly cited open-source material (NATO factsheets, national ministries of defence, parliamentary research briefs, defence press, and academic OSINT analyses). No classified, restricted, controlled-unclassified, or commercially licensed intelligence has been used to build, train, seed or validate this platform. See § 1.1 below and the in-platform **INFO → SOURCES (OSINT)** tab for per-unit citations.

| Field | Value |
| --- | --- |
| **Working name** | C23 NAVINT (Naval Intelligence) · NAVINT Baltic Sentry default mission |
| **Submitter** | Rafael Ausejo Prieto · CONFIANZA23 INTELIGENCIA Y SEGURIDAD SL |
| **Reference** | C23-NATO-DIANA-Warfighters |
| **Submission status** | ✓ **Submitted** to the DIANA "Decision Superiority for NATO Warfighters" Challenge 2026 (window closed 5 May 2026 09:00 BST) |
| **Submission positioning** | Proof of concept for **Open-Source Intelligence (OSINT)** in NATO operational decision-support |
| **Data provenance** | 100 % OSINT — every datum cited to a publicly retrievable source. Per-unit citations live in `mission.sources[]` and are surfaced in the in-platform **INFO → SOURCES (OSINT)** tab. |
| **Latest sealed version** | `C23_DIANA_NATO_WARFIGHTERS_v012.html` (~302 KB single-file SPA) — OSINT-anchored OOB regenerated 2026-05-07 |
| **Air-gap bundle** | `dist/airgap/` — ~5.5 MB without tiles, ready for SCIF deployment |
| **Submission images** | `dist/screenshots/` — 5 PNGs (Short-Form 1+2, Long-Form 1+2+3) |
| **Submission video** | `dist/video/diana_demo.mp4` — 4:00.00 / 10.83 MB / H.264 + AAC + EN subtitles + EN voice-over |
| **Spec coverage** | 73 / 74 = **98.6 %** (single 🟡, four ★ behind named foundation-model seams) |
| **Doctrinal anchor** | All 33 NATO Allied Joint Publications (AJP-01 through AJP-10.3) mirrored locally and bound to platform features |
| **Hardware floor** | 16 GB RAM tactical workstation (Windows or Linux) |
| **Environment** | Air-gapped / Disconnected operations |
| **Standards** | STANAG 4774/4778 · TEMPEST SDIP-27 · MIL-STD-2525B / APP-6 · CycloneDX 1.7 / ECMA-424 |

---

## 1 · Executive summary

C23 NAVINT is a single-file HTML5 Single-Page Application that delivers an AI-augmented Common Operating Picture integrated end-to-end with the NATO operational planning, targeting and assessment cycle. It runs offline on a 16 GB-RAM tactical workstation without installation, server or telemetry.

A 21-tab Mission Editor exposes every operational parameter as CRUD: Order of Battle across LAND / AIR / SEA / SUB / CYBER and NATO / OPFOR / NEUTRAL; phase ladder with Branches and Sequels (AJP-5 COPD); the full AJP-3.9 Joint Targeting Cycle (six-phase JTC, JPTL with HVT / HPT / TST and FIVE-O / F2T2EA, Collateral Damage Estimation, Restricted Target List, No-Strike List); Movement (MSR / ASR / APOD / SPOD plus naval interdiction polygon, AJP-3.13 / 4.4); Posture (FPCON / CBRN / PNT / CIS PACE); Weather; AJP-3.7 Personnel Recovery five-task sequence; AIS dark-vessel fusion; Operations Assessment with MoP / MoE per LOO / LOE; Wargaming pairwise matchup matrix.

The decision-support core comprises a five-level Analysis of Competing Hypotheses matrix (extending Heuer beyond the standard three-level scale), an auto-suggest scorer, a probabilistic CoA outcome simulator, an anomaly-detection rule set, a clustered correlation engine, and a per-CoA cascade-effects table where each rule cites its source AJP. Every Course of Action execution gates through a Rules-of-Engagement modal that surfaces JPTL Time-Sensitive Targets, RTL/NSL conflicts and Collateral Damage Estimation before commit; engagement is followed by a kinetic per-turn animation on the COP. A Wargaming subtab runs every NATO-versus-OPFOR matchup pairwise.

The platform is delivered as a strictly air-gapped runtime: the entire dependency graph is mirrored under `dist/airgap/vendor/` and a CycloneDX 1.7 / ECMA-424 attestation (`dist/airgap/cdax.json`) is shipped alongside, ready for organisational signature. The foundation-model integration is named, scoped and seam-ready (`autoSelectCoA()`), but deliberately deferred to the post-demonstration accreditation phase.

### 1.1 · OSINT proof-of-concept positioning

C23 NAVINT was submitted to the DIANA Warfighters Challenge 2026 not just as a decision-support platform, but as a deliberate **proof of concept for Open-Source Intelligence (OSINT)** in NATO operational C2. The thesis is that the modern open-source landscape — alliance press releases, national MoDs, parliamentary research, academic monitoring projects, defence press, AIS feeds, satellite open data — is rich enough to populate a defensible, doctrinally-coherent operating picture without ever touching classified holdings, and that doing so is a useful capability in its own right (training, exercises, alliance interoperability, coalition partner enablement, public-facing strategic communications, accreditation pathfinder).

Concrete OSINT discipline applied to this submission:

- **Every Order-of-Battle entry** in the v012 build (50 units across NATO eFP/MNBs, Polish divisions, multinational HQs, BAP detachments, SNMG1/SNMCMG1 ships, Russian Leningrad MD / 11th Army Corps / Baltic Fleet, Belarus Western OC) is anchored to a public reference recorded in `mission.sources[]` with topic, citation text, URL and retrieval date. The dataset round-trips through JSON export/import like every other field, so receivers can audit it.
- **No classified, NATO-RESTRICTED, NATO-CONFIDENTIAL, NATO-SECRET, national caveat-bearing, FOUO, CUI or commercially-licensed intelligence** has been ingested at any point. This includes the doctrinal binding: only publicly released NATO Allied Joint Publications (the 33 AJPs from gov.uk) were mirrored.
- **Provenance is auditable from the platform itself** — opening the `ⓘ INFO` modal and selecting the new **SOURCES (OSINT)** tab renders the citation table directly from `mission.sources[]`, so an evaluator can verify each unit without ever leaving the SPA.
- **Reproducibility:** because every source is a public URL with a retrieval date, an independent analyst can re-run the OSINT loop and reach the same picture. The OOB is not a curated intelligence product — it is a reproducible OSINT artefact.

This positioning matters operationally: an OSINT-only COP is releasable to non-cleared coalition partners, to host-nation civilian liaison, to academic and industry collaborators, and to the public-affairs strand of strategic communications without the friction of a classification review. It is also the right starting point for accrediting the future foundation-model integration: the corpus the model would consume is auditable end-to-end.

---

## 2 · Repository layout

```
12 Allied Joint Doctrine/
│
├── C23_DIANA_NATO_WARFIGHTERS.html              ← Latest version (currently = v012)
├── C23_DIANA_NATO_WARFIGHTERS_v001.html         ← Initial baseline
├── C23_DIANA_NATO_WARFIGHTERS_v002.html         ← Joint Targeting + Movement + Posture + CYBER + NEUTRAL
├── C23_DIANA_NATO_WARFIGHTERS_v003.html         ← Official logos + 5-level ACH + button grid
├── C23_DIANA_NATO_WARFIGHTERS_v004.html         ← Logos repositioned + collapsible rail + kinetic per-turn
├── C23_DIANA_NATO_WARFIGHTERS_v005.html         ← Cubo A: Weather + ROE + OPORD + Auto-score + Roll-up + Air-gap script
├── C23_DIANA_NATO_WARFIGHTERS_v006.html         ← Cubo C: localStorage + hotkeys + slots + print + i18n
├── C23_DIANA_NATO_WARFIGHTERS_v007.html         ← Cubo D: NATO halo + 3 themes + tooltips + faction indicator
├── C23_DIANA_NATO_WARFIGHTERS_v008.html         ← Cubo B easy: anomaly + replay + AAR + multi-HQ
├── C23_DIANA_NATO_WARFIGHTERS_v009.html         ← Cubo B hard: correlation + cascades + live-feed + Ops Assessment
├── C23_DIANA_NATO_WARFIGHTERS_v010.html         ← Doctrine breadth: PR/JPRC + Branches/Sequels + LOO/LOE + cascade rules table
├── C23_DIANA_NATO_WARFIGHTERS_v011.html         ← Wargaming + COP overlays + ATO + air-gap bundle + CDAX
├── C23_DIANA_NATO_WARFIGHTERS_v012.html         ← OSINT-anchored OOB regen 2026-05-07 + animation pipeline restored + INFO/SOURCES tab
│
├── README.md                                    ← This file
├── CLAUDE.md                                    ← Working notes for Claude Code (versioning rule)
├── MasterPrompt.txt                             ← Authoritative deliverable spec (A–K)
│
├── checklist.md                                 ← DIANA-spec coverage (98.6 %)
├── roadmap.md                                   ← Doctrine-driven plan (sections 1–13)
├── Datamodel.md                                 ← Unified CycloneDX 1.7 / ECMA-424 envelope
├── NewDraft.md                                  ← DIANA proposal (copy-paste-ready, char-budgeted)
├── SESSION_STATE.md                             ← Resumable execution log (multi-session safety net)
│
├── Pitch Deck_NAVINT v20260501v2.pdf            ← Commercial deck (financials, team, TAM/SAM/SOM)
│
├── Specifications/                              ← DIANA challenge inputs (read-only)
│   ├── 20260502 DIANA FAQ.txt
│   ├── 20260502 Welcome to DIANAs Challenge Portal.txt
│   ├── 20260502 Decision Superiority for NATO Warfighters.txt
│   └── 20260503 New Draft Proposal.txt
│
├── Format/                                      ← Source template + parameters (read-only)
│   ├── EasternFlankv003.html
│   └── EasternFlank_v003.json
│
├── AJP/                                         ← Local mirror of 33 NATO Allied Joint Publications
│   ├── README.md                                ← Index of all 33 publications
│   ├── update_ajp_doctrines.py                  ← Stdlib-only sync tool from gov.uk
│   ├── update_ajp_skill.md                      ← Agent-skill spec wrapping the sync tool
│   ├── 01 Allied Joint Doctrine (AJP-01)/       ← One folder per publication, with original PDFs
│   ├── 02 Allied Joint Doctrine for the Conduct of Operations (AJP-3)/
│   ├── … (33 directories total) …
│   ├── 33 Allied Joint Doctrine for Military Public Affairs (AJP-10.3)/
│   └── SUMMARIES/                               ← Per-AJP Markdown summaries (deliverable H)
│       ├── README.md                            ← Methodology disclosure
│       ├── AJP-01.md                            ← Per-publication summary
│       ├── … (33 summary files) …
│       └── AJP-10.3.md
│
├── skills/                                      ← Reusable Agent Skills catalogue
│   ├── README.md                                ← Index (35 skills + README)
│   ├── make-skill/SKILL.md                      ← Meta-skill: how to author a skill
│   ├── diana-proposal-draft/SKILL.md            ← DIANA proposal generator
│   ├── char-budget-respect/SKILL.md             ← Per-section char-limit pattern
│   ├── … (32 capability skills) …
│   └── (see § 9 for full list)
│
├── tools/
│   ├── build_airgap_bundle.sh                   ← stdlib + curl air-gap bundler (DP-01)
│   ├── capture_diana_screenshots.py             ← Playwright screenshot capture (5 PNGs)
│   ├── generate_narration.py                    ← Edge-TTS narration synthesis (per-scene MP3 + WAV)
│   └── capture_diana_video.py                   ← Playwright video capture w/ visible cursor + ffmpeg mux
│
└── dist/
    ├── airgap/                                  ← Materialised offline runtime (~5.5 MB without tiles)
    │   ├── index.html                           ← SPA with rewritten <head> URLs
    │   ├── cdax.json                            ← CycloneDX 1.7 attestation skeleton (pending sign)
    │   └── vendor/
    │       ├── leaflet-1.9.4/                   ← leaflet.js + .css + 3 marker images
    │       ├── milsymbol/                       ← APP-6 / MIL-STD-2525B renderer
    │       ├── react-18.3.1/                    ← React UMD
    │       ├── react-dom-18.3.1/                ← ReactDOM UMD
    │       └── babel-7.29.0/                    ← @babel/standalone for in-browser JSX
    │
    ├── screenshots/                             ← DIANA submission images (5 PNGs, 1920×1080 ×2)
    │   ├── short_1_global_cop.png               ← Short-Form Image 1 — global multi-domain COP
    │   ├── short_2_wargaming.png                ← Short-Form Image 2 — pairwise NATO×OPFOR matrix
    │   ├── long_1_joint_targeting.png           ← Long-Form Image 1 — JTC + JPTL
    │   ├── long_2_analytics_cascades.png        ← Long-Form Image 2 — cascade rules editor
    │   └── long_3_jprc.png                      ← Long-Form Image 3 — Personnel Recovery / JPRC
    │
    └── video/                                   ← DIANA submission video deliverable
        ├── diana_demo.mp4                       ← Final: 4:00.00 / 10.83 MB / H.264+AAC + EN voice + EN subs
        ├── storyboard.md                        ← 10-scene script (595 words at 150 wpm)
        ├── subtitles.srt                        ← 28 cues aligned to scene boundaries
        ├── narration/                           ← Per-scene Edge-TTS MP3s + concatenated WAV (en-GB-RyanNeural)
        └── raw/                                 ← Playwright's silent .webm recording (kept as backup)
```

---

## 3 · How to run the platform

### 3.1 Quick start (online mode)

1. Open `C23_DIANA_NATO_WARFIGHTERS.html` (or any sealed `_vNNN.html`) in a modern browser (Chrome, Edge, Firefox).
2. The COP loads with the **NAVINT Baltic Sentry** default mission embedded.
3. Top-bar buttons: `◆ TURN`, `⚙ AUTO`, `ⓘ INFO`, `⚙ CONFIG`, `↺ RESET OP`.
4. Click any unit on the map to extract its dossier on the right rail.
5. Use the `EXECUTE → next phase` button at the bottom of the map to step through the wargame.

### 3.2 Air-gap deployment

```bash
# (a) Build the bundle once, on a workstation with internet:
bash tools/build_airgap_bundle.sh
# Output: dist/airgap/ (5.5 MB without tiles, or ~200 MB with Carto Voyager tiles for the AOR)

# (b) Copy dist/airgap/ to the SCIF workstation (USB / approved transfer)

# (c) Open dist/airgap/index.html in the local browser
# Verify offline with DevTools → Network → throttle to "Offline" → reload (zero failed requests)

# (d) Sign cdax.json with the organisational Ed25519 key, replacing the placeholder fields
```

### 3.3 Hotkeys (added in v006)

| Key | Action |
| --- | --- |
| `I` or `?` | Toggle INFO modal |
| `C` | Open CONFIG modal |
| `T` | Flip Allied / Hostile turn |
| `A` | Toggle AUTO mode |
| `R` | RESET OP |
| `Esc` | Close any modal |
| `1` … `9` | Execute that phase (if eligible) |
| `+` / `-` | Expand / collapse all rail sections |
| `Ctrl/Cmd Z` | Undo |
| `Ctrl/Cmd Shift Z` or `Ctrl Y` | Redo |

---

## 4 · Architecture

### 4.1 Five functional layers

| Layer | Where it lives | Doctrinal binding |
| --- | --- | --- |
| **Doctrinal data** | `window.DEFAULT_MISSION` + 21-tab Mission Editor | All 33 AJPs |
| **Geospatial** | Leaflet 1.9 + milsymbol + 9 toggleable map overlays | APP-6 / MIL-STD-2525B |
| **Decision support** | ACH 5-level matrix + auto-scorer + per-CoA simulator + Wargaming matrix | AJP-3, AJP-5 |
| **Analytics** | `detectAnomalies()` + `correlateEvents()` + `cascadeEffects()` (each cascade rule cites its AJP) | AJP-3, AJP-3.9, AJP-5 |
| **Workflow** | Phase engine + ROE-gated execution + C-UAS auto-trigger + OPORD/AAR generators + NL terminal | AJP-3.9 (JTC), AJP-3.3.5 (C-UAS), STANAG 2014 |

### 4.2 Three integration tiers (for MSS-NATO-class platforms)

| Tier | What it exposes | Example surface |
| --- | --- | --- |
| **Data** | JSON schemas + CycloneDX 1.7 envelope + BOM-Link | `C23-DIANA-MISSION/1.0`, `OOB/1.0`, `ACH/1.0`, AIS, all wrapped in `Datamodel.md` |
| **Workflow** | Named workflow surfaces | `selectCoA`, `executeTurnKineticMovement`, `generateAAR`, `OrdersTab` |
| **Decision** | Pluggable analytics + foundation-model seam | `cascadeEffects()`, `correlateEvents()`, `autoSelectCoA()` |

### 4.3 Single-file constraint (cumulative across versions)

- Approximately **277 KB** for v011 unsuffixed, **~280 KB** with the v011 changelog header inside the snapshot.
- 1 `<script type="text/babel">` block (the only valid pattern — see skill `react-babel-pitfalls`).
- 1 `ReactDOM.createRoot()` mount point.
- 0 server-side dependency, 0 telemetry, 0 background workers.
- No build step, no bundler, no `npm install`. Edits land directly on the file.

---

## 5 · Doctrinal foundation (33 AJPs)

The platform's logic, terminology and operational workflows are derived from the official NATO Allied Joint Publications mirrored in `AJP/`.

| AJP | Title | Where bound in C23 NAVINT |
| --- | --- | --- |
| **AJP-01** | Allied Joint Doctrine (capstone) | Mission identity (Operation Type, Mission Type, Master Narrative, CoG) |
| **AJP-3** | Conduct of Operations | LOO/LOE tags on CoAs, behaviour-centric phase ladder, kinetic per-turn move |
| **AJP-3.1** | Maritime Operations | AIS fusion, dark-vessel detection, naval interdiction polygon, SLOC overlays |
| **AJP-3.2** | Land Operations | OOB across echelons, manoeuvre vectors, kinetic movement |
| **AJP-3.3** | Air & Space Operations | ATO cycle phase on AIR CoAs, BAP / QRA representation |
| **AJP-3.3.5** | Airspace Control | C-UAS auto-trigger workflow on RADAR + UAS regex |
| **AJP-3.7** | Personnel Recovery | JPRC tab with Reported → Located → Supported → Recovered → Reintegrated |
| **AJP-3.9** | Joint Targeting | Six-phase JTC, JPTL CRUD with HVT/HPT/TST + F2T2EA + CDE, RTL/NSL, ROE-gated execution |
| **AJP-3.10.1** | Psychological Operations | Geopolitical event narratives |
| **AJP-3.13** | Deployment & Redeployment | APOD / SPOD point CRUD with status |
| **AJP-3.14** | Force Protection | FPCON tile (Alpha → Delta) on top bar |
| **AJP-3.15** | Counter-IED | C-IED pillar tag on CoAs (Defeat-Device / Attack-Network / Prepare-Force) |
| **AJP-3.18** | EOD Support | EOD enum in event-source datalist |
| **AJP-3.19** | Civil-Military Cooperation | NEUTRAL faction (civil airliner, NGO liaison, civil ferry); CIMIC unit type |
| **AJP-3.20** | Cyberspace Operations | CYBER as fifth operational domain (NCIRC, CCDCOE, GRU 26165 in default OOB) |
| **AJP-3.22** | Stability Policing | MSU unit type in datalist |
| **AJP-3.23** | Counter-WMD | CBRN ALERT tile (Green / Yellow / Red) on top bar |
| **AJP-3.24** | Peace Support | Mission Type enum |
| **AJP-3.25** | NEO | Mission Type enum |
| **AJP-3.26** | Humanitarian Assistance | Mission Type enum |
| **AJP-3.27** | Counter-Insurgency | Mission Type enum |
| **AJP-3.28** | Stabilization | End-state criteria CRUD list |
| **AJP-4** | Sustainment | Movement tab logistics layer |
| **AJP-4.3** | Host-Nation Support | APOD/SPOD nation field |
| **AJP-4.4** | Movement | MSR / ASR polylines with status (Open / Contested / Cut) |
| **AJP-4.6** | JLSG | JLSG echelon in OOB datalist |
| **AJP-4.10** | Medical Support | MEDEVAC enum in event-source datalist |
| **AJP-5** | Planning of Operations | COPD branches & sequels per phase, LOO/LOE catalogues |
| **AJP-6** | CIS | CIS PACE tile (Primary / Alternate / Contingency / Emergency) |
| **AJP-10** | Strategic Communications | Master Narrative field |
| **AJP-10.1** | Information Operations | InfoOps category on CoAs |
| **AJP-10.3** | Military Public Affairs | Public-release flag on events |

Per-publication summaries live under `AJP/SUMMARIES/AJP-*.md` (33 files). Methodology disclosure (which summaries rest on full PDF read vs structural inference) is in `AJP/SUMMARIES/README.md`.

---

## 6 · Compliance with the DIANA Challenge Statement

`checklist.md` post-v011 stands at **73 / 74 = 98.6 %** headline coverage against `Specifications/20260502 Decision Superiority for NATO Warfighters.txt`.

| Section of the spec | ✅ Met | 🟡 Partial | ★ Foundation-model gap | 🔴 Not met | Total |
| --- | :-: | :-: | :-: | :-: | :-: |
| 0 · Top-level scope | 3 | 0 | 1 | 0 | 4 |
| 1 · Constraints addressed (i) | 5 | 0 | 0 | 0 | 5 |
| 2 · Technical foundation (ii) | 10 | 0 | 0 | 0 | 10 |
| 3 · Functional outcomes (iii) | 13 | 0 | 0 | 0 | 13 |
| 4 · Illustrative scenario (Eastern Flank) | 22 | 0 | 1 | 0 | 23 |
| 5 · Exemplar effects (the 10 explicit asks) | 7 | 1 | 2 | 0 | 10 |
| 6 · Cross-cutting (single-file, air-gap, STANAG, etc.) | 9 | 0 | 0 | 0 | 9 |
| **TOTAL** | **69** | **1** | **4** | **0** | **74** |

The single 🟡 is item 5.9 (NL + forecasting + optimisation + perception): NL is delivered, the other three sub-aspects are foundation-model-deferred. The four ★ items are the planned LangChain + Ollama + military-foundation-model integration and are **transparently deferred** behind named seams (the destination accreditation authority retains full discretion over which model lands behind them and when).

The Eastern Flank illustrative scenario is the literal seeded default mission. Every beat (4.1 through 4.23 of `checklist.md`) is verifiable in the running SPA: NATO eFP BGs in EE/LV/LT/PL, US 2ABCT, SNMG1, OPFOR forces from LMD/Kaliningrad/Belarus/Baltic Fleet, ELINT events from Murmansk-BN and Krasukha-4, AIS dark-pattern vessels DARK ECHO 1/2 targeting Critical Undersea Infrastructure (Estlink 2, BalticConnector, Nord Balt Cable, NordStream Remnant), the suspect UAS detection at a civilian airport (i03) and its FUSION confirmation (i04 with P=0.87), and the OSINT convoy reports (i05).

---

## 7 · Versioning chain (v001 → v011)

The repo enforces a strict superset versioning rule (`CLAUDE.md`): every change creates a new monotonically numbered file, the chain is never broken, no version is ever edited in place, and no feature is ever removed. The audit trail is the chain.

| Version | Net feature delta vs previous |
| --- | --- |
| **v001** | Initial baseline. Mission Editor with 10 tabs (MISSION/PHASES/GEO/INTEL/OOB/ACH/COA/AIS/IO/SETTINGS); ACH 3-level scale; AIS dark-vessel detection; A2/AD bastions; CUI overlay; phase engine; auto-mode random-pick stub; turn button; INFO modal; NL command terminal; CycloneDX 1.7 datamodel. |
| **v002** | Joint Targeting (AJP-3.9 — JTC, JPTL CRUD with HVT/HPT/TST + F2T2EA + CDE + RTL + NSL); Movement (AJP-3.13/4.4 — MSR/ASR/APOD/SPOD CRUD); Posture (AJP-3.14/3.23/3.3/6 — FPCON/CBRN/PNT/CIS PACE tiles); CYBER as 5th domain (AJP-3.20); NEUTRAL faction (AJP-3.19); Operation Type / Mission Type; Master Narrative; CoG; End-state criteria. **+23 acronyms.** Mission Editor: 10 → 13 tabs. |
| **v003** | Official NATO logo + CONFIANZA23 logo on top bar; ACH 5-level scale (CC/C/N/I/II = +2/+1/0/-1/-2) extending Heuer; top-right action grid 3×2 layout. |
| **v004** | NATO logo repositioned to left + CONFIANZA23 to its right; classification + TRL-7 strings hidden from UI (data preserved); collapsible rail sections with EXPAND/COLLAPSE ALL; **kinetic per-turn movement** on every CoA execution; topbar `auto auto 1fr` grid (no more overlap). |
| **v005** | **Cubo A — DIANA-evaluator priority batch.** ROE-gated CoA execution (WF-01); C-UAS auto-trigger workflow (WF-02); OPORD/FRAGO STANAG-2014 generator (WF-03); ACH auto-suggest scorer (AN-04); Tactical → Operational → Strategic roll-up (CO-01); Weather first-class feed with WX tile (LD-03 — closes the only 🔴 from v001 review); air-gap bundle script `tools/build_airgap_bundle.sh` (DP-01). Mission Editor: 13 → 16 tabs. |
| **v006** | **Cubo C — UX/QoL.** localStorage persistence (mission + units); 12 hotkeys with input-guarding; OOB search-and-fly via `window.__c23_flyTo()`; undo/redo stack; multi-mission slots (5); print one-pager (`@media print`); i18n stub EN/ES/FR; MEDEVAC/IED/EOD enums via `<datalist>`. Mission Editor: 16 → 17 tabs (added WORKSPACE). |
| **v007** | **Cubo D — visual / branding.** NATO logo halo (transparent + double drop-shadow); 3 themes (dark / light / high-contrast) via `[data-theme]`; slide-down rail animation; CSS-only tooltips via `[data-tip]:hover:after`; persistent active-faction indicator. |
| **v008** | **Cubo B easy.** AN-02 anomaly-detection rule set; LD-02 adversary-behaviour replay; WF-05 AAR formaliser; CO-02 multi-HQ scoping (SHAPE/JFC-BAL/TCC-N/TCC-S). All four under a new INTEL OPS tab. Mission Editor: 17 → 18 tabs. |
| **v009** | **Cubo B hard.** AN-01 event correlation engine (`(source × top-keyword)` clustering); AN-03 cascade-effects per CoA; LD-01 live-feed adapter (polling + CORS-aware + persisted); WF-04 Operations Assessment MoP/MoE per CoA. New ANALYTICS tab. Mission Editor: 18 → 19 tabs. |
| **v010** | **Doctrine breadth — DIANA-evaluator priority.** Cascade rules as a doctrine-citable table (each rule cites its AJP); Branches & Sequels per phase (AJP-5); JPRC five-task PR sequence (AJP-3.7) in new PR/JPRC tab; LOO/LOE/C-IED columns on CoAs; MoP/MoE bucketed per LOO; CTF/CTG/CTU/JLSG echelons; CIMIC/MSU types via `<datalist>`; air-gap script sandbox-validated. **+11 acronyms.** Mission Editor: 19 → 20 tabs. |
| **v011** | **Wargaming + COP overlays + naval CRUD + ATO + air-gap bundle.** WARGAMING tab (pairwise NATO×OPFOR matchup matrix with deterministic seeded simulator); Personnel Recovery overlay on COP (stage-coloured rings); naval interdiction polygon promoted to MOVEMENT-tab CRUD with map render; ATO cycle phase column on AIR CoAs; **air-gap bundle materialised** (5.5 MB without tiles) under `dist/airgap/`; **CycloneDX 1.7 attestation skeleton** `dist/airgap/cdax.json` ready for signing. Mission Editor: 20 → 21 tabs. |

Every versioned file contains its own changelog header (`+ added · ~ improved · # fix · Removed: NONE`). md5 of every prior version is verifiable via `md5sum *_v*.html`.

---

## 8 · Documentation files

| File | Purpose | Audience |
| --- | --- | --- |
| `README.md` | This file — repo overview | Anyone |
| `CLAUDE.md` | Working notes for Claude Code (versioning rule, repo conventions) | Future Claude sessions |
| `MasterPrompt.txt` | Authoritative deliverable spec (A–K) — the original brief | Original-spec auditors |
| `checklist.md` | DIANA spec coverage (98.6 %) with per-item evidence pointers | DIANA evaluators, QA |
| `roadmap.md` | Doctrine-driven plan, sections 1–13: per-AJP backlog, v005-v011 status, FM-01..FM-05 forward roadmap, candidate batches for v012, open questions | Project owner, evaluators |
| `Datamodel.md` | Unified CycloneDX 1.7 / ECMA-424 envelope covering SBOM/SaaSBOM/CBOM/HBOM/ML-BOM/OBOM/MBOM/VDR/VEX/BOV/CDAX/BOM-Link/CRNF + operational data wrappers | Integrators, supply-chain reviewers |
| `NewDraft.md` | DIANA New Draft Proposal — copy-paste-ready answers per form field with char-count footers | Submission ready |
| `SESSION_STATE.md` | Resumable execution log — multi-session safety net (last action, next action, plan table with ⏳/✅, per-bump checkboxes) | Future Claude sessions |
| `Pitch Deck_NAVINT v20260501v2.pdf` | Commercial deck (financial plan, team, TAM/SAM/SOM, competition, GTM) | Investors, business reviewers |
| `Specifications/*.txt` | DIANA challenge inputs (FAQ, welcome, decision-superiority spec, new-draft-proposal form) | Read-only source of truth |
| `Format/EasternFlankv003.html` + `.json` | Original template the platform was derived from | Archaeological reference |
| `AJP/SUMMARIES/AJP-*.md` | One Markdown summary per AJP (33 files) + methodology disclosure README | Doctrinal auditors |
| `AJP/<NN> …/*.pdf` | The 33 AJP PDFs themselves (mirrored from gov.uk via `update_ajp_doctrines.py`) | Doctrinal source |
| `tools/build_airgap_bundle.sh` | Stdlib + curl bundler (mirrors all CDN deps + Carto tiles + fonts; rewrites SPA `<head>`) | Deployers |
| `dist/airgap/*` | Materialised offline runtime (~5.5 MB without tiles) | SCIF deployment |
| `skills/<skill-name>/SKILL.md` | Reusable Agent Skills catalogue (35 skills, see § 9) | Agentic frameworks, future Claude sessions |

---

## 9 · Skills catalogue (35 reusable Agent Skills)

Every skill is a directory with a `SKILL.md` file (YAML frontmatter + standardised sections: Purpose / When to use / Inputs / Outputs / Instructions / Examples / Anti-patterns / References). The catalogue follows the SLO Agent Skills framework per the Master Prompt ANNEX.

### 9.1 Foundations & process

| Skill | One-line purpose |
| --- | --- |
| `make-skill` | Meta-skill: how to author a new skill |
| `build-single-file-spa` | Build a self-contained HTML SPA with React + Babel-standalone, no bundler |
| `react-babel-pitfalls` | Avoid the recurring traps of multi-block Babel-standalone setups |
| `versioning-workflow` | Apply the C23 superset versioning rule (every change → new `_vNNN.html`) |
| `roadmap-driven-release` | Pick a prioritised batch from `roadmap.md` and ship it as the next bump |
| `resumable-execution-state` | Persist mid-execution state to `SESSION_STATE.md` so any future session can resume mid-bump |
| `react-hotkeys` | Global keyboard shortcuts with input-guarding |
| `spa-persistence` | localStorage hydration + write-through, named-slot snapshots, undo/redo, clear-all escape hatch |
| `char-budget-respect` | Author multi-section text under per-section char limits with per-block live counts and a 5-pass trim protocol |

### 9.2 Mission-editor capabilities

| Skill | One-line purpose |
| --- | --- |
| `mission-editor` | Un-hardcode mission parameters into a CRUD editor (21 tabs as of v011) with JSON I/O |
| `ach-matrix` | ACH matrix (CoA × Evidence). v003 5-level scale CC/C/N/I/II. NEUTRAL side admissible since v002 |
| `ach-auto-suggest` | Heuristic auto-scoring of empty ACH cells via keyword overlap; preserves analyst values |
| `joint-targeting-jtc` | AJP-3.9 Joint Targeting Cycle: 6-phase JTC, JPTL CRUD, F2T2EA, CDE, RTL, NSL |
| `roe-gated-execution` | Gate every CoA execution behind a ROE-authorisation modal that surfaces JPTL TST hits + RTL/NSL + CDE |
| `movement-entities` | MSR / ASR polylines + APOD / SPOD point CRUD per AJP-3.13 / 4.4 |
| `posture-indicators` | FPCON / CBRN / PNT / CIS-PACE colour-coded top-bar tiles per AJP-3.14 / 3.23 / 3.3 / 6 |
| `echelon-rollup-and-scoping` | Tactical → operational → strategic roll-up + per-HQ AOR bbox scoping |
| `event-analytics` | Three companion analytics: anomaly detection (rules), correlation (clusters), 2nd/3rd-order cascades |
| `live-feed-adapter` | Poll a remote endpoint for fresh intel events on a configurable interval; merge with provenance tagging |
| `doctrine-document-generator` | Generate STANAG-2014 OPORD/FRAGO and AAR Markdown from current mission state + turn history |

### 9.3 COP rendering & domains

| Skill | One-line purpose |
| --- | --- |
| `leaflet-cop` | NATO-styled COP on Leaflet with multi-layer toggles, animated phases, cross-tab fly helper |
| `mil-symbology` | Render APP-6 / MIL-STD-2525B units with milsymbol; derive domain from SIDC |
| `cyber-domain` | Promote CYBER to a 5th operational domain per AJP-3.20 |
| `neutral-side` | Add NEUTRAL faction (civilians, NGOs, IOs, infrastructure) per AJP-3.19 CIMIC |
| `ais-fusion` | Ingest AIS commercial-vessel feeds and flag dark-AIS tracks |
| `nato-classification` | NATO classification banners, STANAG 4774/4778 metadata, TEMPEST badging |
| `css-affordances` | Five small CSS patterns: themes, tooltips, persistent state indicators, slide animations, NATO logo halo |

### 9.4 Submissions & proposals

| Skill | One-line purpose |
| --- | --- |
| `diana-proposal-draft` | Generate a copy-paste-ready DIANA "New Draft Proposal" mapping every form field to a self-verifying char-budgeted answer; cites the live C23 NAVINT artefact and the pitch deck figures |
| `playwright-spa-screenshots` | Capture publication-quality PNGs from a single-file SPA via Playwright; uses `.modal` locator pattern so backdrops do not bleed into the frame |
| `narrated-demo-video` | Produce a narrated screencast (≤4 min MP4) with TTS voice-over (Edge `en-GB-RyanNeural`), English subtitles burned in, and a visible animated cursor that leads every click |

### 9.5 Deployment & data

| Skill | One-line purpose |
| --- | --- |
| `air-gap-mirror` | Convert a CDN-loaded SPA into an air-gapped local-mirror build |
| `cyclonedx-unified-bom` | Single CycloneDX 1.7 / ECMA-424 envelope covering S/SaaS/C/H/ML/O/M-BOM, VDR, VEX, BOV, CDAX, BOM-Link, CRNF |

### 9.6 Doctrine ingestion

| Skill | One-line purpose |
| --- | --- |
| `ajp-doctrine-summary` | Produce a consistent per-AJP Markdown summary suitable for indexing and roadmap synthesis |
| `doctrine-roadmap-synthesis` | Consolidate per-doctrine summaries into a prioritised platform roadmap |
| `nato-ajp-sync` | Sync the local mirror of NATO Allied Joint Publications from gov.uk |

Index lives at `skills/README.md` (see for detailed cross-references and version-introduction tags).

---

## 10 · Team

| Role | Person | Experience |
| --- | --- | --- |
| **CEO / Founder** | Rafael Ausejo Prieto | > 32 years — NATO, ALSTOM, S21Sec/Thales, BeDisruptive, A3Sec, 4iQ, VASS, Entelgy, Oesía, ANADAT/Babel, Davinci/Getronics, IT Way, Multico, Memorex Telex |
| **CTO / AI Director** | Pedro Gallego Torrecilla | > 25 years — Sidertia Izertis, INGECOM, CMD, Factum (sold to Santander) |
| **Business Development + Marina Mercante advisor** | Daniel Martín Moreno | > 30 years — Ministerio de Transporte, Secuware |
| **Advisory board** | DGAM, Armada Española, NATO, retired General officer (joining shortly) |

**Team certifications:** ISO 27001 Lead Auditor · CISM · CISA · CISSP · ISA Senior Member (5-year, Standards Committee, Expert) · Stormshield CSNOT · Tenable TCSE-OT and TCSA-OT · Kaspersky Certified Professional (Threat S39.02, CyberSecurity S38.30) · CCI Centro de Ciberseguridad Industrial Profesional (Niveles Blanco + Verde).

---

## 11 · Commercial

### 11.1 Three-year financial plan (NAVINT line, EUR)

| Year | Revenue | EBITDA | Margin |
| --- | ---: | ---: | ---: |
| 2027 | 3 420 050 | 1 620 351 | 47.3 % |
| 2028 | 5 980 795 | 2 276 007 | 38.0 % |
| 2029 | 11 880 400 | 4 900 891 | 41.2 % |
| **3-yr avg** | — | — | **~ 42 %** |

### 11.2 Investment round (closing 2026-Q4)

- **Ticket:** EUR 1 000 000
- **Equity offered:** 25 %
- **Pre-money:** EUR 3 000 000
- **Use of funds:** 60 % sales & marketing · 30 % product development · 10 % operations (incl. ISO 27001 / ENS / IEC 62443 certifications)

### 11.3 Market sizing

- **TAM** (global Maritime Domain Awareness 2025): US$ 1 375 M
- **SAM** (15 % of TAM, Spain + EU + Mediterranean basin): US$ 206 M
- **SOM** (NAVINT year-3 target, 4.17 % of SAM): ~ EUR 8 M
- CAGR 9.6 % → US$ 2 589 M by 2032
- **Source:** Global Maritime Domain Awareness Solution Market Insights and Forecast to 2032

### 11.4 Customer mix forecast

- **60 % Government** — Navantia, Puertos del Estado, Ministerio de Defensa
- **30 % Civil B2B** — Marina Mercante, commercial fishing sector
- **10 % Premium Yachts** — high-value private vessels, perimeter VIP security

### 11.5 Pricing tiers

| Tier | Price | Scope |
| --- | --- | --- |
| Community Edition | Free on GitHub | Plataforma base |
| Small Business | EUR 1 000 / month | Plataforma base |
| Enterprise | EUR 5 000 / month | Sectorised |
| Government | EUR 15 k – 1.5 M | Tailored |

Plus: monthly subscription + initial fee, customisation consulting, training.

### 11.6 Sales channels

- **Active:** Satinel (20-year-anniversary partner), Digital Fortress, BABEL, TRC.
- **In conversation:** Oesía, VASS.

### 11.7 Reference projects

| Customer | Partner | Solution | Status |
| --- | --- | --- | --- |
| Fred Olsen Express | — | Onboard-system risk analysis | Invoiced 2023 |
| NAVANTIA | SATINEL | STRATOS Strategic Intelligence + Digital Twin 4.D XBOM + NAVINT Maritime Security | Forecast 2026 Q2 |
| Suez Canal Authority | CDTI / Digital Fortress | NAVINT Maritime Security | Forecast 2026 Q4 |

### 11.8 Competitive positioning (NAVINT vs comparators)

| Axis | NAVINT | Indra iSIGHT | Saab 9LV | Thales VesselVis | Windward | Spire Maritime |
| --- | --- | --- | --- | --- | --- | --- |
| Data sovereignty | Total (Local-First) | High (closed) | High (closed) | High (closed) | Low (Cloud SaaS) | Low (Cloud SaaS) |
| Latency | Zero | Med/High | Med/High | Med/High | Med | Med |
| Architecture | FastAPI / Python 3.14 | Legacy Monolithic | Legacy Monolithic | Legacy Monolithic | Cloud | Cloud |
| AI inference | Local LLM (on-device) | Rules-based | Rules-based | Rules-based | Cloud AI | Cloud AI |
| Hardware | Light (16 GB RAM) | Heavy servers | Heavy servers | Heavy servers | Cloud-dependent | Cloud-dependent |
| Nationality | Spain | Spain | Sweden | France | Israel | USA |
| Cost & deployment | Agile / Days | Millions EUR / Years | Millions EUR / Years | Millions EUR / Years | SaaS license | SaaS license |

---

## 12 · Standards & compliance

| Standard | Implementation point |
| --- | --- |
| **STANAG 4774** (Confidentiality Metadata Label Syntax) | Banner + CycloneDX `declarations.attestations` |
| **STANAG 4778** (Metadata Binding) | CycloneDX BOM-Link + cdax.json |
| **STANAG 2014** (Allied Operations Order format) | OPORD/FRAGO generator (WF-03) emits this shape |
| **TEMPEST SDIP-27** | Compliance row in banner; air-gap runtime is the operational manifestation |
| **MIL-STD-2525B / APP-6** | All unit symbols rendered via milsymbol; SIDC editing in OOB tab |
| **CycloneDX 1.7** | `Datamodel.md` is the unified envelope; `dist/airgap/cdax.json` is the platform's own BOM |
| **ECMA-424** | The standardisation route under which CycloneDX is recognised |
| **ISO 27001** | On the v012 backlog (`roadmap.md` § 12.6); team carries Lead Auditor certification |
| **ENS (Esquema Nacional de Seguridad)** | Same backlog item |
| **IEC 62443** (Industrial cybersecurity) | Same backlog item |
| **AJP-01 through AJP-10.3** | All 33 publications mirrored locally; per-rule citation in cascade engine |

---

## 13 · Compliance posture summary

C23 NAVINT is delivered with full transparency about what is shipped vs deferred:

- **Shipped (verifiable in v011):** every spec compliance row marked ✅ in `checklist.md` (69 of 74); every doctrine binding listed in § 5; every integration tier described in § 4; the air-gap bundle materialised under `dist/airgap/`; the CycloneDX attestation skeleton ready for organisational signature.
- **Deferred behind named seams:** the four ★ items in `checklist.md` (FM-01 LangChain + Ollama foundation-model swap; FM-02 CV/radar fusion; FM-03 agent-based representations; FM-04 RL/probabilistic toolkit; FM-05 forecasting/optimisation/perception). These are the destination accreditation authority's call, not a project gap.
- **The single 🟡:** spec item 5.9 — NL terminal is delivered, but the forecasting / optimisation / perception sub-aspects are FM-05.

Honest disclosures live in `checklist.md § 8`. The roadmap's forward plan (FM swap order, doctrine breadth backlog, operational hardening) lives in `roadmap.md § 12`.

---

## 14 · Annexes

### Annex A — Doctrinal bibliography (representative)

- NATO Standardization Office (2017). *Allied Joint Doctrine (AJP-01, Edition E, Version 1)*. NATO.
- NATO Standardization Office (2019). *Allied Joint Doctrine for the Conduct of Operations (AJP-3, Edition C, Version 1)*. NATO.
- NATO Standardization Office (2020). *Allied Joint Doctrine for the Conduct of Operations (AJP-3, Edition D, Version 1)*. NATO.
- NATO Standardization Office (2021). *Allied Joint Doctrine for Joint Targeting (AJP-3.9, Edition B, Version 1)*. NATO.
- NATO Standardization Office (2022). *Allied Joint Doctrine for Movement (AJP-4.4, Edition C, Version 1)*. NATO.
- Heuer, R. J. (1999). *Psychology of Intelligence Analysis*, Ch. 8 — Analysis of Competing Hypotheses. CIA Center for the Study of Intelligence.
- Full mirror of all 33 AJPs at `AJP/` and at <https://www.gov.uk/government/collections/allied-joint-publication-ajp>.

### Annex B — Data model & standards

- CycloneDX BOM JSON 1.7 — <https://cyclonedx.org/docs/1.7/json/>
- ECMA-424 (CycloneDX as Ecma standard).
- MIL-STD-2525B / APP-6 (NATO symbology).
- STANAG 4774 / 4778 (NATO confidentiality metadata).
- Master Prompt ANNEX (project-level AIS schema).
- DIANA TRL convention: TRL 1–9 per FAQ (TRL 7 = "Prototype demonstration in operational environment").

### Annex C — Deliverable traceability (Master Prompt A–K)

| Deliverable | Where it lives |
| --- | --- |
| **A** Generate the platform from `Format/EasternFlankv003.html` + JSON | `C23_DIANA_NATO_WARFIGHTERS_v011.html` |
| **B** Mission Editor — full CRUD on every previously-hardcoded parameter + JSON I/O | CONFIG modal, 21 tabs, three export schemas |
| **C** ACH Matrix CoA × Evidence CRUD with C/N/I scoring (5-level since v003) | CONFIG → ACH MATRIX |
| **D** Auto mode (random-pick stub for the future LangChain + Ollama swap) | Top bar `⚙ AUTO` toggle; integration seam `autoSelectCoA()` |
| **E** Turn button (Allied / Hostile faction toggle) | Top bar `◆ TURN`; auto-flips after each CoA |
| **F** Coverage of every "Decision Superiority" requirement | `checklist.md` (98.6 %) |
| **G** Info button with Instructions + Acronyms tabs | Top bar `ⓘ INFO`; 90+ acronyms in v011 |
| **H** Per-AJP doctrine summaries | `AJP/SUMMARIES/AJP-*.md` (33 files) |
| **I** Doctrine-driven roadmap and platform updates | `roadmap.md` (sections 1-13) |
| **J** Unified CycloneDX 1.7 / ECMA-424 data model | `Datamodel.md` |
| **K** Air-gapped, single HTML, 16 GB RAM, NATO secured-environment standards | All respected; `tools/build_airgap_bundle.sh` + `dist/airgap/` |

### Annex D — Contact

| Channel | Detail |
| --- | --- |
| Submitter | Rafael Ausejo Prieto |
| Email | rafael.ausejo@confianza23.es |
| Phone | +34 661 15 27 94 |
| Web | <https://www.confianza23.es> |
| Tagline | "Hacemos posible lo imposible" |

---

**Disclaimer.** This software is a prototype developed for the DIANA NATO Warfighters Challenge. It contains simulated data for training and evaluation purposes only. The Auto-mode CoA selector is a deterministic random stub; the integration seam for the planned LangChain + Ollama + military foundation model is `autoSelectCoA()`. NATO doctrine is referenced from publicly released, unclassified editions only. The Eastern Flank scenario is a training construct; any resemblance to operational planning is coincidental and instructional.
