# mix3.py <epdir> <seconds> [music_start=12] : narrated mix. Voice on top, music ducked under the voice, subtle effects.
import sys, os, wave, subprocess, numpy as np
ep, T = sys.argv[1], float(sys.argv[2]); START = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0; SR = 44100; N = int(SR * T)
TRACK = os.environ.get("WHATIF_TRACK", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "music", "main_track.mp3"))
def read_wav(p):
    with wave.open(p) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float).reshape(-1, 2) / 32768
    return np.pad(x, ((0, max(0, N - len(x))), (0, 0)))[:N]
sfx = read_wav(f'{ep}/sfx.wav'); vo = read_wav(f'{ep}/vo.wav')
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(START), '-i', TRACK, '-t', str(T), '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
mus = np.frombuffer(raw, np.int16).astype(float).reshape(-1, 2) / 32768; mus = np.pad(mus, ((0, max(0, N - len(mus))), (0, 0)))[:N]
t = np.arange(N) / SR; mus *= (np.clip(t / 0.4, 0, 1) * np.clip((T - t) / 2.0, 0, 1))[:, None]
# sidechain: follow the voice level (fast attack, slow release) and pull the music down while it speaks
e = np.abs(vo).max(1); k = int(.05 * SR); e = np.convolve(e, np.ones(k) / k, 'same'); rel = np.exp(-1 / (.45 * SR)); g = np.zeros(N); a = 0.
on = (e > .02).astype(float)
for i in range(0, N, 64):
    v = on[i:i + 64].max(); a = max(v, a * rel ** 64); g[i:i + 64] = a
duck = 1 - .68 * g
mix = vo * 1.0 + mus * (0.34 * duck)[:, None] + sfx * 0.42 * (1 - .35 * g)[:, None]
pk = np.max(np.abs(mix)); mix = mix / pk * 0.95 if pk > 0.95 else mix
with wave.open(f'{ep}/mix_music.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok narrated mix', ep)
