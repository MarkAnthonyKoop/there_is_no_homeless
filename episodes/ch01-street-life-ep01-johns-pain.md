---
episode: ch01-ep01
master_audio: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/master_v5.wav
fps: 30
resolution: 1920x1080
output: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/v6/ep01.mp4
fonts:
  display: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
  typewriter: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
---

# Chapter 1 — Street Life · Episode 1 — John's Pain

**Series:** *There Is No Homeless*
**Artist / channel:** Mark Nadon · MiddleMatter Music
**Runtime:** ~1h 15min

---

## Premise

Three days in May 2026. On May 7, Mark picks John up from the hospital — John
covered in lesions from a "skin infection" the doctors won't name. Three days
later, on May 10, Mark goes back to find him. John has moved camps. By the
time Mark finds him, John has spent the afternoon writing songs on Suno — and
plays them for the camera. The episode ends with *Puddle* (Mark Nadon),
*Half Grown Boy* (John MacLellan), and a set of Ob's Suno tracks from the
same week.

---

## Cast (handles only — see Description for full-name credit)

- **the guy with the dog** — subject of the episode ("Half Grown Boy")
- **busta** — the guy with the dog's service dog
- **obiwana**, **hunter**, **t.k.** — cold-open intros (in narration)
- **juliet** — house-shows organizer; interviews characters
- **streetlife guy** — featured short interview (camp → job → apartment → woods); coins the word "streetlifers"
- **mark nadon** — narrator, driver, recordist
- **complexscenes6180** — Suno handle credited on the closing 10 tracks
- *editing:* mark nadon + claude code

Real names appear only in:
1. YouTube metadata (full name as the episode subject)
2. The closing star-credit ("starring …")
3. Author/episode-credit ("an episode by …")
No real names anywhere on-screen otherwise.

---

## Description

> **There Is No Homeless · Chapter 1 — Street Life · Episode 1 — John's Pain**
>
> Mark picks John up from the hospital. Three days later, he goes back.
> An episode by **John Matesowicz**.
>
> 0:00  Cold open · introducing obiwana, hunter, t.k., the guy with the dog
> 3:33  Looking for the guy with the dog (May 10)
> 8:28  Picking him up from the hospital (May 7) — featuring John Matesowicz
> 24:53 The reunion — Half Grown Boy and the other Suno songs
> 35:33.74 *Puddle* — Mark Nadon (MiddleMatter Music)
> 39:24.74 *Half Grown Boy* — the guy with the dog (John Matesowicz)
> 43:49.34 *Some stuff Ob was working on tonight* — 10 tracks by `complexscenes6180`
>
> Music: *Puddle* by Mark Nadon; *Half Grown Boy* by John Matesowicz;
> closing set by Suno handle `complexscenes6180`.
> Filmed in Austin, TX, May 2026.
>
> All editing tools and the raw footage are open source —
> github.com/markanthonykoop
>
> Edited by Claude Code + Mark Nadon. Starring John Matesowicz.

## Build state

- [x] Phone pull complete — `/mnt/d/downloads/there_is_no_homeless/`
- [x] Field footage transcribed
- [x] Master audio mixed (75:11 — narration · hunt · refind · pickup · reunion · puddle · HGB · 10× ob)
- [x] v1 render — pillarboxed portrait clips
- [x] v2 render — blur-fill for portrait clips
- [x] v3 render — colour-graded pickup, John credit fix
- [ ] **v4 — IN PROGRESS** (this file). Changes vs v3:
  - cold open split into `seg-01a…01e` with **introducing!** + handle reveals (Special Elite + Bebas Neue)
  - all real names removed from on-screen text except John Matesowicz in star/author credits
  - Puddle credits rewritten handles-only
  - HGB credit changed to handle `the guy with the dog`
  - GitHub open-source notice appended to seg-18
- [ ] master_audio remix: insert juliet self-intro · streetlife-guy arc · strip 2s n-word from talk_p2 · drop-C# power-chord stinger × 4 over the intro cards
- [ ] HGB animated cartoon (replaces static still in seg-08)
- [ ] Puddle cartoon-mark lip-sync intro (prefix of seg-07)
- [ ] Thumbnail finalized
- [ ] Upload (YouTube)

## Timeline

