# Issues / notes log

## 2026-11-10 (nightly run, 02:17 Asia/Shanghai)
- Only ONE slot was free: 12:00 today was already booked by Ep10 (3 Buffer posts confirmed `scheduled`). Made 1 episode (Ep11) for 19:00 instead of 2, as the runbook says — no duplicates.
- Ep11 set: hid two north lamp posts (x=21, 30), one south lamp (x=35), one south tree (x=33) and two parked cars (26/3.2, 40/-3.2) in this episode only, so nothing blocks the camera. Street files unchanged.
- New reusable bits: `tools/sfx2.py` one-shots `pop` (thought bubble), `chips` (poker), `ding`, and bed `murmur` (crowd). Ep11 scene.js has `person()` (recoloured Jeremy rig with long hair / apron / tie / tinfoil hat), HTML thought clouds `thought()`, bistro table, poker table, gift box, billboard (made-up brand "FIZZO"), podium, and an Earth "global mind" network — copy from there.
- Framing lesson: two-shots need the camera ~6 m from the actors with the look target at y≈2.0, otherwise heads end up under the counter. Captions moved to y=1225 (`capY`) and the note line to 1378 so faces stay clear.

## 2026-11-10 (owner session)
- Ep12 render: worker B timed out taking a screenshot in seg_1 (6k high-detail popcorn instances). Fixed: piece detail 2 and a 180 s screenshot timeout in render.cjs; re-ran resumable render.
- The cloud container restarted once mid-render (all work files survived; the render had to be restarted).
