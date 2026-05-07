---
name: narrated-demo-video
description: Produce a narrated screencast video (≤4 min, MP4) of a single-file HTML SPA with TTS voice-over, English subtitles burned in, and a visible animated cursor that moves before every click — the deliverable shape DIANA-style portals expect.
version: 1.0.0
author: CONFIANZA23
slo:
  inputSchema:
    spa: "absolute path to the .html file under capture"
    storyboard: "scenes = ordered list of (sceneName, durationSeconds, narrationText); must sum to ≤ targetSeconds"
    targetSeconds: "video length cap (DIANA = 240 = 4:00); also the value passed to ffmpeg -t"
    subtitles: "optional pre-built .srt; otherwise derived from narrationText with even cue spacing"
    voice: "edge-tts voice id (default en-GB-RyanNeural)"
  outputSchema:
    video: "dist/video/diana_demo.mp4 (h264 + aac, MP4 with faststart, narration + burned subtitles)"
    narration: "dist/video/narration/narration.wav (concatenated TTS, padded to targetSeconds)"
    perScene: "dist/video/narration/scene_NN.mp3 (one per scene)"
    raw: "dist/video/raw/<random>.webm (Playwright's silent recording, retained as backup)"
  errorHandling:
    sceneOverrun: "if TTS clip > scene window, accelerate via ffmpeg atempo (cap 1.25× to stay natural); pad short clips with apad"
    subtitleInvisible: "ASS PrimaryColour with leading FF means alpha=transparent — use &H00FFFFFF (opaque white)"
    noCursor: "use page.evaluate(CURSOR_INIT_JS) AFTER each goto() — add_init_script ordering is unreliable"
    audioMissing: "ffmpeg -map 0:v:0 -map 1:a:0 explicitly, do not rely on -shortest with anullsrc"
  stateless: true
tools: [Read, Write, Bash]
---

# narrated-demo-video

## Purpose
DIANA (and most defence / EU funding portals) require a short narrated video of the platform: ≤ 4 min, MP4, ≤ 100 MB, English audio AND English subtitles, screen capture of the actual platform, and a demonstration of integration features + the defence use case. Recording a screen-cast by hand is fragile, hard to time, and the speaker accent varies. This skill produces it deterministically: TTS narration → Playwright screen recording with a visible animated cursor → ffmpeg mux + burn-in. Re-runnable end-to-end.

## When to use
- The user is preparing a video deliverable for a defence / dual-use portal (DIANA, EDF, EU Horizon, NATO ACT).
- The platform is a single-file HTML SPA driven by selectors stable enough to script (CONFIG → tab pattern).
- The user wants subtitles AND voice-over (DIANA mandates both for accessibility).
- The user wants the cursor to be visible — Playwright's bundled chromium does not render the OS cursor in headless screen-capture, so a CSS overlay is needed.

## Inputs
1. **The SPA path.** Same constraints as `playwright-spa-screenshots`.
2. **A storyboard** — ordered list of `(sceneName, targetSeconds, narrationText)`. Total seconds must equal the cap (DIANA = 240). Narrate at ~150 wpm; 25 s ≈ 60 words.
3. **A subtitles.srt** aligned to scene boundaries (or auto-derived). Cues should not last > 12 s each (readability).
4. **A voice** — Edge neural TTS voice id. Defaults: `en-GB-RyanNeural` (NATO/British, formal), `en-US-GuyNeural` (American), `en-US-JennyNeural` (female). All free, no API key.

## Outputs
- `dist/video/diana_demo.mp4` — the deliverable.
- `dist/video/narration/scene_NN.mp3` — per-scene TTS clips (debug-friendly).
- `dist/video/narration/narration.wav` — concatenated, silence-padded.
- `dist/video/raw/<random>.webm` — Playwright's native silent recording (kept as backup).
- `dist/video/storyboard.md`, `dist/video/subtitles.srt` — human-editable inputs.

## Instructions

### 1. Install once

```bash
pip install --quiet edge-tts playwright
python -m playwright install chromium
# ffmpeg must be on PATH (winget install Gyan.FFmpeg or apt install ffmpeg)
```

### 2. Generate the narration first

Run a TTS step BEFORE recording so the script knows each scene's actual audio length and can pad / time-stretch to fit. See `tools/generate_narration.py` — produces:
- `scene_NN.mp3` per scene via `edge_tts.Communicate(text, voice, rate, pitch)` (`rate=+8%` keeps dense scenes inside their slot).
- For each scene, build an exact-length WAV: if TTS > target, `ffmpeg -filter:a atempo=<r>` (cap r ≤ 1.25 for natural speech); if TTS < target, `ffmpeg -af apad=pad_dur=<delta>`.
- Concatenate to `narration.wav` with `ffmpeg -f concat`.