### seg-01a · 0:00:00-0:00:42.00
# Title card; full 42s of Mark's opening narration plays over it.
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "THERE IS NO HOMELESS"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 140
    pos: center
    fade_in: 1.5
    fade_out: 1.0
    start: 1.0
    duration: 8.0
  - text: "Chapter 1  ·  Street Life"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 64
    pos: "(w-text_w)/2,640"
    fade_in: 1.0
    fade_out: 1.0
    start: 3.0
    duration: 6.0
  - text: "Episode 1  ·  John's Pain"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 72
    pos: "(w-text_w)/2,720"
    color: "#dddddd"
    fade_in: 1.0
    fade_out: 1.0
    start: 4.0
    duration: 6.0
  - text: "narrator: mark nadon"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 36
    color: "#888888"
    pos: bottom-center
    fade_in: 0.5
    fade_out: 0.8
    start: 14.0
    duration: 5.0

### seg-01b_card · 0:00:42.00-0:00:47.00
# 5s reveal card; chord-hit lands at 0:43.0 = 1.0s into segment.
# Mark's narration line at 00:43: "This guy here is Obiwana."
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "introducing!"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 80
    color: "#cccccc"
    pos: "(w-text_w)/2,h/2-160"
    fade_in: 0.4
    fade_out: 0.3
    start: 0.2
    duration: 0.8
  - text: "obiwana"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 240
    pos: center
    fade_in: 0.05
    fade_out: 1.5
    start: 1.0
    duration: 4.0

### seg-01b_vid · 0:00:47.00-0:01:03.00
# Obiwana on camera. Mark's narration plays over. Source-start picked so the
# "John the Fisherman and Obi-Wan Kenobi" line (clip[31:04]) lands ~ep[01:00].
source: /mnt/d/downloads/there_is_no_homeless/VID_20260430_172504884.mp4
source_start: 30:30
fill: blur
overlays:
  - text: "obiwana"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 36
    color: "#dddddd"
    pos: bottom-left
    fade_in: 0.5
    fade_out: 0.8
    start: 0.5
    duration: 8.0

### seg-01c_card · 0:01:03.00-0:01:08.00
# 5s reveal card; chord-hit at ep[01:04] = 1.0s into segment.
# Mark's narration at 01:06: "This is Hunter."
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "introducing!"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 80
    color: "#cccccc"
    pos: "(w-text_w)/2,h/2-160"
    fade_in: 0.4
    fade_out: 0.3
    start: 0.2
    duration: 0.8
  - text: "hunter"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 240
    pos: center
    fade_in: 0.05
    fade_out: 1.5
    start: 1.0
    duration: 4.0

### seg-01c_vid · 0:01:08.00-0:01:50.00
# Hunter on camera. Source-start picked so "what's your utopia, Hunter?"
# (clip[03:53]) lands ~ep[01:31], which slots between the narrator's intro line
# at ep[01:06] and the next character intro at ep[01:51].
source: /mnt/d/downloads/there_is_no_homeless/VID_20260508_054433020.mp4
source_start: 3:30
fill: blur
overlays:
  - text: "hunter"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 36
    color: "#dddddd"
    pos: bottom-left
    fade_in: 0.5
    fade_out: 0.8
    start: 0.5
    duration: 8.0

### seg-01d_card · 0:01:50.00-0:01:55.00
# 5s reveal card; chord-hit at ep[01:51] = 1.0s into segment.
# Mark's narration at 01:51: "And this crazy guy is T.K."
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "introducing!"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 80
    color: "#cccccc"
    pos: "(w-text_w)/2,h/2-160"
    fade_in: 0.4
    fade_out: 0.3
    start: 0.2
    duration: 0.8
  - text: "t.k."
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 240
    pos: center
    fade_in: 0.05
    fade_out: 1.5
    start: 1.0
    duration: 4.0

### seg-01d_vid · 0:01:55.00-0:02:30.00
# T.K. on camera. Source-start so "What's your name? — TK." (clip[03:35])
# lands ~ep[02:30], aligning his self-intro with end of this segment / lead
# into seg-01e.
source: /mnt/d/downloads/there_is_no_homeless/VID_20260510_191046988.mp4
source_start: 3:00
fill: blur
overlays:
  - text: "t.k."
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 36
    color: "#dddddd"
    pos: bottom-left
    fade_in: 0.5
    fade_out: 0.8
    start: 0.5
    duration: 8.0

### seg-01e_card · 0:02:30.00-0:02:36.00
# 6s reveal card (longer for the dual-line reveal).
# Mark's narration at 02:31: "I pick up John from the hospital."
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "introducing!"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 80
    color: "#cccccc"
    pos: "(w-text_w)/2,h/2-200"
    fade_in: 0.4
    fade_out: 0.3
    start: 0.2
    duration: 0.8
  - text: "the guy with the dog"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 180
    pos: center
    fade_in: 0.05
    fade_out: 1.5
    start: 1.0
    duration: 5.0
  - text: "and his service dog, busta"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 48
    color: "#bbbbbb"
    pos: "(w-text_w)/2,h/2+120"
    fade_in: 0.6
    fade_out: 1.0
    start: 2.5
    duration: 3.0

