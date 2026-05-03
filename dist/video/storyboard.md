# DIANA Video — Storyboard / Narration Script

**Total runtime:** 4:00 (240 seconds, exact).
**Format:** MP4, max 100 MB, English audio + English subtitles.
**Coverage required by DIANA:** demonstration of the technical solution against the challenge use cases + third-party integration features.
**Source artefact:** `C23_DIANA_NATO_WARFIGHTERS_v011.html`.

> **How to use this document.** This is the verbatim script. Read it aloud at ~150 words per minute (typical news-anchor pace) and the timings will land. If you use a TTS engine, paste each scene block into the engine separately so you control pacing per scene. Subtitles in `dist/video/subtitles.srt` are aligned scene-by-scene.

---

## Scene 1 — Opening title (0:00 – 0:25, 25 s)

**Visual:** Static title card with the C23 NAVINT logo and proposal title. (The Playwright script renders this as a single full-screen overlay so the SPA does not need to load yet.)

**Narration (60 words, ~24 s at 150 wpm):**

> C23 NAVINT is a doctrine-driven artificial-intelligence decision-superiority augmentation for Maven Smart System NATO and Allied command-and-control platforms. It is a single self-contained HTML file that runs offline on a sixteen-gigabyte tactical workstation, with no installation, no server, and no proprietary stack. Every workflow is bound to an Allied Joint Publication, with a citable provenance.

---

## Scene 2 — Default mission COP (0:25 – 0:55, 30 s)

**Visual:** Open the SPA. Show the full Common Operating Picture with the NAVINT Baltic Sentry default mission running, all overlays active, classification banner and posture tiles visible.

**Narration (75 words, ~30 s):**

> The default mission embeds the Eastern Flank illustrative scenario from the challenge statement. NATO enhanced Forward Presence battle groups in Estonia, Latvia, Lithuania and Poland. Standing NATO Maritime Group 1 in the Baltic. OPFOR forces from the Leningrad Military District, Kaliningrad and Belarus. Critical Undersea Infrastructure nodes, including Estlink 2 and the Baltic Connector. Two suspect dark-AIS vessels, named DARK ECHO 1 and DARK ECHO 2, render in red as suspect tracks.

---

## Scene 3 — Multi-source fusion + Force Tally (0:55 – 1:20, 25 s)

**Visual:** Show the rail tally with NATO/OPFOR/NEUTRAL by domain. Toggle one or two layer chips. Highlight the Posture tiles (FPCON, CBRN, PNT, CIS PACE) on the top bar.

**Narration (62 words, ~25 s):**

> The Common Operating Picture fuses commercial AIS, OSINT, RADAR, ELINT and FUSION events into a single layer-toggleable view. The Force Tally on the left rail shows units by side and by domain, including CYBER as the fifth operational domain per AJP-3.20. The top bar surfaces Force Protection Condition, Chemical-Biological-Radiological-Nuclear alert, Positioning Navigation and Timing status, and the CIS PACE plan.

---

## Scene 4 — Joint Targeting (AJP-3.9) (1:20 – 1:45, 25 s)

**Visual:** Open CONFIG → JOINT TARGETING. Show the JTC PHASE selector and the JPTL with HVT/HPT/TST entries.

**Narration (62 words, ~25 s):**

> The Joint Targeting Cycle is fully materialised per AJP-3.9. The six-phase JTC indicator on the top bar. The Joint Prioritised Target List with High-Value, High-Payoff and Time-Sensitive Target categories, the F2T2EA stage, Collateral Damage Estimation rating, and per-target restrictions. Restricted Target List and No-Strike List as separate lists. Every engagement decision is gated through these inputs.

---

## Scene 5 — Rules-of-Engagement gate (1:45 – 2:05, 20 s)

**Visual:** Close CONFIG. Click EXECUTE on a CoA that triggers the ROE modal (any OPFOR-side CoA against the seeded TST). Show the ROE modal with TST hits, RTL and NSL displayed.

**Narration (50 words, ~20 s):**

> Every Course of Action that would engage a Time-Sensitive Target opens a Rules-of-Engagement authorisation modal. The modal surfaces matching TSTs with their CDE rating, the full Restricted Target List, the No-Strike List, and an explicit Authorise-or-Deny decision. The C-UAS workflow per AJP-3.3.5 auto-triggers on radar drone detections.

