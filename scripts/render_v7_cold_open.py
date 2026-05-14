"""Render the v7 cold open + character intros for ep01.

Structure (per user's instructions, 2026-05-14):
  - Title (no narration, silence)
  - Wiley question-card → full Wiley clip (231s)
  - Hunter card → full Hunter clip (605s)
  - T.K. card → full T.K. clip (231s)
  - Busta-big + John-small + Busta backstory card → pickup (985s, John clip 1)
  - "The next day..." card → refind (171s, John clip 2)

Obi/Lance segment intentionally omitted — Lance has not given permission.

Audio bleeping of Mark's "fucks" deferred to a later pass.
Hunter AI beat overlay + BSS window shatter deferred to a later pass.

Output: /mnt/d/theres_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/v7/cold_open_test.mp4
"""
from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

EP_DIR = Path("/mnt/d/theres_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain")
V7 = EP_DIR / "v7"
V7.mkdir(parents=True, exist_ok=True)
SEGS = V7 / "segs"
SEGS.mkdir(exist_ok=True)

BLACK_SRC = EP_DIR / "working/black_1080p30_5min.mp4"
BEBAS = "/home/xx/.local/share/fonts/BebasNeue-Regular.ttf"
ELITE = "/home/xx/.local/share/fonts/SpecialElite-Regular.ttf"
PICKUP = EP_DIR / "working/pickup/pickup_20260507_graded.mp4"
REFIND = EP_DIR / "working/reunion/02_refind_20260510_2003.mp4"
PHONE = Path("/mnt/d/downloads/there_is_no_homeless")
WALGREENS_P1 = PHONE / "VID_20260510_200845459.mp4"     # 5:22, finds John, John starts singing
WALGREENS_P2 = PHONE / "VID_20260510_200845459_02.mp4"  # continuation; contains n-word ~5:17 (bleep later)
W, H, FPS = 1920, 1080, 30


@dataclass
class Line:
    text: str
    font: str = BEBAS
    size: int = 80
    color: str = "white"
    y: str = "(h-text_h)/2"          # vertical position expression
    x: str = "(w-text_w)/2"          # horizontal position expression
    fade_in: float = 1.6             # seconds — slowed ~3x from 0.5 per user
    fade_out: float = 2.4            # slowed ~3x from 0.8
    start: float = 0.0
    duration: float = 8.0            # text holds longer too


SKIP_EXISTING = True  # idempotency: don't re-render segments whose mp4 already exists


def run(cmd: list[str], *, label: str) -> None:
    print(f"[{label}] {shlex.join(cmd[:6])} ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise RuntimeError(f"{label} failed")


def _escape(text: str) -> str:
    """Escape a string for ffmpeg drawtext."""
    return (text
            .replace("\\", "\\\\")
            .replace(":", r"\:")
            .replace("'", r"\\\'")
            .replace(",", r"\,"))


def _drawtext_filter(line: Line) -> str:
    end = line.start + line.duration
    fadein_end = line.start + line.fade_in
    fadeout_start = end - line.fade_out
    alpha = (f"if(lt(t,{line.start}),0,"
             f"if(lt(t,{fadein_end}),(t-{line.start})/{line.fade_in},"
             f"if(lt(t,{fadeout_start}),1,"
             f"if(lt(t,{end}),1-(t-{fadeout_start})/{line.fade_out},0))))")
    # Commas inside the alpha expression must be escaped because the outer
    # filtergraph parser splits filters on top-level commas.
    alpha_escaped = alpha.replace(",", r"\,")
    # Also escape colons inside x/y/alpha (the option separator within a filter).
    x_escaped = line.x.replace(":", r"\:")
    y_escaped = line.y.replace(":", r"\:")
    parts = [
        f"fontfile={line.font}",
        f"text='{_escape(line.text)}'",
        f"fontcolor={line.color}",
        f"fontsize={line.size}",
        f"x={x_escaped}",
        f"y={y_escaped}",
        f"alpha='{alpha_escaped}'",
    ]
    return "drawtext=" + ":".join(parts)


def render_card(lines: list[Line], duration: float, out: Path, label: str) -> None:
    if SKIP_EXISTING and out.exists():
        print(f"[card-{label}] skip (exists)", flush=True)
        return
    chain = ",".join(_drawtext_filter(l) for l in lines)
    vf = f"scale={W}:{H},{chain}"
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-t", str(duration), "-i", str(BLACK_SRC),
        "-f", "lavfi", "-t", str(duration), "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-map", "0:v", "-map", "1:a",
        "-vf", vf,
        "-r", str(FPS),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24",
        "-preset", "ultrafast",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out),
    ]
    run(cmd, label=f"card-{label}")


