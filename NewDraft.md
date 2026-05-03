# NewDraft.md — DIANA "Decision Superiority for NATO Warfighters" Proposal

**Submitter:** Rafael Ausejo Prieto · CONFIANZA23 INTELIGENCIA Y SEGURIDAD SL
**Form:** `Specifications/20260503 New Draft Proposal.txt`
**Artefact:** C23 NAVINT v011 (single-file SPA), `dist/airgap/` runtime bundle, `Datamodel.md` (CycloneDX 1.7 / ECMA-424), 33 AJP summaries.

> **Character limits (form-imposed):** Short-Form sections 1500 each · Abstract 750 · Technical Merit 12000 · Suitability 3500 · Defence and Security 3500 · Company and Commercial 3500. Each block below ends with its char count.

---

## Proposal Title

```
C23 NAVINT: doctrine-driven AI decision-superiority augmentation for Maven Smart System NATO and Allied C2 platforms
```

`[114 chars]`

---

## TRL Level

```
TRL 7
```

---

## System Type

```
Software. Browser-resident single-file HTML5 SPA (~280 KB) with an offline runtime bundle (~5.5 MB) that runs unmodified on a 16 GB-RAM tactical workstation under Windows or Linux, with no installation, no server, no telemetry and no proprietary stack.
```

---

## System Level

```
A complete platform that is also a first-class integration target for AI-enabled NATO C2 systems such as MSS NATO. Operational data flows through documented JSON schemas (C23-DIANA-MISSION/1.0, OOB/1.0, ACH/1.0, the Master-Prompt ANNEX AIS schema) wrapped in a CycloneDX 1.7 / ECMA-424 envelope (Datamodel.md) covering SBOM/SaaSBOM/CBOM/HBOM/ML-BOM/OBOM/MBOM/VDR/VEX/BOV/CDAX/BOM-Link/CRNF plus operational artefacts. A polling live-feed adapter consumes ISR/OSINT producers; a STANAG-2014 OPORD emitter and an AAR formaliser publish downstream. C23 NAVINT can run standalone on a tactical workstation or embed as the decision-support layer above an MSS-NATO-class COP without changes to either side.
```

---

# SHORT-FORM PROPOSAL

## Section 1: Technical Solution (1500 chars)

```
DESCRIBE. C23 NAVINT is a single-file HTML5 SPA delivering an AI-augmented Common Operating Picture integrated end-to-end with NATO planning, targeting and assessment. Runs offline on a 16 GB-RAM tactical workstation; no install, no server, no telemetry. A 21-tab Mission Editor exposes every parameter as CRUD: OOB across LAND/AIR/SEA/SUB/CYBER and NATO/OPFOR/NEUTRAL; phase ladder with Branches and Sequels (AJP-5 COPD); the full AJP-3.9 JTC (six phases, JPTL with HVT/HPT/TST and F2T2EA, CDE, RTL, NSL); Movement (MSR/ASR/APOD/SPOD plus naval interdiction, AJP-3.13/4.4); Posture (FPCON/CBRN/PNT/CIS PACE); Weather; AJP-3.7 Personnel Recovery; AIS dark-vessel fusion; Ops Assessment MoP/MoE per LOO/LOE.

NOVELTY. (1) Doctrine-as-code: every workflow cites its AJP; the cascade engine carries per-rule AJP citation in the analyst UI. (2) Single-file delivery with verifiable air-gap: full dependency mirror under dist/airgap/vendor and a CycloneDX 1.7 attestation (cdax.json). (3) Universal CycloneDX 1.7 / ECMA-424 envelope across software, services, crypto, hardware, ML, ops and operational data. (4) Five-level ACH (CC/C/N/I/II = +2/+1/0/-1/-2) extending Heuer's three-level scale, with keyword-overlap auto-scorer preserving analyst values. (5) Foundation-model-ready seam (autoSelectCoA, live-feed adapter, NL terminal) so the destination authority retains full discretion over the model.
```

`[1397 / 1500 chars]`

---

## Section 2: Technical Alignment (1500 chars)

