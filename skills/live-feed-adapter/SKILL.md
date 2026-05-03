---
name: live-feed-adapter
description: Poll a remote endpoint for fresh intel events on a configurable interval; merge into the mission with provenance tagging.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    config: "{ url, intervalSec, enabled } persisted in localStorage 'c23.live'"
  outputSchema:
    appendedEvents: "added to mission.intelEvents with source: 'LIVE-FEED'"
    log:            "[LIVE] entries on poll success or error"
  errorHandling:
    cors: "log the error and keep polling on the next tick — don't disable the adapter"
    badJson: "log; skip this tick; do NOT mutate state"
  stateless: false
tools: [Read, Edit]
---

# live-feed-adapter

## Purpose
Replace "load this static JSON" with "subscribe to this URL". The pattern is small and demonstrates the seam where a real ISR feed plugs in (LD-01 in `roadmap.md`). Analysts opt in: state is `enabled: false` by default.

## When to use
- The user has a JSON endpoint emitting intel events and wants to subscribe.
- A demo wants to show "events arriving live" without a server-push setup.
- The integration target (real ISR / FMV / SIGINT feed) hasn't shipped yet but you want the swap-in surface ready.

## Inputs
- `live.url` — the endpoint to poll.
- `live.intervalSec` — clamp ≥ 5 sec (CORS + politeness).
- `live.enabled` — boolean.

## Outputs
- A `useEffect` that starts/stops a `setInterval` based on the config.
- Each successful poll appends new events to `mission.intelEvents`, tagging missing ids and missing sources.
- A `[LIVE]` log channel for both success and failure.

## Instructions

1. **Persist config in `localStorage`** (key `c23.live`). The user expects the URL to survive a reload.
2. **Default OFF.** Enabling is an analyst decision; never auto-poll random URLs.
3. **One `useEffect`** keyed on the three config fields. On entry, clear any prior interval; on exit, clear too. This handles toggling, URL change, and unmount.
4. **`fetch` with `mode: "cors"`** explicitly. Surfaces the CORS failure as a normal error rather than a cryptic network exception.
5. **Be tolerant of two response shapes:** an array, or `{ intelEvents: [...] }`. Reject anything else with a log line; do not throw.
6. **Tag provenance on every appended event:** `source: e.source || "LIVE-FEED"`, `id: e.id || newId("live")`. Lets the analyst filter for live-injected items.
7. **Provide a "FETCH NOW" button** so the user can validate the endpoint without waiting for the interval.
8. **Cap the interval at ≥ 5 sec** with `Math.max(5, intervalSec)`. Smaller intervals create a polite-bombing pattern.
9. **Log every poll outcome.** Silence is worse than noise — the operator must know whether the adapter is working.

## Examples

### The complete adapter (paste-ready, from v009)
```js
const [live, setLive] = useState(()=>{
  try { return JSON.parse(window.localStorage?.getItem("c23.live") || "{}"); } catch { return {}; }
});
const setLiveP = (k,v) => { const next = {...live, [k]:v};
  setLive(next); try { window.localStorage?.setItem("c23.live", JSON.stringify(next)); } catch {} };

const liveTimerRef = useRef(null);
const fetchOnce = useCallback(async () => {
  if (!live.url) return;
  try {
    const res = await fetch(live.url, { mode: "cors" });
    const data = await res.json();
    const arr = Array.isArray(data) ? data : (data.intelEvents||[]);
    if (arr.length) {
      setMission(m => ({...m, intelEvents:[...(m.intelEvents||[]),
        ...arr.map(e=>({...e, id: e.id || newId("live"), source: e.source || "LIVE-FEED" }))]}));
      pushLog?.("LIVE", `Pulled ${arr.length} events from ${live.url}.`, "info");
    }
  } catch (err) { pushLog?.("LIVE", `Adapter error: ${err.message}`, "warn"); }
}, [live.url, setMission, pushLog]);

useEffect(() => {
  if (liveTimerRef.current) { clearInterval(liveTimerRef.current); liveTimerRef.current = null; }
  if (live.enabled && live.url) {
    liveTimerRef.current = setInterval(fetchOnce, Math.max(5,(parseInt(live.intervalSec,10)||30))*1000);
  }
  return () => { if (liveTimerRef.current) clearInterval(liveTimerRef.current); };
}, [live.enabled, live.url, live.intervalSec, fetchOnce]);
```

### Minimal endpoint shape the adapter accepts
```json
[
  { "phase": 2, "dtg": "2026-05-02T08:30:00Z", "title": "New radar contact",
    "source": "RADAR", "narrative": "Track 042, 350 kn, FL280 — ID pending.",
    "severity": "warn" }
]
```

## Anti-patterns
- ❌ Default ON. Surprises the user with traffic from somewhere they didn't sign up for.
- ❌ A retry loop on parse failure. Logs flood; the actual problem is unfixed.
- ❌ Treating "no new events" as an error. Many polls will return `[]`.
- ❌ Mutating state inside `fetch` callbacks without using the functional setter. Race-prone with React 18 batching.
- ❌ Forgetting CORS in the user-facing error message. "Adapter error: NetworkError" wastes 20 minutes; "Adapter error: NetworkError (likely CORS — set Access-Control-Allow-Origin on the source)" saves them.

## References
- `C23_DIANA_NATO_WARFIGHTERS_v009.html` — `AnalyticsTab` LD-01 section.
- `roadmap.md § 11.2` — LD-01 / LD-02 / LD-03.
- Skill `event-analytics` — what consumes the events the adapter delivers.