def _mute_filter(ranges: list[tuple[float, float]], source_start: float) -> str | None:
    """Build a volume=0 filter for the given (start,end) mute windows.

    Ranges are in *source-clip* time; subtract source_start so they map onto
    the output's timeline.
    """
    adjusted = []
    for s, e in ranges:
        s2 = s - source_start
        e2 = e - source_start
        if e2 <= 0:
            continue
        adjusted.append((max(0.0, s2), e2))
    if not adjusted:
        return None
    enable_expr = "+".join(f"between(t\\,{s:.3f}\\,{e:.3f})" for s, e in adjusted)
    return f"volume=volume=0:enable='{enable_expr}'"


def render_vid(src: Path, source_start: float, duration: float | None,
               handle_lower: str, out: Path,
               mute_ranges: list[tuple[float, float]] | None = None) -> None:
    if SKIP_EXISTING and out.exists():
        print(f"[vid-{handle_lower}] skip (exists)", flush=True)
        return
    handle_line = Line(
        text=handle_lower, font=ELITE, size=36, color="0xdddddd",
        x="40", y="h-80",
        fade_in=0.5, fade_out=0.8, start=0.5, duration=8.0,
    )
    # Draft-quality letterbox fit (no expensive blur). Phone-vertical source
    # gets scaled to 1080 height and padded centred on a 1920x1080 black bg.
    # Swap back to blur-fill (boxblur=20:5) once structure is locked.
    vf = (
        "scale=-1:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(1920-iw)/2:0:color=black,"
        + _drawtext_filter(handle_line)
    )
    cmd = ["ffmpeg", "-y", "-ss", f"{source_start:.3f}", "-i", str(src)]
    if duration is not None:
        cmd += ["-t", str(duration)]
    cmd += [
        "-vf", vf,
        "-r", str(FPS),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24",
        "-preset", "ultrafast",
    ]
    if mute_ranges:
        af = _mute_filter(mute_ranges, source_start)
        if af:
            cmd += ["-af", af]
    cmd += [
        "-c:a", "aac", "-b:a", "192k", "-ac", "2",
        str(out),
    ]
    run(cmd, label=f"vid-{handle_lower}")


def title_lines() -> list[Line]:
    return [
        Line("THERE IS NO HOMELESS", BEBAS, 140, "white",
             y="(h-text_h)/2-160", fade_in=2.0, fade_out=2.5, start=1.5, duration=14.0),
        Line("Chapter 1  ·  Street Life", BEBAS, 64, "white",
             y="640", fade_in=2.0, fade_out=2.5, start=5.0, duration=11.0),
        Line("Episode 1  ·  John's Pain", BEBAS, 72, "white",
             y="720", fade_in=2.0, fade_out=2.5, start=7.0, duration=9.0),
    ]


def _load_bleeps() -> dict:
    p = Path(__file__).parent.parent / "bleep_ranges.json"
    if not p.exists():
        return {}
    import json as _json
    return _json.loads(p.read_text())


