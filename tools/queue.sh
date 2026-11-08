#!/bin/bash
# Renders each episode in 5 s chunks (kept across restarts), 2 workers, then finalizes.
S=/tmp/claude-0/-home-claude/a4041def-814a-5246-8af3-30b1a0476968/scratchpad
for pair in "ep2:50:WhatIf_Ep2_Doubling1c" "ep3:50:WhatIf_Ep3_HoleThroughEarth" "ep4:48:WhatIf_Ep4_EarthStopsSpinning" "ep5:50:WhatIf_Ep5_CarNeverStops" "ep6:47.5:WhatIf_Ep6_GravityDoubles"; do
  IFS=: read d T name <<< "$pair"; cd $S/$d
  if [ -f "$name"_final.mp4 ] && [ -f "/mnt/user-data/outputs/${name}_upload.mp4" ]; then echo "$d already done"; continue; fi
  segs=$(python3 -c "import math; T=$T; n=math.ceil(T/5); print(' '.join(f'{i}:{i*5}:{min(T,(i+1)*5)}' for i in range(n)))")
  todo=(); for sg in $segs; do IFS=: read i a b <<< "$sg"; [ -f seg_$i.mp4 ] || todo+=("$sg"); done
  worker() { for sg in "$@"; do IFS=: read i a b <<< "$sg"; node render.cjs video $a $b seg_$i.mp4 >> log_$i.txt 2>&1; done; }
  A=(); B=(); k=0; for sg in "${todo[@]}"; do if (( k % 2 == 0 )); then A+=("$sg"); else B+=("$sg"); fi; k=$((k+1)); done
  worker "${A[@]}" & worker "${B[@]}" & wait
  $S/finalize.sh $S/$d $name && echo "$d DONE"
done
echo ALL DONE
