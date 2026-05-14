# there_is_no_homeless

A documentary / episode-publishing project. Each episode is a chapter+number under
`episodes/`, scripted and shipped as a YouTube video with an AI-overlay intro,
field footage, and a song outro.

Heavy media (raw recordings, working files, finals) lives on the **D: drive** to
keep `C:` from filling up. The on-disk layout for each episode mirrors a normal
post-production cut.

## State as of 2026-05-12

The raw data is on disk and partial transcription has started — **do not
re-pull the phone or re-run transcription that's already complete.**

- **Phone videos** (132 × mp4, 9.6 h, ~74 GB) are at
  `/mnt/d/downloads/there_is_no_homeless/`. The asset symlink under
  `assets/` points to a sibling dir `/mnt/d/there_is_no_homeless/` that's
  still mostly empty — the ingest move hasn't happened yet.
- **Sound recordings** (151 × m4a, 7.4 GB) are at
  `/mnt/c/Users/x/Documents/Sound recordings/`. The most recent 5 are
  transcribed. `Recording (140).m4a` is the episode-1 narration; `ez.m4a`
  is the "ez pz" marker file.
- **WhatsApp re-encodes** (5 × mp4) are at
  `…/there_is_no_homeless/whatsapp/` — all 5 transcribed.
- **Per-source transcripts, manifest, database, and dedup tooling** all
  live under `/mnt/d/downloads/there_is_no_homeless/transcriptions/`,
  which has its **own** `README.md` and `CLAUDE.md`. Read those before
  touching transcripts.
- **WhatsApp ↔ phone-video dedup tool is written but not yet run.** Phone-side
  video transcription is gated on that.

---

## §1 User manual

```bash
# the project root has scripts; assets are a symlink to /mnt/d/there_is_no_homeless
cd ~/claude/there_is_no_homeless

# pull whatever's currently on the tethered phone (audio + video + DCIM)
python3 -m scripts.phone_backup            # → /mnt/d/phone_backups/<phone>/<date>/

# transcribe the N most-recent sound recordings (driver lives in transcriptions/)
cd /mnt/d/downloads/there_is_no_homeless/transcriptions
python3 tools/transcribe_recent/main.py \
    --source "/mnt/c/Users/x/Documents/Sound recordings" \
    --output audio --ext m4a --count 5

# rebuild the human-facing transcription database
python3 tools/build_database/main.py        # writes transcriptions/database.md

# decide which WhatsApp videos are re-encodes of phone clips
python3 tools/compare_videos/main.py \
    --whatsapp /mnt/d/downloads/there_is_no_homeless/whatsapp \
    --phone    /mnt/d/downloads/there_is_no_homeless

# search transcripts for a phrase (the "ez pz" file says "easy peasy" in audio)
grep -irn "easy" /mnt/d/downloads/there_is_no_homeless/transcriptions/audio/

# render the episode (compose-from-markdown — see "Episode build" below)
python3 -m video_composer outline   episodes/<id>.md   # human-readable timeline summary
python3 -m video_composer render    episodes/<id>.md   # → final MP4 path on stdout

# fill any [GAP] segments with AI-generated b-roll
python3 -m video_composer gaps      episodes/<id>.md --json > /tmp/gaps.json
python3 -m runway_client batch      /tmp/gaps.json     # → {seg-id: /mnt/d/.../seg-id.mp4}
# paste the returned paths back into the matching segments as `runway_result:` and re-render

# upload the final cut to YouTube + back assets up to Drive    (TODO: scripts.publish_episode)
python3 -m scripts.publish_episode ch01-street-life-ep01-johns-pain
```

## §2 Reference

### Layout
```
~/claude/there_is_no_homeless/         project root (code + this doc)
├── README.md                           this file
├── CLAUDE.md                           AI norms
├── episodes/                           one .md per episode (script, credits, decisions)
│   └── ch01-street-life-ep01-johns-pain.md
├── scripts/                            phone_backup, etc. (most still TODOs)
├── ai_overlay/                         intro-narration audio + simple "title card" video gen
└── assets -> /mnt/d/there_is_no_homeless
                                        symlink — heavy media lives here (mostly empty so far)
```