```
ALIGNMENT. C23 NAVINT addresses the Challenge Statement on three levels. Constraints (linear processes, manual workflows, static plans) are dissolved by an editable phase ladder, an NL command terminal and a polling live-feed adapter. Functional outcomes: the correlation engine clusters events by source and keyword; the anomaly rule set covers AIS dark-pattern, OOB disrupted/R4 units, JPTL high-CDE TSTs and posture interactions; multi-mission slots automate scenario prep; the CoA simulator and Wargaming subtab analyse high-dimensional CoA spaces; the NL terminal supports intuitive C2. Of the ten exemplar effects, seven are fully delivered (5.1 red/blue/neutral including CYBER as the fifth domain, 5.4 multi-faceted CoA params, 5.5 scenario prep, 5.6 planning/assessment via OPORD/AAR/Ops-Assessment, 5.7 full AJP-3.9 targeting, 5.8 multi-source ISR fusion + anomaly + correlation, 5.10 commercial/OSS); 5.9 (NL+forecasting+optimisation+perception) is partially delivered (NL ready, rest behind the foundation-model seam); 5.2 (agent-based) and 5.3 (RL/probabilistic) are scoped behind named seams.

AUGMENTATION. C23 NAVINT operates as a decision-support overlay above MSS-NATO-class COPs through three integration tiers: data (JSON schemas + CycloneDX BOM-Link), workflow (OPORD/AAR/JTC/Wargaming surfaces) and decision (autoSelectCoA, cascade rules, NL terminal). 73 of 74 spec items met (98.6%).
```

`[1407 / 1500 chars]`

---

## Section 3: Integration (1500 chars)

```
TRL 7+ JUSTIFICATION. DIANA defines TRL 7 as "Prototype demonstration in operational environment". C23 NAVINT meets it on five criteria. (1) Operationally representative scenario: the spec's own Eastern Flank/Baltic Sentry is the seeded default mission, beat-by-beat verifiable in the SPA. (2) Operationally representative workstation: runs on the 16 GB-RAM tactical laptop, no install, with full dependency mirror under dist/airgap/vendor. (3) Doctrinal integration: all 33 NATO AJPs mirrored locally and bound to features, with per-rule AJP citation in the cascade engine. (4) Compliance posture: STANAG 4774/4778, TEMPEST SDIP-27, MIL-STD-2525B/APP-6, CycloneDX 1.7 attestation ready for signing. (5) Release engineering: 11 versions on disk (v001–v011), md5-verified, governed by a strict superset rule prohibiting feature regression.

INTEGRATIONS. Six surfaces: (a) Three primary JSON schemas + AIS schema, auto-detected on import. (b) Universal CycloneDX 1.7 / ECMA-424 envelope (Datamodel.md). (c) Polling live-feed adapter (configurable URL+interval, CORS-aware, REPLAY/LIVE-FEED provenance tagging). (d) Adversary-behaviour replay. (e) NL command terminal with extensible verb set. (f) autoSelectCoA() seam for LangChain + Ollama + foundation-model substitution at TRL-7→8. Air-gap bundle materialised under dist/airgap/ (5.5 MB without tiles); cdax.json attestation pending sign.
```

`[1390 / 1500 chars]`

---

## Section 4: Defence Use Case (1500 chars)

```
DEFENCE USE CASE. C23 NAVINT augments NATO ACO C2 (MSS NATO and equivalents) as a doctrine-bound decision-superiority overlay across tactical/operational/strategic echelons. The Challenge Statement scenario (Eastern Flank, Baltic Sentry, drone incursion, undersea cable severance, suspect dark-AIS vessels, unmarked convoys) is the default mission. Every beat exercises a major capability: multi-source fusion drives the COP (RADAR i03 + FUSION i04 with P=0.87 + AIS DARK ECHO 1/2 + OSINT i05 + ELINT i01); the AJP-3.9 JTC carries the suspect vessel as a TST and the Iskander-M/Bastion-P brigade as an HVT; the ROE modal gates engagement with TST/RTL/NSL/CDE; the C-UAS workflow (AJP-3.3.5) auto-triggers on RADAR+UAS regex; the Wargaming subtab pairwise-tests every NATO×OPFOR matchup; the OPORD generator emits the STANAG-2014 order; the AAR formaliser closes the lessons-learned loop.

VALIDATION/TESTING. Demonstrated end-to-end against the spec's scenario; checklist.md verifies all 23 scenario beats against v011 (items 4.1–4.23). Air-gap bundle sandbox-tested for upstream URL availability (six CDN URLs HTTP 200 with expected sizes; bash -n passes; tile XY computation verified). Chain v001→v011 preserved on disk and md5-verified at every bump. 73 of 74 spec compliance items met (98.6%); the four foundation-model items are deliberately and transparently deferred behind named seams.
```