### 3. Record the screen capture with Playwright

Two non-obvious mechanics:

- **Visible cursor**: inject a CSS overlay `#__c23_cursor` (28 px yellow-on-NATO-blue dot) plus a click pulse-ring `#__c23_ring` AFTER each `page.goto()`. `add_init_script` runs at document-start which is unreliable for IIFE element creation; explicit `page.evaluate(CURSOR_INIT_JS)` is the reliable seam.
- **Cursor + mouse co-motion**: write a `move_cursor(page, x, y, steps=22)` helper that interpolates with ease-in-out (`cos(πt)`-based), driving BOTH the overlay (`page.evaluate('window.__c23_cursor_move(...)')`) and the real Playwright mouse (`page.mouse.move()`) in lockstep. Without the real mouse the SPA's own hover states do not trigger.
- For every click, `move_and_click(page, selector)` resolves selector → bounding box → smooth-move cursor → `page.evaluate('window.__c23_cursor_click(...)')` → `page.mouse.click()`.

Scene loop pattern:

```python
for name, dur in SCENES:
    scene_t0 = time.time()
    # navigation + cursor sweeps
    open_config_tab(page, "WARGAMING")
    move_cursor(page, 700, 350); move_cursor(page, 1100, 550); ...
    # park cursor in a corner and dwell to fill the slot
    park_cursor(page)
    elapsed = (time.time() - scene_t0) * 1000
    page.wait_for_timeout(max(0, dur*1000 - elapsed))
    close_modal(page)
```

Browser/context options:

```python
browser = p.chromium.launch(headless=True)
ctx = browser.new_context(
    viewport={"width": 1920, "height": 1080},
    record_video_dir=str(RAW_DIR),
    record_video_size={"width": 1920, "height": 1080},
)
```

### 4. Mux + burn-in subtitles + cap to target seconds

```bash
ffmpeg -y \
  -i raw/<random>.webm \
  -i narration/narration.wav \
  -vf "subtitles='dist/video/subtitles.srt':force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&HB0000000,BorderStyle=3,Outline=2,Shadow=0,MarginV=60,Bold=1'" \
  -map 0:v:0 -map 1:a:0 \
  -c:v libx264 -preset medium -crf 28 -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -t 240 \
  -movflags +faststart \
  diana_demo.mp4
```

Notes on the burn-in style block:
- `PrimaryColour=&H00FFFFFF` — `&HAABBGGRR`; AA=00 means OPAQUE in libass (inverse of CSS). `&HFFFFFFFF` is **transparent** = invisible text. Recurring trap.
- `BorderStyle=3` + `BackColour=&HB0000000` paints a translucent black box behind the text — survives noisy backgrounds (basemaps, photos).
- `MarginV=60` keeps the box well clear of the bottom edge so 16:9 portals do not crop it.

### 5. Verify the deliverable

```bash
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=codec_type,codec_name,channels \
  -of default=noprint_wrappers=0 dist/video/diana_demo.mp4
```

Expect `duration=240.0`, two streams (`h264`, `aac`), file size 5–15 MB at CRF 28.

Sample 4–5 frames at scattered timestamps to confirm subtitles render:

```bash
ffmpeg -y -ss 5   -i diana_demo.mp4 -frames:v 1 _check_5s.png
ffmpeg -y -ss 60  -i diana_demo.mp4 -frames:v 1 _check_60s.png
ffmpeg -y -ss 130 -i diana_demo.mp4 -frames:v 1 _check_130s.png
ffmpeg -y -ss 230 -i diana_demo.mp4 -frames:v 1 _check_230s.png
```

If any frame shows the SPA without the subtitle box → re-check the `&H00FFFFFF` fix; if the cursor is missing → confirm `install_cursor(page)` was called after every `page.goto()`.

## Reference implementation

- `tools/generate_narration.py` — TTS step, per-scene MP3, padded WAV.
- `tools/capture_diana_video.py` — Playwright recorder with visible cursor + mouse motion + ffmpeg mux.
- `dist/video/storyboard.md` — 4-min worked storyboard (10 scenes, 595 words).
- `dist/video/subtitles.srt` — 28 cues aligned to those scenes.
- `dist/video/diana_demo.mp4` — DIANA-ready output (4:00.00 / 10.83 MB / H.264 + AAC).

## Cursor overlay snippet (drop into your script)

