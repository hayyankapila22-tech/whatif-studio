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
- Re-rendered Ep12 and Ep13 with the fixes and swapped the video on their Buffer posts (new files `*-v2.mp4` in whatif-media).
