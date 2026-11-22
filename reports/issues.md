# Issues / notes log

## 2026-11-10 (nightly run, 02:17 Asia/Shanghai)
- Only ONE slot was free: 12:00 today was already booked by Ep10 (3 Buffer posts confirmed `scheduled`). Made 1 episode (Ep11) for 19:00 instead of 2, as the runbook says — no duplicates.
- Ep11 set: hid two north lamp posts (x=21, 30), one south lamp (x=35), one south tree (x=33) and two parked cars (26/3.2, 40/-3.2) in this episode only, so nothing blocks the camera. Street files unchanged.
- New reusable bits: `tools/sfx2.py` one-shots `pop` (thought bubble), `chips` (poker), `ding`, and bed `murmur` (crowd). Ep11 scene.js has `person()` (recoloured Jeremy rig with long hair / apron / tie / tinfoil hat), HTML thought clouds `thought()`, bistro table, poker table, gift box, billboard (made-up brand "FIZZO"), podium, and an Earth "global mind" network — copy from there.
- Framing lesson: two-shots need the camera ~6 m from the actors with the look target at y≈2.0, otherwise heads end up under the counter. Captions moved to y=1225 (`capY`) and the note line to 1378 so faces stay clear.

## 2026-11-10 (owner session)
- Ep12 render: worker B timed out taking a screenshot in seg_1 (6k high-detail popcorn instances). Fixed: piece detail 2 and a 180 s screenshot timeout in render.cjs; re-ran resumable render.
- The cloud container restarted once mid-render (all work files survived; the render had to be restarted).

## 2026-11-10 evening (owner session)
- Ep13: v5.1 render is ~9 s/frame per worker (MSAA + DOF) -> ~105 min for 49 s. The container restarted once mid-render; re-running render_ep.sh resumed. Final shot re-rendered (2 segments) because Jeremy was cut by the frame edge.
- Ep12 (popcorn, Wed 12:00) still has the old aliased floor and no voiceover.

## 2026-11-11 (nightly run, 07:22 Asia/Shanghai) — floor "tweaking" fix
- Both slots today were already booked (Ep12 12:00, Ep13 19:00; all 6 Buffer posts confirmed `scheduled`), so no new episodes were made.
- Owner reported the floor "still tweaking". Causes found and fixed:
  1. **One-frame glitch at the start of every 5 s render segment** (frames 150, 300, 450… — a flicker every 5 s). The first frame after page boot rendered before lighting/textures settled. `render.cjs` now renders and discards 3 warm-up frames before stills/segments (test: first-frame jump 6.4 → 0.25).
  2. **Moire waves on the far floor**: thin dark tile seams were baked into the floor texture. Removed; analytic grid lines now fade per axis well before they crowd (<~6 px apart); floor grain is softer (fine high-contrast specks boil after compression).
  3. **Grid pops when the tile size changes** (Ep12 switched 1→10→100→1000 m tiles in one frame). studio.js grid is now multi-level (tile, 10x, 100x…), each level cross-fading in as the finer one fades; Ep12 now uses a fixed `floorScale(1, sc)`.
  4. Shadow frustum is snapped to shadow-map texels in `shadowFit` so soft shadow edges do not crawl while the camera glides.
- Re-rendered Ep12 and Ep13 with the fixes (checked: segment-boundary jumps gone, durations 42.5 s / 49.1 s, audio present) and swapped the video on all 6 Buffer posts to `*-v2.mp4`. Ep12 v2 went out at 12:00 on TikTok, Instagram and YouTube. Ep13 v2 is scheduled for 19:00.
- The cloud container restarted once during the Ep12 re-render; render_ep.sh resumed from the finished segments.

