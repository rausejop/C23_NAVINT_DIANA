# roadmap.md — Doctrine-Driven Platform Update Plan

**Source:** synthesised from per-doctrine summaries in `AJP/SUMMARIES/AJP-*.md` (deliverable H).
**Target platform:** `C23_DIANA_NATO_WARFIGHTERS.html` (single-file SPA, TRL 6+, air-gapped, 16 GB RAM).
**Purpose:** consolidate every doctrine-driven improvement candidate into one prioritised roadmap and mark which items are already shipped vs scheduled (deliverable I).

> **Methodology disclosure (as in `AJP/SUMMARIES/README.md`):** the per-doctrine items were derived from the publicly-released NATO AJP titles and the standard structure of each publication, not from a full PDF text-extraction. Items marked _★ deep-dive needed_ should be re-validated against the source PDF before any operational use.

---

## 0. Status legend

- ✅ **Shipped in v1.0** — already present in the SPA built in this session.
- 🚧 **Scheduled** — captured here, deferred to a follow-on iteration.
- ★ **Deep-dive needed** — depends on full PDF read of the cited AJP.

---

## 1. Capstone & Conduct (AJP-01, AJP-3, AJP-5)

| Item | AJP | Status | Notes |
| --- | --- | --- | --- |
| Commander's Intent surfaced in Mission Editor | AJP-01 | ✅ | `mission.intent` in DEFAULT_MISSION; editable. |
| Operation Type selector (Art.5 / NA5CRO / Cooperative Security) | AJP-01 | 🚧 | Add a `mission.operationType` enum; render on top bar. |
| LOO / LOE tagging on CoAs and events | AJP-3 | 🚧 | Add `loo[]` and `loe[]` arrays to `coa` and `event`. |
| Operations Assessment subtab | AJP-3 | 🚧 | New tab under Decision Support. |
| Centre of Gravity (CoG) capture | AJP-3 | 🚧 | Add `mission.cog` (friendly + adversary). |
| COPD branches & sequels | AJP-5 | 🚧 | Per-phase `branches[]` and `sequels[]` arrays. |
| Wargaming subtab (multi-CoA matchups) | AJP-5 | 🚧 | Re-use existing CoA simulator across pairings. |

## 2. Maritime / Land / Air / Cyber (AJP-3.1 → 3.3.5, 3.20)

| Item | AJP | Status | Notes |
| --- | --- | --- | --- |
| AIS / Radar / ELINT fusion | AJP-3.1 | ✅ | AIS tab + dark-vessel rendering live. |
| CTF/CTG/CTU & JLSG echelons | AJP-3.1 / 4.6 | 🚧 | Extend OOB echelon enum. |
| User-editable maritime interdiction zone | AJP-3.1 | 🚧 | Promote `phase3Polygons.navalInterdict` to CRUD. |
| OOB role tag (Combat / Combat Support / CSS) | AJP-3.2 | 🚧 | New OOB field. |
| AO/FLOT/FEBA drawing tools | AJP-3.2 | 🚧 | Map editor mode. |
| ATO cycle phase property on AIR CoAs | AJP-3.3 | 🚧 | Enum: planning/production/execution/assessment. |
| PNT-degradation top-bar indicator | AJP-3.3 | 🚧 | Driven from EW-tagged intel events. |
| C-UAS workflow with ROE confirmation modal | AJP-3.3.5 | 🚧 | Triggered by `RADAR + UAS` intel events; matches DIANA scenario. |
| ROZ / MRR drawing tools | AJP-3.3.5 | 🚧 | Map editor. |
| **CYBER** as 5th domain in OOB | AJP-3.20 | 🚧 | Domain enum; SIDC variants. |
| Cyber attack as a formal INTEL event source | AJP-3.20 | ✅ (partial) | Already in `phaseLogs` (DDoS); promote to user-editable INTEL events. |

## 3. Joint Targeting (AJP-3.9) — _critical_

