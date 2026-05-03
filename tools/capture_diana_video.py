#!/usr/bin/env python3
"""
capture_diana_video.py  (v2 — narrated, with visible cursor + mouse motion)

Drives Chromium via Playwright through the C23 NAVINT v011 SPA following the
storyboard in dist/video/storyboard.md, recording a 4:00 video with:
  * a visible animated cursor injected as a CSS overlay,
  * mouse motion before every click so the operator's gaze leads the action,
  * scene durations matching dist/video/narration/narration.wav per-scene timings.

Then ffmpeg muxes the recorded video with the TTS narration and burns the
English subtitles in.

Outputs:
  dist/video/raw/<random>.webm     # Playwright's native silent recording
  dist/video/diana_demo.mp4        # final deliverable for the DIANA portal

Usage:
    python tools/generate_narration.py    # produces narration.wav (run first)
    python tools/capture_diana_video.py
"""
from pathlib import Path
import shutil, subprocess, time, sys, json

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
SPA = REPO / "C23_DIANA_NATO_WARFIGHTERS_v011.html"
OUT_DIR = REPO / "dist" / "video"
RAW_DIR = OUT_DIR / "raw"
SUBS = OUT_DIR / "subtitles.srt"
NARRATION = OUT_DIR / "narration" / "narration.wav"
FINAL_MP4 = OUT_DIR / "diana_demo.mp4"

VIEWPORT = {"width": 1920, "height": 1080}

# Scene durations in seconds (must total 240 = 4:00)
SCENES = [
    ("title",               25),
    ("cop_overview",        30),
    ("fusion_tally",        25),
    ("joint_targeting",     25),
    ("roe_gate",            20),
    ("wargaming",           25),
    ("cascades",            25),
    ("pr_movement",         20),
    ("integration",         25),
    ("airgap_close",        20),
]
assert sum(s for _, s in SCENES) == 240

# ── Visible-cursor overlay injected on every page ─────────────────────────
CURSOR_INIT_JS = r"""
(() => {
  if (window.__c23_cursor_installed) return;
  window.__c23_cursor_installed = true;
  const cur = document.createElement('div');
  cur.id = '__c23_cursor';
  Object.assign(cur.style, {
    position: 'fixed', left: '-100px', top: '-100px',
    width: '28px', height: '28px',
    pointerEvents: 'none', zIndex: 2147483647,
    background: 'radial-gradient(circle at 35% 35%, #fff 0%, #FFC72C 35%, rgba(255,199,44,0.0) 75%)',
    border: '2px solid #04243f',
    borderRadius: '50%',
    boxShadow: '0 0 14px rgba(255,199,44,0.85), 0 0 28px rgba(0,73,144,0.55)',
    transform: 'translate(-50%, -50%)',
    transition: 'left 80ms linear, top 80ms linear, width 90ms ease, height 90ms ease, opacity 200ms',
    opacity: '1',
  });
  document.documentElement.appendChild(cur);
  // pulse ring on click
  const ring = document.createElement('div');
  ring.id = '__c23_ring';
  Object.assign(ring.style, {
    position: 'fixed', left: '-100px', top: '-100px',
    width: '12px', height: '12px',
    pointerEvents: 'none', zIndex: 2147483646,
    border: '3px solid #FFC72C',
    borderRadius: '50%',
    transform: 'translate(-50%, -50%) scale(1)',
    opacity: '0',
    transition: 'transform 350ms ease-out, opacity 350ms ease-out',
  });
  document.documentElement.appendChild(ring);
  window.__c23_cursor_move = (x, y) => {
    cur.style.left = x + 'px';
    cur.style.top = y + 'px';
  };
  window.__c23_cursor_click = (x, y) => {
    ring.style.transition = 'none';
    ring.style.left = x + 'px'; ring.style.top = y + 'px';
    ring.style.transform = 'translate(-50%, -50%) scale(0.8)';
    ring.style.opacity = '0.95';
    requestAnimationFrame(() => {
      ring.style.transition = 'transform 420ms ease-out, opacity 420ms ease-out';
      ring.style.transform = 'translate(-50%, -50%) scale(3.2)';
      ring.style.opacity = '0';
    });
    cur.animate([{ width:'28px', height:'28px' },
                 { width:'18px', height:'18px' },
                 { width:'28px', height:'28px' }],
                { duration: 220, easing: 'ease-in-out' });
  };
})();
"""