## 2026-11-11 evening (owner session) — Ep14 black hole, Ep15 water drop
- Owner direction changed: doubling episodes are back (grey studio floor + scale); regular what-ifs go back to the street look (Ep10/11); every episode narrated with voice 1 (Kokoro af_heart). Owner asked for a Trump / Andrew Tate AI voice — declined (no imitating real people).
- Could not update the nightly scheduled task's prompt from this session (permission denied); RUNBOOK "OWNER DIRECTION 2026-11-11" carries the new rules. The owner should edit the task prompt (it still says "no doubling / studio look only").
- Bugs found and fixed while making Ep14/15: (1) tiny subjects vanished into the floor (20 km floor quad depth error) -> floor drawn without depth write; (2) floor flickered on/off in extreme close-ups -> `floorScale(1, Math.max(.01, dist/400))`; (3) references placed in front of the subject sat inside the camera during fast pull-backs -> they now grow in only once the camera is past them; (4) tags were projected with the previous frame's camera -> call orbit() before tag3().
- Ep14 was first scheduled with a version that still had the close-up floor flicker; replaced by `-v2.mp4` on all 3 posts the same evening.

## 2026-11-12 (owner session) — Ep16 robots, Ep17 nuclear explosion
- Street-look episodes with narration: beats are built from vo.json (`T = LN.map(l => l.t0 - .12)`, line 0 is spoken over the intro, line 1 needs `"pre": 0.3` so it starts after the 3.2 s intro). Reference: season2/episodes/ep16 and ep17.
- Street renders were slow in this container: ~17 s/frame per worker (2 workers) -> about 3 hours per 45 s episode. Start early.
- Look targets at y ~1.55 (not 2.0) keep faces above the captions (capY 1225). Hide the parked car at (26, 3.2) unless it is the subject: it blocks the usual camera.
- rimLight() breaks on unlit (MeshBasicMaterial) parts: set `material.userData.rim = true` on them first.
- Ep17 is framed as preparedness education (FEMA / Ready.gov), no casualties shown.

## 2026-11-14 (nightly run, 02:18 Asia/Shanghai) — Ep18 Moon, Ep19 gravity flip
- Both slots were free (0 rows for 2026-11-14 in posts.csv, nothing in Buffer for the day). Made Ep18 (12:00) and Ep19 (19:00), both v5.1 premium studio look, narrated (Kokoro af_heart), Timeless from 0:12 via mix3.py.
- Rule conflict noted: RUNBOOK "OWNER DIRECTION 2026-11-11" / TOPICS.md say regular what-ifs use the street look, but tonight's scheduled-task prompt says v5.1 studio look for everything and street is legacy. Followed the task prompt (studio). The owner may want to make RUNBOOK/TOPICS and the task prompt agree.
- Ep19 physics uses quadratic air drag (terminal ~53 m/s): 338 m after 10 s (not the 490 m vacuum number in TOPICS.md), peak 431 m, touchdown ~186 km/h. Touchdown is never shown (dip to black ~13 m up).
- render_ep.sh gotcha: when re-rendering a segment, do NOT keep the old file as seg_N_old.mp4 in the folder — the concat list is `ls seg_*.mp4`, so it was spliced in (caught in the frame check before upload). Move old segments to a subfolder.
- 2-pass upload encode overshoots the 9.3 MB target by ~5-7% (Ep18 9.36 MB, Ep19 first try 9.93 MB). Ep19 re-encoded at an 8.6 MB target (8.68 MB). Consider lowering the target in render_ep.sh.
- Renders: ~8.5-10 s/frame per worker in the gallery, ~5 s/frame in the flight shots; Ep18 took ~2 h, Ep19 ~1 h 15 min (run after Ep18, not in parallel; 2 CPUs).
- Ep19 transitional frames: the 330 m tower enters/leaves through the left frame edge during the pull-back and the descent (continuous camera); its tag fades out on the way down so it never sits on the HUD text.
- Earth globes (earth_atmos texture) read dark when the Pacific faces the camera; set the spin offset so land faces the camera (tested with stills).