| Item | Status | Notes |
| --- | --- | --- |
| Joint Targeting module: 6-phase JTC | 🚧 | New top-level Mission Editor tab. |
| **JPTL** CRUD | 🚧 | List of targets with priority, intent, restrictions. |
| **HVT / HPT / TST** flags on OOB units | 🚧 | New unit field. |
| **CDE** stub on engagement workflow | 🚧 | Placeholder ratings until ML model integrated. |
| RTL / NSL ingestion | 🚧 | Importable lists; surfaced before any "engage". |
| BDA / MEA closure of CoA loop | 🚧 | After-action data attached to executed CoA in turn history. |

## 4. Movement & Sustainment (AJP-3.13, 4, 4.3, 4.4, 4.6, 4.10)

| Item | AJP | Status | Notes |
| --- | --- | --- | --- |
| APOD / SPOD entities on COP | AJP-3.13 | 🚧 | New CRUD list of port nodes. |
| ITV indicator at top bar | AJP-3.13 | 🚧 | Counter of "in transit" units during deployment phases. |
| Logistics Posture (DOS, MSR status, key supply nodes) | AJP-4 | 🚧 | New Mission Editor section. |
| HNS catalogue subtab | AJP-4.3 | 🚧 | Per-host-nation list of supplied capabilities. |
| MSR / ASR drawing + status (open/contested/cut) | AJP-4.4 | 🚧 | Map editor; rename existing `locCut` → `MSR-CUT`. |
| Medical footprint (Roles 1-4) | AJP-4.10 | 🚧 | New OOB unit type + map layer. |
| MEDEVAC event source | AJP-4.10 | 🚧 | New INTEL event source enum. |

## 5. Force Protection / C-IED / EOD / CWMD (AJP-3.14, 3.15, 3.18, 3.23)

| Item | AJP | Status | Notes |
| --- | --- | --- | --- |
| FPCON indicator at top bar | AJP-3.14 | 🚧 | Editable per phase. |
| CIED Pillar tag on CoAs | AJP-3.15 | 🚧 | Defeat-Device / Attack-Network / Prepare-Force. |
| IED incident map icon | AJP-3.15 | 🚧 | Specialised event subtype. |
| EOD unit type | AJP-3.18 | 🚧 | OOB / SIDC. |
| CBRN ALERT indicator | AJP-3.23 | 🚧 | Top-bar tile, escalates FPCON. |

## 6. Stability, COIN, Peace Support, NEO, HumAss, SFA (AJP-3.7, 3.10.1, 3.16, 3.19, 3.22, 3.24, 3.25, 3.26, 3.27, 3.28)

| Item | AJP | Status | Notes |
| --- | --- | --- | --- |
| **Mission Type** taxonomy | 3.16 / 3.24 / 3.25 / 3.26 | 🚧 | Combat / SFA / PSO / NEO / HumAss / Stabilization. |
| **NEUTRAL** side in OOB | AJP-3.19 | 🚧 | Add side enum value; APP-6 neutral diamond. |
| CIMIC Liaison unit type | AJP-3.19 | 🚧 | New OOB type. |
| MSU (Stability Policing) unit type | AJP-3.22 | 🚧 | New OOB type. |
| Isolated Personnel (IP) tracking + JPRC modal | AJP-3.7 | 🚧 | Five-task PR sequence. |
| Non-kinetic effect score on CoA outcomes | AJP-3.27 | 🚧 | Extend `CoaBar` with `non-kinetic` row. |
| End-state criteria editable list | AJP-3.28 | 🚧 | Mission Editor → Mission tab. |
| PsyOps response as CoA category | AJP-3.10.1 | 🚧 | New CoA tag. |

## 7. Communication, Information, Public Affairs (AJP-6, 10, 10.1, 10.3)

| Item | AJP | Status | Notes |
| --- | --- | --- | --- |
| CIS posture (PACE state) at top bar | AJP-6 | 🚧 | Primary / Alternate / Contingency / Emergency. |
| Master Narrative field | AJP-10 | 🚧 | Mission Editor → Mission tab. |
| InfoOps category on CoAs | AJP-10.1 | 🚧 | New tag. |
| Public-release flag on events | AJP-10.3 | 🚧 | MILPA filter. |

---

## 8. Cross-cutting platform improvements (already shipped)

