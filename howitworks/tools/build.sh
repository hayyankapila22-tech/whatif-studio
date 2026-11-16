#!/usr/bin/env bash
# Build one HOW DOES IT WORK? episode end to end.
#   howitworks/tools/build.sh howitworks/episodes/hiwNN_slug  OUTNAME
# Steps: voice (Kokoro af_heart) + word timings -> textures/grain -> render in parallel chunks
#        -> mix (voice + very quiet Timeless + sfx) -> -14 LUFS -> OUTNAME_final.mp4 + OUTNAME_upload.mp4 (< 9.3 MB)
# Re-runnable: finished chunks are kept (delete parts/ to force a full re-render).
set -e
EP="$(cd "$1" && pwd)"; NAME="$2"
T="$(cd "$(dirname "$0")" && pwd)"
cd "$EP"
[ -s timings.json ] && [ -s vo_raw.wav ] || python3 "$T/tts.py"
[ -s grain0.png ] || python3 "$T/grain.py"
if grep -q 'skin_' episode.py && ! ls skin_*.png >/dev/null 2>&1; then python3 "$T/make_skin.py" "${TONE:-#D7A47E}"; fi
N=$(python3 -c "import json;print(int(json.load(open('timings.json'))['duration']*30))")
J=$(nproc); [ "$J" -lt 2 ] && J=2
mkdir -p parts
q=$(( (N + J*2 - 1) / (J*2) ))
pids=(); list=""
for ((i=0; i<J*2; i++)); do
  a=$((i*q)); b=$(( (i+1)*q )); [ $b -gt $N ] && b=$N; [ $a -ge $N ] && break
  f=$(printf "parts/p%02d.mp4" $i); list="$list$f\n"
  if [ ! -s "$f" ]; then
    python3 episode.py $a $b "$f" 2>/dev/null & pids+=($!)
    if [ ${#pids[@]} -ge $J ]; then wait "${pids[0]}"; pids=("${pids[@]:1}"); fi
  fi
done
wait
printf "$list" | sed "s/^/file '/; s/$/'/" > list.txt
python3 "$T/audio.py"
ffmpeg -hide_banner -i mix_pre.wav -af loudnorm=I=-14:TP=-1:LRA=7:print_format=json -f null - 2>&1 | tail -12 > ln.json
read I TP LRA TH OFF < <(python3 -c "import json;d=json.load(open('ln.json'));print(d['input_i'],d['input_tp'],d['input_lra'],d['input_thresh'],d['target_offset'])")
ffmpeg -y -loglevel error -i mix_pre.wav -af "loudnorm=I=-14:TP=-1.6:LRA=7:measured_I=$I:measured_TP=$TP:measured_LRA=$LRA:measured_thresh=$TH:offset=$OFF:linear=true,aresample=48000" -c:a pcm_s16le mix.wav
ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy video.mp4
ffmpeg -y -loglevel error -i video.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "${NAME}_final.tmp.mp4"
mv "${NAME}_final.tmp.mp4" "${NAME}_final.mp4"
# upload copy under 9.3 MB (two-pass, bitrate from duration)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${NAME}_final.mp4")
VB=$(python3 -c "print(int((8.4*8*1024*1024/$D - 128000)/1000))")
ffmpeg -y -loglevel error -i "${NAME}_final.mp4" -c:v libx264 -preset medium -b:v ${VB}k -pass 1 -an -f null /dev/null
ffmpeg -y -loglevel error -i "${NAME}_final.mp4" -c:v libx264 -preset medium -b:v ${VB}k -pass 2 -c:a aac -b:a 128k -movflags +faststart "${NAME}_upload.tmp.mp4"
mv "${NAME}_upload.tmp.mp4" "${NAME}_upload.mp4"; rm -f ffmpeg2pass*
ls -la "${NAME}_final.mp4" "${NAME}_upload.mp4"
ffmpeg -hide_banner -i "${NAME}_upload.mp4" -af ebur128=peak=true -f null - 2>&1 | grep -A15 Summary | grep -E " I:|Peak:"