## 2026-11-15 (nightly run, 02:18 Asia/Shanghai) — Ep20 Earth stops spinning, Ep21 oceans disappear
- Both slots were free (0 rows for 2026-11-15 in posts.csv, nothing in Buffer for the day). Made Ep20 (12:00) and Ep21 (19:00), v5.1 studio gallery, narrated (Kokoro af_heart), Timeless from 0:12 via mix3.py. Both checked: audio present (mean ≈ -16 dB), durations match vo.json (56.3 s / 57.1 s), no jumps at segment boundaries.
- Same rule conflict as 2026-11-14: RUNBOOK "OWNER DIRECTION 2026-11-11" / TOPICS.md say street look for regular what-ifs; the nightly task prompt says v5.1 studio for everything. Followed the task prompt again. Please make them agree.
- TOPICS.md backlog still listed topics that were already made (all humans disappeared = Ep10, Moon vanished = Ep18, read minds = Ep11). Removed them so the next run doesn't repeat them.
- VO came out a bit long (56-57 s vs the 45-55 s target) after trimming once; renders ~2 h each sequentially (~10 s/frame per worker).
- Ep21 frame check caught the CHALLENGER DEEP tag covering the "Everest fits in the trench" ghost and Jeremy behind it; moved Jeremy/tag and re-rendered segments 2-5 only (old segments moved to old_segs/, per the 2026-11-14 note).
- Upload encodes again overshoot 9.3 MB slightly (9.35 / 9.37 MB); Buffer accepted them. The target in render_ep.sh could be lowered to ~8.6 MB.
- ep21 drain shader detects ocean pixels by colour (blue-dominant) in earth_atmos_2048.jpg; a few dark land pixels near coasts also turn sea-floor brown. Not noticeable at globe size.

## 2026-11-16 (nightly run, 02:18 Asia/Shanghai) — Ep22 two moons, Ep23 two suns
- Both slots were free (0 rows for 2026-11-16 in posts.csv, no scheduled posts in Buffer). Made Ep22 (12:00) and Ep23 (19:00), v5.1 studio gallery, narrated (Kokoro af_heart), Timeless from 0:12 via mix3.py. Checked: audio present (mean ≈ -16 dB), durations match vo.json (51.7 s / 48.3 s), no jumps at segment boundaries (big frame diffs only inside camera glides), no dark frames.
- Same rule conflict as before: RUNBOOK "OWNER DIRECTION 2026-11-11" / TOPICS.md say street look for regular what-ifs; tonight's task prompt says v5.1 studio for everything. Followed the task prompt.
- Frame checks of rendered segments caught problems the stills missed (stills are only one moment per line): Ep22 Jeremy cut at the frame edge at the tide tank, the companion moon flying across Jeremy's face, two tags overlapping at the mini-moon; Ep23 two tags overlapping at Kepler-16. Fixed and re-rendered those segments only (old ones in old_segs/). Lesson: render stills at 2-3 moments per line, especially during animations that move objects across the frame.
- Jeremy at scale is about as tall as the globe stands: placing him at negative x (camera side, yaw < 0) makes him huge and cut off; behind and to the +x side (x0 + 1.4…2, z -0.9…-1.8) works.
- Upload encodes re-done at an 8.6 MB target (9.46 / 9.36 MB from render_ep.sh); final 8.76 / 8.66 MB.
- Renders ~12 s/frame per worker (2 workers); running stills or a second episode at the same time slows everything down proportionally.

## 2026-11-17 (nightly run, 02:19 Asia/Shanghai) — HOW DOES IT WORK? day 1: HIW01, HIW02, HIW03
- All 3 slots were free (no 2026-11-17 rows in posts.csv, nothing scheduled in Buffer). 12:00 = HIW01 blackheads, 15:30 = HIW02 wrinkly fingers (both from ready/, queue now empty), 19:00 = new HIW03 brain freeze.
- **Yesterday's Ep22 (two moons) Instagram post failed** in Buffer: "issue with the media attached… check it meets all specifications" (post 6afa3611a869c35e5b9f8236, still in error state). TikTok/YouTube went out. Ep22's file has the same specs as Ep21, which posted fine, so it may be a one-off on Instagram's side. I left it alone; it can be retried from Buffer ("Share now" or reschedule).
- ready/ is now empty, so tomorrow's run must build all 3 episodes from scratch (~25-30 min each including research and stills). Consider pre-building a buffer of episodes.
- HIW03: Kokoro's word timings for "In 2012," / "In 2002," are short (weights barely change them), so the year captions build a little early. Not noticeable at speed.
- HIW03 build: 4.5 min on this machine; upload 8.87 MB, -14.4 LUFS, peak -1.3 dBFS, music/voice -27 dB (very quiet as asked).

