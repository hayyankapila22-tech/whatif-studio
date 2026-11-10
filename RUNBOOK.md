# Nightly runbook: 2 new episodes a day (v3 quality)

Runs as a scheduled task every night at ~02:17 Asia/Shanghai. Posts go out at **12:00 and 19:00 Asia/Shanghai (+08:00)** the same day. Fill only the free slots (an episode may already be booked at 12:00 or 19:00). Each v3 episode renders in ~95 min, so start the first render as early as possible and run the second while checking the first.

## 0. Setup (fresh cloud session)
- Attach repos with push: `hayyankapila22-tech/whatif-studio` and `hayyankapila22-tech/whatif-media`; clone to `/home/claude/`.
- `export WHATIF_TRACK=/home/claude/whatif-studio/assets/music/main_track.mp3` (Timeless instrumental, mixed from 0:12 on ALL platforms incl. Instagram).
- Commits: author `Claude <noreply@anthropic.com>`.

## 1. Pick topics
Take the top 2 from `TOPICS.md` → "Next up" (or 1 if one slot is already booked). Next episode number = last episode in `reports/posts.csv` + 1.

## Two formats
- DOUBLING (ep7–9): one thing doubles every minute; counter = the amount.
- TIMELINE (most of the owner's ideas): counter = time elapsed (e.g. `fmt: v => v < 1 ? Math.round(v*24)+' hours' : ...`, label 'TIME SINCE …'); every 2.4 s a new, bigger consequence; ends in a payoff + "What should happen next? 👇" (or "Would you survive? 👇").
  For history / speculative episodes say so on screen ("Speculation:" in the caption or a small 'what scientists think' vs 'our guess') and keep real facts accurate.

## 2. Write each episode (`season2/episodes/epN/scene.js`)
Copy the closest existing episode (ep10 timeline + world.js = the v3 reference; ep7 coffee/flood + space, ep8 growing Jeremy + planet scale, ep9 instanced swarm + space) and change:
title (≤ 32 chars so it fits the bar), reel (last item = topic, ≤ 30 chars), beats `{t, m, cap, hi/red, big, space, bubble}` every 2.4 s from t=3.2, `ctaAt`, `total` (≈ last beat + 3.3 s).
Fact-check every number with a web search; keep the values exact (counter shows the real computed value).
Safe zone: all text inside x 60–930, y 250–1440 (kit already places counter/captions/bubbles there). Keep Jeremy out from behind lamp posts (x = 21, 30, 39 on z = 4.8) and parked car (x = 26, z = 3.2): good spots x ≈ 34.5 or 21.5–23.

## v5 PREMIUM STUDIO LOOK (2026-11-10) — THE CHANNEL STYLE FROM NOW ON. Reference episode: season2/episodes/ep12 (popcorn)
- Look: clean infinite grey tiled floor, soft studio light (HDRI 'studio'), photoreal-ish objects, muted palette with ONE accent colour (orange `ACCENT`), soft shadows, no outlines, no cartoon effects, no flashes/shakes, no slot-machine intro.
- One slow CONTINUOUS camera (studio.js `orbit(target, dist, {yaw, pitch, fov})`) that pulls back as things grow. The framing size must be a smooth function of time/value (see ep12 `refAt`) — never jumps. Hard cuts only for a change of world (e.g. ground -> space), done with a 0.3 s dip (`#v5fade`).
- HUD (studio.js `setHUD`): tiny tracked brand line, the question at top-left with the key phrase in orange (`<b>`), small orange caps labels with white numbers, the big orange value, and an italic serif one-liner that changes at each milestone ("Minute 15: a full bathtub."). End card text centred (`end`) + "What should double next? 👇" (or a fitting question), data fades out.
- Callout tags (`tag3(title, detail, worldPos)`): dark rounded boxes, orange caps title + italic detail, e.g. "JEREMY · 1.75 m", "OLYMPIC POOL · 2,500 m³". Max 3-4 at once; anchor them so they never cover the HUD (they clamp to y ≥ 880).
- Jeremy is the scale reference ("JEREMY 1.75 m") via `jeremy(pos, ry, pose)`; keep him small in frame, beside/behind the subject, never covering the HUD.
- Props in studio.js: `bathtub()`, `pool()`, `pyramid()`, `planets()` (real NASA Earth/Moon textures), plus `makeCar()`. Build new props smooth and real-scale.
- Runner: the episode writes its own `window.SPEC` ({total, reel:1, ctaAt, subtle:true, beats:[], beds, sfx}) and `window.renderAt(t)`; see ep12. Values roll continuously (e.g. minute as an eased function of time), numbers exact.
- Audio: music (Timeless from 0:12) + SUBTLE effects only: `subtle: true`, beds 'room' (ground) / 'space', a few soft `swell`s at milestones and object-specific one-shots (e.g. `kpop`/`pops` for popcorn). No voiceover.
- Timeline topics use the same studio look: objects on the clean floor (or clean space) with the counter as time, tags and one-liners.

## v4 realistic look (2026-11-10) — street episodes only (legacy)
- Realism first: no ink outlines (INK.strength = 0), real HDRI lighting (`season2/assets/hdri`, CC0 Poly Haven via @pmndrs/assets; `setEnv(name)` or via `setSky`), screen-space ambient occlusion, soft filmic grade, depth of field.
- NO low-poly shapes: foliage = `crown(radius, seed, k)` from foliage.js (alpha leaf cards), grass = `grassGeo/grassMat`, animals = `makeAnimal` (smooth, fur-textured). Never use flat-shaded icosahedrons or bare spheres for nature. New props: smooth geometry (enough segments, rounded edges via RoundedBoxGeometry), real-looking materials (canvas textures with noise/grime, correct roughness).
- Render cost: ~4 s/frame on the street, ~10 s/frame in dense foliage — keep heavy foliage shots short.
## v3 kit notes (still valid)
- Engine adds a painted gradient sky, depth of field and a colour grade automatically (`INK`, `DOF`, `GRADE`, `LOOK` in engine.js).
- Per shot: `focus(worldPos, amount, maxR)` on close/medium shots (subject sharp, background soft); `noFocus()` on wides.
- `world.js`: `buildWorld(K)` once, then per shot `setSky('day'|'golden'|'dusk'|'night'|'overcast'|'ominous'|'winter')` and, for timeline topics, `setAge(years, t, {lights, lamps, snow})` (grass, vines, cracks, broken windows, rust, moss, wild trees). Also `makeAnimal('dog'|'dog2'|'wolf'|'deer'|'doe')`, `collapse(block,k)`, `flood(k)`, `towers(on,t)`, `poof(pos,k)`.
- Call `mode('street')` BEFORE `hideAll()` (mode() re-shows Jeremy).
- Sound: give the spec `beds` (ambience: city, wind, crickets, birds, drip, winter, drone) and `sfx` one-shots (see tools/sfx2.py ONESHOT) timed to the action; autosfx.py mixes them with the beat whooshes. Music stays Timeless from 0:12.
- Framing rules: Jeremy's face never under the counter (keep his head below y≈700) or under the caption; no lamp posts/trees within 2 m of a camera; captions ≤ 2 lines (≤ ~45 characters at size 62).

## 3. Check, render, mix
```
tools/new_episode.sh /home/claude/work/epN season2/episodes/epN/scene.js
cd /home/claude/work/epN && node render.cjs stills 4.5 7 9.5 ...   # one still per beat; look at them, fix framing
/home/claude/whatif-studio/tools/render_ep.sh /home/claude/work/epN WhatIf_EpN_Name   # ~70 min, resumable, run in background (2 h limit per command; rerun to resume)
```
Outputs `WhatIf_EpN_Name_final.mp4` and `WhatIf_EpN_Name_upload.mp4` (< 9.3 MB, used for posting). Watch a few frames of the final before uploading.

## 4. Publish
- Copy upload file to `whatif-media/epNN-what-if-<slug>.mp4`, push, confirm the raw URL returns 200:
  `https://raw.githubusercontent.com/hayyankapila22-tech/whatif-media/main/<file>`
- Buffer org `6aefe0af293c0ea7295e2704` (account timezone LA → always send explicit `+08:00` times). `mode: customScheduled`.
  - TikTok `6aeff89b62b70b94b0b8d292` — metadata `{tiktok:{title}}`
  - Instagram `6aeff80962b70b94b0b8cdfb` — metadata `{instagram:{type:"reel", shouldShareToFeed:true}}`
  - YouTube `6aeff6c162b70b94b0b8c295` — metadata `{youtube:{title:"… #shorts", categoryId:"27", madeForKids:false, privacy:"public"}}`
- Caption style: hook question + 2–3 escalating facts + "What should double next? 👇" + "Purely hypothetical · for entertainment" + 5–7 hashtags (#whatif #science …).
- Buffer free plan: max 10 queued posts per channel — 2/day stays well inside.

## 5. Log
Append rows to `reports/posts.csv`, move topics to "Done" in `TOPICS.md`, commit + push. If anything fails, still schedule what is ready and note the problem in `reports/issues.md`.

## Reports
Daily stats via Buffer `get_aggregated_post_metrics`; weekly report every Monday; month-end summary on the 1st (Docs artifact).
