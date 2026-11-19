#!/usr/bin/env bash
# One-time setup for a fresh cloud session: python deps, Kokoro voice model, JetBrains Mono.
set -e
A="${HIW_ASSETS:-/home/claude/hiw_assets}"
mkdir -p "$A"
pip install --break-system-packages -q skia-python kokoro-onnx soundfile scipy pillow numpy 2>&1 | grep -v -i warn || true
cd "$A"
[ -s kokoro.onnx ] || curl -sSL -o kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s voices.bin ] || curl -sSL -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
if [ ! -d jbm/fonts ]; then
  curl -sSL -o jbm.zip https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
  unzip -oq jbm.zip -d jbm
fi
ls /usr/share/fonts/opentype/inter/InterDisplay-Bold.otf >/dev/null || { echo "Inter fonts missing: install fonts-inter"; exit 1; }
# Human-sounding voice (owner pick 2026-11-19): Chatterbox in its own venv (~6 GB, ~5 min), Liam reference voice.
# Needs huggingface.co + *.huggingface.co + *.hf.co allowed (Settings > Capabilities). Falls back to Kokoro if this fails.
CBX="${HIW_CB_VENV:-/home/claude/cbx}"
if [ ! -x "$CBX/bin/python" ] || ! "$CBX/bin/python" -c "import chatterbox" 2>/dev/null; then
  python3 -m venv "$CBX" && "$CBX/bin/pip" install -q chatterbox-tts "setuptools<81" 2>&1 | grep -v -i warn || true
fi
"$CBX/bin/python" -c "from chatterbox.tts import ChatterboxTTS; ChatterboxTTS.from_pretrained(device='cpu')" >/dev/null 2>&1 \
  && echo "Chatterbox ready ($CBX)" || echo "WARNING: Chatterbox not available -> tts.py falls back to Kokoro (log it in reports/issues.md)"
echo "HIW setup ok -> $A"
