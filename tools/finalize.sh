#!/bin/bash
set -e
cd "$1"
ls seg_*.mp4 | sort -V | sed "s/^/file '/; s/$/'/" > list.txt
ffmpeg -y -loglevel error -f concat -i list.txt -c copy vid.mp4
ffmpeg -y -loglevel error -i vid.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$2_final.mp4"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 vid.mp4)
BR=$(python3 -c "print(int((9.3e6*8/$D - 100e3)/1000))")
ffmpeg -y -loglevel error -i vid.mp4 -c:v libx264 -preset slow -b:v ${BR}k -pass 1 -passlogfile pl -an -f null /dev/null
ffmpeg -y -loglevel error -i vid.mp4 -i mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -b:v ${BR}k -pass 2 -passlogfile pl -pix_fmt yuv420p -c:a aac -b:a 96k -shortest -movflags +faststart "/mnt/user-data/outputs/$2_upload.mp4"
ls -la "$2_final.mp4" "/mnt/user-data/outputs/$2_upload.mp4"
