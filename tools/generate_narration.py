#!/usr/bin/env python3
"""
generate_narration.py

Renders the storyboard narration to per-scene MP3 files via Microsoft Edge
neural TTS (en-GB-RyanNeural — clean male British accent, fits NATO context).
Then concatenates them into a single 240 s narration track padded with silence
so that each scene starts at the precise timecode the SRT expects.

Outputs:
  dist/video/narration/scene_NN.mp3      # one per scene
  dist/video/narration/narration.wav     # concatenated, silence-padded, 240.0 s
  dist/video/narration/scene_durations.json
"""
import asyncio, json, subprocess, shutil
from pathlib import Path
import edge_tts

REPO = Path(__file__).resolve().parent.parent
OUT  = REPO / "dist" / "video" / "narration"
OUT.mkdir(parents=True, exist_ok=True)

VOICE = "en-GB-RyanNeural"
RATE  = "+8%"   # slight speed-up so the dense scenes fit comfortably
PITCH = "+0Hz"

# (scene index, target window seconds, narration text)
SCENES = [
    (1, 25, "C23 NAVINT is a doctrine-driven artificial-intelligence decision-superiority augmentation for Maven Smart System NATO and Allied command-and-control platforms. It is a single self-contained HTML file that runs offline on a sixteen-gigabyte tactical workstation, with no installation, no server, and no proprietary stack. Every workflow is bound to an Allied Joint Publication, with citable provenance."),
    (2, 30, "The default mission embeds the Eastern Flank illustrative scenario from the challenge statement. NATO enhanced Forward Presence battle groups in Estonia, Latvia, Lithuania and Poland. Standing NATO Maritime Group 1 in the Baltic. OPFOR forces from the Leningrad Military District, Kaliningrad and Belarus. Critical Undersea Infrastructure nodes including Estlink 2 and the Baltic Connector. Two suspect dark A-I-S vessels, named DARK ECHO 1 and DARK ECHO 2, render in red as suspect tracks."),
    (3, 25, "The Common Operating Picture fuses commercial A-I-S, OSINT, RADAR, ELINT and FUSION events into a single layer-toggleable view. The Force Tally on the left rail shows units by side and by domain, including CYBER as the fifth operational domain per A-J-P 3.20. The top bar surfaces Force Protection Condition, Chemical Biological Radiological Nuclear alert, Positioning Navigation and Timing status, and the C-I-S PACE plan."),
    (4, 25, "The Joint Targeting Cycle is fully materialised per A-J-P 3.9. The six-phase J-T-C indicator on the top bar. The Joint Prioritised Target List with High-Value, High-Payoff and Time-Sensitive Target categories, the F-2-T-2-E-A stage, Collateral Damage Estimation rating, and per-target restrictions. Restricted Target List and No-Strike List as separate lists. Every engagement decision is gated through these inputs."),
    (5, 20, "Every Course of Action that would engage a Time-Sensitive Target opens a Rules-of-Engagement authorisation modal. The modal surfaces matching T-S-Ts with their C-D-E rating, the full Restricted Target List, the No-Strike List, and an explicit Authorise or Deny decision. The Counter-U-A-S workflow per A-J-P 3.3.5 auto-triggers on radar drone detections."),
    (6, 25, "Operational wargaming runs in-platform without any external simulator. Every NATO Course of Action is matched pairwise against every OPFOR Course of Action through a deterministic seeded outcome model. The matrix is colour-coded by net score, and a best-and-worst summary highlights which adversary moves are most threatening to each friendly option. This is one of the spec's named exemplar effects."),
    (7, 25, "The cascade-effects engine is doctrine-as-code. Each second-order and third-order effect per Course of Action is driven by an editable rule that cites its source Allied Joint Publication. A-J-P 3.1 for naval interdiction. A-J-P 4.4 for movement. A-J-P 3.20 for cyber. The analyst can audit every analytical output back to the doctrinal text that produced it."),
    (8, 20, "Personnel Recovery per A-J-P 3.7 implements the five-task sequence: Reported, Located, Supported, Recovered, Reintegrated. Movement per A-J-P 3.13 and A-J-P 4.4 manages Main and Alternate Supply Routes plus Air and Sea Ports of Debarkation, status-coloured. The naval interdiction polygon is editable and renders directly on the C-O-P."),
    (9, 25, "Third-party integration is a first-order design constraint. Three documented JSON schemas plus the Master-Prompt A-I-S schema, all wrapped in a CycloneDX 1.7 envelope covering software, services, cryptography, hardware, machine-learning, operations, manufacturing and operational data. A polling live-feed adapter consumes I-S-R endpoints. A STANAG 2014 OPORD generator publishes downstream. The auto-Select-CoA function is the named seam for foundation-model substitution."),
    (10, 20, "The platform is shipped as a strictly air-gapped runtime. The dependency graph is mirrored under dist airgap vendor. A CycloneDX attestation skeleton accompanies the bundle, ready for organisational signing. Spec coverage stands at ninety-eight-point-six percent. C23 NAVINT, by CONFIANZA23 Inteligencia y Seguridad. Ready for evaluation."),
]
assert sum(t for _,t,_ in SCENES) == 240, f"target windows must sum to 240, got {sum(t for _,t,_ in SCENES)}"

