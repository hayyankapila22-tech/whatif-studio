#!/bin/bash
# render_ep.sh <epdir> <name> : resumable 5 s chunks on 2 workers -> sfx -> Timeless@0:12 mix -> final + <9.3 MB upload copy
set -e
D=$(cd "$1" && pwd); NAME=$2; TOOLS=$(cd "$(dirname "$0")" && pwd); cd "$D"
[ -f spec.json ] || node render.cjs spec
T=$(python3 -c "import json;print(json.load(open('spec.json'))['total'])")
segs=$(python3 -c "import math; T=$T; n=math.ceil(T/5); print(' '.join(f'{i}:{i*5}:{min(T,(i+1)*5)}' for i in range(n)))")
todo=(); for sg in $segs; do IFS=: read i a b <<< "$sg"; [ -f seg_$i.mp4 ] || todo+=("$sg"); done
worker() { for sg in "$@"; do IFS=: read i a b <<< "$sg"; node render.cjs video $a $b seg_$i.mp4 >> log_$i.txt 2>&1; done; }
A=(); B=(); k=0; for sg in "${todo[@]}"; do if (( k % 2 == 0 )); then A+=("$sg"); else B+=("$sg"); fi; k=$((k+1)); done
worker "${A[@]}" & worker "${B[@]}" & wait
n=$(python3 -c "import math;print(math.ceil($T/5))"); for ((i=0;i<n;i++)); do [ -f seg_$i.mp4 ] || { echo "missing seg_$i"; exit 1; }; done
python3 "$TOOLS/autosfx.py" "$D"
python3 "$TOOLS/mix2.py" "$D" "$T" 12
ls seg_*.mp4 | sort -V | sed "s/^/file '/; s/$/'/" > list.txt
ffmpeg -y -loglevel error -f concat -i list.txt -c copy vid.mp4
ffmpeg -y -loglevel error -i vid.mp4 -i mix_music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "${NAME}_final.mp4"
BR=$(python3 -c "print(int((9.3e6*8/$T - 100e3)/1000))")
ffmpeg -y -loglevel error -i vid.mp4 -c:v libx264 -preset slow -b:v ${BR}k -pass 1 -passlogfile pl -an -f null /dev/null
ffmpeg -y -loglevel error -i vid.mp4 -i mix_music.wav -map 0:v -map 1:a -c:v libx264 -preset slow -b:v ${BR}k -pass 2 -passlogfile pl -pix_fmt yuv420p -c:a aac -b:a 96k -shortest -movflags +faststart "${NAME}_upload.mp4"
ls -la "${NAME}_final.mp4" "${NAME}_upload.mp4"; echo RENDER_DONE
