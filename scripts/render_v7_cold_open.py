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


def render_vid(src: Path, source_start: float, duration: float | None,
               handle_lower: str, out: Path) -> None:
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
        "-c:a", "aac", "-b:a", "192k", "-ac", "2",
        str(out),
    ]
    run(cmd, label=f"vid-{handle_lower}")


def title_lines() -> list[Line]:
    return [
        Line("THERE IS NO HOMELESS", BEBAS, 140, "white",
             y="(h-text_h)/2-160", fade_in=0.5, fade_out=1.0, start=1.0, duration=9.0),
        Line("Chapter 1  ·  Street Life", BEBAS, 64, "white",
             y="640", fade_in=1.0, fade_out=1.0, start=3.0, duration=7.0),
        Line("Episode 1  ·  John's Pain", BEBAS, 72, "white",
             y="720", fade_in=1.0, fade_out=1.0, start=4.0, duration=6.0),
    ]


def main() -> None:
    seg_paths: list[Path] = []

    # 01a — Title
    title = SEGS / "01a_title.mp4"
    render_card(title_lines(), duration=12.0, out=title, label="title")
    seg_paths.append(title)

    # 01a2 — Open-source bumper (brief teaser; the full CTA lands in end credits)
    osb = SEGS / "01a2_open_source_bumper.mp4"
    render_card([
        Line("an open source project", ELITE, 70, "0xeeeeee", y="h/2-60", start=0.4, duration=4.0),
        Line("about an open source community.", ELITE, 70, "0xeeeeee", y="h/2+30", start=1.0, duration=3.6),
    ], duration=6.0, out=osb, label="opensrc-bumper")
    seg_paths.append(osb)

    # 01b — Wiley (question card)
    c = SEGS / "01b_wiley_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-260", start=0.2, duration=2.0),
        Line("Wiley?", BEBAS, 240, "white", y="(h-text_h)/2-40", start=0.8, duration=6.5),
        Line("I think he said his name was Wiley.", ELITE, 44, "0xcccccc", y="h/2+120", start=2.0, duration=5.5),
        Line("Or Texas Wiley.  Or maybe Texas.", ELITE, 44, "0xcccccc", y="h/2+180", start=2.5, duration=5.0),
        Line("Let me know in the comments.", ELITE, 44, "0xaaaaaa", y="h/2+260", start=3.0, duration=4.5),
    ], duration=8.0, out=c, label="wiley")
    seg_paths.append(c)
    v = SEGS / "01b_wiley_vid.mp4"
    render_vid(PHONE / "VID_20260508_082801655.mp4", 0.0, None, "wiley?", v)
    seg_paths.append(v)

    # 01c — Hunter
    c = SEGS / "01c_hunter_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-160", start=0.2, duration=1.0),
        Line("hunter", BEBAS, 240, "white", y="(h-text_h)/2", start=1.0, duration=4.0),
    ], duration=5.0, out=c, label="hunter")
    seg_paths.append(c)
    v = SEGS / "01c_hunter_vid.mp4"
    render_vid(PHONE / "VID_20260508_054433020.mp4", 0.0, None, "hunter", v)
    seg_paths.append(v)

    # 01d — T.K.
    c = SEGS / "01d_tk_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-160", start=0.2, duration=1.0),
        Line("t.k.", BEBAS, 240, "white", y="(h-text_h)/2", start=1.0, duration=4.0),
    ], duration=5.0, out=c, label="tk")
    seg_paths.append(c)
    v = SEGS / "01d_tk_vid.mp4"
    render_vid(PHONE / "VID_20260510_191046988.mp4", 0.0, None, "t.k.", v)
    seg_paths.append(v)

    # 01d2 — Obi-Wan (40s of the cowboy-hat guitar clip — verified Obie footage)
    c = SEGS / "01d2_obi_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-160", start=0.2, duration=1.0),
        Line("obi-wan", BEBAS, 240, "white", y="(h-text_h)/2", start=1.0, duration=4.0),
    ], duration=5.0, out=c, label="obi")
    seg_paths.append(c)
    v = SEGS / "01d2_obi_vid.mp4"
    render_vid(PHONE / "VID_20260501_004914722.mp4", 0.0, None, "obi-wan", v)
    seg_paths.append(v)

    # 01e — Busta (big) + John (small) + backstory + pickup
    c = SEGS / "01e_busta_card.mp4"
    render_card([
        Line("introducing!", ELITE, 80, "0xcccccc", y="h/2-340", start=0.2, duration=1.5),
        Line("BUSTA", BEBAS, 320, "white", y="(h-text_h)/2-120", start=0.8, duration=10.0),
        Line("…and the guy with the dog.", ELITE, 56, "0xcccccc", y="h/2+100", start=2.0, duration=9.0),
        Line("John puts his dog ahead of himself.  Busta eats first.", ELITE, 38, "0xbbbbbb", y="h/2+200", start=3.5, duration=7.5),
        Line("Busta barks short notes in time while John plays.", ELITE, 36, "0xbbbbbb", y="h/2+260", start=4.5, duration=6.5),
        Line("Someone once said, \"That dog is bustin' rhymes.\"", ELITE, 36, "0xbbbbbb", y="h/2+320", start=5.5, duration=5.5),
        Line("The name stuck.  Busta Rhymes.", ELITE, 40, "0xeeeeee", y="h/2+390", start=6.5, duration=4.5),
    ], duration=11.5, out=c, label="busta")
    seg_paths.append(c)
    pickup_intro = SEGS / "01e_pickup_intro_card.mp4"
    render_card([
        Line("John has had a skin disease for a couple weeks.", ELITE, 50, "0xdddddd", y="h/2-120", start=0.5, duration=5.5),
        Line("It was getting debilitating.  I told him to go to the hospital.", ELITE, 50, "0xdddddd", y="h/2-40", start=1.5, duration=5.0),
        Line("Here I am picking him up after he was released.", ELITE, 50, "0xdddddd", y="h/2+60", start=2.5, duration=4.5),
        Line("(maybe after only a day.)", ELITE, 38, "0xaaaaaa", y="h/2+140", start=3.5, duration=3.5),
    ], duration=7.5, out=pickup_intro, label="pickup-intro")
    seg_paths.append(pickup_intro)
    v = SEGS / "01e_pickup_vid.mp4"
    render_vid(PICKUP, 0.0, None, "the guy with the dog  ·  may 7", v)
    seg_paths.append(v)

    # 01f — The next day...
    c = SEGS / "01f_nextday_card.mp4"
    render_card([
        Line("the next day…", ELITE, 110, "white", y="(h-text_h)/2", start=0.5, duration=4.5),
    ], duration=5.5, out=c, label="nextday")
    seg_paths.append(c)
    v = SEGS / "01f_refind_vid.mp4"
    render_vid(REFIND, 0.0, None, "the guy with the dog  ·  may 10", v)
    seg_paths.append(v)

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