## 2026-11-19 (nightly run, 02:18 Asia/Shanghai) — HIW09 static shock
- Run started after midnight Shanghai time, so "today" = 2026-11-19. 12:00 (HIW07) and 15:30 (HIW08) were already booked and still `scheduled` in Buffer on all 3 channels (raw URLs return 200); only 19:00 was free. ready/ queue was empty, so built HIW09 from the top of TOPICS "Next up" (static shock off car doors / trolleys).
- No `error` posts in Buffer for 2026-11-17/18.
- HIW09: 27.3 s, standard "So," loop (frame 1 ≈ last frame), build ~3 min, upload 8.9 MB, -14.6 LUFS, peak -1.4 dBFS, audio track present. Media pushed to whatif-media (as the task prompt says); the last runs had put media in whatif-studio/howitworks/media instead — both work, maybe pick one.
- Music level: task prompt says Timeless "VERY quiet / subtle", RUNBOOK_HIW (2026-11-17 evening) says "clearly audible, HIW_MUSIC_DB -11". Kept the engine default (-11, music/voice measured -14.4 dB, ducked further under speech) for consistency with HIW04-08. Please make the prompt and runbook agree.
- HIW07/HIW08 folders had no prompt.md; HIW09 has one.
- Tomorrow's run: ready/ is still empty, so all 3 slots need new episodes.

## 2026-11-20 (nightly run, 02:18 Asia/Shanghai) — HIW12 tickle, HIW13 onions, HIW14 voice on recordings
- All 3 slots were free (no 2026-11-20 rows in posts.csv, nothing scheduled in Buffer for the day). ready/ queue was empty,
  so built HIW12–14 from the top of TOPICS "Next up" (tickle yourself, onions, voice on recordings). HIW10 (find the C) and
  HIW11 (fork in the microwave) exist from the owner session but were never put in ready/, so I did not post them.
  TOPICS "Next up" #10 (metal sparks in the microwave) is the same topic as HIW11 — skip it or post HIW11.
- **Buffer limits YouTube to 2 scheduled posts per day, counted in the account time zone (America/Los_Angeles).**
  12:00 and 15:30 Shanghai fall on the same LA day as the previous night's 19:00 post, so HIW13's YouTube post at 15:30
  was refused ("maximum number of posts YouTube allows in a day (2)"). Booked HIW13 YouTube at 16:30 +08:00 instead
  (= 00:30 LA, next LA day); TikTok/Instagram at 15:30. With 3 posts/day this will keep happening: each LA day gets
  12:00 + 15:30 (Shanghai, day N) + 19:00 (day N-1) = 3 YouTube posts. Options: post only 2 YouTube Shorts a day, move
  one slot after 16:00 Shanghai (00:00 LA), or switch the Buffer account time zone to Asia/Shanghai (then 3/day still
  exceeds 2 — YouTube via Buffer seems capped at 2/day regardless).
- **2026-11-19 YouTube posts for HIW07 (12:00) and HIW08 (15:30) failed in Buffer** ("An unknown error has occurred",
  posts 6afc5b9dddb326928b5e347a / 6afc5b9f685aa7614ba642c7); TikTok/Instagram went out. Possibly the same 2/day cap.
  Left in error state; can be retried from Buffer.
- Voice: Chatterbox Liam installed fine (~5 min setup). Videos are short: 22.4 s / 25.6 s / 25.8 s (Liam speaks fast).
- Music: kept the engine default (-11 dB, measured music/voice -14.4/-14.5 dB) for consistency with HIW04–11, although
  the task prompt says "VERY quiet". Same conflict as 2026-11-19 — please make prompt and runbook agree.