async def synth_one(idx: int, text: str, out_path: Path):
    comm = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE, pitch=PITCH)
    await comm.save(str(out_path))

def ffprobe_duration(path: Path) -> float:
    res = subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(path)],
        capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def main():
    durations = []
    for idx, target, text in SCENES:
        out = OUT / f"scene_{idx:02d}.mp3"
        print(f"[*] Scene {idx:02d} (target {target} s) -> {out.name}")
        await synth_one(idx, text, out)
        d = ffprobe_duration(out)
        durations.append({"scene": idx, "target": target, "actual": d})
        print(f"    actual {d:.2f} s (target {target} s, slack {target - d:+.2f} s)")

    # Build per-scene wavs that are exactly `target` seconds long: TTS audio
    # placed at the start of the window, the rest filled with silence.
    print("[*] Building per-scene padded WAVs at exact target lengths…")
    padded_wavs = []
    for idx, target, _ in SCENES:
        src = OUT / f"scene_{idx:02d}.mp3"
        dst = OUT / f"scene_{idx:02d}_padded.wav"
        actual = ffprobe_duration(src)
        if actual >= target:
            # Speed up so it fits exactly into the window with 0.2 s margin.
            atempo = actual / max(target - 0.2, 1.0)
            atempo = min(atempo, 1.5)  # atempo allowed range, but stays natural < 1.25
            print(f"    scene {idx:02d}: TTS {actual:.2f}s > {target}s window, atempo={atempo:.3f}")
            cmd = ["ffmpeg","-y","-i",str(src),
                   "-filter:a", f"atempo={atempo}",
                   "-ar","48000","-ac","2",
                   str(dst)]
        else:
            # Pad trailing silence to reach exactly `target` seconds.
            cmd = ["ffmpeg","-y","-i",str(src),
                   "-af", f"apad=pad_dur={target-actual:.3f}",
                   "-t", f"{target}",
                   "-ar","48000","-ac","2",
                   str(dst)]
        subprocess.run(cmd, check=True, capture_output=True)
        padded_wavs.append(dst)

    # Concatenate
    print("[*] Concatenating to narration.wav…")
    concat_list = OUT / "_concat.txt"
    concat_list.write_text("\n".join(f"file '{w.as_posix()}'" for w in padded_wavs), encoding="utf-8")
    final = OUT / "narration.wav"
    cmd = ["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat_list),
           "-c","copy", str(final)]
    subprocess.run(cmd, check=True, capture_output=True)
    total = ffprobe_duration(final)
    print(f"[*] narration.wav: {total:.3f} s (target 240.000 s)")

    (OUT / "scene_durations.json").write_text(json.dumps(durations, indent=2), encoding="utf-8")
    print("[*] Done.")

if __name__ == "__main__":
    asyncio.run(main())