def install_cursor(page):
    """Install (idempotent) on the current document."""
    page.evaluate(CURSOR_INIT_JS)
    # Wait until the elements actually exist
    page.wait_for_function("() => !!document.getElementById('__c23_cursor')", timeout=3000)

def hide_cursor(page):
    page.evaluate(
        "() => { const c=document.getElementById('__c23_cursor'); if(c) c.style.opacity='0';"
        " const r=document.getElementById('__c23_ring'); if(r) r.style.opacity='0'; }"
    )

def show_cursor(page):
    page.evaluate(
        "() => { const c=document.getElementById('__c23_cursor'); if(c) c.style.opacity='1'; }"
    )

def move_cursor(page, x: int, y: int, *, steps: int = 22, settle_ms: int = 250):
    """Move the visible cursor smoothly to (x,y) and the real Playwright mouse
       in lockstep, then settle."""
    # Read current visible-cursor position (or default to centre).
    cur = page.evaluate(
        "() => { const c=document.getElementById('__c23_cursor'); "
        "if(!c) return [960,540]; const r=c.getBoundingClientRect(); "
        "return [r.left + r.width/2, r.top + r.height/2]; }"
    )
    sx, sy = cur if cur else (960, 540)
    for i in range(1, steps + 1):
        t = i / steps
        # ease-in-out
        e = 0.5 - 0.5 * (__import__('math').cos(__import__('math').pi * t))
        x_i = sx + (x - sx) * e
        y_i = sy + (y - sy) * e
        page.evaluate(f"window.__c23_cursor_move({x_i:.1f}, {y_i:.1f})")
        page.mouse.move(x_i, y_i)
        page.wait_for_timeout(18)
    page.wait_for_timeout(settle_ms)

def cursor_click(page, x: int, y: int):
    page.evaluate(f"window.__c23_cursor_click({x}, {y})")
    page.mouse.click(x, y)

def move_and_click(page, selector: str, *, settle_ms: int = 350):
    """Resolve selector → centre → smooth-move cursor → click."""
    el = page.locator(selector).first
    el.wait_for(state="visible", timeout=8000)
    box = el.bounding_box()
    if not box:
        # fall back to plain click
        el.click()
        return
    cx = box["x"] + box["width"] / 2
    cy = box["y"] + box["height"] / 2
    move_cursor(page, int(cx), int(cy), settle_ms=settle_ms)
    cursor_click(page, int(cx), int(cy))

def open_config_tab(page, tab_label, settle=0.6):
    move_and_click(page, "button.btn-ghost:has-text('CONFIG')")
    page.wait_for_selector(".cfg-tabs", timeout=5000)
    move_and_click(page, f".cfg-tab:has-text('{tab_label}')")
    page.wait_for_timeout(int(settle*1000))

def close_modal(page):
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

def park_cursor(page, x=1850, y=1040):
    """Park the cursor in a corner so it doesn't obscure content during dwell."""
    move_cursor(page, x, y, steps=14, settle_ms=120)

