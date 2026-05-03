---
name: mission-editor
description: Un-hardcode every parameter of a wargame / scenario into a CRUD editor with JSON import/export of the full mission, the OOB only, or sub-bundles.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    sourceFile: HTML/JS file with hardcoded scenario data
    paramGroups: ["mission","phases","oob","events","scoring","aisFeed", … ]
  outputSchema:
    editorComponent: a React modal with one tab per param group + IO tab
    schemaName: e.g. "C23-DIANA-MISSION/1.0"
  errorHandling:
    invalidImport: "show window.alert with parse error; never overwrite state"
    schemaMismatch: "auto-detect by schema field; reject unknown shapes"
  stateless: true
tools: [Read, Edit, Write]
---

# mission-editor

## Purpose
Promote every "magic" hardcoded scenario parameter (mission name, phase ladders with relative + absolute dates, geopolitical events, intel events, OOB, ACH matrix, AIS feed, A2/AD zones, CUI nodes, phase vectors, polygons) into a CRUD interface with JSON I/O. Defaults remain unchanged so existing demos still work.

## When to use
- A demo / wargame ships with parameters baked into source.
- Stakeholders want to edit scenarios without touching code.
- A platform must be re-skinnable to a new mission inside one user session.

## Inputs
- The original file's `window.INITIAL_*` / inline arrays.
- The list of parameter groups to expose. For DIANA-class platforms (v009 catalogue, **19 tabs**): `mission`, `phases`, `geo`, `intel`, `oob`, `ach`, `coa`, `ais`, `jpt` (Joint Targeting), `mov` (Movement), `pos` (Posture), `wx` (Weather, v005), `orders` (OPORD, v005), `rollup` (Echelon, v005), `qol` (Workspace, v006), `intelops` (v008), `analytics` (v009), `io`, `settings`.

## Outputs
- A `MissionEditor` React modal with a tab per group (the v002 catalogue ships thirteen — see `Inputs`).
- Three import schemas (auto-detected by `schema` field):
  - `C23-DIANA-MISSION/1.0` — full mission.
  - `C23-DIANA-OOB/1.0` — order of battle only.
  - `C23-DIANA-ACH/1.0` — ACH matrix only.
- Three export buttons (full / OOB / ACH).

## Instructions

1. **Define a single `DEFAULT_MISSION`** object that mirrors every previously-hardcoded array, exposed as `window.DEFAULT_MISSION`.
2. **Make the React `App` reducer state derive from it on first mount:**
   ```js
   const [mission, setMission] = useState(() => deepClone(window.DEFAULT_MISSION));
   const [units, setUnits]     = useState(() => deepClone(window.DEFAULT_MISSION.oob));
   ```
3. **Create one tab component per param group** following the same pattern: filter input + count badge + `+ ADD` button + table with inline `<input>` cells + `DEL` button per row.
4. **Use a single shared `Field` wrapper** for the create/edit form. Don't replicate label/input markup.
5. **Implement IO with auto-detect by `schema` field.** Never accept a blob without checking — at minimum verify either `schema` matches a known string or the top-level shape (`Array.isArray(data.oob)`).
6. **Round-trip everything you read.** If you import a field you don't render, keep it under `mission.<field>` and re-export it untouched.
7. **Gate the "Restore Baseline" action behind `window.confirm`.** Reset is destructive and should reload the page or replace `mission` wholesale.
8. **Log every CRUD via the same `pushLog(prefix, msg, tone)` channel** so audit is consistent.

## Examples

### Schema discrimination (deliverable B)
```js
const importMission = (data) => {
  if (data.schema === "C23-DIANA-OOB/1.0" || (Array.isArray(data.oob) && !data.mission)) {
    setUnits(data.oob.map(u => ({...u, domain: u.domain || getDomainFromSIDC(u.sidc)})));
    return;
  }
  if (data.schema === "C23-DIANA-ACH/1.0" || data.achMatrix) {
    setMission(m => ({...m, achMatrix: data.achMatrix || m.achMatrix}));
    return;
  }
  setMission({...window.DEFAULT_MISSION, ...data});
  setUnits(deepClone(data.oob));
};
```

### Phase CRUD with rel + abs dates
```jsx
<input type="number" step="0.5" value={p.relDays}
       onChange={e=>upd(p.id,"relDays",e.target.value)}/>
<input value={p.absISO||""}
       onChange={e=>upd(p.id,"absISO",e.target.value)}/>
```

## Anti-patterns
- ❌ One tab that exposes every field as a giant form. Tabs map 1:1 to param groups for navigability.
- ❌ Validating only on import; let invalid edits live in state. The editor's job is exactly to surface them.
- ❌ Forgetting the **"OOB only" export** — that is what most users will round-trip.
- ❌ Letting "Restore Baseline" silently throw away unsaved work.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v009.html` — `MissionEditor` with the full 19-tab catalogue.
- Companion skills (one per tab where applicable): `ach-matrix`, `ach-auto-suggest`, `joint-targeting-jtc`, `movement-entities`, `posture-indicators`, `ais-fusion`, `doctrine-document-generator` (ORDERS), `echelon-rollup-and-scoping` (ROLL-UP + INTEL OPS HQ scoping), `spa-persistence` (WORKSPACE), `event-analytics` (INTEL OPS + ANALYTICS), `live-feed-adapter` (ANALYTICS).
- Master Prompt deliverable B.