`[1393 / 1500 chars]`

---

# LONG-FORM PROPOSAL

## Section 1: Abstract (750 chars)

```
C23 NAVINT is a single-file, air-gap-capable, browser-resident decision-superiority platform that augments MSS-NATO-class C2 with a complete decision-support stack derived from all 33 NATO AJPs. It runs offline on a 16 GB-RAM tactical workstation, ingests multi-source ISR/OSINT/AIS/weather feeds, renders an APP-6 multi-domain COP, orchestrates the AJP-3.9 Joint Targeting Cycle with full JPTL/RTL/NSL/CDE gating, drives a five-level ACH, runs deterministic pairwise CoA wargaming, and emits STANAG-2014 OPORDs and structured AARs. Every workflow cites its AJP. The dependency graph is mirrored locally with a CycloneDX 1.7 / ECMA-424 attestation, ready for SCIF deployment, and the foundation-model seam is named for the TRL-7→8 transition.
```

`[742 / 750 chars]`

---

## Section 2: Technical Merit (12000 chars)

```
DETAIL. C23 NAVINT is delivered as one HTML file (~280 KB, v011) plus a 5.5 MB offline dependency bundle. It loads Leaflet 1.9 (geospatial), milsymbol (APP-6 / MIL-STD-2525B), React 18 and Babel standalone from locally-mirrored vendor paths under dist/airgap/vendor, then instantiates a 21-tab Mission Editor modal over a left-rail / centre-COP / right-dossier / bottom-command-log workbench. Every state change is persisted to localStorage with named multi-mission slots, undo/redo stacks and cross-session recovery. The platform is organised in five functional layers.

The DOCTRINAL DATA layer. A single mission object exposes mission identity (name, classification, commander, AOR, D-Day, Operation Type per AJP-01, Mission Type, Master Narrative per AJP-10, friendly and adversary Centre of Gravity per AJP-3/5, end-state criteria); phase ladder with Branches and Sequels per AJP-5 COPD; OOB by side (NATO/OPFOR/NEUTRAL per AJP-3.19) and domain (LAND/AIR/SEA/SUB/CYBER per AJP-3.20); Joint Targeting (jtcPhase, jptl with HVT/HPT/TST/NSL category and F2T2EA stage per AJP-3.9, rtl, nsl); Movement entities (msrs, asrs, apods, spods, navalInterdict polygon per AJP-3.13/4.4); operational posture (FPCON per AJP-3.14, CBRN per AJP-3.23, PNT per AJP-3.3, CIS PACE per AJP-6); a first-class weather feed driving sea state (Douglas 0–9), visibility, cloud okta; geopolitical and intelligence event streams; ACH matrix with five-level scores; Personnel Recovery (mission.personnelRecovery.isolated[] with the AJP-3.7 five-task sequence Reported→Located→Supported→Recovered→Reintegrated); cascade rules (each citing its AJP); AIS feed per the Master-Prompt ANNEX schema; LOO/LOE catalogues per AJP-3/5. Every field is editable; every change is JSON-exportable.

The GEOSPATIAL layer. Leaflet renders the COP with NATO Reflex Blue / NATO Gold chrome and overlays for unit symbols (APP-6 / MIL-STD-2525B via milsymbol), A2/AD bastions, Critical Undersea Infrastructure (CUI), AIS commercial vessels with dark-vessel triangles, Movement entities (MSR/ASR polylines status-coloured, APOD/SPOD ringed markers), JPTL target rings by category, the naval interdiction polygon, and the Personnel Recovery isolated-personnel symbols with stage-coloured rings. Phase execution drives deterministic kinetic animation; each Course-of-Action execution produces an additional kinetic move on the executing side, animating plan-versus-reality drift.

The DECISION-SUPPORT layer. A five-level Analysis of Competing Hypotheses matrix (CC/C/N/I/II = +2/+1/0/-1/-2, extending Heuer's three-level convention) correlates evidence with Courses of Action; an auto-suggest scorer fills empty cells via keyword overlap without overwriting analyst-set values. A per-CoA probabilistic outcome simulator produces deterministic seeded distributions across Mission Success, Risk, Own Casualties, Logistics Burden and Escalation. The Wargaming subtab pairwise-matches every NATO CoA against every OPFOR CoA and produces a colour-coded net-score matrix with best- and worst-case recommendations per friendly CoA.

The ANALYTICS layer. Three pure functions over the event streams. detectAnomalies is a pluggable rule set spanning AIS dark-pattern + low-speed loitering, OOB disrupted or low-readiness units, JPTL high-CDE TSTs, and posture interactions (PNT denial under Primary CIS escalates to a fall-back recommendation; CBRN Red without FPCON Delta escalates force protection). correlateEvents clusters geopolitical+intel events by (source × top-keyword) pair and surfaces clusters with two or more members, severity-rolled-up. cascadeEffects produces per-CoA second- and third-order effects driven by the editable mission.cascadeRules table; each rule is a record carrying its source AJP, allowing the analyst to audit every analytical output back to doctrinal text. An Operations Assessment subtab consumes turn history to compute MoP and MoE per CoA, bucketed by Line of Operation and Line of Effort per AJP-3 and AJP-5.

The WORKFLOW layer. Every Course-of-Action execution gates through a Rules-of-Engagement modal whenever the CoA would engage a Time-Sensitive Target on the opposing side or carries an explicit requiresROE flag. The modal surfaces the matching TSTs (with CDE rating, F2T2EA stage and restrictions), the full RTL, the full NSL, and an explicit AUTHORISE/DENY decision. The C-UAS workflow per AJP-3.3.5 auto-triggers on intelligence events tagged RADAR with UAS/UAV/drone matches, emitting a [C-UAS] log entry citing the AJP. The OPORD/FRAGO generator emits a STANAG-2014-shaped Markdown order from live mission state plus executed turn history (Sections 1 Situation · 2 Mission · 3 Execution · 4 Sustainment · 5 C2, plus Annex A JPTL and Annex B Turn History). The After-Action Review formaliser produces a structured AAR populated with detected anomalies. The natural-language command terminal accepts plain-language verbs (auto, manual, turn, phase, tally, analyse coas, reset, help) and routes unhandled queries to the foundation-model stub.

A strict superset versioning rule (CLAUDE.md) governs the release chain. Eleven versioned files (v001 through v011) are preserved on disk, all md5-verifiable; no version regresses functionality. The audit trail is the chain.

ALIGNMENT. C23 NAVINT addresses every named element of the Challenge Statement. Modelling and simulation: probabilistic per-CoA outcome simulator across five axes; deterministic pairwise Wargaming matrix; cascade-effects engine carrying second- and third-order domain impacts per CoA; kinetic per-turn movement on the COP; weather feed driving sea-state weighting. Targeting support: the full AJP-3.9 JTC is materialised — six-phase JTC indicator, JPTL CRUD with HVT/HPT/TST and F2T2EA stage tracking, CDE rating, RTL and NSL as separate CRUD lists, JPTL ring overlay on the COP, and the ROE gate. Operational wargaming: the Wargaming subtab is in place; the Decision Support tab runs in parallel; the turn-history archive is the substrate of the AAR formaliser; the OPORD generator closes the planning loop. Illustrative scenario (Eastern Flank, Baltic Sentry, drone incursion, cable severance, suspect vessels, unmarked convoys): the default mission ships the spec's own scenario, with each of 23 beats traceable to a specific data artefact in the running SPA (checklist.md verifies items 4.1–4.23). The ten exemplar effects: seven fully delivered (5.1, 5.4, 5.5, 5.6, 5.7, 5.8, 5.10), one partially delivered (5.9, NL ready; forecasting/optimisation/perception behind the foundation-model seam), two scoped behind named seams (5.2 agent-based, 5.3 RL/probabilistic optimisation). Headline coverage stands at 73 of 74 spec compliance items (98.6%); the four foundation-model items are transparently deferred to the post-demonstration accreditation phase behind named integration seams.

NOVELTY AND COMPARISON TO STATE OF THE ART. The closest comparators fall in two categories: heavy server-side decision-support suites integrated into a parent C2 stack (the NCIA NATO Common Operational Picture client; the Maven Smart System ecosystem; national JCATS-derived simulators); and lightweight COP overlays providing situational awareness without a doctrinal decision-support core. C23 NAVINT differs from both on five specific axes.

(1) Doctrine-as-code with citable provenance. Every analytical workflow in the platform binds to a specific AJP edition. The 2nd- and 3rd-order cascade effects per CoA are not a black-box heuristic; each cascade rule is an editable record carrying its AJP citation, its operational domain and its derivation, surfaced as a column in the analyst-facing UI. State of the art is to embed doctrine in training material; C23 surfaces it at the point of analytical decision.

(2) Single-file delivery with verifiable air-gap readiness. State of the art for NATO C2 augmentations is multi-component server-side deployment with installation, accreditation and patching overhead. C23 is one HTML file, mirrorable in five megabytes, deployable in a SCIF in one cp command. The strict superset versioning rule (documented in CLAUDE.md and applied across the entire chain v001→v011, all md5-verified) guarantees that no released version regresses functionality. The offline bundle is materialised under dist/airgap/ by a stdlib-only bash script and accompanied by a CycloneDX 1.7 / ECMA-424 attestation skeleton (cdax.json) ready for organisational signature.

(3) Universal CycloneDX 1.7 / ECMA-424 envelope across every artefact. State of the art is a parallel-schema posture (separate SBOM, ML-BOM, OBOM, custom mission schemas). C23 wraps every artefact in one envelope: software (SBOM), services (SaaSBOM), cryptography (CBOM), hardware (HBOM), ML (ML-BOM), operations (OBOM), manufacturing (MBOM), vulnerability disclosure (VDR), vulnerability exploitability (VEX), aggregate vulnerabilities (BOV), attestations (CDAX), BOM-Link and CRNF — extended with operational data wrappers (MissionBOM, OOB-BOM, ACH-BOM, AIS-BOM, DoctrineBOM). One ingestion pipeline, one validator, one trust boundary.

(4) Five-level Analysis of Competing Hypotheses. Heuer's original construct is three-level (Consistent / Neutral / Inconsistent). C23 extends to five levels (Most Consistent / Consistent / Neutral / Inconsistent / Most Inconsistent at +2/+1/0/-1/-2) to expose the strength of correlation that a three-level scale collapses, materially improving rank discrimination on tightly contested CoA sets, and ships a keyword-overlap auto-scoring heuristic that preserves analyst-set values.

(5) Foundation-model-ready integration seam. State of the art either bundles a model (and inherits its accreditation overhead) or omits the model question entirely. C23 names the seams (autoSelectCoA, the live-feed adapter, the cascade-rule table, the NL terminal, the OPORD generator, the per-CoA outcome simulator) so the destination accreditation authority retains full discretion over which model lands behind them and when. The platform is doctrine-complete today and TRL-7-demonstrable today; the foundation-model substitution is a one-file change at TRL-7→TRL-8 transition.

The result is a platform that is doctrine-complete today and TRL-7-demonstrable today, on a tactical workstation, in an air-gapped SCIF, with a one-file substitution path to TRL-8 once the foundation-model authority approves the brain. No comparator product in the NATO market combines all five axes; each comparator delivers one or two at most.
```

