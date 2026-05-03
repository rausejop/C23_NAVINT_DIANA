---
name: cyclonedx-unified-bom
description: Design a single CycloneDX 1.7 / ECMA-424 envelope covering SBOM, SaaSBOM, CBOM, HBOM, ML-BOM, OBOM, MBOM, VDR, VEX, BOV, CDAX, BOM-Link and CRNF.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    bomKind: "SBOM|SaaSBOM|CBOM|HBOM|ML-BOM|OBOM|MBOM|VDR|VEX|BOV|CDAX|MissionBOM|OOB-BOM|ACH-BOM|AIS-BOM|DoctrineBOM"
    items:   array of artefacts to encode
  outputSchema:
    json: a CycloneDX 1.7 envelope, schema-valid
  errorHandling:
    invalidKind: "refuse with the list of accepted bomKind values"
  stateless: true
tools: [Read, Write, Edit]
---

# cyclonedx-unified-bom

## Purpose
Use **one** CycloneDX 1.7 envelope as the universal Bill-of-Materials carrier for every artefact in a NATO platform — software, services, crypto, hardware, ML models, operations, manufacturing, vulnerabilities, attestations, release notes, and even operational data (mission, OOB, ACH, AIS, doctrine). One schema, one validator, one ingestion pipeline.

## When to use
- The platform must satisfy NATO supply-chain transparency obligations.
- The user needs a unified data model (Master Prompt deliverable J).
- Multiple BOM variants exist in the same project and would otherwise live in parallel schemas.

## Inputs
- The `bomKind` discriminator (one of the accepted values).
- The artefacts to encode.

## Outputs
- A schema-valid CycloneDX 1.7 JSON envelope. The discriminator goes in `metadata.properties[*]` as `c23:bomKind` and in `metadata.lifecycles[*].name`.

## Instructions

1. **One envelope, always.** Header fields are constant: `bomFormat:"CycloneDX"`, `specVersion:"1.7"`, `serialNumber:"urn:uuid:…"`, `version:1`, `metadata.timestamp`.
2. **Discriminate by `c23:bomKind`** in `metadata.properties[*]` and by `metadata.lifecycles[*].name`:
   - `SBOM` → `lifecycles: [{name:"build"},{name:"pre-build"}]`
   - `SaaSBOM` → `operations`
   - `CBOM` → `design`, `operations`
   - `HBOM` → `design`, `manufacture`
   - `ML-BOM` → `design`, `pre-build`, `build`
   - `OBOM` → `operations`
   - `MBOM` → `manufacture`
   - `VDR` / `VEX` / `BOV` / `CDAX` → `operations`
3. **Components are universal.** Use the appropriate `type`:
   `application | framework | library | container | platform | operating-system | device | device-driver | firmware | file | machine-learning-model | data | cryptographic-asset`.
4. **Crypto goes in `cryptoProperties`** with `assetType ∈ {algorithm, certificate, protocol, related-crypto-material}`.
5. **ML models use `modelCard`** with `modelParameters`, `quantitativeAnalysis`, `considerations`, `properties`. Training data is a separate `data` component referenced by `bom-ref`.
6. **SaaS goes in `services[*]`**, with `endpoints`, `authenticated`, `data[*].flow`, `trustZone`. Always cross-link to `components` via `dependencies`.
7. **Vulnerabilities** use `vulnerabilities[*]`:
   - VDR omits `analysis`.
   - VEX adds `analysis.state` and `analysis.justification`.
   - BOV is an aggregate envelope with `compositions[*].aggregate` set.
8. **Attestations** go in `declarations` (assessors, attestations, claims, evidence, targets, affirmation, signature). This is **CDAX**.
9. **BOM-Link** = `externalReferences[*].type = "bom"` with URN `urn:cdx:<serial>/<version>#<bom-ref>`.
10. **CRNF** = `externalReferences[*].type = "release-notes"` plus `properties` of form `crnf:*`.
11. **Operational data** (mission / OOB / ACH / AIS / doctrine) is wrapped as `components[*].type = "data"` with `properties` carrying domain-specific keys (`c23:mission:*`, `c23:ais:*`, `c23:doctrine:*`).
12. **Validate** with the official JSON Schema before emitting.

## Examples

### Mission as a BOM (excerpt)
```jsonc
{
  "bomFormat":"CycloneDX","specVersion":"1.7","serialNumber":"urn:uuid:0a","version":1,
  "metadata":{
    "timestamp":"2026-05-02T00:00:00Z",
    "lifecycles":[{"name":"operations"}],
    "properties":[{"name":"c23:bomKind","value":"MissionBOM"}]
  },
  "components":[
    { "type":"data","bom-ref":"data/mission/baltic-sentry","name":"C23 Mission",
      "data":[{"name":"mission.json","classification":"UNCLASSIFIED",
        "contents":{"attachment":{"contentType":"application/json","encoding":"base64","content":"…"}}}] }
  ],
  "externalReferences":[
    { "type":"bom","url":"urn:cdx:00000000-0000-0000-0000-0000000000bb/1","comment":"Linked OOB BOM" }
  ]
}
```

### VEX overlay on a VDR
```jsonc
"analysis": {
  "state": "not_affected",
  "justification": "code_not_reachable",
  "response": ["will_not_fix"],
  "detail": "Function never invoked in air-gapped build path."
}
```

## Anti-patterns
- ❌ Producing one custom JSON schema per BOM kind. The whole point of CycloneDX is one envelope.
- ❌ Using SPDX or in-house formats alongside CycloneDX. Pick one transport; CycloneDX is the only ECMA-standardised option.
- ❌ Storing crypto facts in free-text components. Use `cryptoProperties`.
- ❌ Mixing VDR and VEX records without `analysis.state`. VEX is the disposition layer; without `state` it is not VEX.

## References
- `Datamodel.md` — full worked spec for this project.
- CycloneDX 1.7 schema: <https://cyclonedx.org/docs/1.7/json/>
- ECMA-424 (CycloneDX as Ecma standard).