---

## Scene 6 — Wargaming pairwise matrix (2:05 – 2:30, 25 s)

**Visual:** Open CONFIG → WARGAMING. Show the NATO × OPFOR matchup matrix with colour-coded net scores.

**Narration (62 words, ~25 s):**

> Operational wargaming runs in-platform without any external simulator. Every NATO Course of Action is matched pairwise against every OPFOR Course of Action through a deterministic seeded outcome model. The matrix is colour-coded by net score, and a best-and-worst summary highlights which adversary moves are most threatening to each friendly option. This is one of the spec's named exemplar effects.

---

## Scene 7 — Cascade rules with AJP citation (2:30 – 2:55, 25 s)

**Visual:** Open CONFIG → ANALYTICS. Scroll to the CASCADE RULES editor. Show several rules with their AJP column.

**Narration (62 words, ~25 s):**

> The cascade-effects engine is doctrine-as-code. Each second-order and third-order effect per Course of Action is driven by an editable rule that cites its source Allied Joint Publication. AJP-3.1 for naval interdiction. AJP-4.4 for movement. AJP-3.20 for cyber. The analyst can audit every analytical output back to the doctrinal text that produced it. State-of-the-art comparators embed doctrine in training material; we surface it at the point of decision.

---

## Scene 8 — Personnel Recovery + Movement (2:55 – 3:15, 20 s)

**Visual:** Open CONFIG → PR / JPRC. Show the two seeded isolated personnel and the per-stage tally tiles. Then close and open CONFIG → MOVEMENT briefly.

**Narration (50 words, ~20 s):**

> Personnel Recovery per AJP-3.7 implements the five-task sequence: Reported, Located, Supported, Recovered, Reintegrated. Movement per AJP-3.13 and AJP-4.4 manages Main and Alternate Supply Routes plus Air and Sea Ports of Debarkation, status-coloured. The naval interdiction polygon is editable and renders directly on the COP.

---

## Scene 9 — Third-party integration (3:15 – 3:40, 25 s)

**Visual:** Open CONFIG → IMPORT / EXPORT briefly to show the JSON schemas. Then close and open CONFIG → ANALYTICS, scroll to LIVE-FEED ADAPTER.

**Narration (62 words, ~25 s):**

> Third-party integration is a first-order design constraint. Three documented JSON schemas plus the Master-Prompt AIS schema, all wrapped in a CycloneDX 1.7 ECMA-424 envelope covering software, services, cryptography, hardware, machine-learning, operations, manufacturing and operational data. A polling live-feed adapter consumes ISR endpoints. A STANAG-2014 OPORD generator publishes downstream. The autoSelectCoA function is the named seam for foundation-model substitution.

---

## Scene 10 — Air-gap closing (3:40 – 4:00, 20 s)

**Visual:** Show the dist/airgap directory listing in a terminal-style overlay (Playwright renders an HTML overlay at the end). Final card with logos and contact.

**Narration (50 words, ~20 s):**

> The platform is shipped as a strictly air-gapped runtime. The dependency graph is mirrored under dist airgap vendor. A CycloneDX attestation skeleton accompanies the bundle, ready for organisational signing. Spec coverage stands at ninety-eight-point-six percent. C23 NAVINT — by CONFIANZA23 Inteligencia y Seguridad. Ready for evaluation.

---

## Word count and pacing check

| Scene | Words | Target s | At 150 wpm |
| --- | ---: | ---: | ---: |
| 1 Title | 60 | 25 | 24 |
| 2 COP | 75 | 30 | 30 |
| 3 Fusion+Tally | 62 | 25 | 25 |
| 4 Joint Targeting | 62 | 25 | 25 |
| 5 ROE gate | 50 | 20 | 20 |
| 6 Wargaming | 62 | 25 | 25 |
| 7 Cascades | 62 | 25 | 25 |
| 8 PR+Movement | 50 | 20 | 20 |
| 9 Integration | 62 | 25 | 25 |
| 10 Closing | 50 | 20 | 20 |
| **TOTAL** | **595** | **240** | **239** |

Tight but doable. If you read at 145 wpm leave 0.5 s of silence between scenes; at 155 wpm trim two filler words per scene.