`[10494 / 12000 chars]`

---

## Section 3: Technical Suitability (3500 chars)

```
AUGMENTATION OF AN AI-ENABLED WARFIGHTING PLATFORM. C23 NAVINT is positioned as a decision-support overlay above MSS-NATO-class C2 systems through three integration tiers. Data tier: explicit JSON schemas (C23-DIANA-MISSION/1.0, OOB/1.0, ACH/1.0, the AIS schema) wrapped in a CycloneDX 1.7 / ECMA-424 envelope using BOM-Link to associate operational artefacts (Mission, OOB, ACH, AIS, Doctrine) with software supply-chain artefacts under one ingestion pipeline. An MSS-NATO platform can subscribe to or write into these schemas without adapter glue. Workflow tier: the CoA execution path, the JPTL/RTL/NSL gating, the AJP-3.7 Personnel Recovery five-task sequence, the OPORD/FRAGO generation, the AAR formalisation and the Wargaming matchup runner are named workflow surfaces that an MSS-NATO platform can trigger or consume. Decision tier: the cascade-effects engine, Operations Assessment per LOO/LOE, anomaly-detection rule set, correlation engine and NL terminal are decision-support surfaces; autoSelectCoA() is the foundation-model seam.

TRL 7+ JUSTIFICATION. DIANA defines TRL 7 as "Prototype demonstration in operational environment". C23 NAVINT meets this on five criteria. Operationally representative scenario: the spec's own Eastern Flank/Baltic Sentry illustrative scenario is the seeded default mission (every beat 4.1–4.23 in checklist.md is verifiable in the running SPA: NATO eFP BGs in EE/LV/LT/PL, US 2ABCT, SNMG1, OPFOR forces from LMD/Kaliningrad/Belarus/Baltic Fleet, ELINT events from Murmansk-BN and Krasukha-4, AIS dark-pattern vessels DARK ECHO 1/2 targeting CUI, the suspect UAS detection at a civilian airport (i03) and its FUSION confirmation (i04 with P=0.87), the OSINT convoy reports (i05)). Operationally representative workstation: 16 GB-RAM Windows tactical laptop (and Linux equivalents), no install, no service, no telemetry, with dependency mirror under dist/airgap/vendor verifiable via DevTools "Offline". Doctrinal integration: 33 publicly-released NATO AJPs mirrored locally with per-publication summaries; cascade-effects engine carries the AJP citation per rule. Compliance posture: STANAG 4774/4778, TEMPEST SDIP-27, MIL-STD-2525B/APP-6, CycloneDX 1.7 / ECMA-424 declarations.attestations skeleton (cdax.json). Release engineering: 11 versioned files (v001–v011) preserved, md5-verifiable, governed by a strict superset rule.

THIRD-PARTY INTEGRATIONS. Six explicit surfaces. (1) JSON schemas: round-trippable, schema-detected on import, reject on shape mismatch. (2) CycloneDX 1.7 / ECMA-424 envelope (Datamodel.md): one schema for every artefact. (3) Live-feed adapter: configurable URL + interval (≥5s), tolerant of array or {intelEvents:[…]} shapes, [LIVE] log channel with explicit CORS guidance, persisted in localStorage. (4) Adversary-behaviour replay: append historical intel events with REPLAY tagging. (5) NL command terminal: extensible verb set. (6) autoSelectCoA() seam: one-file LangChain + Ollama swap-in. In progress: air-gap bundle materialised under dist/airgap/ (5.5 MB without tiles), six pinned CDN URLs sandbox-tested HTTP 200; cdax.json shipped pending organisational signature; 31 reusable Agent Skills under skills/ following the SLO Agent Skills specification.
```

