# HOW DOES IT WORK? — nightly runbook (owner direction 2026-11-16, overrides the WHAT IF / Jeremy notes)

**3 videos a day**, posted at **12:00, 15:30 and 19:00 Asia/Shanghai (+08:00)** on TikTok, Instagram and YouTube via Buffer.
**No Jeremy.** Narrated (Kokoro `af_heart`), build-captions, 2.5D "lab" look. The Timeless instrumental plays **very quietly**
under the voice (owner wants it subtle). Everything renders here in the cloud.


## ★ STANDARD FORMAT from 2026-11-17 (owner approved, reference: `episodes/hiw04_dandruff`)
**"What is this?"** — every video now follows this shape (it overrides the older 55 s structure):
- **Hook 0–2 s:** an extreme, unrecognisable close-up of something everyday, boxed with a Figma selection box, voice
  "What is this?" (or a close variant). **Reveal at ~2 s** with a fast zoom out ("It's dandruff. Up close.").
- **A visual shift every ~2 s:** zoom in/out, cut to a new set, pill pop, counter, wipe. Every phrase start gets the
  small 3 % "cut punch" (see `cut_punch()` in hiw04) so the frame never feels static. Snappy: 35–45 s, ~110–130 words,
  voice speed `HIW_SPEED=0.96`.
- Myth-bust / "Not exactly." turn, chapter switch DARK → WHITE → DARK, ≥ 3 sourced numbers, honest footnotes.
- **Perfect loop:** the last spoken line is just **"So,"** so it plays straight into "…what is this?" The last frame must be
  identical to frame 1 (make the hook shot's motion periodic in DUR, like `macro_flake_pose()`). Build with
  `HIW_LOOP=1 HIW_HEAD=0.12 HIW_TAIL=0.18` (no music fades, tiny head/tail silence):
  `HIW_SPEED=0.96 HIW_HEAD=0.12 HIW_TAIL=0.18 python3 ../../tools/tts.py` then `HIW_LOOP=1 howitworks/tools/build.sh …`.
- Topics: everyday objects and body mysteries people have personally noticed (see TOPICS.md, top of "Next up").
- **Owner direction 2026-11-17: less "sciencey", smoother, cleaner.** Plain everyday words (no study names, Latin or
  anatomy terms on screen or in the voice; say "in one study" not "Kaczorowski 2002"). Clean, simple, smooth shapes on
  soft gradient backgrounds (see `episodes/hiw03b_brain_freeze`), ONE short pill at a time, no HUD, max 2 tiny footnotes
  (source + "not medical advice"). **Every ~2 s a new frame or a new element must appear** — never hold a static shot.

Reference episodes (copy the closest one; hiw04 is the template for the standard format):
- `episodes/hiw01_blackheads` — cut-away skin block, macro skin surface, split-screen, apple inset, white-studio "fix" chapter.
- `episodes/hiw03b_brain_freeze` — **cleanest reference** (owner's preferred look): ice-cream hook, smooth head profile with camera moves, simple bar chart, white-studio twist, tongue fix, loop.
- `episodes/hiw04_dandruff` — **standard format**: mystery macro → zoom-out reveal, flake cell mosaic, scalp block with travelling cells, 1-in-2 grid, yeast macro, white-studio fix (shampoo + timer), loop back to frame 1.
- `episodes/hiw02_wrinkly_fingers` — underwater fingertip pad with growing wrinkles, side cross-section with nerve pulses
  and vessels, white-studio experiment (race bars, counter, tyre), "well, not exactly" debate, pattern-match finale.
Each folder has `prompt.md` (the full episode prompt: script, beats, JSON spec, sources) — write one for every new episode first.

## 0. Setup (fresh session)
```
bash howitworks/tools/setup.sh          # deps, Kokoro model, JetBrains Mono (~1 min)
export WHATIF_TRACK=/home/claude/whatif-studio/assets/music/main_track.mp3
```

## 1. Fill today's 3 slots (never duplicate)
- Check `reports/posts.csv` AND Buffer for posts already scheduled today at 12:00 / 15:30 / 19:00. Only fill free slots.
- **First use finished videos in `howitworks/ready/`** (listed in `ready/queue.json`, oldest first). They are already checked.
  After posting one, delete it from `ready/` and its entry from `queue.json`.
- For the remaining slots make new episodes from `howitworks/TOPICS.md` → "Next up" (top first).

## 2. Make a new episode (`howitworks/episodes/hiwNN_slug/`)
1. Research + fact-check every number with web search. Health topics: AAD/NHS/Mayo/DermNet-grade sources only.
   Debated science = say it's debated. Never invent numbers.
2. Write `prompt.md` in the same structure as the reference prompts (hook options, script with markup, beat table, JSON spec,
   sources). Script: 140–160 spoken words (~50–60 s), hook in the first second, ≥ 3 real numbers, ≥ 3 cliffhanger breaks,
   one "Well… not exactly" turn, chapter switch DARK → WHITE (→ DARK), final line loops into the first.
3. `script.py`: SENTENCES list — `cap` (on-screen, `*keyword*`, `||` phrase breaks), optional `say` (numbers as words),
   `gap` (pause after), `weights` for digit words. Then `python3 ../../tools/tts.py` inside the folder → `vo_raw.wav`, `timings.json`.
4. `episode.py`: copy the closest reference and rebuild the scenes for the topic with the shared `engine.py`
   (Captions, pill, hud, footnote, big_number, wipe, studio_dark/white, dust, vignette, grain). Every beat time comes from
   `kw(i)` / `p0(i)` (phrase index from timings), never hand-typed seconds. Keep: one keyword box per phrase coloured like
   its object, ≤ 3 pills on screen, text inside x 60–950 and y 160–1536, motion in every frame, impacts on the big beats.
5. Stills: `python3 episode.py still <t> <t> ...` for every beat → LOOK at them (nothing cut off, nothing overlapping, text
   readable, subject clear). Fix and re-check.
6. Build: `howitworks/tools/build.sh howitworks/episodes/hiwNN_slug hiwNN_slug` (~6 min; re-runnable, keeps finished chunks).
   Produces `hiwNN_slug_final.mp4` and `hiwNN_slug_upload.mp4` (< 9.3 MB, -14 LUFS). Check 4–6 frames of the upload file and
   that it has an audio track before posting.

## 3. Publish (same as RUNBOOK.md §4)
- Copy the upload file to `whatif-media/hiwNN-<slug>.mp4`, push, confirm the raw URL returns 200.
- Buffer org `6aefe0af293c0ea7295e2704`, `mode: customScheduled`, explicit `+08:00` times, `schedulingType: automatic`:
  TikTok `6aeff89b62b70b94b0b8d292` `{tiktok:{title}}` · Instagram `6aeff80962b70b94b0b8cdfb` `{instagram:{type:"reel", shouldShareToFeed:true}}` ·
  YouTube `6aeff6c162b70b94b0b8c295` `{youtube:{title:"… #shorts", categoryId:"27", madeForKids:false, privacy:"public"}}`.
- Caption: the hook question + 2 surprising facts + the comment question + (health topics) "Educational only, not medical advice"
  + 5–7 hashtags (#howitworks #science #learnontiktok #didyouknow …). Never schedule a time in the past; if a slot is
  missed, use the next free hour that day.
- Buffer free plan = max 10 queued posts per channel; 3 a day is fine as long as yesterday's have published.

## 4. Log
Append to `reports/posts.csv` (episode column = `HIWNN`), move the topic to "Done" in `howitworks/TOPICS.md`,
problems to `reports/issues.md`, commit as `Claude <noreply@anthropic.com>` and push.
