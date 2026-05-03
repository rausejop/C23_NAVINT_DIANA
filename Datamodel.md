# Datamodel.md — C23 DIANA NATO Warfighters

**Unified data model based on the CycloneDX BOM JSON 1.7 specification, acting as a single ECMA-424 Bill-of-Materials envelope across Software, SaaS, Cryptography, Hardware, ML, Operations, Manufacturing, Vulnerability Disclosure, Vulnerability Exploitability, Bill of Vulnerabilities, Cyclone Attestations, BOM-Link and Common Release Notes.**

- **Reference specification:** <https://cyclonedx.org/docs/1.7/json/>
- **Standard alignment:** ECMA-424 (CycloneDX as ratified by Ecma International).
- **Schema id (this document):** `C23-DIANA-DATAMODEL/1.0`
- **Date:** 2026-05-02
- **Author:** CONFIANZA23

---

## 1. Design intent

The C23 platform must remain interpretable across every NATO BOM domain (software supply chain, hardware, cryptographic posture, ML provenance, operational tasking, manufacturing, vulnerability state) without introducing parallel schemas. CycloneDX 1.7 is the only specification today that natively unifies all of those concerns under one envelope and one set of identifiers (`bom-ref`, `purl`, `cpe`, `swid`, `omniborid`), and that is recognised by an ECMA standard (ECMA-424). The model below uses the CycloneDX root document as the **single envelope** and discriminates between BOM types by the value of `metadata.bomFormat` (always `"CycloneDX"`) plus the contents of `metadata.lifecycles[*].name` and the component types populated under `components[*].type`.

For the C23 platform specifically, the same envelope is also used to wrap mission, OOB, ACH, AIS and doctrine metadata as **CycloneDX `formulation` and `components.type=data`** entries, so that the Single Page Application stays auditable as a self-describing artefact (an "Operational BOM").

---

## 2. Root envelope (common to every BOM type)

```jsonc
{
  "$schema": "http://cyclonedx.org/schema/bom-1.7.schema.json",
  "bomFormat": "CycloneDX",
  "specVersion": "1.7",
  "serialNumber": "urn:uuid:00000000-0000-0000-0000-000000000000",
  "version": 1,
  "metadata": {
    "timestamp": "2026-05-02T00:00:00Z",
    "lifecycles": [
      { "name": "operations" }                // see §3 for allowed values per BOM type
    ],
    "tools": {
      "components": [
        { "type": "application", "name": "C23 DIANA NATO Warfighters", "version": "1.0.0",
          "publisher": "CONFIANZA23",
          "externalReferences": [
            { "type": "website", "url": "https://www.diana.nato.int" }
          ] }
      ]
    },
    "authors": [{ "name": "CONFIANZA23 / NAVINT Baltic Sentry" }],
    "manufacturer": { "name": "CONFIANZA23" },
    "supplier":     { "name": "DIANA / Allied Command Operations" },
    "licenses": [{ "license": { "id": "Apache-2.0" } }],
    "properties": [
      { "name": "nato:classification", "value": "UNCLASSIFIED // FOFO — TRAINING/WARGAME" },
      { "name": "nato:stanag",         "value": "4774;4778" },
      { "name": "nato:tempest",        "value": "SDIP-27 Level B" },
      { "name": "diana:trl",           "value": "7" },
      { "name": "c23:bomKind",         "value": "SBOM"           // see §3
      }
    ]
  },

  "components":      [ /* §4 */ ],
  "services":        [ /* §5 — populated for SaaSBOM */ ],
  "dependencies":    [ /* §6 */ ],
  "compositions":    [ /* §7 */ ],
  "vulnerabilities": [ /* §8 — VDR / VEX / BOV */ ],
  "annotations":     [ /* §9 */ ],
  "formulation":     [ /* §10 — ML-BOM training, Ops tasks, Manufacturing routings */ ],
  "declarations":    { /* §11 — CDAX attestations */ },
  "definitions":     { /* §12 — standards / cryptography reference data */ },
  "externalReferences": [ /* BOM-Link, CRNF, evidence */ ]
}
```

Every BOM type below is the same envelope with a discriminating `c23:bomKind` and a corresponding `lifecycles[*].name`. This is what lets a single ingestion pipeline parse everything.

---

## 3. BOM type discriminators