`[3233 / 3500 chars]`

---

## Section 4: Defence and Security (3500 chars)

```
DEFENCE USE CASE. C23 NAVINT augments NATO ACO C2 (MSS NATO and equivalents) as a doctrine-bound decision-superiority overlay across tactical/operational/strategic echelons. The default mission embeds the operational reality of NATO's Eastern Flank: permanent forward presence under continuous grey-zone pressure, kinetic capability concentrated either side of the Suwalki Corridor and the Baltic SLOCs, constant tempo of hybrid events (cyber, EW, dark-AIS shipping, OSINT disinformation, undersea infrastructure tampering, drone incursion). An ACO analyst opening the platform sees their own theatre. The platform's value to a Joint Force Command (CJTF-BAL in the seed; parameterisable to any HQ) is the compression of the sense-decide-act cycle: multi-source feeds land in a single COP; correlation and anomaly detection surface what matters; the five-level ACH matrix ranks Courses of Action against the evidence; the Wargaming subtab pairwise-tests friendly options against every adversary option; the ROE-gated execution prevents unauthorised engagement; the kinetic per-turn movement gives the commander ground truth; the OPORD generator emits the order; the AAR formaliser closes the loop. Sub-HQ scoping (SHAPE, JFC-BAL, TCC-N, TCC-S in the seed) lets each echelon see only its AOR. For ACT, the platform is a doctrine laboratory (editable cascade rules with AJP citation; per-AJP summaries; per-CoA outcome simulator as a sandbox). For Allied nations integrating with MSS NATO, it is a portable, air-gap-capable decision-support overlay deployable on existing tactical workstations without procurement or accreditation overhead.

POTENTIAL TACTICAL/OPERATIONAL/STRATEGIC BENEFITS. Tactical: decision latency from sensor signal to ROE-authorised engagement compressed from manual workflow time-frame to seconds (multi-source fusion automatic, ACH ranking automatic, ROE gate one modal interaction); cognitive-load reduction at the commander's workstation through layer-toggle taxonomy, collapsible rail, NL terminal, keyboard shortcut set; kinetic per-turn movement on the COP closes the plan-versus-reality loop visibly. Operational: Operations Assessment per LOO/LOE per AJP-3/5 gives J3/J5 a doctrinal performance lens replacing ad-hoc spreadsheet aggregations; the OPORD/FRAGO generator emits orders in the STANAG-2014 shape expected by the JFC staff process, eliminating the parallel manual-authoring effort; the AAR formaliser closes the lessons-learned loop into a structured Markdown deliverable directly ingestible by JALLC; multi-HQ scoping gives each echelon its own AOR view. Strategic: the unified CycloneDX 1.7 / ECMA-424 attestation across software, hardware, crypto, ML, ops, manufacturing, vulnerability and operational data brings supply-chain transparency to the full decision-support stack, not just the SBOM; doctrine-as-code makes every analytical decision auditable back to its AJP, enabling responsible AI deployment in a multinational C2 environment where doctrinal divergence between nations would otherwise compound foundation-model opacity; the strict superset versioning rule produces a release chain the destination accreditation authority can rely on; foundation-model-readiness without lock-in (the destination retains full discretion over which model lands behind autoSelectCoA, when, under what regime).
```

