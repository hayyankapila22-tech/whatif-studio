# narrate.py <epdir> [voice=af_heart] [speed=1.0] : AI voiceover (Kokoro, open-source, runs locally).
# Reads <epdir>/vo_lines.json = [{"say": "text to speak (numbers written as words)", "show": "caption text"}, ...]
# Writes <epdir>/vo.wav (44.1 kHz stereo, full episode length) and <epdir>/vo.json = {total, lines:[{t0,t1,show}]}.
# The scene reads vo.json and times every camera move / caption / sound to it, so picture and voice always match.
import sys, os, json, subprocess, urllib.request, wave, numpy as np
from scipy.signal import resample_poly
ep = sys.argv[1]; voice = sys.argv[2] if len(sys.argv) > 2 else 'af_heart'; speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
M = os.environ.get('KOKORO_DIR', '/home/claude/tts'); os.makedirs(M, exist_ok=True)
for f in ('kokoro-v1.0.onnx', 'voices-v1.0.bin'):
    p = os.path.join(M, f)
    if not os.path.exists(p) or os.path.getsize(p) < 1e6:
        subprocess.run(['curl', '-sSL', '-f', '-o', p, 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/' + f], check=True)
try: from kokoro_onnx import Kokoro
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', 'kokoro-onnx', 'soundfile'], check=True); from kokoro_onnx import Kokoro
k = Kokoro(os.path.join(M, 'kokoro-v1.0.onnx'), os.path.join(M, 'voices-v1.0.bin'))
lines = json.load(open(os.path.join(ep, 'vo_lines.json')))
SR = 44100; START, GAP, TAIL = 0.35, 0.30, 3.4
t = START; clips = []; out = []
for ln in lines:
    s, sr = k.create(ln['say'], voice=voice, speed=speed, lang='en-gb' if voice[0] == 'b' else 'en-us')
    s = np.asarray(s, dtype=np.float64); nz = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, nz[0] - 400): nz[-1] + 1200] if len(nz) else s
    s = resample_poly(s, SR, sr); d = len(s) / SR
    gap = ln.get('gap', GAP); t += ln.get('pre', 0)
    clips.append((t, s)); out.append({'t0': round(t, 3), 't1': round(t + d, 3), 'show': ln.get('show', ln['say'])}); t += d + gap
total = round(t - GAP + TAIL, 2); N = int(total * SR); x = np.zeros(N)
for t0, s in clips: i = int(t0 * SR); x[i:i + len(s)] += s[:N - i]
# gentle compression + normalise so the voice sits clearly on top
env = np.abs(x); c = np.tanh(x * 2.2) / 2.2; x = c / (np.max(np.abs(c)) + 1e-9) * 0.9
with wave.open(os.path.join(ep, 'vo.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.repeat(x[:, None], 2, 1) * 32767).astype(np.int16).tobytes())
json.dump({'total': total, 'voice': voice, 'lines': out}, open(os.path.join(ep, 'vo.json'), 'w'), indent=1)
print('vo ok', total, 's', len(out), 'lines')