| BOM kind     | `c23:bomKind` value | `lifecycles[*].name`            | Mandatory population                                                                          |
| ------------ | ------------------- | ------------------------------- | --------------------------------------------------------------------------------------------- |
| **SBOM**     | `SBOM`              | `build`, `pre-build`            | `components[*].type ∈ {library, framework, application, file, container, operating-system}` plus `dependencies` |
| **SaaSBOM**  | `SaaSBOM`           | `operations`                    | `services[*]` with `endpoints`, `authenticated`, `data`, `trustZone`, plus `dependencies` between services and components |
| **CBOM**     | `CBOM`              | `design`, `operations`          | `components[*].type = cryptographic-asset` with `cryptoProperties` (assetType, algorithmProperties, certificateProperties, relatedCryptoMaterialProperties, protocolProperties) |
| **HBOM**     | `HBOM`              | `design`, `manufacture`         | `components[*].type ∈ {device, hardware, firmware, machine-learning-model}` with `manufacturer`, `modelCard`, `cpe` |
| **ML-BOM**   | `ML-BOM`            | `design`, `pre-build`, `build`  | `components[*].type = machine-learning-model` with full `modelCard` (modelParameters, quantitativeAnalysis, considerations, properties) plus training-data lineage in `formulation` |
| **OBOM**     | `OBOM`              | `operations`                    | `formulation[*].workflows[*]` with operational tasks, plus `services[*]` for the runtime environment |
| **MBOM**     | `MBOM`              | `manufacture`                   | `formulation[*].workflows[*]` describing manufacturing routings; `components[*].type ∈ {device, machine-learning-model, file}` for produced artefacts and their provenance |
| **VDR**      | `VDR`               | `operations`                    | `vulnerabilities[*]` with full `affects`, `ratings`, `advisories`, `published`, `updated` |
| **VEX**      | `VEX`               | `operations`                    | `vulnerabilities[*]` with `analysis.state ∈ {resolved, exploitable, in_triage, false_positive, not_affected}` and `analysis.justification` |
| **BOV**      | `BOV`               | `operations`                    | `vulnerabilities[*]` aggregated across one or more BOMs (broader scope than a single VDR) |
| **CDAX**     | `CDAX`              | `operations`                    | `declarations.attestations[*]` referencing `assessors`, `claims`, `evidence`, `signature` |
| **BOM-Link** | `BOM-Link`          | (any)                           | `externalReferences[*].type = "bom"` carrying URN of form `urn:cdx:<serial>/<version>#<bom-ref>` |
| **CRNF**    | `CRNF`              | `operations`                    | `externalReferences[*].type = "release-notes"` plus `properties` of form `crnf:*` |

> **C23 extensions** (operational data wrapped as a BOM): `c23:bomKind ∈ {MissionBOM, OOB-BOM, ACH-BOM, AIS-BOM, DoctrineBOM}`. These reuse `components[*].type = "data"` and `formulation[*].workflows[*]` and are described in §13.

---

## 4. `components[*]` — the universal item

Every artefact is a `component`. CycloneDX 1.7 reserves the following `type` values, all of which are used somewhere in the C23 envelope:

```
application | framework | library | container | platform | operating-system |
device | device-driver | firmware | file |
machine-learning-model | data | cryptographic-asset
```

Universal fields used across BOM kinds:

```jsonc
{
  "bom-ref": "pkg:npm/react@18.3.1",          // stable internal reference
  "type":    "library",
  "group":   "facebook",
  "name":    "react",
  "version": "18.3.1",
  "scope":   "required",                       // required | optional | excluded
  "purl":    "pkg:npm/react@18.3.1",
  "cpe":     "cpe:2.3:a:facebook:react:18.3.1:*:*:*:*:*:*:*",
  "swid":    { "tagId": "react-18.3.1", "name": "React" },
  "omniborid":"gitoid:blob:sha1:e1bc...",
  "supplier":     { "name": "Meta Platforms" },
  "manufacturer": { "name": "Meta Platforms" },
  "licenses": [{ "license": { "id": "MIT" } }],
  "hashes":   [{ "alg": "SHA-256", "content": "…" }],
  "evidence": { "identity": [ /* §11.1 */ ], "occurrences": [ … ], "callstack": { … } },
  "externalReferences": [
    { "type": "vcs", "url": "https://github.com/facebook/react" },
    { "type": "release-notes", "url": "https://github.com/facebook/react/releases/tag/v18.3.1" }
  ],
  "properties": [
    { "name": "c23:airgap:bundled", "value": "true" }
  ]
}
```

