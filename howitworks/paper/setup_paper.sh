#!/bin/bash
# Paper-cutout format setup (cloud session). Installs into the system Python + a chatterbox venv at /home/claude/cbx.
set -e
pip install --break-system-packages -q skia-python scipy pillow numpy >/dev/null 2>&1 || true
which ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
if [ ! -x /home/claude/cbx/bin/python3 ]; then
  python3 -m venv --system-site-packages /home/claude/cbx
  /home/claude/cbx/bin/pip install -q chatterbox-tts
fi
echo "paper setup ok. Voice: /home/claude/cbx/bin/python3 ../../tts_voice.py (inside an episode folder)"
