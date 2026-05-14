# There Is No Homeless

An open-source documentary project. Each episode is a chapter, scripted as
markdown, rendered with `ffmpeg` and the sibling tools in this org, and
published to YouTube. Filmed in Austin, TX. All editing tools, episode
scripts, and AI-generation prompts live in this repo (or its siblings) and
are open for anyone to fork, remix, or reuse.

The premise (in one sentence): **the people on Austin's streets are some of
the most articulate, talented, and considered people we've met — and
"homelessness" is not the story they're telling.**

---

## §1 What's here

- **`episodes/`** — one markdown per episode, with cast list, segment
  timeline, description copy, and AI-prompt notes. The first one is
  `ch01-street-life-ep01-johns-pain.md`.
- **`scripts/`** — `ffmpeg`-based render scripts that consume the episode
  markdown and produce the final cut. Also helpers (`find_bleep_ranges.py`,
  `extract_v6_songs.py`, `publish_v04.py`).
- **`transcripts/`** — Whisper transcripts of every source clip used in a
  published episode, organized `video/` (phone footage) and `audio/`
  (songs and standalone recordings). Word-level timestamps available on
  request.
- **`bleep_ranges.json`** — machine-readable word-level timing of every
  bleeped F-word or n-word in the published cut, in case anyone wants to
  audit the edit choices.
- **`assets/`** *(symlink, not in repo)* — raw phone footage and high-bitrate
  intermediates. **Off-repo** because they total ~10 GB. See §4.

## §2 Episodes

| # | Title | Status | YouTube |
|---|---|---|---|
| Ch1 Ep1 | *John's Pain* | published 2026-05-14 | (link will be in the repo description once live) |

## §3 How others can collaborate

We're trying to keep the bar to participation **low**. Pick any of these:

### Watch an episode and send a track
The closing songs on each episode are written by characters in it (Suno,
Reaper, garage demos — anything). If you watch Ep1 and want yours included
on Ep2, send a stem or a final mix to the discussion section of this repo
or as an issue with the `track-submission` label. Original work only; you
keep the rights, we credit you by your street-handle (or real name if you
prefer).

### Open a PR against an episode script
The episode markdowns are the source of truth for the cut. If you have a
sharper title-card line, a better caption rewrite, or a fix to the segment
timing — open a PR. The render scripts are idempotent, so we can re-cut
quickly to compare.

### Add an AI overlay
Each music segment can host an AI-generated cartoon or stinger. Prompts
live in `episodes/ai_prompts_ep01.md` (and per-episode for future ones).
Generate one in Sora/Veo/Grok, drop the MP4 in the issue, we composite.

### Build a new sibling tool
If you spot something the pipeline does badly (or doesn't do at all),
build it as a sibling repo under your own account and link it here. The
existing siblings are listed in §5.

### Be in an episode
We film a lot, only use a fraction. Permission is per-person, per-clip.
If you're in Austin and want to be in something, open an issue describing
who you are and where you hang out. We'll find you.

## §4 Raw assets — where they live

Phone footage and high-bitrate intermediates are too big for the repo
(~10 GB for Ep1 alone). They will be uploaded to **GitHub Releases** for
this repo as `ep01-raw-<clip>.mp4` (each file ≤ 2 GB).

While that's being staged, the canonical local paths on the maintainer's
machine are documented in `episodes/<episode>.md` under the relevant
`seg-XX` entries. If you need a specific clip before the release is up,
open an issue with the timestamp + episode segment and we'll DM you a
Google Drive link.

## §5 Sibling tools

| Repo | What it does |
|---|---|
| `MarkAnthonyKoop/youtube_publisher` | Tag MP4 metadata + upload to YouTube |
| `MarkAnthonyKoop/speech_transcriber` | faster-whisper wrapper, used for the transcripts under `transcripts/` |
| `MarkAnthonyKoop/video_composer` | Declarative markdown timeline → MP4 (designed for this project) |
| `MarkAnthonyKoop/suno_client` | Suno API access (the closing-set tracks are generated here) |
| `MarkAnthonyKoop/runway_client` | Runway public API client (reserved for future AI inserts) |
| `MarkAnthonyKoop/cover_art` | Procedural cover art |
| `MarkAnthonyKoop/ai_cover_art` | AI cover art (Pollinations.ai free / OpenAI paid) |
| `MarkAnthonyKoop/chrome_auth` | Pull cookies from a running Chrome (used by suno_client) |
| `MarkAnthonyKoop/computer_control` | Selenium / pyautogui / Chrome-CDP utilities |
| `MarkAnthonyKoop/github_client` | Minimal GitHub REST client with leak guardrails |

Each is its own repo, its own README, and its own license — designed to be
reusable outside this project.

## §6 Tech stack (ep1)

- **Edit**: `ffmpeg` orchestrated by `scripts/render_v7_cold_open.py`.
- **Transcription**: `faster-whisper` (distil-large-v3, GPU).
- **Music**: human-recorded (Puddle) + Suno (Ob's set, Half Grown Boy
  attributed to the artist).
- **AI overlays** (planned): Sora 2, Veo 3, Grok Imagine. Prompts pre-written.
- **Publish**: `youtube_publisher` sibling, cached OAuth.

## §7 Licensing

- **Code** (`scripts/`, render and helper Python): MIT.
- **Episode scripts and prompts** (`episodes/*.md`): CC BY-SA 4.0.
- **Transcripts** (`transcripts/`): CC BY-SA 4.0.
- **Raw video and audio assets**: per-person consent; use is limited to
  the published episode unless the depicted person grants additional rights.
  Contact maintainer for clarification.
- **Songs**:
  - *Puddle* — Mark Nadon · MiddleMatter Music.
  - *Half Grown Boy* — John Matesowicz ("the guy with the dog").
  - Closing set — Suno handle `complexscenes6180`.

If you want to use the work in a way these licenses don't cover, open an
issue and we'll figure it out.

## §8 Contact

Until we set up something nicer, use:
- Issues on this repo for technical, editorial, or participation questions.
- The cast handles inside an episode for people-specific outreach (we
  pass messages along).
- Send-it-and-see uploads under `track-submission` label for music.

## §9 Status

This is **early.** Expect breakage. Expect the markdown formats to change.
Expect the render scripts to be replaced by something cleaner. Expect us
to fail in interesting ways. PRs and patches welcome.

© 2026 MiddleMatterMedia. The works in this repo are licensed per §7.