def main() -> None:
    seg_paths: list[Path] = []
    bleeps = _load_bleeps()

    # Per the user's "leave John's fucks" rule:
    #   - Wiley clip & Hunter politics:  bleep ALL fucks
    #   - Walgreens p1 (John already speaking by 0:02):  no fuck bleep
    #   - Walgreens p2 (all John):  no fuck bleep, but n-words muted at very end
    wiley_mutes  = [tuple(r) for r in bleeps.get("VID_20260508_082801655", {}).get("fuck", [])]
    hunter_mutes = [tuple(r) for r in bleeps.get("VID_20260508_054433020", {}).get("fuck", [])]
    walg_p2_mutes = [tuple(r) for r in bleeps.get("VID_20260510_200845459_02", {}).get("n_word", [])]

    # 01a — Title (slower fades per user)
    title = SEGS / "01a_title.mp4"
    render_card(title_lines(), duration=18.0, out=title, label="title")
    seg_paths.append(title)

    # 01a2 — Open-source bumper
    osb = SEGS / "01a2_open_source_bumper.mp4"
    render_card([
        Line("an open source project", ELITE, 70, "0xeeeeee", y="h/2-60", start=1.0, duration=9.0),
        Line("about an open source community.", ELITE, 70, "0xeeeeee", y="h/2+30", start=2.5, duration=8.0),
    ], duration=12.0, out=osb, label="opensrc-bumper")
    seg_paths.append(osb)

    # 01b — Wiley (question card)
    c = SEGS / "01b_wiley_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-260", start=0.5, duration=4.0),
        Line("Wiley?", BEBAS, 240, "white", y="(h-text_h)/2-40", start=2.0, duration=12.0),
        Line("I think he said his name was Wiley.", ELITE, 44, "0xcccccc", y="h/2+120", start=4.0, duration=10.0),
        Line("Or Texas Wiley.  Or maybe Texas.", ELITE, 44, "0xcccccc", y="h/2+180", start=5.5, duration=8.5),
        Line("Let me know in the comments.", ELITE, 44, "0xaaaaaa", y="h/2+260", start=7.0, duration=7.0),
    ], duration=15.0, out=c, label="wiley")
    seg_paths.append(c)
    v = SEGS / "01b_wiley_vid.mp4"
    render_vid(PHONE / "VID_20260508_082801655.mp4", 0.0, None, "wiley?", v,
               mute_ranges=wiley_mutes)
    seg_paths.append(v)

    # 01c — Hunter
    c = SEGS / "01c_hunter_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-160", start=0.5, duration=4.0),
        Line("hunter", BEBAS, 240, "white", y="(h-text_h)/2", start=2.0, duration=8.0),
    ], duration=10.0, out=c, label="hunter")
    seg_paths.append(c)
    v = SEGS / "01c_hunter_vid.mp4"
    render_vid(PHONE / "VID_20260508_054433020.mp4", 0.0, None, "hunter", v,
               mute_ranges=hunter_mutes)
    seg_paths.append(v)

    # 01d — T.K.
    c = SEGS / "01d_tk_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-160", start=0.5, duration=4.0),
        Line("t.k.", BEBAS, 240, "white", y="(h-text_h)/2", start=2.0, duration=8.0),
    ], duration=10.0, out=c, label="tk")
    seg_paths.append(c)
    v = SEGS / "01d_tk_vid.mp4"
    render_vid(PHONE / "VID_20260510_191046988.mp4", 0.0, None, "t.k.", v)
    seg_paths.append(v)

    # 01d2 — Obi-Wan (40s of the cowboy-hat guitar clip — verified Obie footage)
    c = SEGS / "01d2_obi_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-160", start=0.5, duration=4.0),
        Line("obi-wan", BEBAS, 240, "white", y="(h-text_h)/2", start=2.0, duration=8.0),
    ], duration=10.0, out=c, label="obi")
    seg_paths.append(c)
    v = SEGS / "01d2_obi_vid.mp4"
    render_vid(PHONE / "VID_20260501_004914722.mp4", 0.0, None, "obi-wan", v)
    seg_paths.append(v)

    # 01e — Busta (big) + John (small) + backstory + pickup
    c = SEGS / "01e_busta_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-340", start=0.5, duration=4.5),
        Line("BUSTA", BEBAS, 320, "white", y="(h-text_h)/2-120", start=2.0, duration=20.0),
        Line("…and the guy with the dog.", ELITE, 56, "0xcccccc", y="h/2+100", start=5.0, duration=17.0),
        Line("John puts his dog ahead of himself.  Busta eats first.", ELITE, 38, "0xbbbbbb", y="h/2+200", start=8.0, duration=14.0),
        Line("Busta barks short notes in time while John plays.", ELITE, 36, "0xbbbbbb", y="h/2+260", start=10.5, duration=11.5),
        Line("Someone once said, \"That dog is bustin' rhymes.\"", ELITE, 36, "0xbbbbbb", y="h/2+320", start=13.0, duration=9.0),
        Line("The name stuck.  Busta Rhymes.", ELITE, 40, "0xeeeeee", y="h/2+390", start=15.5, duration=6.5),
    ], duration=22.0, out=c, label="busta")
    seg_paths.append(c)
    pickup_intro = SEGS / "01e_pickup_intro_card.mp4"
    render_card([
        Line("John has had a skin disease for a couple weeks.", ELITE, 50, "0xdddddd", y="h/2-120", start=1.0, duration=12.0),
        Line("It was getting debilitating.  I told him to go to the hospital.", ELITE, 50, "0xdddddd", y="h/2-40", start=3.0, duration=11.0),
        Line("Here I am picking him up after he was released.", ELITE, 50, "0xdddddd", y="h/2+60", start=5.5, duration=9.0),
        Line("(maybe after only a day.)", ELITE, 38, "0xaaaaaa", y="h/2+140", start=8.0, duration=6.5),
    ], duration=15.0, out=pickup_intro, label="pickup-intro")
    seg_paths.append(pickup_intro)
    v = SEGS / "01e_pickup_vid.mp4"
    render_vid(PICKUP, 0.0, None, "the guy with the dog  ·  may 7", v)
    seg_paths.append(v)

    # 01f — "The next day..." → refind (search for John on May 10)
    c = SEGS / "01f_nextday_card.mp4"
    render_card([
        Line("the next day…", ELITE, 110, "white", y="(h-text_h)/2", start=1.0, duration=9.0),
    ], duration=11.0, out=c, label="nextday")
    seg_paths.append(c)
    v = SEGS / "01f_refind_vid.mp4"
    render_vid(REFIND, 0.0, None, "the guy with the dog  ·  may 10", v)
    seg_paths.append(v)

    # 01g — John finally texted: at Walgreens (find moment)
    c = SEGS / "01g_walgreens_intro_card.mp4"
    render_card([
        Line("John finally texted:", ELITE, 70, "0xeeeeee", y="h/2-120", start=1.0, duration=10.0),
        Line("\"I'm a f-ing idiot.  I'm at Walgreens not CVS.\"", ELITE, 60, "white", y="h/2", start=3.0, duration=10.0),
    ], duration=13.0, out=c, label="walgreens-intro")
    seg_paths.append(c)
    v1 = SEGS / "01g_walgreens_p1_vid.mp4"
    render_vid(WALGREENS_P1, 0.0, None, "the guy with the dog  ·  may 10  ·  walgreens", v1)
    seg_paths.append(v1)
    v2 = SEGS / "01g_walgreens_p2_vid.mp4"
    render_vid(WALGREENS_P2, 0.0, None, "the guy with the dog  ·  may 10  ·  walgreens (cont.)", v2,
               mute_ranges=walg_p2_mutes)
    seg_paths.append(v2)

    # Concat
    list_file = V7 / "cold_open_concat.txt"
    list_file.write_text("\n".join(f"file '{p}'" for p in seg_paths) + "\n")
    out = V7 / "cold_open_test.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(out),
    ]
    run(cmd, label="concat")
    print(f"\nDONE -> {out}")


if __name__ == "__main__":
    main()