```javascript
// Injected via page.evaluate() after every page.goto()
(() => {
  if (window.__c23_cursor_installed) return;
  window.__c23_cursor_installed = true;
  const cur = document.createElement('div'); cur.id = '__c23_cursor';
  Object.assign(cur.style, {
    position:'fixed', left:'-100px', top:'-100px', width:'28px', height:'28px',
    pointerEvents:'none', zIndex:2147483647,
    background:'radial-gradient(circle at 35% 35%, #fff 0%, #FFC72C 35%, transparent 75%)',
    border:'2px solid #04243f', borderRadius:'50%',
    boxShadow:'0 0 14px rgba(255,199,44,0.85), 0 0 28px rgba(0,73,144,0.55)',
    transform:'translate(-50%,-50%)',
    transition:'left 80ms linear, top 80ms linear',
  });
  document.documentElement.appendChild(cur);
  // pulse ring on click — analogous element + animation
  window.__c23_cursor_move  = (x,y) => { cur.style.left=x+'px'; cur.style.top=y+'px'; };
  window.__c23_cursor_click = (x,y) => { /* animate the ring + cursor pulse */ };
})();
```

## Anti-patterns

- ❌ Recording first, then trying to time the narration to the video. Always TTS-first; let audio drive scene durations.
- ❌ `&HFFFFFFFF` for subtitle colour. Alpha-FF in libass = transparent; your text vanishes. Use `&H00FFFFFF`.
- ❌ Relying on `add_init_script` for cursor injection. Order is unreliable across page transitions. Re-inject after each `goto()`.
- ❌ Calling `page.mouse.click()` without first `move_cursor()` to that exact spot. The visible cursor will teleport instead of leading the click.
- ❌ Mixing `headless=False` (to "see what is happening") with `record_video_dir`. The recorder still captures the same headless surface; the visible window is wasted.
- ❌ Picking `--crf 18` "for quality". Output blows past 100 MB. CRF 26-30 is the DIANA-fitting band at 1920×1080 / 4 min.
- ❌ Letting any one scene's narration overflow > 1.25× atempo. Above that, TTS sounds like Alvin & the Chipmunks. If you cannot fit, shorten the text.
- ❌ Skipping `-movflags +faststart`. The first second of playback in a browser hangs while the moov atom is fetched from EOF.
- ❌ Hard-coding scene durations independent of TTS length. Always probe the rendered MP3 with `ffprobe -show_entries format=duration` and decide per-scene whether to pad or atempo.
- ❌ Submitting a video where the closing card has no closing-narration cue. The last 5 s feel like a frozen frame; always end with a "Ready for evaluation" subtitle + line.

## Voice selection (Edge neural)

| Voice id | Use when | Notes |
|---|---|---|
| `en-GB-RyanNeural` | NATO / formal | British, calm, minimal "ums" — default for DIANA |
| `en-GB-SoniaNeural` | NATO / formal female | Pairs naturally with Ryan in dual-narrator scripts |
| `en-US-GuyNeural` | EDF / US-facing | American, slightly faster cadence |
| `en-US-JennyNeural` | EDF / US-facing female | Clear, neutral US accent |
| `en-IE-ConnorNeural` | Irish / EU | Distinct enough to differentiate vs UK voices |

All are zero-cost, no token, no SDK; `edge-tts` reaches Microsoft's public endpoint. For air-gap delivery, generate the MP3s on a connected machine and copy the WAV across — the final video has no Edge dependency.

## DIANA-specific compliance check (apply at the end)

| Requirement (portal text) | Verify |
|---|---|
| Maximum 4 minutes | `ffprobe ... duration ≤ 240` |
| MP4 only | container=mov,mp4,m4a,3gp,3g2,mj2 + `codec_name=h264` |
| ≤ 100 MB | `ls -la diana_demo.mp4` |
| English language | TTS voice id starts with `en-` |
| English subtitles | SRT cues present + visually verified at sample timestamps |
| Screen capture + audio commentary | Playwright video stream + non-empty AAC audio stream |
| Third-party integration features demonstrated | Storyboard scene mentions JSON schemas / CycloneDX / live-feed adapter / OPORD generator / model seam |
| Defence use case demonstrated | Storyboard includes Eastern Flank scenario beats: COP → Wargaming → ROE-gate → JTC → Cascades → PR/Movement |

## References
- `tools/generate_narration.py`, `tools/capture_diana_video.py` — concrete implementations.
- `dist/video/storyboard.md` + `subtitles.srt` — human-editable inputs that drive the build.
- <https://github.com/rany2/edge-tts> — Edge neural TTS, zero-cost.
- <https://playwright.dev/python/docs/videos> — Playwright video recording API.
- <http://www.tcax.org/docs/ass-specs.htm> — ASS / libass colour & style spec (the `&HAABBGGRR` alpha trap).
- DIANA "Decision Superiority for NATO Warfighters" call (2026-05) — video format requirements.
- Skill `playwright-spa-screenshots` — sibling skill for the still-image deliverable.
- Skill `diana-proposal-draft` — references the output of this skill in the proposal package.