`[3345 / 3500 chars]`

---

## Section 5: Company and Commercial (3500 chars)

```
FINANCIAL. CONFIANZA23 INTELIGENCIA Y SEGURIDAD SL — Spanish private limited company in Madrid, principal place of business in Spain (NATO nation), majority NATO-owned and controlled per T&Cs. Reference projects: Fred Olsen Express (onboard risk analysis) invoiced 2023; NAVANTIA via partner SATINEL (STRATOS Strategic Intelligence + Digital Twin 4.D XBOM + NAVINT Maritime Security) forecast 2026Q2; Suez Canal Authority via CDTI/Digital Fortress (NAVINT Maritime Security) forecast 2026Q4. Three-year NAVINT plan (EUR): 2027 rev 3.42M / EBITDA 1.62M (47.3%); 2028 5.98M / 2.28M (38%); 2029 11.88M / 4.90M (41.2%); avg ~42% margin. Investment round closing 2026-Q4: EUR 1M for 25% equity (pre-money 3M); use of funds 60% sales/marketing, 30% product, 10% ops incl. ISO 27001 / ENS / IEC 62443. DIANA EUR 100k would fund the cloud demo environment; CONFIANZA23 runway is independent of it.

TEAM, RISKS, DELIVERY. Rafael Ausejo Prieto (CEO/Founder, >32 yrs — NATO, ALSTOM, S21Sec/Thales, BeDisruptive, A3Sec, 4iQ, VASS, Entelgy, Oesía, ANADAT/Babel); Pedro Gallego Torrecilla (CTO/AI Director, >25 yrs — Sidertia Izertis, INGECOM, CMD, Factum-to-Santander); Daniel Martín Moreno (BD + Marina Mercante advisor, >30 yrs — Ministerio de Transporte, Secuware). Advisory board: DGAM, Armada Española, NATO, retired General officer (joining shortly). Certifications: ISO 27001 Lead Auditor, CISM, CISA, CISSP, ISA Senior Member, Stormshield CSNOT, Tenable TCSE-OT/TCSA-OT, Kaspersky. Risks. R1 foundation-model accreditation lag: v011 fully functional without it; demo runs on seeded heuristic and swaps to the authority-approved model when accreditation lands. R2 cloud-demo friction (CORS/auth/policy): live-feed adapter is a generic poller; air-gap bundle is the contingency. R3 AJP edition evolution: doctrine-as-code (cascade rules with AJP citation, per-AJP summaries, update_ajp_doctrines.py synchroniser) makes migration mechanical. R4 multinational iteration: Mission Editor CRUDs every parameter, JSON I/O round-trippable, multi-mission slots for side-by-side comparison. Delivery posture for follow-on NATO contracts: superset versioning + 11-version chain demonstrate discipline; single-file delivery eliminates installation/accreditation/patching overhead; CycloneDX attestation chain ensures supply-chain transparency; air-gap runtime supports SCIF deployment. Sales channels: Satinel, Digital Fortress, BABEL, TRC; in conversations with Oesía and VASS.

MARKETS, PLAN. TAM US$ 1,375M (global MDA 2025), CAGR 9.6% to US$ 2,589M by 2032 (Global MDA Solution Market Insights & Forecast to 2032). SAM US$ 206M (Spain+EU+Mediterranean). SOM ~EUR 8M (4.17% of SAM, NAVINT year-3). Defence: NATO entities (ACO/SHAPE/JFC/TCC, ACT, NCIA); Allied nations integrating with NATO C2 (FR SCORPION, DE HERAKLES, UK MORPHEUS, ES BMS); exercises (BALTOPS, STEADFAST DEFENDER); primes (Lockheed/Maven, Thales, Leonardo, IBM/NCIA). Civilian: critical-infrastructure (NIS2/IEC 62443/MARSEC); maritime industry (insurers, flag states, port authorities — dark-AIS+AJP-3.1 as MDA product); crisis response (OCHA/ICRC/EU Civil Protection). Customer mix: 60% Government (Navantia, Puertos del Estado, MinDef), 30% Civil B2B (Marina Mercante, fishing), 10% premium yachts. Pricing: Community free on GitHub; Small Business EUR 1k/mo; Enterprise EUR 5k/mo; Government EUR 15k–1.5M. GTM: 2026 visibility (SEO/LinkedIn), 2027 lead-gen (webinars, lead magnets), 2028 conversion, then scale.
```

