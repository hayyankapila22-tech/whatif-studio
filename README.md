# WHAT IF (x)? — studio

Private production template for the WHAT IF (x)? Shorts series.

- `season2/` — current template: Jeremy's Street (`street.js`), Jeremy v2 (`jeremy2.js`), realistic sky/sun engine, phone-safe HUD (`index.html`, `hud.js`), slot-machine intro + live counter.
- `season1/` — Season 1 episodes (reference).
- `tools/` — sound-effects library, original music generator (`remix.py`), resumable chunked render queue and finalize scripts.
- `fonts/` — Inter (SIL Open Font License).

Render: `npm i three@0.170.0`, then `node render.cjs stills <t...>` or `node render.cjs video <start> <end> out.mp4` (uses Playwright + SwiftShader).
Rendered videos are published from the separate public `whatif-media` repo; posting goes through Buffer.