### 4.1 Cryptographic asset (CBOM)
`type: "cryptographic-asset"` with `cryptoProperties` covering `assetType ∈ {algorithm, certificate, protocol, related-crypto-material}` and the appropriate sub-objects (`algorithmProperties.primitive`, `parameterSetIdentifier`, `nistQuantumSecurityLevel`, `executionEnvironment`, `certificateProperties.subjectName`, `protocolProperties.tlsCipherSuites`, etc.).

### 4.2 Machine-learning model (ML-BOM / HBOM)
`type: "machine-learning-model"` with `modelCard`:

```jsonc
"modelCard": {
  "modelParameters": {
    "approach": { "type": "supervised" },
    "task": "course-of-action-recommendation",
    "architectureFamily": "transformer",
    "modelArchitecture": "Llama-3.1-70B-fine-tuned",
    "datasets":  [ { "ref": "training-corpus-mil-strategy" } ],
    "inputs":    [ { "format": "text/plain" } ],
    "outputs":   [ { "format": "application/json" } ]
  },
  "quantitativeAnalysis": { "performanceMetrics": [
    { "type": "rouge-L", "value": "0.42" },
    { "type": "bleu",    "value": "0.31" }
  ] },
  "considerations": {
    "ethicalConsiderations": [ { "name": "bias", "description": "…" } ],
    "useCases":              [ { "name": "wargaming",     "description": "…" } ],
    "useRestrictions":       [ "no-targeting-of-civilians" ]
  },
  "properties": [
    { "name": "c23:trl",         "value": "6" },
    { "name": "c23:airgap:onnx", "value": "true" }
  ]
}
```

### 4.3 Hardware component (HBOM)
`type: "device" | "hardware" | "firmware"` with `manufacturer`, `modelCard` (for an ML accelerator), `cpe` (when applicable), `properties` for `c23:tempest:rating`, `c23:formfactor`, `c23:powerW`.

### 4.4 Data wrapper (Mission/OOB/ACH/AIS/Doctrine — see §13)
`type: "data"` with `description`, `data[*]`:

```jsonc
{
  "type": "data", "bom-ref": "data/mission/c23",
  "name": "C23 Mission · NAVINT Baltic Sentry",
  "data": [{
    "name": "mission.json",
    "contents": { "attachment": { "contentType": "application/json", "encoding": "base64", "content": "…" } },
    "classification": "UNCLASSIFIED // FOFO",
    "sensitiveData": ["operational"]
  }]
}
```

---

## 5. `services[*]` — SaaSBOM core

```jsonc
{
  "bom-ref": "svc/cop-tile-server",
  "provider":  { "name": "Local mirror" },
  "group":     "c23.platform",
  "name":      "cop-tile-server",
  "version":   "1.0.0",
  "endpoints": [ "https://tiles.local/{z}/{x}/{y}.png" ],
  "authenticated": true,
  "x-trust-boundary": true,
  "trustZone": "RESTRICTED",
  "data": [ { "flow": "inbound|outbound|bi-directional", "classification": "UNCLASSIFIED",
              "name": "Map tiles", "description": "Carto Voyager mirror" } ],
  "licenses": [{ "license": { "id": "ODbL-1.0" } }],
  "externalReferences": [{ "type": "documentation", "url": "https://carto.com/help/" }]
}
```

---

## 6. `dependencies[*]` — universal graph

```jsonc
{ "ref": "pkg:npm/react@18.3.1", "dependsOn": ["pkg:npm/scheduler@0.23.0"] }
```

Used across SBOM, SaaSBOM, OBOM, MBOM and CBOM (where it expresses cryptographic protocol → algorithm → primitive chains).

---

## 7. `compositions[*]` — assertion of completeness

```jsonc
{
  "aggregate": "complete | incomplete | incomplete_first_party_only | unknown",
  "assemblies":   ["urn:cdx:.../#root-assembly"],
  "dependencies": ["pkg:npm/react@18.3.1"],
  "vulnerabilities": ["CVE-2025-12345"]
}
```

Used in **VDR** and **BOV** to declare scope, and in **MBOM** to mark whether a manufacturing routing is fully specified.

