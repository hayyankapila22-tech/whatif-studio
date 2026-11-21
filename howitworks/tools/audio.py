"""HOW DOES IT WORK? audio mix. Run inside an episode folder (needs vo_raw.wav + episode.py).

voice (processed) on top · Timeless instrumental from 0:12 VERY quietly underneath (owner: "very low, subtle"),
ducked further under the voice · synthesized UI sfx from episode.sfx_events(). Writes mix_pre.wav.
Loudness (-14 LUFS / -1 dBTP) is applied afterwards by build.sh.
"""
import os, sys, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.getcwd())
from episode import sfx_events, DUR

SR = 48000
N = int(DUR * SR)
rng = np.random.default_rng(1)
TRACK = os.environ.get("WHATIF_TRACK", "/home/claude/whatif-studio/assets/music/main_track.mp3")
MUSIC_START = float(os.environ.get("HIW_MUSIC_START", "12"))
MUSIC_LEVEL = float(os.environ.get("HIW_MUSIC_DB", "-11"))   # music RMS relative to voice RMS (dB)


def lp(x, f):
    return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)


def hp(x, f):
    return sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)


def bp(x, f1, f2):
    return sosfilt(butter(2, [f1, f2], "band", fs=SR, output="sos"), x)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-np.maximum(t - a, 0) / d)


# ---- voice ----
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo_raw.wav", "-af",
                "highpass=f=80,deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=4,alimiter=limit=0.89",
                "-ar", str(SR), "-ac", "1", "vo_proc.wav"], check=True)
v, _ = sf.read("vo_proc.wav")
v = np.pad(v, (0, max(0, N - len(v))))[:N]
v_rms = np.sqrt(np.mean(v[np.abs(v) > 0.01] ** 2))

# ---- music: Timeless instrumental from 0:12, very low ----
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(MUSIC_START), "-i", TRACK, "-t", str(DUR + 1),
                "-ar", str(SR), "-ac", "1", "music_seg.wav"], check=True)
m, _ = sf.read("music_seg.wav")
if len(m) < N:  # loop if the track is shorter than the episode (2 s crossfade at each seam, for long-form)
    full, _ = sf.read("music_seg.wav")
    xf = int(2.0 * SR)
    out = full.copy()
    while len(out) < N:
        fade = np.linspace(0, 1, xf)
        out[-xf:] = out[-xf:] * (1 - fade) + full[:xf] * fade
        out = np.concatenate([out, full[xf:]])
    m = out
m = m[:N]
m_rms = np.sqrt(np.mean(m ** 2)) + 1e-9
m = m / m_rms * v_rms * 10 ** (MUSIC_LEVEL / 20)
t_all = np.arange(N) / SR
if os.environ.get("HIW_LOOP") == "1":   # seamless loop: no fades, short crossfade of the music tail into its head
    xf = int(0.25 * SR)
    m[-xf:] = m[-xf:] * np.linspace(1, 0, xf) + m[:xf] * np.linspace(0, 1, xf)
else:
    m *= np.minimum(t_all / 0.6, 1) * np.minimum(1, np.maximum(0, (DUR - t_all) / 1.2))
# duck a further ~6 dB while the voice is talking
e = np.convolve(np.abs(v), np.ones(480) / 480, "same")
g = np.zeros(N); y = 0.0
att, rel = np.exp(-48 / (0.01 * SR)), np.exp(-48 / (0.3 * SR))
for i in range(0, N, 48):
    x = e[i]
    y = att * y + (1 - att) * x if x > y else rel * y + (1 - rel) * x
    g[i:i + 48] = y
duck = 1 - 0.35 * np.clip(g / (g.max() * 0.35 + 1e-9), 0, 1)
m *= duck

# ---- sfx ----
fx = np.zeros(N)


def add(sig, t, gain):
    s = int(t * SR)
    if s < 0:
        sig = sig[-s:]; s = 0
    e_ = min(N, s + len(sig))
    if e_ > s:
        fx[s:e_] += sig[: e_ - s] * gain


def sfx(kind):
    if kind == "tick":
        L = int(0.04 * SR); tt = np.arange(L) / SR
        return np.sin(2 * np.pi * 3200 * tt) * env(L, 0.0005, 0.008)
    if kind == "pop":
        L = int(0.12 * SR); tt = np.arange(L) / SR
        f = 380 + 700 * np.exp(-tt * 40)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(L, 0.002, 0.035)
    if kind == "whoosh":
        L = int(0.55 * SR); nz = rng.normal(0, 1, L); out = np.zeros(L)
        for k in range(10):
            a, b = k * L // 10, (k + 1) * L // 10
            fc = 400 + 3000 * np.sin(np.pi * k / 10)
            out[a:b] = bp(nz, fc * 0.6, fc * 1.4)[a:b]
        tt = np.arange(L) / SR
        return out * np.sin(np.pi * tt / tt[-1]) ** 2 * 1.2
    if kind == "paper":
        L = int(0.3 * SR); nz = hp(rng.normal(0, 1, L), 2500); tt = np.arange(L) / SR
        return nz * np.sin(np.pi * tt / tt[-1]) ** 3 * 0.5
    if kind == "hit":
        L = int(1.2 * SR); tt = np.arange(L) / SR
        f = 38 + 50 * np.exp(-tt * 12)
        sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(L, 0.003, 0.45)
        tr = lp(rng.normal(0, 1, L), 900) * env(L, 0.001, 0.05) * 0.8
        return np.tanh((sub * 1.4 + tr) * 1.2)
    if kind == "riser":
        L = int(1.6 * SR); tt = np.arange(L) / SR
        nz = bp(rng.normal(0, 1, L), 800, 5000)
        tone = np.sin(2 * np.pi * np.cumsum(200 + 600 * (tt / tt[-1]) ** 2) / SR)
        return (nz * 0.5 + tone * 0.3) * (tt / tt[-1]) ** 2.5
    if kind == "ding":
        L = int(1.0 * SR); tt = np.arange(L) / SR
        return (np.sin(2 * np.pi * 1320 * tt) + 0.4 * np.sin(2 * np.pi * 2640 * tt)) * env(L, 0.002, 0.25)
    raise ValueError(kind)


GAIN = {"tick": 0.10, "pop": 0.22, "whoosh": 0.22, "paper": 0.18, "hit": 0.55, "riser": 0.22, "ding": 0.10}
for kind, t in sfx_events():
    add(sfx(kind), t, GAIN[kind])

mix = v + m + fx
mix /= np.abs(mix).max() * 1.05
sf.write("mix_pre.wav", mix.astype(np.float32), SR)
print("music/voice dB:", round(20 * np.log10(np.sqrt(np.mean(m ** 2)) / v_rms), 1))