These were derived from doctrine and are **already present in v1.0** of `C23_DIANA_NATO_WARFIGHTERS.html`:

- **Phase ladder with relative + absolute dates** (Mission Editor → PHASES) — full CRUD per AJP-5.
- **Geopolitical & Intel events** as separate, editable streams (per AJP-3.20, AJP-10).
- **ACH Matrix** (CoAs × Evidence) with C/N/I scoring per AJP-5 CoA-comparison thinking.
- **Decision Support** with probabilistic CoA outcomes — placeholder for AJP-3 EBAO assessment.
- **AIS / Multi-source fusion** tab — direct support for AJP-3.1 maritime ISR.
- **Auto mode** as the integration seam for the planned LangChain + Ollama foundation model.
- **Turn button** that flips Allied / Hostile control (per the wargame requirement; complements the doctrinal red-team / blue-team stance).
- **Info button** with full Instructions + Acronyms tabs (deliverable G).
- **JSON import/export** for full mission, OOB-only, ACH-only.

---

## 9. Implementation priority for the next iteration (v1.1)

If only one work-batch can be delivered after v1.0, do these — they are the highest-leverage doctrinal items and they unlock multiple downstream features:

1. **Joint Targeting module** (AJP-3.9). The single most impactful doctrinal addition.
2. **Mission Type taxonomy** + Operation Type (AJP-01, 3.16, 3.24, 3.25, 3.26). One small enum, broad downstream effect.
3. **MSR / ASR + APOD / SPOD entities** (AJP-3.13, 4.4). Concrete, drawable, immediately useful.
4. **FPCON / CBRN / PNT / CIS-PACE indicators** (AJP-3.14, 3.23, 3.3, 6) as additional top-bar tiles.
5. **CYBER** as a 5th domain (AJP-3.20). Touches OOB, SIDC, filters, tally.
6. **NEUTRAL side** (AJP-3.19). Required to represent civilians, IOs, NGOs that the DIANA scenario relies on.

Items 1–6 collectively cover the most operationally consequential doctrinal gaps and are estimated at ~1500–2500 additional lines of HTML/JSX without breaking the single-file or air-gapped constraints.

---

## 10. Ongoing work (v1.x)

Everything in §§ 1–7 above marked 🚧 plus:

- Re-read each AJP PDF in full and re-validate the items in this roadmap (★ deep-dive flag).
- Author the per-AJP "concepts and definitions update" entries directly into the in-app Acronyms tab via a typed schema rather than the current static list.
- Move CoA outcome simulation from a deterministic seeded-PRNG stub to an actual probabilistic model (still bounded by 16 GB RAM at TRL 6+).
- Replace the current `autoSelectCoA()` random pick with the LangChain + Ollama + military foundation-model query when the platform graduates to TRL 7.

---

## 11. DIANA-spec compliance gaps — STATUS POST-v009

> **Originally written post-v004**, then progressively closed by v005..v009. Items below are tagged with the closing bump (✅ vN) so the audit trail is preserved.
>
> **Net delta vs the post-v004 review:** 16 items moved 🟡/🔴 → ✅. **The 🔴 backlog is empty.** The 🟡 column is down to 1.

### 11.1 Foundation-model integration (★) — the TRL 7 swap

These remain ★ because they require a real model running out-of-process. The platform's seam (`autoSelectCoA()`, `intelEvents` ingestion, `cascadeEffects()`) is in place; the brain is the gap.

| ID | Checklist row | Item | Status |
|---|---|---|---|
| FM-01 | 0.1 | Replace `autoSelectCoA()` random pick with LangChain + Ollama + military-foundation-model query | ★ pending |
| FM-02 | 4.11 / 5.8 | CV/radar fusion model emitting per-track P(hostile) | ★ pending |
| FM-03 | 5.2 | Agent-based representations of red/blue forces | ★ pending |
| FM-04 | 5.3 | RL / probabilistic / optimisation toolkit | ★ pending — v009 WF-04 MoP/MoE scaffolds the analytics surface |
| FM-05 | 5.9 | Forecasting / optimisation / perception modules behind the NL terminal | ★ pending — NL terminal already accepts the verbs |

