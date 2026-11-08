# Nightly runbook: 3 new episodes a day

Runs as a scheduled task every night at ~02:17 Asia/Shanghai. Posts go out at **12:00, 16:00, 19:00 Asia/Shanghai (+08:00)** the same day.

## 0. Setup (fresh cloud session)
- Attach repos with push: `hayyankapila22-tech/whatif-studio` and `hayyankapila22-tech/whatif-media`; clone to `/home/claude/`.
- `export WHATIF_TRACK=/home/claude/whatif-studio/assets/music/main_track.mp3` (Timeless instrumental, mixed from 0:12 on ALL platforms incl. Instagram).
- Commits: author `Claude <noreply@anthropic.com>`.

## 1. Pick topics
Take the top 3 from `TOPICS.md` → "Next up". Next episode number = last episode in `reports/posts.csv` + 1.

## 2. Write each episode (`season2/episodes/epN/scene.js`)
Copy the closest existing episode (ep7 coffee/flood + space, ep8 growing Jeremy + planet scale, ep9 instanced swarm + space) and change:
title (≤ 32 chars so it fits the bar), reel (last item = topic, ≤ 30 chars), beats `{t, m, cap, hi/red, big, space, bubble}` every 2.4 s from t=3.2, `ctaAt`, `total` (≈ last beat + 3.3 s).
Fact-check every number with a web search; keep the values exact (counter shows the real computed value).
Safe zone: all text inside x 60–930, y 250–1440 (kit already places counter/captions/bubbles there). Keep Jeremy out from behind lamp posts (x = 21, 30, 39 on z = 4.8) and parked car (x = 26, z = 3.2): good spots x ≈ 34.5 or 21.5–23.

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
- Buffer free plan: max 10 queued posts per channel — 3/day stays well inside.

## 5. Log
Append rows to `reports/posts.csv`, move topics to "Done" in `TOPICS.md`, commit + push. If anything fails, still schedule what is ready and note the problem in `reports/issues.md`.

## Reports
Daily stats via Buffer `get_aggregated_post_metrics`; weekly report every Monday; month-end summary on the 1st (Docs artifact).
