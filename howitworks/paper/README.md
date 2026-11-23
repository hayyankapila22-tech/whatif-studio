# ★ PAPER-CUTOUT FORMAT — the channel standard from 2026-11-24 (owner direction 2026-11-23)

Owner loved this look ("PERFECT!!!", "nice!!!!!!!!!"). It overrides the "2.5D lab" look in RUNBOOK_HIW.md for every NEW
episode. Everything else in RUNBOOK_HIW.md (slots, ready/ queue, Buffer + Metricool booking, retries, logging) still applies.
Reference episode: `episodes/p01_onions/` (copy it). Older reference render: owner-approved "wrinkly fingers premium".

## The look (keep ALL of it)
- **Real photo props as paper stickers** (thick white border + soft shadow), never drawn shapes for the main objects.
  At least 2 props per scene and the props CHANGE on every line. Use `stk(c, name, x, y, scale, rot, k)`.
- **A new colour on every line**: crumpled-paper backgrounds from `PALETTE` (blue, purple, pink, orange, mint, navy, red,
  teal, yellow, coral), torn-paper wipe between scenes, camera punch-in on every scene, screen shake on big hits.
- **Stop-motion feel**: everything moves at 15 poses/s with a small jitter (`f.jx, f.jy, f.jr`).
- **Paper labels**: 2 per scene at y≈330 and y≈470 (white / yellow / red / black), short and punchy, keyword in CAPS.
  Stamps (`stamp`) for NOPE!/STING!/NO TEARS!, big `glyph('?')`, `rays`, `bolt`, `cloud` (gas/steam), photo `water`/`drop`.
- **Sound**: royalty-free funk bed `music/funk_music1.mp3` (ducks under the voice automatically) + LOTS of effects:
  a pop on every prop/label, swoosh + paper rustle on every scene change (`K.default_sfx()`), impacts on stamps,
  splash/bubble/scratch/ding/sparkle/snip where they fit. Aim for 30–45 effects per video.
- **Voice**: VOICE 2 "bubbly presenter" (owner's pick for this format; overrides "Liam" for paper videos):
  `voices/voice2_bubbly_presenter_ref.wav`, Chatterbox exaggeration 0.8, cfg 0.35 (`tts_voice.py`). Synthetic reference — never clone a real person.
- **Script**: 6 lines, 20–26 s. Line 1 = the hook question in the viewer's words ("Why do onions make you cry?").
  Then a myth/twist, 2–3 plain facts (no studies, no Latin), and end with a useful tip or a surprising payoff + stamp.
  Bubbly, casual tone. Fact-check with web search; keep sources in the docstring of episode.py.
- **Safe zone**: labels/key objects inside x 60–1020, y 280–1560 (TikTok/Reels/Shorts UI).

## Props: fully automatic downloads (no human needed)
The cloud session cannot reach Pixabay, so a GitHub Action (`.github/workflows/fetch-props.yml`, secret `PIXABAY_KEY`)
downloads props for us:
1. Check `library/` first — reuse what is there (`ls howitworks/paper/library`).
2. Add the missing ones to `props_requests.json` as `{"name": "rabbit", "q": "rabbit"}` (optional `"type"`: photo /
   illustration / vector, or `"id"` to pin a Pixabay id). Commit + push.
3. Wait ~1–3 min, then `git pull` until `library/<name>.png` exists. `library/_last_fetch.log` lists OK / MISS / ERR.
   For a MISS, try a simpler query (one or two words) and push again, or use another prop.
4. LOOK at each new prop (contact sheet) before using it. Only transparent PNGs are accepted by the fetcher.

## Build
```
bash howitworks/paper/setup_paper.sh                    # once per session: chatterbox venv, skia, scipy, pillow
cd howitworks/paper/episodes/pNN_slug
/home/claude/cbx/bin/python3 ../../tts_voice.py      # lines.json -> vo_0.wav ... (≈40 s per line on 2 CPUs)
python3 episode.py stills                               # one still per scene (or: stills 1.0,3.5,...) -> LOOK at every one
python3 episode.py all                                  # video (~4 min) + mix + pNN_slug_final.mp4 + pNN_slug_upload.mp4 (<9.3 MB)
```
Check 4–6 frames of the upload file (colours, nothing cut off) and that it has audio, then publish exactly as RUNBOOK_HIW.md §3.
Episode ids: `P01`, `P02`, … (posts.csv episode column), media file `pNN-<slug>.mp4` in whatif-media.