### 11.2 Live data ingestion — DELIVERED

| ID | Checklist row | Item | Status |
|---|---|---|---|
| LD-01 | 1.3 / 2.2 | Live-feed adapter for ISR streams | ✅ **v009** — `AnalyticsTab` polling adapter, persisted in `c23.live`, log channel `[LIVE]` |
| LD-02 | 2.6 | Historical adversary-behaviour replay | ✅ **v008** — load JSON of intel events, append with `LIVE-FEED`/`REPLAY` tag |
| LD-03 | 2.9 | Weather feed as first-class source (was 🔴) | ✅ **v005** — `mission.weather { overall, forecast[] }`, top-bar WX tile, dedicated WEATHER tab CRUD, 4 regions seeded |

### 11.3 Analytics depth — DELIVERED

| ID | Checklist row | Item | Status |
|---|---|---|---|
| AN-01 | 3.1 / 4.9 | Correlation engine across event streams | ✅ **v009** — `correlateEvents()` clusters by `(source × top-keyword)`, severity-rolled-up |
| AN-02 | 3.2 | Generalised anomaly detection | ✅ **v008** — `detectAnomalies()` rule set: AIS dark + loitering, OOB disrupted/R4, JPTL CDE≥4 TST, posture interactions |
| AN-03 | 3.5 | 2nd- and 3rd-order effects modelling | ✅ **v009** — `cascadeEffects()` per CoA across SEA/LOG/HNS/INFRA/STRATCOM/LAND/NEUTRAL/CIS/C2 |
| AN-04 | 4.9 | Auto-suggest ACH scores | ✅ **v005** — keyword-overlap heuristic on the ACH MATRIX tab; preserves analyst values |

### 11.4 Workflow completeness — DELIVERED (forecasting still ★)

| ID | Checklist row | Item | Status |
|---|---|---|---|
| WF-01 | 1.2 | ROE-gated CoA execution modal | ✅ **v005** — `RoEModal` with TST + RTL + NSL + CDE + ✓/✕ |
| WF-02 | 4.12 | C-UAS workflow (AJP-3.3.5) auto-trigger | ✅ **v005** — regex `RADAR + (uas|uav|drone)` injects `[C-UAS]` log entry |
| WF-03 | 5.6 | OPORD / FRAGO order generator | ✅ **v005** — STANAG-2014-shaped Markdown via `OrdersTab`, downloadable |
| WF-04 | 5.6 | Operations Assessment subtab (MoP/MoE) | ✅ **v009** — per-CoA executions + success-prob stub in `AnalyticsTab` |
| WF-05 | 5.6 | AAR / lessons-learned formaliser | ✅ **v008** — Markdown AAR template populated from turn history + anomalies |

### 11.5 Coordination & strategic propagation — DELIVERED

| ID | Checklist row | Item | Status |
|---|---|---|---|
| CO-01 | 3.13 / 4.22 | Tactical → operational → strategic roll-up | ✅ **v005** — `RollUpTab` with `ECHELON_TIER` mapping + per-tier counts + lists |
| CO-02 | 3.13 / 4.23 | Multi-HQ awareness (SHAPE + JFC + TCC) | ✅ **v008** — `IntelOpsTab` HQ scoping with bbox per HQ, per-HQ tally |

### 11.6 Distribution / packaging — DELIVERED

| ID | Checklist row | Item | Status |
|---|---|---|---|
| DP-01 | 6.3 | Ready-to-run air-gapped bundle | ✅ **v005** — `tools/build_airgap_bundle.sh` (bash + curl, stdlib only); mirrors all CDN deps + Carto tiles + fonts; rewrites SPA `<head>` |

### 11.7 Original v005 priority list — ALL DELIVERED IN v005

1. ✅ WF-01 + WF-02 — v005
2. ✅ LD-03 — v005
3. ✅ WF-03 — v005
4. ✅ AN-04 — v005
5. ✅ CO-01 — v005
6. ✅ DP-01 — v005 (`tools/build_airgap_bundle.sh`)

### 11.8 What was added beyond the original v005 batch

