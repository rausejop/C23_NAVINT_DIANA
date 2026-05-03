---
name: event-analytics
description: Three companion analytics over the event stream — anomaly detection (rule set), correlation (clustering), and 2nd/3rd-order cascade modelling.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    mission:    "live mission state"
    units:      "current OOB"
    coaHistory: "executed turns"
  outputSchema:
    anomalies:   "[{ severity, source, text }]"
    clusters:    "[{ key, count, severity, events }]"
    cascades:    "per-CoA [{ order, dom, txt }]"
  errorHandling:
    emptyInputs: "return empty arrays; never throw"
  stateless: true
tools: [Read, Edit]
---

# event-analytics

## Purpose
Three pure functions that together turn the platform's event streams into something an analyst can act on:

- **AN-02 — `detectAnomalies()`** — pluggable rule set across AIS, OOB, JPTL and posture interactions.
- **AN-01 — `correlateEvents()`** — keyword clustering of geopolitical + intel events to surface "this is the same story playing out in three places".
- **AN-03 — `cascadeEffects()`** — heuristic 2nd/3rd-order effects per CoA, mapped onto SEA / LOG / HNS / INFRA / STRATCOM / LAND / NEUTRAL / CIS / C2 domains.

All three are deliberately heuristic and pure. The integration seam for an ML correlator (FM-02 in `roadmap.md`) is the same call site.

## When to use
- The user references "anomaly", "correlation", "cluster", "cascade", "2nd-order effect".
- The platform produces enough events that hand-scanning them stops scaling.
- The decision support tab needs more substance than just CoA × Evidence.

## Inputs
- `mission` (uses `aisFeed`, `intelEvents`, `geopoliticalEvents`, `jointTargeting`, `posture`).
- `units` (status, readiness, side).
- `coaHistory` (only for the AAR-time anomaly entry).

## Outputs
- `anomalies` — list of structured findings rendered with severity colour-coding.
- `clusters` — list of event-clusters keyed by `(source × top-keyword)`.
- `cascades` — per-CoA list of derived effects with order (2 / 3) and domain tag.

## Instructions

1. **Anomaly rules are ordered, additive, and small.** Each rule reads a slice of state and may push 0..N entries:
   ```js
   if ((mission.posture?.pnt||"")==="Denied" && (mission.posture?.cisPace||"P")==="P")
     A.push({severity:"alert", source:"FUSION",
             text:"PNT denied while still on Primary CIS — fall back to Alternate (CIS PACE)."});
   ```
   Resist the urge to wrap rules in classes. Keep them inlined for grep-ability.
2. **Correlation key = `${source}::${topKeyword}`.** Tokenise event title + narrative, drop tokens shorter than 5, pick the first as the cluster key. Surface clusters with ≥ 2 members. The aggregate severity is the worst severity in the cluster.
3. **Cascade rules are keyed off the CoA name + description**, not the CoA id. Patterns (`/interdict|naval/`, `/cui|sabotage|cable/`, etc.) emit 2nd- and 3rd-order effects with explicit `dom` tags.
4. **Always emit at least one cascade per CoA.** The fallback is a `dom:"GEN"` row that says "(no cascade rules matched — extend cascadeEffects() for this CoA pattern)". Tells the next agent where to add rules.
5. **Memoise** all three with `useMemo` keyed on the inputs that matter — they will run on every render otherwise.
6. **Render colour-coded.** Severity drives a status pill; cluster severity rolls up; cascade order (2 vs 3) drives the visual emphasis.

## Examples

### Anomaly rule set (excerpt, paste-ready)
```js
function detectAnomalies({ mission, units, coaHistory }) {
  const A = [];
  (mission.aisFeed?.DATA||[]).forEach(v => {
    if ((v.DESTINATION||"").toUpperCase().includes("AIS OFF"))
      A.push({severity:"alert", source:"AIS", text:`${v.SHIPNAME} reports DESTINATION="AIS OFF" (dark-AIS pattern).`});
    if (v.FLAG==="RU" && parseFloat(v.SPEED||"0") < 4)
      A.push({severity:"warn",  source:"AIS", text:`${v.SHIPNAME} (RU flag) loitering at ${v.SPEED} kn.`});
  });
  units.forEach(u => {
    if ((u.status||"").toLowerCase()==="disrupted")
      A.push({severity:"warn", source:"OOB", text:`Unit ${u.id} (${u.designation}) reported DISRUPTED.`});
  });
  (mission.jointTargeting?.jptl||[]).forEach(t => {
    if (t.category==="TST" && parseInt(t.cde||"0",10) >= 4)
      A.push({severity:"alert", source:"JPTL", text:`TST "${t.name}" carries a high CDE rating (${t.cde}).`});
  });
  if ((mission.posture?.pnt||"")==="Denied" && (mission.posture?.cisPace||"P")==="P")
    A.push({severity:"alert", source:"FUSION", text:"PNT denied while still on Primary CIS — fall back to Alternate."});
  return A;
}
```

### Correlation engine
```js
function correlateEvents(events) {
  const tokenize = (s) => (s||"").toLowerCase().split(/[^a-z0-9]+/).filter(w=>w.length>4);
  const clusters = new Map();
  events.forEach(e => {
    const toks = [...tokenize(e.title), ...tokenize(e.narrative)];
    if (!toks.length) return;
    const key = `${e.source||"?"}::${toks[0]}`;
    if (!clusters.has(key)) clusters.set(key, []);
    clusters.get(key).push(e);
  });
  return [...clusters.entries()]
    .filter(([,arr]) => arr.length >= 2)
    .map(([k,arr]) => ({ key:k, count:arr.length, events:arr,
      severity: arr.some(e=>e.severity==="alert") ? "alert"
              : arr.some(e=>e.severity==="warn") ? "warn" : "info" }))
    .sort((a,b)=>b.count-a.count);
}
```

### Cascade rule pattern
```js
function cascadeEffects(coa, mission) {
  const out = []; const desc = `${coa.name} ${coa.description||""}`.toLowerCase();
  const push = (order, dom, txt) => out.push({ order, dom, txt });
  if (/interdict|naval/.test(desc)) {
    push(2,"SEA",  "Civil shipping reroute around exclusion zone.");
    push(3,"INFO", "Insurance market reaction; freight rates spike.");
  }
  /* … more rules … */
  if (out.length === 0) push(2,"GEN", "(no cascade rules matched — extend cascadeEffects())");
  return out;
}
```

## Anti-patterns
- ❌ One giant `analyze()` function returning everything. Splitting them keeps each one ≤ 30 LOC and easy to extend.
- ❌ Holding analytics in state. Re-derive on render with `useMemo`.
- ❌ Hard-coding doctrine concepts inside the rule set ("if cardinal direction == North then OPFOR Bravo"). Generalise around event fields.
- ❌ Storing cluster output for "performance". Inputs are tiny; the perf concern is theoretical.
- ❌ Emitting cascades that the analyst can't act on ("Side will be confused"). Each cascade should map to a CoA the analyst could pre-stage.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v008.html` — `detectAnomalies()` and `IntelOpsTab`.
- `C23_DIANA_NATO_WARFIGHTERS_v009.html` — `correlateEvents()`, `cascadeEffects()`, `AnalyticsTab`.
- `roadmap.md § 11.3` — AN-01..AN-04 backlog (AN-04 lives in skill `ach-auto-suggest`).
