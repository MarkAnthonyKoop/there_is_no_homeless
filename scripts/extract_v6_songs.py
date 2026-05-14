"""Extract song segments from v6/ep01.mp4 for reuse in v7.

User's new song order: Puddle -> Obi's 10 tracks -> Half Grown Boy.
v6's order was: Puddle -> HGB -> Obi's 10 tracks; we reorder via concat.

Uses -c copy so encoding stays untouched (fast and lossless).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

EP_DIR = Path("/mnt/d/theres_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain")
SRC = EP_DIR / "v6/ep01.mp4"
OUT = EP_DIR / "v7/songs"
OUT.mkdir(parents=True, exist_ok=True)

# Per ch01-street-life-ep01-johns-pain.md timeline (seg-07..18).
EXTRACTS = [
    # (label,           start_s,    end_s)
    ("01_puddle",       35 * 60 + 33.74,  39 * 60 + 24.74),
    ("02_hgb",          39 * 60 + 24.74,  43 * 60 + 49.34),
    ("03_obi_t01",      43 * 60 + 49.34,  47 * 60 + 18.14),
    ("04_obi_t02",      47 * 60 + 18.14,  50 * 60 + 16.22),
    ("05_obi_t03",      50 * 60 + 16.22,  53 * 60 + 3.58),
    ("06_obi_t04",      53 * 60 + 3.58,   56 * 60 + 16.78),
    ("07_obi_t05",      56 * 60 + 16.78,  59 * 60 + 31.58),
    ("08_obi_t06",      59 * 60 + 31.58,  62 * 60 + 36.42),
    ("09_obi_t07",      62 * 60 + 36.42,  65 * 60 + 21.94),
    ("10_obi_t08",      65 * 60 + 21.94,  68 * 60 + 31.54),
    ("11_obi_t09",      68 * 60 + 31.54,  71 * 60 + 43.82),
    ("12_obi_t10",      71 * 60 + 43.82,  75 * 60 + 8.54),
]


def extract(label: str, start: float, end: float) -> Path:
    out = OUT / f"{label}.mp4"
    duration = end - start
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{start:.3f}",
        "-i", str(SRC),
        "-t", f"{duration:.3f}",
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        raise RuntimeError(f"extract {label} failed")
    return out


def main() -> None:
    for label, s, e in EXTRACTS:
        out = extract(label, s, e)
        print(f"  {label}: {out.stat().st_size // 1024 // 1024} MB  ({e-s:.1f}s)")
    print(f"\nAll extracts -> {OUT}")


if __name__ == "__main__":
    main()
