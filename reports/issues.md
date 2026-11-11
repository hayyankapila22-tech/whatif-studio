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