`[3469 / 3500 chars]`

---

# AGREEMENT CHECKBOXES

Tick all four. The text is informational only; nothing to write.

- Agreement to T&Cs
- Confirmation of company identity
- Personnel Agreement
- Information Sharing — Bidder Identity (default opt-in unless you have a reason to opt out)
- Information Sharing — Bidder Documentation (default opt-in unless you have a reason to opt out)

---

# IMAGES (form's two Short-Form and three Long-Form image slots)

DIANA forbids narrative text inside the images — only labels. Suggested captures from the v011 SPA:

Short-Form image slots (max 2):
1. Top-bar + COP + left rail + dossier, with the default Baltic Sentry mission running, all overlays on (NATO/OPFOR/NEUTRAL/A2-AD/CUI/AIS/Movement/JPTL/IPs). Labels only: "MULTI-DOMAIN COP", "MISSION EDITOR (21 TABS)", "ROE-GATED CoA", "KINETIC PER-TURN".
2. WARGAMING tab matchup matrix, NATO×OPFOR pairwise, colour-coded. Label: "DETERMINISTIC PAIRWISE WARGAMING".

Long-Form image slots (max 3):
1. JOINT TARGETING tab + RoEModal open, showing JPTL with HVT/HPT/TST + RTL/NSL + CDE. Labels: "AJP-3.9 JTC", "ROE GATE".
2. ANALYTICS tab + CASCADE RULES editor open, showing the AJP-cited rule table. Labels: "AJP-CITED CASCADES", "CORRELATION", "OPS ASSESSMENT MoP/MoE per LOO".
3. Architecture diagram (one figure, no narrative text) showing the integration tiers (data → workflow → decision), CycloneDX envelope wrapping Mission/OOB/ACH/AIS/Doctrine, live-feed adapter inbound, OPORD/AAR/Wargaming outbound, foundation-model seam labelled. Labels: "C23 NAVINT INTEGRATION TIERS".

---

# CHECKLIST BEFORE SUBMISSION

- [ ] Replace every `[BRACKETED PLACEHOLDER]` in Section 5 with the actual figures.
- [ ] Confirm CONFIANZA23's principal place of business and ownership composition match the T&Cs.
- [ ] Capture the five images per the suggestions above; verify no narrative text inside.
- [ ] Optionally produce the supplementary video (max 4 minutes, .mp4, ≤ 100 MB) as a screen capture of the running v011 SPA with audio commentary in English; subtitles recommended.
- [ ] Verify the proposal title fits the form's character limit.
- [ ] Submit before the deadline; resubmission is allowed up until the submission window closes per the FAQ.