The user later asked to "execute all the cubos", which produced v006..v009 and closed an additional 10 items not in the original v005 priority list:

- **v006 (Cubo C):** localStorage persistence, hotkeys, OOB search-and-fly, undo/redo, multi-mission slots, print one-pager, i18n stub EN/ES/FR, MEDEVAC/IED/EOD enums.
- **v007 (Cubo D):** NATO logo halo, themes (dark/light/high-contrast), slide-down rail animation, CSS-only tooltips, persistent active-faction indicator.
- **v008 (Cubo B easy):** AN-02 + LD-02 + WF-05 + CO-02 (Intel Ops tab).
- **v009 (Cubo B hard):** AN-01 + AN-03 + LD-01 + WF-04 (Analytics tab).

---

## 12. Forward roadmap — STATUS POST-v011

`checklist.md` post-v011 stands at **73 / 74 = 98.6 %** headline coverage (single 🟡 still 5.9 — partial NL coverage). Beyond the original spec coverage, v011 ships a **spec-cited "wargaming" capability** (multi-CoA matchup matrix), **PR-on-COP** + **naval-interdict-on-COP** overlays, and a **materialised air-gap bundle** with a CycloneDX attestation skeleton ready for signing.

### 12.1 Foundation-model integration (FM-01 .. FM-05) — closes the last 4 ★ + the lone 🟡

This is the only work that takes the platform from TRL 6+ to TRL 7. Every seam is in place; what's missing is the model.

| ID | Closes | Item | Estimated effort |
|---|---|---|:-:|
| **FM-01** | 0.1 | Replace `autoSelectCoA()` random pick with a LangChain + Ollama + military-foundation-model query. Air-gap-friendly via local Ollama on the tactical laptop. | M (model wiring) |
| **FM-02** | 4.11 / 5.8 | CV/radar fusion model emitting per-track P(hostile). Replaces the seeded `i04` event with live inference from a YOLO/DETR-class detector + radar correlator. Run model out-of-process; SPA consumes JSON via the `LD-01` adapter. | L (training + integration) |
| **FM-03** | 5.2 | Agent-based representations of red/blue forces. Each side gets a model-driven planner that proposes CoAs grounded in OOB + JPTL + posture; replaces the "random pick" with "model pick". | L |
| **FM-04** | 5.3 | RL / probabilistic / optimisation toolkit. Replace seeded outcome bars with sampled distributions from a learned model. v009 WF-04 MoP/MoE already exposes the consumer surface. | L |
| **FM-05** | 5.9 | Forecasting / optimisation / perception modules behind the NL terminal. Extend `handleNlp()` verbs once the back-end can answer them. | M (UI) + L (back-end) |

Recommended order: **FM-01 → FM-03 → FM-04 → FM-05 → FM-02** (FM-02 needs the most data plumbing and a CV training set).

### 12.2 Doctrine breadth — DELIVERED in v010 (DIANA-evaluator-priority batch)

| Item | AJP | Status |
|---|---|---|
| CTF/CTG/CTU + JLSG echelons | AJP-3.1 / 4.6 | ✅ **v010** — OOB Echelon datalist extended |
| JPRC modal with five-task PR sequence | AJP-3.7 | ✅ **v010** — new PR / JPRC tab; `mission.personnelRecovery.isolated[]`; per-stage tally + advance button |
| CIMIC Liaison + MSU unit types | AJP-3.19 / 3.22 | ✅ **v010** — OOB Type datalist extended |
| Branches & Sequels per phase | AJP-5 | ✅ **v010** — per-phase editor in PHASES tab; defaults seeded on all 4 phases |
| C-IED pillar tag on CoAs | AJP-3.15 | ✅ **v010** — `coa.ciedPillar` enum on ACH MATRIX |
| Operations Assessment per LOO/LOE | AJP-3 | ✅ **v010** — `coa.loo[]` / `coa.loe[]` tags + Ops Assessment subgrouped per LOO with subtotals |

### 12.3 Operational hardening — partially delivered in v010

