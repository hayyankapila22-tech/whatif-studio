# mix2.py <epdir> <seconds> [music_start=12] : Season 2 audio.
#   mix_music.wav -> main track from 0:00 under the sound effects (TikTok + YouTube)
#   mix_ig.wav    -> sound effects only (Instagram, which restricts copyrighted music)
import sys, os, wave, subprocess, numpy as np
ep, T = sys.argv[1], float(sys.argv[2]); START = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0; SR = 44100; N = int(SR * T)
TRACK = os.environ.get("WHATIF_TRACK", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "music", "main_track.mp3"))
def read_wav(p):
    with wave.open(p) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float).reshape(-1, 2) / 32768
    return np.pad(x, ((0, max(0, N - len(x))), (0, 0)))[:N]
def save(p, x):
    pk = np.max(np.abs(x)); x = x / pk * 0.95 if pk > 0.95 else x
    with wave.open(p, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())
sfx = read_wav(f'{ep}/sfx.wav'); sfx = sfx / max(1e-6, np.max(np.abs(sfx))) * 0.92
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(START), '-i', TRACK, '-t', str(T), '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
mus = np.frombuffer(raw, np.int16).astype(float).reshape(-1, 2) / 32768; mus = np.pad(mus, ((0, max(0, N - len(mus))), (0, 0)))[:N]
t = np.arange(N) / SR; mus *= (np.clip(t / 0.15, 0, 1) * np.clip((T - t) / 1.5, 0, 1))[:, None]
save(f'{ep}/mix_music.wav', mus * 0.40 + sfx * 1.0)   # effects sit above the music (the hook)
save(f'{ep}/mix_ig.wav', sfx)
print('ok', ep)