# ── Title / closing static cards (unchanged from v1) ──────────────────────
TITLE_HTML = """
<!doctype html><html><head><meta charset='utf-8'><title>C23 NAVINT</title>
<style>
  html,body{margin:0;height:100%;background:#04080f;color:#e6edf7;
    font-family:"Roboto Condensed","IBM Plex Sans",system-ui,sans-serif;}
  .stage{display:flex;flex-direction:column;align-items:center;justify-content:center;
    height:100vh;text-align:center;
    background:radial-gradient(1400px 700px at 50% 30%,rgba(0,73,144,0.35),transparent 70%),
      linear-gradient(180deg,#04080f 0%,#060c16 100%);}
  h1{font-size:80px;letter-spacing:0.18em;color:#fff;margin:0;font-weight:700;}
  h1 .gold{color:#FFC72C;}
  h2{font-size:24px;letter-spacing:0.18em;color:#a9c4ea;margin:30px 0 0;font-weight:500;max-width:1400px;line-height:1.5;}
  .stripe{margin-top:60px;height:6px;width:60%;
    background:repeating-linear-gradient(90deg,#004990 0 64px,#FFC72C 64px 80px);}
  .badge{margin-top:80px;font-family:"JetBrains Mono",monospace;font-size:14px;letter-spacing:0.22em;color:#92a1bd;}
</style></head><body>
<div class='stage'>
  <h1>C23 <span class='gold'>NAVINT</span></h1>
  <h2>DOCTRINE-DRIVEN AI DECISION-SUPERIORITY AUGMENTATION FOR<br/>
      MAVEN SMART SYSTEM NATO AND ALLIED C2 PLATFORMS</h2>
  <div class='stripe'></div>
  <div class='badge'>CONFIANZA23 INTELIGENCIA Y SEGURIDAD &middot; DIANA &middot; v011 &middot; 2026</div>
</div></body></html>
"""

CLOSING_HTML = """
<!doctype html><html><head><meta charset='utf-8'>
<style>
  html,body{margin:0;height:100%;background:#04080f;color:#e6edf7;
    font-family:"Roboto Condensed",sans-serif;}
  .stage{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;text-align:center;
    background:radial-gradient(1400px 700px at 50% 30%,rgba(0,73,144,0.35),transparent 70%),
      linear-gradient(180deg,#04080f 0%,#060c16 100%);}
  h1{font-size:64px;letter-spacing:0.18em;color:#FFC72C;margin:0;font-weight:700;}
  .lines{margin-top:36px;display:grid;grid-template-columns:auto auto;gap:8px 40px;font-family:"JetBrains Mono",monospace;font-size:18px;}
  .lines .k{color:#a9c4ea;letter-spacing:0.18em;text-align:right;}
  .lines .v{color:#fff;text-align:left;}
  .stripe{margin-top:60px;height:6px;width:60%;
    background:repeating-linear-gradient(90deg,#004990 0 64px,#FFC72C 64px 80px);}
  .footer{margin-top:50px;font-size:14px;color:#92a1bd;letter-spacing:0.16em;}
</style></head><body>
<div class='stage'>
  <h1>READY FOR EVALUATION</h1>
  <div class='lines'>
    <div class='k'>SPEC COVERAGE</div><div class='v'>73 / 74 = 98.6 %</div>
    <div class='k'>VERSION CHAIN</div><div class='v'>v001 -- v011 (md5-verified)</div>
    <div class='k'>AJPS BOUND</div><div class='v'>33 / 33</div>
    <div class='k'>AIR-GAP BUNDLE</div><div class='v'>dist/airgap/ (5.5 MB) + cdax.json</div>
    <div class='k'>SUBMITTER</div><div class='v'>Rafael Ausejo Prieto</div>
    <div class='k'>COMPANY</div><div class='v'>CONFIANZA23 INTELIGENCIA Y SEGURIDAD SL</div>
    <div class='k'>CONTACT</div><div class='v'>rafael.ausejo@confianza23.es</div>
  </div>
  <div class='stripe'></div>
  <div class='footer'>"Hacemos posible lo imposible"</div>
</div></body></html>
"""