---

## 8. `vulnerabilities[*]` — VDR / VEX / BOV

```jsonc
{
  "bom-ref": "vuln/CVE-2025-12345",
  "id":      "CVE-2025-12345",
  "source":  { "name": "NVD", "url": "https://nvd.nist.gov/vuln/detail/CVE-2025-12345" },
  "ratings": [
    { "source": { "name": "NVD" }, "score": 9.1, "severity": "critical",
      "method": "CVSSv4", "vector": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N" }
  ],
  "cwes": [79],
  "description": "Improper neutralisation of input during web-page generation.",
  "advisories":  [ { "title": "Vendor advisory", "url": "https://example.org/adv" } ],
  "published": "2026-04-15T00:00:00Z",
  "updated":   "2026-04-30T00:00:00Z",
  "credits":   { "individuals": [{ "name": "researcher" }] },
  "tools":     { "components": [{ "type": "application", "name": "trivy", "version": "0.55" }] },
  "affects":   [ { "ref": "pkg:npm/react@18.3.1",
                   "versions": [{ "version": "18.3.1", "status": "affected" }] } ],
  "analysis":  {                                  // populated for VEX
    "state":         "not_affected",              // resolved | exploitable | in_triage | false_positive | not_affected
    "justification": "code_not_reachable",
    "response":      ["will_not_fix"],
    "detail":        "Function never invoked in air-gapped build path."
  },
  "rejected": false,
  "workaround": "—"
}
```

- **VDR** = full descriptive disclosure (omit `analysis`).
- **VEX** = decision overlay (must include `analysis.state` + `justification`).
- **BOV** = an aggregate envelope; multiple `vulnerabilities[*]` referencing many `affects[*].ref` from many BOMs. The envelope's `compositions[*].aggregate` must be set.

---

## 9. `annotations[*]` — analyst notes

```jsonc
{
  "bom-ref": "ann/coa-c4-warning",
  "subjects": ["data/coa/c4"],
  "annotator": { "individual": { "name": "JFC Brunssum analyst", "email": "n/a" } },
  "timestamp": "2026-05-02T05:11:00Z",
  "text": "OPFOR Suwalki Pincer is the highest-scoring CoA per ACH; recommend pre-positioning 18th Iron Div."
}
```

---

## 10. `formulation[*]` — workflows for ML-BOM, OBOM, MBOM

```jsonc
{
  "bom-ref": "form/op-baltic-sentry",
  "components":  [ /* assets produced by the workflow */ ],
  "services":    [ /* services exercised by the workflow */ ],
  "workflows": [
    {
      "bom-ref": "wf/ach-decision",
      "uid":     "wf-001",
      "name":    "ACH-driven CoA decision",
      "description": "Score evidence against CoAs; rank; emit recommendation.",
      "resourceReferences": [ { "ref": "data/ach/matrix" } ],
      "steps": [
        { "name": "ingest-events", "description": "Pull intel + geopolitical events",
          "commands": [{ "executed": "GET /events" }] },
        { "name": "score-coas",    "description": "Apply ACH scoring",
          "commands": [{ "executed": "POST /ach/score" }] },
        { "name": "recommend",     "description": "Pick top CoA per side",
          "outputs": [{ "type": "artifact", "resource": { "ref": "data/coa/recommendation" } }] }
      ],
      "trigger": { "type": "scheduled", "event": { "uid": "phase-transition" } }
    }
  ]
}
```

---

## 11. `declarations` — CDAX attestations

```jsonc
"declarations": {
  "assessors":   [ { "bom-ref": "assr/diana", "thirdParty": false,
                     "organization": { "name": "DIANA Programme Office" } } ],
  "attestations":[ { "bom-ref": "att/airgap-readiness",
                     "summary": "All third-party assets are mirrored locally.",
                     "assessor": "assr/diana",
                     "map": [
                       { "requirement": "req/airgap",
                         "claims":     ["claim/no-internet"],
                         "counterClaims":[],
                         "conformance": { "score": 1.0, "rationale": "Verified by build inspection" } }
                     ],
                     "signature": { "algorithm": "Ed25519", "publicKey": { "crv": "Ed25519", "kty": "OKP" }, "value": "…" } } ],
  "claims":       [ { "bom-ref": "claim/no-internet", "target": "tools/c23",
                      "predicate": "no_outbound_traffic_at_runtime", "mitigationStrategies": ["mit/local-mirror"] } ],
  "evidence":     [ { "bom-ref": "ev/build-log", "propertyName": "build:network", "description": "Build run with --offline; no DNS resolution observed." } ],
  "targets":      { "organizations": [], "components": ["tools/c23"], "services": [] },
  "affirmation":  { "statement": "We affirm the above attestations.", "signatories":[ { "name":"CONFIANZA23 CTO" } ] },
  "signature":    { /* envelope signature */ }
}
```