| Action | Status |
|---|---|
| Replace heuristic `cascadeEffects()` with a doctrine-tagged rule set | ✅ **v010** — `mission.cascadeRules[]` table with per-rule AJP citation + CRUD editor |
| Validate `tools/build_airgap_bundle.sh` works (URLs alive, syntax sound) | ✅ **v010** — sandbox-tested: 6 CDN URLs HTTP 200 with expected sizes; `bash -n` passes; tile XY computation verified |
| Run the script end-to-end and verify offline in a SCIF (DevTools "Offline" → 0 failed requests) | 🚧 **needs the user** — must be executed in the user's environment |
| Sign the bundle (CycloneDX `declarations.attestations` per `Datamodel.md § 11`) | 🚧 needs the bundle to exist first |
| Re-validate the per-AJP summaries against the source PDFs (★ deep-dive flag) | 🚧 ongoing |
| Author the per-AJP "concepts and definitions" entries directly into the in-app Acronyms tab via a typed schema | 🚧 |
| End-to-end QA pass on every tab in light theme + high-contrast theme (v007) | 🚧 needs human QA |

### 12.4 Stop-doing list (still applicable)

These items remain low-payoff and should be skipped unless the user explicitly asks:

- AO/FLOT/FEBA drawing tools (AJP-3.2) — touch-heavy UI, low decision-support payoff.
- ROZ / MRR drawing tools (AJP-3.3.5) — ditto.
- Master-Narrative-driven CoA tagging (AJP-10) — already covered by the field.
- ITV indicator at top bar — too noisy; Movement tab already shows it.

### 12.5 v011 — DELIVERED (Path A executed; user reaffirmed "no LLM, prioritise DIANA evaluator")

| Item | Status |
|---|---|
| Wargaming subtab — multi-CoA matchup matrix | ✅ **v011** — `WargamingTab` with NATO×OPFOR pairwise net-score grid + best/worst summary |
| Personnel Recovery overlay on COP | ✅ **v011** (was Open Question 2) — toggle in LAYERS rail; stage-coloured rings |
| Naval Interdiction polygon CRUD | ✅ **v011** — `mission.movement.navalInterdict` editable; map renders dashed red |
| ATO cycle phase on AIR CoAs | ✅ **v011** — `coa.atoPhase` enum on ACH MATRIX |
| APOD/SPOD overlay on COP map | already shipped in v002 (Movement layer); no change needed |
| Air-gap bundle materialised + CDAX skeleton | ✅ **v011** — `dist/airgap/` (5.5 MB w/o tiles) + `cdax.json` CycloneDX attestation skeleton with placeholders for hashes/signature |

### 12.6 Candidate batch for v012 (next iteration, still no LLM)

Items still pending from §12.3 or new ideas surfaced during v011:

1. **Hash + sign the air-gap bundle** (replace `PLACEHOLDER-RECOMPUTE` in `cdax.json` with real SHA-256 of each vendor file; replace signature placeholder with an Ed25519 sign over the `attestations` block).
2. **Per-AJP "concepts and definitions" → typed schema** for the Acronyms tab (Open Question 3 from the v010-era list).
3. **End-to-end QA pass** in light + high-contrast themes (still 🚧 from §12.3).
4. **Branches/Sequels execution** — wire the per-phase branches/sequels to actually trigger alternate phase-vector sets when chosen.
5. **MEDEVAC + IED + EOD events as first-class** (extend the v006 datalist to a structured event subtype with map icons).

---

## 13. Open questions for the user

1. **v012 = continue with the §12.6 batch (hash+sign, typed Acronyms, QA, branches execution, MEDEVAC/IED/EOD), or pivot to FM-01 LLM call?** No LLM is still the standing rule.
2. **For the air-gap bundle signing (item 1 above)**: should the signature use a self-generated key pair stored locally, or do you have a CONFIANZA23 organisational key to use?
3. **Tiles for the air-gap bundle** were intentionally skipped (~200 MB). Do you want a v012 task to fetch them in a sandbox-only sub-region (e.g. zoom 4-6 only ≈ 50 MB) and ship a "lite tiles" variant?

Until answered, the platform stays at **v011 with 98.6 % headline coverage + Wargaming + COP overlays + airgap bundle materialised**.