```
/mnt/d/there_is_no_homeless/
└── episodes/
    └── ch01-street-life-ep01-johns-pain/
        ├── raw/audio/                  (ingest dest; not yet populated)
        ├── raw/video/                  (ingest dest; not yet populated)
        ├── working/                    transcripts, trimmed clips, intermediate renders
        └── final/                      final MP4 + thumbnail + description
```

```
/mnt/d/downloads/there_is_no_homeless/      where the data actually lives right now
├── VID_YYYYMMDD_HHMMSS_*.mp4           132 phone videos (~74 GB, 9.6 h)
├── IMG_*.jpg                           46 phone photos
├── whatsapp/                           5 WhatsApp re-encodes (mostly dupes of phone clips)
└── transcriptions/                     transcripts + tools + database (own README + CLAUDE.md)
    ├── audio/                          per-recording transcripts (.json + .md)
    ├── video_whatsapp/
    ├── video_phone/                    (planned, after dedup)
    ├── tools/
    │   ├── transcribe_recent/
    │   ├── build_database/
    │   └── compare_videos/
    ├── database.md                     human-readable index + summary
    └── manifest.jsonl                  append-only record per transcript
```

```
/mnt/c/Users/x/Documents/Sound recordings/   Windows Voice Recorder app store
    151 × Recording (NNN).m4a + a few renamed favorites (ez.m4a, etc.)
```

### Episodes

| ID | Chapter | Title |
|----|---------|-------|
| ch01-street-life-ep01-johns-pain | Street Life | John's Pain |

### Credentials in use
- **YouTube + Drive** OAuth: `~/.cache/youtube_publisher/token_677495352.pickle`
  (already includes `youtube.upload` + `drive.file` from the Fog release).

## §3 Architecture

Pure orchestration. Each leaf concern is in (or will be split into) a sibling
under `~/claude/`:

- `video_composer/` — episode markdown → final MP4 (parser + ffmpeg + sha1 cache)
- `runway_client/` — AI b-roll for `[GAP]` segments (text → image → motion clip)
- `speech_transcriber/` — faster-whisper transcripts of pulled audio and master mix
- `youtube_publisher/` — final MP4 → YouTube
- `ai_cover_art/` — title-card / thumbnail
- `computer_control/` — for any screen capture / UI driving
- `audio_metadata/` (planned) — tagging

This project's scripts only **compose** those siblings; they do not implement
audio/video transforms inline. If a script grows past ~150 lines, that's the
signal it should be split into a sibling.

### Episode build (video_composer-driven)

Each episode `.md` has TWO halves:
1. **The human document at the top** — outline, transcripts, credits, open
   decisions, description draft. This is for *you*.
2. **A `## Timeline` section with YAML frontmatter and `### seg-NN` blocks** —
   this is what `video_composer` actually reads.

See `~/claude/video_composer/README.md` §1 for the timeline schema. The
frontmatter (`master_audio`, `fps`, `resolution`) lives **inside** the
`## Timeline` section as its own YAML block — keep it separate from the
narrative top of the file so editing prose doesn't risk breaking the parser.

The phone-pull and ADB-Wi-Fi workaround live in `scripts/phone_backup.py` and
`scripts/setup_wireless_adb.md` — see `CLAUDE.md` for the why.

### Where transcription work lives

The transcript / manifest / database / dedup tooling is a self-contained
subtree under `/mnt/d/downloads/there_is_no_homeless/transcriptions/`. It
has its own [`README.md`](../../mnt/d/downloads/there_is_no_homeless/transcriptions/README.md)
and [`CLAUDE.md`](../../mnt/d/downloads/there_is_no_homeless/transcriptions/CLAUDE.md).
That tree is a **build artifact** — every file in it can be regenerated
from the raw media plus the `speech_transcriber/` sibling.
