#!/bin/bash
# new_episode.sh <workdir> <scene.js> : makes a ready-to-render episode folder from the Season 2 kit.
set -e
R=$(cd "$(dirname "$0")/.." && pwd); W=$1; mkdir -p "$W"
cp "$R"/season2/{engine.js,street.js,jeremy2.js,hud.js,kit.js,world.js,foliage.js,studio.js,index.html,render.cjs} "$W"/
cp "$R"/fonts/*.otf "$W"/
cp "$2" "$W"/scene.js
[ -f "$(dirname "$2")/vo_lines.json" ] && cp "$(dirname "$2")/vo_lines.json" "$W"/ && python3 "$R/tools/narrate.py" "$W"
[ -d "$R/season2/node_modules/three" ] || (cd "$R/season2" && npm i --silent --no-save three@0.170.0 >/dev/null)
ln -sfn "$R/season2/node_modules" "$W/node_modules"
ln -sfn "$R/season2/assets" "$W/assets"
echo "ready: $W"