---

## 12. `definitions` — standards & references

```jsonc
"definitions": {
  "standards": [
    { "bom-ref": "std/stanag-4774", "name": "STANAG 4774", "version": "Ed.1",
      "owner": "NATO", "description": "Confidentiality Metadata Label Syntax",
      "externalReferences": [{ "type": "specification", "url": "https://nso.nato.int/" }] },
    { "bom-ref": "std/ajp-3.9",     "name": "AJP-3.9 Joint Targeting", "version": "Edition B v1",
      "owner": "NSO" },
    { "bom-ref": "std/cyclonedx",   "name": "CycloneDX",     "version": "1.7", "owner": "Ecma" },
    { "bom-ref": "std/ecma-424",    "name": "ECMA-424",      "version": "1st",  "owner": "Ecma" }
  ]
}
```

---

## 13. C23 operational data as a BOM (Mission/OOB/ACH/AIS/Doctrine)

The DIANA platform stores operational artefacts inside the same CycloneDX envelope by populating `components[*].type = "data"` (for the artefact itself) and `formulation[*]` (for the workflows that consume it). This means `import → validate → ship` works for all artefacts with one schema.

### 13.1 Mission (`c23:bomKind = "MissionBOM"`)

The C23 in-app schema `C23-DIANA-MISSION/1.0` maps onto:

```jsonc
{
  "type": "data",
  "bom-ref": "data/mission/baltic-sentry",
  "name":    "C23 Mission · NAVINT Baltic Sentry",
  "data": [{ "name": "mission.json", "classification": "UNCLASSIFIED",
             "contents": { "attachment": { "contentType": "application/json",
                                            "encoding": "base64", "content": "…" } } }],
  "properties": [
    { "name": "c23:mission:name",       "value": "NAVINT Baltic Sentry" },
    { "name": "c23:mission:dStart",     "value": "2026-05-02T00:00:00Z" },
    { "name": "c23:mission:phaseCount", "value": "4" }
  ]
}
```

### 13.2 OOB (`c23:bomKind = "OOB-BOM"`)

Each unit becomes one `data` component with `properties[*]` carrying SIDC, side, domain, designation, type, equipment, mission, status, lat/lng, echelon, readiness — i.e. exactly the in-app schema.

### 13.3 ACH (`c23:bomKind = "ACH-BOM"`)

Two arrays:
- One `data` component per CoA (`properties: c23:ach:side, c23:ach:weight`).
- One `data` component per Evidence (`properties: c23:ach:phase, c23:ach:dtg, c23:ach:source`).
- Scoring stored in a `formulation[*].workflows[*].steps[*].outputs[*]` pointing at `data/ach/score-{eid}-{coaId}` with property `c23:ach:value ∈ {C, N, I}`.

### 13.4 AIS (`c23:bomKind = "AIS-BOM"`)

The Master-Prompt ANNEX AIS schema maps 1:1 onto a `data` component per vessel; properties prefixed `c23:ais:*` carry the original AIS field names (MMSI, IMO, FLAG, LAT, LON, …). The `metadata.lifecycles[*].name = "operations"` and `c23:bomKind = "AIS-BOM"`.

### 13.5 Doctrine (`c23:bomKind = "DoctrineBOM"`)

Each AJP publication is a `data` component referencing the local PDF file by hash:

```jsonc
{
  "type": "data", "bom-ref": "data/ajp/ajp-3.9-edB-v1",
  "name": "AJP-3.9 Allied Joint Doctrine for Joint Targeting (Ed B v1)",
  "supplier": { "name": "NATO Standardization Office" },
  "hashes":   [ { "alg": "SHA-256", "content": "…" } ],
  "externalReferences": [
    { "type": "documentation", "url": "file://AJP/08%20Allied%20Joint%20Doctrine%20for%20Joint%20Targeting%20(AJP-3.9)/AJP-3.9_EDB_V1_E.pdf" }
  ],
  "properties": [
    { "name": "c23:doctrine:edition",   "value": "B" },
    { "name": "c23:doctrine:version",   "value": "1" },
    { "name": "c23:doctrine:publisher", "value": "NSO" }
  ]
}
```