### seg-01e_vid · 0:02:36.00-0:03:32.92
# Guy-with-dog on camera. Pickup clip @1:00 skips the verbal "we're here with
# John" intro and goes into him talking.
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/pickup/pickup_20260507_graded.mp4
source_start: 1:00
fill: blur
overlays:
  - text: "the guy with the dog  ·  may 7"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 36
    color: "#dddddd"
    pos: bottom-left
    fade_in: 0.5
    fade_out: 0.8
    start: 0.5
    duration: 8.0


### seg-02 · 0:03:32.92-0:05:36.72
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/reunion/01_hunt_20260510_2001.mp4
source_start: 0:00
fill: blur
overlays:
  - text: "Three days later — may 10. looking for the guy with the dog."
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 40
    pos: bottom-left
    color: "#e8e8e8"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 5.0

### seg-03 · 0:05:36.72-0:08:27.75
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/reunion/02_refind_20260510_2003.mp4
source_start: 0:00
fill: blur

### seg-04 · 0:08:27.75-0:24:52.83
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/pickup/pickup_20260507_graded.mp4
source_start: 0:00
fill: blur
overlays:
  - text: "may 7 — the pickup."
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 40
    pos: bottom-left
    color: "#e8e8e8"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 6.0

### seg-05 · 0:24:52.83-0:30:15.10
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/reunion/03_songs_20260510_2008.mp4
source_start: 0:00
fill: blur
overlays:
  - text: "may 10 — the guy with the dog plays his suno songs."
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 40
    pos: bottom-left
    color: "#e8e8e8"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 6.0

### seg-06a · 0:30:15.10-0:35:31.60
# Bus story up to slur. Visual cuts at clip[5:16.5]; audio splice in master_v5.
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/reunion/04_talk_20260510_2008_p2.mp4
source_start: 0:00
fill: blur

### seg-06b · 0:35:31.60-0:35:33.74
# 2.14s tail after slur — clip's last natural beat ("No, that wouldn't afford.").
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/reunion/04_talk_20260510_2008_p2.mp4
source_start: 5:20.00
fill: blur

### seg-07 · 0:35:33.74-0:39:24.74
# Puddle. PLANNED: open with AI cartoon-mark video lip-syncing "insane,
# get out of my membrane" (~6-8s), cross-fade to black, then handle-only
# credits scroll in. Real names only where flagged.
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "puddle"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 180
    pos: center
    fade_in: 1.0
    fade_out: 1.0
    start: 10.0      # held back so the cartoon-mark intro can land first
    duration: 10.0
  - text: "music & vocals: mark nadon  ·  middlematter music"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 44
    pos: "(w-text_w)/2,640"
    color: "#cccccc"
    fade_in: 1.0
    fade_out: 1.0
    start: 12.0
    duration: 8.0
  # ---- handle-only end-credits roll-in (last ~30s of Puddle) ----
  - text: "starring"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 36
    color: "#777777"
    pos: "(w-text_w)/2,460"
    fade_in: 0.5
    fade_out: 1.0
    start: 198.0
    duration: 28.0
  - text: "the guy with the dog"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 84
    pos: "(w-text_w)/2,520"
    color: "#eeeeee"
    fade_in: 0.6
    fade_out: 1.0
    start: 198.5
    duration: 28.0
  - text: "and busta"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 40
    color: "#bbbbbb"
    pos: "(w-text_w)/2,620"
    fade_in: 0.6
    fade_out: 1.0
    start: 200.0
    duration: 26.0
  - text: "with: obiwana  ·  hunter  ·  t.k.  ·  juliet  ·  streetlife guy"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 34
    color: "#999999"
    pos: "(w-text_w)/2,720"
    fade_in: 0.6
    fade_out: 1.0
    start: 204.0
    duration: 22.0
  - text: "filmed & narrated: mark nadon"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 30
    color: "#888888"
    pos: "(w-text_w)/2,820"
    fade_in: 0.5
    fade_out: 1.0
    start: 207.0
    duration: 19.0
  - text: "edited: claude code  ·  mark nadon"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 30
    color: "#888888"
    pos: "(w-text_w)/2,860"
    fade_in: 0.5
    fade_out: 1.0
    start: 209.0
    duration: 17.0
  - text: "an episode by john matesowicz"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 32
    color: "#aaaaaa"
    pos: "(w-text_w)/2,920"
    fade_in: 0.5
    fade_out: 1.0
    start: 211.0
    duration: 15.0
  - text: "there is no homeless  ·  ch 1  ·  ep 1"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 28
    color: "#666666"
    pos: bottom-center
    fade_in: 0.5
    fade_out: 1.0
    start: 215.0
    duration: 10.0

