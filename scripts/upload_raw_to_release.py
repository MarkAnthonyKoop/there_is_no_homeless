"""Upload raw video assets used in ep01 to a GitHub Release.

GitHub Releases support 2GB-per-file uploads with no repo-size impact —
the right home for the ~10 GB of source footage that won't fit in git.

Run this from a session with bandwidth (it'll be slow). It creates a
release tagged v0.4-raw on this repo, and uploads each phone clip plus
the final published mp4 as release assets.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import requests

REPO = "MarkAnthonyKoop/there_is_no_homeless"
TAG = "v0.4-raw"
RELEASE_NAME = "Ep1 raw assets (v0.4)"
RELEASE_BODY = """\
Source phone footage + the published v0.4 cut.

This release exists because these files (~10 GB) are too large for the
repo proper. Per-file sizes range from 98 MB to 3.3 GB; all under
GitHub's 2 GB/file release-asset limit.

Each file's role is documented in
`episodes/ch01-street-life-ep01-johns-pain.md`.
"""

CRED_FILE = Path.home() / ".git-credentials"
PHONE = Path("/mnt/d/downloads/there_is_no_homeless")
EP_DIR = Path("/mnt/d/theres_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain")

ASSETS = [
    # (path, upload_name) — upload_name avoids spaces and stays under GitHub's filename limits.
    (PHONE / "VID_20260508_082801655.mp4", "wiley_VID_20260508_082801655.mp4"),
    (PHONE / "VID_20260508_054433020.mp4", "hunter_politics_VID_20260508_054433020.mp4"),
    (PHONE / "VID_20260508_051020881.mp4", "hunter_beats_VID_20260508_051020881.mp4"),
    (PHONE / "VID_20260510_191046988.mp4", "tk_VID_20260510_191046988.mp4"),
    (PHONE / "VID_20260501_004914722.mp4", "obi_VID_20260501_004914722.mp4"),
    (PHONE / "VID_20260510_200845459.mp4",    "walgreens_p1_VID_20260510_200845459.mp4"),
    (PHONE / "VID_20260510_200845459_02.mp4", "walgreens_p2_VID_20260510_200845459_02.mp4"),
    (EP_DIR / "working/pickup/pickup_20260507_graded.mp4", "pickup_graded.mp4"),
    (EP_DIR / "working/reunion/02_refind_20260510_2003.mp4", "refind.mp4"),
    (EP_DIR / "v7/there_is_no_homeless_ch1_street_life_ep1_johns_pain_v0.4.mp4",
     "there_is_no_homeless_ep1_v0.4.mp4"),
]


def _token() -> str:
    for line in CRED_FILE.read_text().splitlines():
        if "github.com" in line:
            return line.split("://", 1)[1].split(":", 1)[1].split("@", 1)[0]
    raise RuntimeError(f"no GitHub token in {CRED_FILE}")


def get_or_create_release(token: str) -> dict:
    h = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    r = requests.get(f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}", headers=h)
    if r.status_code == 200:
        print(f"reusing release {TAG}", flush=True)
        return r.json()
    print(f"creating release {TAG}", flush=True)
    r = requests.post(
        f"https://api.github.com/repos/{REPO}/releases",
        headers=h,
        json={"tag_name": TAG, "name": RELEASE_NAME, "body": RELEASE_BODY,
              "draft": False, "prerelease": False},
    )
    r.raise_for_status()
    return r.json()


def upload_asset(release: dict, src: Path, name: str, token: str) -> None:
    upload_url = release["upload_url"].split("{")[0]
    # Skip if same name already attached.
    for a in release.get("assets", []):
        if a["name"] == name:
            print(f"  {name}: already uploaded ({a['size'] // 1024 // 1024} MB) — skipping",
                  flush=True)
            return
    size = src.stat().st_size
    print(f"  uploading {name} ({size // 1024 // 1024} MB) ...", flush=True)
    with src.open("rb") as f:
        r = requests.post(
            upload_url,
            params={"name": name},
            headers={
                "Authorization": f"token {token}",
                "Content-Type": "video/mp4",
                "Content-Length": str(size),
            },
            data=f,
            timeout=None,
        )
    if r.status_code >= 400:
        print(f"  ERROR {r.status_code}: {r.text[:300]}", flush=True)
        return
    print(f"  done: {r.json().get('browser_download_url')}", flush=True)


def main() -> int:
    token = _token()
    release = get_or_create_release(token)
    print(f"release: {release['html_url']}\n", flush=True)
    for src, name in ASSETS:
        if not src.exists():
            print(f"  SKIP (missing): {src}", flush=True)
            continue
        upload_asset(release, src, name, token)
    print(f"\nrelease URL: {release['html_url']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