---

## 14. BOM-Link

CycloneDX 1.7 BOM-Link allows one BOM to reference another by its serial-number URN. C23 uses BOM-Link to attach an OOB-BOM, an ACH-BOM, an AIS-BOM and a DoctrineBOM to one parent MissionBOM:

```jsonc
"externalReferences": [
  { "type": "bom", "url": "urn:cdx:00000000-0000-0000-0000-0000000000aa/1#data/mission/baltic-sentry",
    "comment": "Linked Mission BOM" },
  { "type": "bom", "url": "urn:cdx:00000000-0000-0000-0000-0000000000bb/1",
    "comment": "Linked OOB BOM" },
  { "type": "bom", "url": "urn:cdx:00000000-0000-0000-0000-0000000000cc/1",
    "comment": "Linked ACH BOM" },
  { "type": "bom", "url": "urn:cdx:00000000-0000-0000-0000-0000000000dd/1",
    "comment": "Linked AIS BOM" },
  { "type": "bom", "url": "urn:cdx:00000000-0000-0000-0000-0000000000ee/1",
    "comment": "Linked Doctrine BOM" }
]
```

---

## 15. Common Release Notes Format (CRNF)

CRNF entries are external references plus a structured `properties` block:

```jsonc
"externalReferences": [
  { "type": "release-notes",
    "url":  "file://RELEASES/c23-1.0.0.md",
    "comment": "C23 platform v1.0.0 release notes",
    "hashes": [{ "alg": "SHA-256", "content": "…" }] }
],
"properties": [
  { "name": "crnf:title",         "value": "C23 DIANA NATO Warfighters 1.0.0" },
  { "name": "crnf:date",          "value": "2026-05-02" },
  { "name": "crnf:tag",           "value": "v1.0.0" },
  { "name": "crnf:type",          "value": "feature" },
  { "name": "crnf:resolves",      "value": "DIANA-2026-DS-001" },
  { "name": "crnf:notes",         "value": "Initial public release." }
]
```

---

## 16. Validation pipeline

| Stage          | Tool                                | Notes                                                   |
| -------------- | ----------------------------------- | ------------------------------------------------------- |
| Schema         | CycloneDX JSON Schema 1.7           | Mandatory before any ingestion.                         |
| Normalisation  | TypeScript / Zod (`strict: true`)   | Mirrors §3 discriminator rules.                         |
| Cross-link     | bom-link resolver                   | Resolves URN BOM-Links against local mirror.            |
| Crypto         | CBOM analyser                       | Flags non-NIST-PQC primitives (per NATO CBOM guidance). |
| Vex application| `cyclonedx vex apply`               | Applies VEX over a VDR or BOV.                         |
| Attestation    | CDAX verifier                       | Verifies signatures, counter-claims and conformance.    |
| Air-gap check  | Custom (C23 attestation)            | Asserts `c23:airgap:bundled = "true"` on every external dependency. |

---

## 17. Worked example — combined BOM bundle (excerpt)

