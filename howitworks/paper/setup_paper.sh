#!/bin/bash
# Paper-cutout format setup (cloud session). Installs into the system Python + a chatterbox venv at /home/claude/cbx.
set -e
pip install --break-system-packages -q skia-python scipy pillow numpy >/dev/null 2>&1 || true
which ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
if [ ! -x /home/claude/cbx/bin/python3 ]; then
  python3 -m venv --system-site-packages /home/claude/cbx
  /home/claude/cbx/bin/pip install -q chatterbox-tts
fi
# sound assets: the original Pixabay sfx/music were never committed (*.mp3 gitignored) -> synthesise sfx, fall back to the
# channel's Timeless bed if music/quirky.mp3 is missing (episodes pick quirky automatically when the file exists)
HERE="$(cd "$(dirname "$0")" && pwd)"
python3 "$HERE/make_sfx.py" >/dev/null
mkdir -p "$HERE/music"; [ -f "$HERE/music/timeless.mp3" ] || cp "$HERE/../../assets/music/main_track.mp3" "$HERE/music/timeless.mp3"
[ -f "$HERE/music/quirky.mp3" ] || echo "WARNING: music/quirky.mp3 missing -> episodes use music/timeless.mp3 (owner must add quirky.mp3, git add -f)"
[ -f "$HERE/voices/voice2_bubbly_presenter_ref.wav" ] || echo "WARNING: voices/voice2_bubbly_presenter_ref.wav missing"
echo "paper setup ok. Voice: /home/claude/cbx/bin/python3 ../../tts_voice.py (inside an episode folder)"