- Uploads: 8.9 / 8.7 / 8.9 MB, -15.2…-15.3 LUFS, audio track present on all three, loop end ≈ frame 1.
- HIW14 hook: the memo scrubber loops 3× per video so the loop seam is a natural restart (0:06 → 0:00).

## 2026-11-20 (owner session, 09:10 Asia/Shanghai) — failed YouTube posts
- 2026-11-19: HIW07 (12:00) and HIW08 (15:30) failed on YouTube only ("unknown error"); TikTok/Instagram fine; HIW09 19:00 fine on all 3.
- Retried both with shareNow (media copied to whatif-media @8e87f92): HIW07 posted (youtube.com/watch?v=c7SDUyR5rJk); HIW08 failed again: "The daily posting limit for this channel has been reached". YouTube caps uploads per channel in a rolling 24 h window; 3 a day is at/over the cap for this (likely unverified) channel. That probably also explains yesterday's failures.
- Fix: owner to phone-verify the channel at youtube.com/verify (vendor docs say this raises the limit). Runbook now has a retry step that respects the 24 h window.
- Today's YouTube posts (12:00 tickle, 16:30 onions, 19:00 voice) may hit the cap because the HIW07 retry used one upload.

## 2026-11-21 (nightly run, 02:18 Asia/Shanghai) — HIW15 knuckles, HIW16 ears pop, HIW17 eye floaters
- All 3 slots were free (no 2026-11-21 rows in posts.csv, nothing scheduled in Buffer). ready/ queue was empty, so built
  HIW15–17 from TOPICS "Next up" (knuckles, ears on a plane, floaters). Skipped #10 "metal sparks in the microwave": it is the
  same topic as the finished HIW11 fork video (not in ready/, so not posted — owner can approve HIW11 instead).
- All 9 Buffer posts accepted as `scheduled` (12:00 / 15:30 / 19:00 +08:00, TikTok + Instagram + YouTube). Buffer did NOT
  refuse the 2nd YouTube post this time.
- **Failed YouTube posts NOT retried this run** (runbook retry step): HIW08 (6afc5b9f685aa7614ba642c7), HIW12
  (6aff41a589881169f7274e40), HIW13 (6aff428fba0fb292d517f522), HIW14 (6aff437bfeda52ccd01f0ed0) are all in `error` with
  "daily posting limit for this channel has been reached". Only 1 YouTube upload went out in the last 24 h (HIW07 retry,
  2026-11-20 01:09 UTC), yet HIW12 failed with just 2 uploads in its 24 h window — the channel looks capped at ~2 uploads
  per rolling 24 h. Today's 3 new YouTube posts already need that budget, so retrying old ones now would make today's fail.
  **Likely result: today's 19:00 (HIW17) YouTube post may also fail.** Fix is still owner-side: verify the channel at
  youtube.com/verify, or drop YouTube to 2 posts/day (e.g. skip YouTube for the 19:00 slot) and use the spare slot for the
  backlog of 4 failed Shorts.
- Music level: used HIW_MUSIC_DB=-17 this time (measured music/voice -20.6 dB) because the task prompt says "VERY quiet,
  subtle"; previous runs used the -11 default. If the owner prefers the louder bed, rebuild with the default.
- Captions: engine wraps >5 words per line, so phrases of 11+ words spill onto a 3rd line and collide with the pill at
  y 560 (HIW16 "the air can be as thin as on a 2,400 metre mountain", HIW17 "and the clumps cast shadows…"). Added a
  caption-only `split_long()` helper in hiw16/hiw17 episode.py; worth moving into engine.Captions.
- Uploads: HIW15 23.5 s / 8.9 MB / -15.5 LUFS; HIW16 29.8 s / 8.8 MB / -14.9 LUFS; HIW17 29.0 s / 8.9 MB / -15.3 LUFS;
  all have an audio track, loop end ≈ frame 1. Media in whatif-media (raw URLs 200).
- Tomorrow: ready/ still empty, 3 new episodes needed (next topics: foot falls asleep, cut apple browns, spinach teeth).