def run():
    if not NARRATION.exists():
        print(f"[!] {NARRATION} not found. Run tools/generate_narration.py first.", file=sys.stderr)
        sys.exit(1)

    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    title_path = OUT_DIR / "_title.html"
    closing_path = OUT_DIR / "_closing.html"
    title_path.write_text(TITLE_HTML, encoding="utf-8")
    closing_path.write_text(CLOSING_HTML, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport=VIEWPORT,
            record_video_dir=str(RAW_DIR),
            record_video_size=VIEWPORT,
        )
        page = ctx.new_page()

        # ── Scene 1: title card ─────────────────────────────────────────
        print("[1/10] Title card (no cursor)")
        page.goto(title_path.as_uri())
        install_cursor(page)
        hide_cursor(page)
        page.wait_for_timeout(SCENES[0][1] * 1000)

        # ── Scene 2: COP overview ───────────────────────────────────────
        print("[2/10] COP overview")
        scene_t0 = time.time()
        page.goto(SPA.as_uri())
        page.wait_for_selector(".app .topbar", timeout=15000)
        page.wait_for_selector(".leaflet-tile", timeout=15000)
        page.wait_for_timeout(2000)  # let symbols settle
        install_cursor(page)
        show_cursor(page)
        move_cursor(page, 480, 120, steps=28, settle_ms=600)   # top bar
        move_cursor(page, 160, 360, steps=28, settle_ms=600)   # left rail
        move_cursor(page, 1100, 540, steps=30, settle_ms=400)  # centre Baltic
        move_cursor(page, 1280, 700, steps=20, settle_ms=300)  # towards DARK ECHO
        # Let scene fill its remaining time
        elapsed_ms = (time.time() - scene_t0) * 1000
        remaining = SCENES[1][1] * 1000 - elapsed_ms
        if remaining > 0: page.wait_for_timeout(int(remaining))

        # ── Scene 3: fusion + tally ─────────────────────────────────────
        print("[3/10] Fusion + Tally")
        scene_t0 = time.time()
        # Hover the FPCON tile then move down the rail tally
        move_cursor(page, 760, 80, steps=22, settle_ms=350)    # FPCON area on top bar
        move_cursor(page, 870, 80, steps=14, settle_ms=300)    # CBRN
        move_cursor(page, 980, 80, steps=14, settle_ms=300)    # PNT
        move_cursor(page, 1090, 80, steps=14, settle_ms=400)   # CIS PACE
        move_cursor(page, 130, 240, steps=24, settle_ms=300)   # rail tally header
        move_cursor(page, 130, 350, steps=12, settle_ms=250)   # sweep down rail
        move_cursor(page, 130, 460, steps=12, settle_ms=400)
        # Toggle a layer chip on then back on (off→on)
        try:
            chip = page.locator(".chip:has-text('NEUTRAL')").first
            if chip.is_visible():
                box = chip.bounding_box()
                if box:
                    move_cursor(page, int(box["x"]+box["width"]/2), int(box["y"]+box["height"]/2), settle_ms=250)
                    cursor_click(page, int(box["x"]+box["width"]/2), int(box["y"]+box["height"]/2))
                    page.wait_for_timeout(700)
                    cursor_click(page, int(box["x"]+box["width"]/2), int(box["y"]+box["height"]/2))
        except Exception:
            pass
        park_cursor(page)
        elapsed_ms = (time.time() - scene_t0) * 1000
        remaining = SCENES[2][1] * 1000 - elapsed_ms
        if remaining > 0: page.wait_for_timeout(int(remaining))

        # ── Scene 4: Joint Targeting ────────────────────────────────────
        print("[4/10] Joint Targeting")
        scene_t0 = time.time()
        open_config_tab(page, "JOINT TARGETING")
        # Sweep the cursor across the JTC phase tiles inside the modal
        move_cursor(page, 700, 260, steps=24, settle_ms=350)
        move_cursor(page, 900, 260, steps=14, settle_ms=300)
        move_cursor(page, 1100, 260, steps=14, settle_ms=300)
        move_cursor(page, 1300, 260, steps=14, settle_ms=300)
        # Then down to the JPTL table
        move_cursor(page, 800, 560, steps=20, settle_ms=400)
        park_cursor(page)
        elapsed_ms = (time.time() - scene_t0) * 1000
        remaining = SCENES[3][1] * 1000 - elapsed_ms
        if remaining > 0: page.wait_for_timeout(int(remaining))
        close_modal(page)

        # ── Scene 5: ROE gate ──────────────────────────────────────────
        print("[5/10] ROE gate")
        scene_t0 = time.time()
        try:
            move_and_click(page, "button.btn-turn", settle_ms=400)  # switch to OPFOR
            page.wait_for_timeout(400)
            execute_btns = page.locator(".coa-card .btn-edit:has-text('EXECUTE')")
            if execute_btns.count() > 0:
                box = execute_btns.first.bounding_box()
                if box:
                    move_cursor(page, int(box["x"]+box["width"]/2), int(box["y"]+box["height"]/2), settle_ms=400)
                    cursor_click(page, int(box["x"]+box["width"]/2), int(box["y"]+box["height"]/2))
                    page.wait_for_timeout(1200)
                    # tour the modal: tst → rtl → nsl → buttons row
                    move_cursor(page, 700, 320, steps=24, settle_ms=350)
                    move_cursor(page, 700, 500, steps=18, settle_ms=350)
                    move_cursor(page, 700, 680, steps=18, settle_ms=350)
        except Exception as e:
            print("    (ROE step skipped:", e, ")")
        elapsed_ms = (time.time() - scene_t0) * 1000
        remaining = SCENES[4][1] * 1000 - elapsed_ms
        if remaining > 0: page.wait_for_timeout(int(remaining))
        try:
            move_and_click(page, "button.btn-danger:has-text('DENY')", settle_ms=300)
            page.wait_for_timeout(300)
        except Exception:
            close_modal(page)

        # ── Scene 6: Wargaming ─────────────────────────────────────────
        print("[6/10] Wargaming")
        scene_t0 = time.time()
        open_config_tab(page, "WARGAMING")
        # Sweep across matchup matrix cells
        move_cursor(page, 700, 350, steps=26, settle_ms=350)
        move_cursor(page, 900, 450, steps=16, settle_ms=350)
        move_cursor(page, 1100, 550, steps=16, settle_ms=350)
        move_cursor(page, 1300, 650, steps=16, settle_ms=400)
        park_cursor(page)
        elapsed_ms = (time.time() - scene_t0) * 1000
        remaining = SCENES[5][1] * 1000 - elapsed_ms
        if remaining > 0: page.wait_for_timeout(int(remaining))
        close_modal(page)

        # ── Scene 7: Cascades ──────────────────────────────────────────
        print("[7/10] Cascades")
        scene_t0 = time.time()
        open_config_tab(page, "ANALYTICS")
        try:
            page.evaluate("const b=document.querySelector('.modal-body'); if(b) b.scrollTop=b.scrollHeight*0.3;")
            page.wait_for_timeout(400)
        except Exception:
            pass
        # Sweep down the rules list
        move_cursor(page, 600, 450, steps=24, settle_ms=400)
        move_cursor(page, 600, 600, steps=16, settle_ms=400)
        move_cursor(page, 600, 750, steps=16, settle_ms=400)
        # Cursor over the AJP citation column
        move_cursor(page, 1300, 600, steps=20, settle_ms=400)
        park_cursor(page)
        elapsed_ms = (time.time() - scene_t0) * 1000
        remaining = SCENES[6][1] * 1000 - elapsed_ms
        if remaining > 0: page.wait_for_timeout(int(remaining))
        close_modal(page)

        # ── Scene 8: PR + Movement ─────────────────────────────────────
        print("[8/10] PR + Movement")
        scene_t0 = time.time()
        open_config_tab(page, "PR / JPRC")
        # Sweep across the 5-stage tally tiles
        move_cursor(page, 600, 280, steps=22, settle_ms=300)
        move_cursor(page, 800, 280, steps=12, settle_ms=300)
        move_cursor(page, 1000, 280, steps=12, settle_ms=300)
        move_cursor(page, 1200, 280, steps=12, settle_ms=400)
        # half time, then go to MOVEMENT
        page.wait_for_timeout(int(SCENES[7][1] * 500 - (time.time()-scene_t0)*1000))
        try:
            move_and_click(page, ".cfg-tab:has-text('MOVEMENT')", settle_ms=350)
            move_cursor(page, 700, 400, steps=20, settle_ms=400)
            move_cursor(page, 1000, 500, steps=16, settle_ms=400)
        except Exception:
            page.wait_for_timeout(2000)
        park_cursor(page)
        elapsed_ms = (time.time() - scene_t0) * 1000
        remaining = SCENES[7][1] * 1000 - elapsed_ms
        if remaining > 0: page.wait_for_timeout(int(remaining))
        close_modal(page)

        # ── Scene 9: Integration ──────────────────────────────────────
        print("[9/10] Integration")
        scene_t0 = time.time()
        open_config_tab(page, "IMPORT / EXPORT")
        # Sweep through schemas
        move_cursor(page, 700, 360, steps=22, settle_ms=400)
        move_cursor(page, 700, 500, steps=14, settle_ms=400)
        move_cursor(page, 700, 640, steps=14, settle_ms=400)
        page.wait_for_timeout(int(SCENES[8][1] * 500 - (time.time()-scene_t0)*1000))
        try:
            move_and_click(page, ".cfg-tab:has-text('ANALYTICS')", settle_ms=350)
            try:
                page.evaluate("const b=document.querySelector('.modal-body'); if(b) b.scrollTop=b.scrollHeight*0.55;")
            except Exception: pass
            move_cursor(page, 700, 500, steps=18, settle_ms=400)
            move_cursor(page, 1000, 600, steps=16, settle_ms=400)
        except Exception:
            page.wait_for_timeout(2000)
        park_cursor(page)
        elapsed_ms = (time.time() - scene_t0) * 1000
        remaining = SCENES[8][1] * 1000 - elapsed_ms
        if remaining > 0: page.wait_for_timeout(int(remaining))
        close_modal(page)

        # ── Scene 10: closing card ─────────────────────────────────────
        print("[10/10] Closing card")
        page.goto(closing_path.as_uri())
        install_cursor(page)
        hide_cursor(page)
        page.wait_for_timeout(SCENES[9][1] * 1000)

        # Stop recording
        page.close()
        ctx.close()
        browser.close()

    # Locate the produced webm
    webms = sorted(RAW_DIR.glob("*.webm"))
    if not webms:
        print("[!] No webm produced", file=sys.stderr); sys.exit(1)
    webm = webms[-1]
    print(f"[*] Raw recording: {webm.name} ({webm.stat().st_size//1024} KB)")

    # ── ffmpeg: webm + narration.wav → mp4 with subtitles burned in ─────
    if FINAL_MP4.exists():
        FINAL_MP4.unlink()
    sub_path = SUBS.as_posix()
    sub_for_filter = sub_path.replace(":", r"\:")
    vf = (
        f"subtitles='{sub_for_filter}'"
        f":force_style='FontName=Arial,FontSize=22,PrimaryColour=&HFFFFFFFF,"
        f"OutlineColour=&H88000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'"
    )
    # Cap total to 240 s exactly via -t.
    cmd = [
        "ffmpeg","-y",
        "-i",str(webm),
        "-i",str(NARRATION),
        "-vf", vf,
        "-map","0:v:0","-map","1:a:0",
        "-c:v","libx264","-preset","medium","-crf","28",
        "-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","128k",
        "-t","240",
        "-movflags","+faststart",
        str(FINAL_MP4),
    ]
    print("[*] Running ffmpeg (mux + burn-in)…")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stderr[-2500:], file=sys.stderr); sys.exit(1)
    size = FINAL_MP4.stat().st_size
    mb = size / (1024*1024)
    print(f"[*] Done: {FINAL_MP4.name} ({mb:.2f} MB / {size//1024} KB)")
    print(f"    Limit 100 MB: {'OK' if size <= 100*1024*1024 else 'OVER'}")

if __name__ == "__main__":
    run()