```jsonc
{
  "$schema":"http://cyclonedx.org/schema/bom-1.7.schema.json",
  "bomFormat":"CycloneDX","specVersion":"1.7","serialNumber":"urn:uuid:0a","version":1,
  "metadata":{
    "timestamp":"2026-05-02T00:00:00Z",
    "lifecycles":[{"name":"operations"}],
    "tools":{"components":[{"type":"application","name":"C23 DIANA NATO Warfighters","version":"1.0.0"}]},
    "properties":[{"name":"c23:bomKind","value":"MissionBOM"}]
  },
  "components":[
    { "type":"application","bom-ref":"app/c23","name":"C23 SPA","version":"1.0.0",
      "purl":"pkg:generic/c23@1.0.0","licenses":[{"license":{"id":"Apache-2.0"}}] },
    { "type":"library","bom-ref":"pkg:npm/react@18.3.1","name":"react","version":"18.3.1",
      "purl":"pkg:npm/react@18.3.1","licenses":[{"license":{"id":"MIT"}}] },
    { "type":"cryptographic-asset","bom-ref":"crypto/tls13",
      "name":"TLS 1.3","cryptoProperties":{"assetType":"protocol",
      "protocolProperties":{"type":"tls","version":"1.3","tlsCipherSuites":["TLS_AES_256_GCM_SHA384"]}} },
    { "type":"machine-learning-model","bom-ref":"ml/coa-stub",
      "name":"CoA Recommender (stub)","version":"0.1.0",
      "modelCard":{"modelParameters":{"task":"course-of-action-recommendation",
        "approach":{"type":"supervised"},"architectureFamily":"transformer"}} },
    { "type":"data","bom-ref":"data/mission/baltic-sentry","name":"C23 Mission",
      "data":[{"name":"mission.json","classification":"UNCLASSIFIED",
        "contents":{"attachment":{"contentType":"application/json","encoding":"base64","content":"e30="}}}] }
  ],
  "services":[
    { "bom-ref":"svc/cop-tile-server","name":"cop-tile-server","version":"1.0.0",
      "endpoints":["https://tiles.local/{z}/{x}/{y}.png"],"authenticated":true,"trustZone":"RESTRICTED" }
  ],
  "dependencies":[
    { "ref":"app/c23","dependsOn":["pkg:npm/react@18.3.1","ml/coa-stub","data/mission/baltic-sentry","svc/cop-tile-server","crypto/tls13"] }
  ],
  "vulnerabilities":[
    { "bom-ref":"vuln/CVE-2025-12345","id":"CVE-2025-12345",
      "source":{"name":"NVD"},"ratings":[{"score":9.1,"severity":"critical","method":"CVSSv4"}],
      "affects":[{"ref":"pkg:npm/react@18.3.1","versions":[{"version":"18.3.1","status":"affected"}]}],
      "analysis":{"state":"not_affected","justification":"code_not_reachable"} }
  ],
  "declarations":{
    "attestations":[
      { "bom-ref":"att/airgap","summary":"Verified air-gap readiness","assessor":"assr/diana",
        "map":[{"requirement":"req/airgap","claims":["claim/no-internet"],
                "conformance":{"score":1.0,"rationale":"Build verified offline"}}] }
    ],
    "claims":[ { "bom-ref":"claim/no-internet","target":"app/c23","predicate":"no_outbound_traffic_at_runtime"} ]
  },
  "definitions":{
    "standards":[
      { "bom-ref":"std/cyclonedx","name":"CycloneDX","version":"1.7","owner":"Ecma" },
      { "bom-ref":"std/ecma-424",  "name":"ECMA-424","version":"1st","owner":"Ecma" }
    ]
  },
  "externalReferences":[
    { "type":"bom","url":"urn:cdx:00000000-0000-0000-0000-0000000000bb/1","comment":"Linked OOB BOM" },
    { "type":"release-notes","url":"file://RELEASES/c23-1.0.0.md","comment":"v1.0.0 release notes" }
  ]
}
```

---

## 18. Mapping summary table

| C23 in-app schema           | CycloneDX representation                                                                                  |
| --------------------------- | --------------------------------------------------------------------------------------------------------- |
| `C23-DIANA-MISSION/1.0`     | Single envelope, `c23:bomKind="MissionBOM"`, mission JSON wrapped under `components[*].type="data"`        |
| `C23-DIANA-OOB/1.0`         | Single envelope, `c23:bomKind="OOB-BOM"`, one `data` component per unit                                    |
| `C23-DIANA-ACH/1.0`         | Single envelope, `c23:bomKind="ACH-BOM"`, `data` components for CoAs/Events plus scoring under `formulation` |
| AIS feed (Master-Prompt)    | Single envelope, `c23:bomKind="AIS-BOM"`, one `data` component per vessel                                  |
| AJP doctrine PDFs           | Single envelope, `c23:bomKind="DoctrineBOM"`, one `data` component per publication                         |
| Platform release            | SBOM + CRNF + CDAX combined envelope, signed.                                                              |

This single-envelope discipline is what enables the C23 platform to ingest every artefact through one ECMA-424 / CycloneDX 1.7 pipeline regardless of whether it is software, ML, hardware, operational data, doctrine or vulnerability disclosure.