## 2026-11-22 (nightly run, 02:18 Asia/Shanghai) — HIW18 foot asleep, HIW19 apple browns, HIW20 spinach teeth
- All 3 slots were free (no 2026-11-22 rows in posts.csv, nothing scheduled in Buffer). ready/ queue empty, so built HIW18–20
  from TOPICS "Next up" (#10 microwave sparks still skipped: same topic as the unposted HIW11 fork video).
- All 9 Buffer posts accepted as `scheduled`. **YouTube times shifted +5 min (12:05, 15:35)** so each lands just after
  yesterday's YouTube upload at the same slot turns 24 h old (HIW15 sent 04:00:17 UTC, HIW16 07:30:08 UTC). TikTok/Instagram
  at exactly 12:00 / 15:30 / 19:00.
- **Expect the 19:00 YouTube post (HIW20) to fail** with "daily posting limit": yesterday the 3rd YouTube upload (HIW17 19:00)
  failed again, so the channel is capped at ~2 uploads per rolling 24 h. Fix is owner-side: verify the channel at
  youtube.com/verify, or drop YouTube to 2 posts/day.
- **Failed YouTube posts not retried** (runbook retry rule: any retry inside the 24 h window would push today's scheduled
  YouTube posts over the cap): HIW08 6afc5b9f685aa7614ba642c7, HIW12 6aff41a589881169f7274e40, HIW13 6aff428fba0fb292d517f522,
  HIW14 6aff437bfeda52ccd01f0ed0, HIW17 6b0096f773831df0147c2536 (new, 2026-11-21 19:00) — all "daily posting limit".
  Backlog is now 5 Shorts that never reached YouTube.
- HIW20 script: dropped the planned "Rhubarb can do it too" line (couldn't find a reputable source saying rhubarb causes the
  teeth feeling); replaced with "spinach has more of that acid than almost any other veggie" (Live Science). The closing
  visual is a spinach leaf with a crown, with no invented bar-chart numbers.
- Music at HIW_MUSIC_DB=-17 again (measured music/voice ≈ -20.4 dB) per the task prompt's "VERY quiet". Runbook still says
  -11 default — same conflict as before.
- Uploads: HIW18 32.4 s / 9.0 MB / -15.3 LUFS; HIW19 29.9 s / 8.9 MB / -15.3 LUFS; HIW20 28.0 s / 8.9 MB / -15.2 LUFS; audio
  track present on all three, loop end = hook scene. Media in whatif-media (raw URLs 200).
- Tomorrow: ready/ still empty, 3 new episodes needed (next topics: goosebumps, then the older list).

## 2026-11-22 (owner session, ~20:15 Asia/Shanghai) — YouTube backlog moved to Metricool
- Root cause corrected: the "daily posting limit" is **Buffer's free-plan cap of 2 YouTube Shorts per channel per 24 h**
  (support.buffer.com/article/646-daily-posting-limits), not YouTube's — the channel is already verified.
- Today's 19:00 HIW20 YouTube post failed in Buffer as expected; someone also retried the 5 old ones in Buffer ~19:42 and
  they failed again.
- Owner approved moving YouTube posts to Metricool (already connected, YouTube channel linked). Booked in Metricool:
  HIW20 spinach 22 Nov 21:00 (437507078), HIW17 floaters 22 Nov 22:30 (437507334), HIW08 stars 23 Nov 21:00 (437507343),
  HIW12 tickle 23 Nov 22:30 (437507359), HIW13 onions 24 Nov 21:00 (437507380), HIW14 voice 24 Nov 22:30 (437507402).
- Deleted the failed Buffer YouTube copies of HIW20, HIW12, HIW13. Deleting HIW17 (6b0096f773831df0147c2536), HIW08
  (6afc5b9f685aa7614ba642c7) and HIW14 (6aff437bfeda52ccd01f0ed0) was blocked by a permission check — they stay in Buffer
  in `error`; **do NOT retry them in Buffer** (they're already booked in Metricool → duplicate risk).
- Runbook updated: 19:00 YouTube goes through Metricool from now on; never retry the Buffer YouTube limit error.
