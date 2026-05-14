"""Render (if needed) and publish ep01 to YouTube as public + immediate.

Per user direction:
  - Title: There Is No Homeless · Ch 1 Street Life · Ep 1 — John's Pain
  - Privacy: public (= "instant premier" in casual usage)
  - Copyright: © 2026 MiddleMatterMedia
  - Authors: John Matesowicz (first), then cast
  - Channel: whatever youtube_publisher's cached OAuth is set to
"""
from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, "/home/xx/claude")
from youtube_publisher.upload import upload_video, PRIVACY_PUBLIC
from youtube_publisher.credentials import pick_client_secrets

EP_DIR = Path("/mnt/d/theres_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain")
V7 = EP_DIR / "v7"
MP4 = V7 / "there_is_no_homeless_ep1_v0.4.mp4"
RENDER_SCRIPT = Path("/home/xx/claude/there_is_no_homeless/scripts/render_v7_cold_open.py")

TITLE = "There Is No Homeless · Ch 1 Street Life · Ep 1 — John's Pain"

DESCRIPTION = """\
An episode by John Matesowicz.

Starring John Matesowicz ("the guy with the dog"), with Busta Rhymes (his
service dog), Wiley, Hunter, T.K., and Obi-Wan.

There Is No Homeless · Chapter 1 — Street Life · Episode 1 — John's Pain
Mark picks John up from the hospital after a couple-week skin disease.
Three days later he goes back looking for him. Filmed in Austin, TX, May 2026.

Songs:
  Puddle — Mark Nadon (MiddleMatter Music)
  Half Grown Boy — the guy with the dog (John Matesowicz)
  Closing tracks by complexscenes6180

All editing tools and raw scaffolding are open source:
  github.com/MarkAnthonyKoop/there_is_no_homeless
  github.com/MarkAnthonyKoop  ←  the sibling tooling

Send tracks, ideas, code — help decide where this goes next.

© 2026 MiddleMatterMedia
"""

TAGS = [
    "There Is No Homeless", "Street Life", "John's Pain",
    "John Matesowicz", "Mark Nadon", "MiddleMatter Music",
    "Half Grown Boy", "Puddle", "complexscenes6180",
    "Austin Texas", "documentary", "open source",
]


def ensure_rendered() -> Path:
    """If v0.4 mp4 doesn't exist, render it using the existing script with
    the output filename swapped to v0.4."""
    if MP4.exists():
        size_mb = MP4.stat().st_size / (1024 * 1024)
        print(f"[publish] {MP4} already exists ({size_mb:.0f} MB)", flush=True)
        return MP4

    # The render script outputs v0.2ai by default — swap the constant via a sed
    # before run, then swap it back. Avoids editing the script's logic.
    text = RENDER_SCRIPT.read_text()
    swapped = text.replace("v0.2ai.mp4", "v0.4.mp4")
    if "v0.4.mp4" not in swapped:
        raise RuntimeError("could not patch render script's output filename")
    RENDER_SCRIPT.write_text(swapped)
    try:
        subprocess.run(["python3", str(RENDER_SCRIPT)], check=True)
    finally:
        RENDER_SCRIPT.write_text(text)
    if not MP4.exists():
        raise RuntimeError(f"render did not produce {MP4}")
    return MP4


def main() -> int:
    mp4 = ensure_rendered()
    print(f"[publish] uploading {mp4} → YouTube ({TITLE!r})", flush=True)
    cs = pick_client_secrets(prefer_project="677495352")
    result = upload_video(
        video_path=str(mp4),
        title=TITLE,
        description=DESCRIPTION,
        tags=TAGS,
        privacy=PRIVACY_PUBLIC,
        made_for_kids=False,
        client_secrets_path=str(cs.path),
        progress_stream=sys.stderr,
    )
    url = result.get("url") or f"https://youtu.be/{result.get('video_id')}"
    print(f"\n[publish] DONE — {url}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