### seg-08 · 0:39:24.74-0:43:49.34
# Half Grown Boy. PLANNED: replace the static cartoon image with an animated
# cartoon video timed to the 4:24 song — story arc: busking → people gather and
# start moving to the music → his eyes go kaleidoscopic → he floats up with
# busta → dog-games in the sky while he keeps playing/singing → land. Must
# resemble the real John (reference frames in working/john_stills/).
# Until generated: keep the existing static frame as a placeholder.
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - image: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/hgb/cartoon_john_busking_v2.jpg
    pos: center
    fade_in: 1.5
    fade_out: 1.0
    start: 0.0
  - text: "half grown boy"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 120
    pos: "(w-text_w)/2,80"
    fade_in: 1.0
    fade_out: 1.0
    start: 1.5
    duration: 12.0
  - text: "the guy with the dog"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 56
    color: "#cccccc"
    pos: "(w-text_w)/2,220"
    fade_in: 1.0
    fade_out: 1.0
    start: 2.5
    duration: 12.0

### seg-09 · 0:43:49.34-0:47:18.14
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "Some stuff Ob was working on tonight"
    size: 56
    pos: center
    color: "#cccccc"
    fade_in: 1.0
    fade_out: 1.0
    start: 0.5
    duration: 8.0
  - text: "1 / 10  —  Brass Tongue Prayer  (take 2)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 8.0
    duration: 12.0

### seg-10 · 0:47:18.14-0:50:16.22
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "2 / 10  —  Brass Tongue Prayer  (take 1)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0

### seg-11 · 0:50:16.22-0:53:03.58
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "3 / 10  —  Brine Gospel Crackle  (take 2)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0

### seg-12 · 0:53:03.58-0:56:16.78
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "4 / 10  —  Brine Gospel Crackle  (take 1)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0

### seg-13 · 0:56:16.78-0:59:31.58
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "5 / 10  —  Sawdust Salvation  (take 2)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0

### seg-14 · 0:59:31.58-1:02:36.42
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "6 / 10  —  Sawdust Salvation  (take 1)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0

### seg-15 · 1:02:36.42-1:05:21.94
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "7 / 10  —  Cypress Ashes  (take 2)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0

### seg-16 · 1:05:21.94-1:08:31.54
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "8 / 10  —  Cypress Ashes  (take 1)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0

### seg-17 · 1:08:31.54-1:11:43.82
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "9 / 10  —  Smokestack Gospel  (take 2)"
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0

### seg-18 · 1:11:43.82-1:15:08.54
source: /mnt/d/there_is_no_homeless/episodes/ch01-street-life-ep01-johns-pain/working/black_1080p30_5min.mp4
source_start: 0:00
overlays:
  - text: "10 / 10  —  Smokestack Gospel  (take 1)"
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 40
    pos: bottom-center
    color: "#888888"
    fade_in: 0.5
    fade_out: 0.5
    start: 0.5
    duration: 12.0
  # ---- open-source notice toward the end of the last track ----
  - text: "every tool used to make this video is open source."
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 42
    color: "#cccccc"
    pos: "(w-text_w)/2,440"
    fade_in: 1.0
    fade_out: 1.0
    start: 160.0
    duration: 18.0
  - text: "so is the raw footage."
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 42
    color: "#cccccc"
    pos: "(w-text_w)/2,500"
    fade_in: 1.0
    fade_out: 1.0
    start: 163.0
    duration: 15.0
  - text: "github.com/markanthonykoop"
    font: /home/xx/.local/share/fonts/BebasNeue-Regular.ttf
    size: 80
    color: "#eeeeee"
    pos: "(w-text_w)/2,600"
    fade_in: 1.0
    fade_out: 1.5
    start: 166.0
    duration: 22.0
  - text: "fin."
    font: /home/xx/.local/share/fonts/SpecialElite-Regular.ttf
    size: 96
    pos: center
    color: "#cccccc"
    fade_in: 1.5
    fade_out: 2.0
    start: 196.0
    duration: 8.0
