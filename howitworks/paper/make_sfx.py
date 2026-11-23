"""Synthesise the paper-kit sound effects into sfx/*.mp3 (fallback when the Pixabay sfx files are not on disk).
The original Pixabay sfx/ and music/ files were never committed (*.mp3 is gitignored), so a fresh cloud session
has none. Run:  python3 make_sfx.py   (writes only the files that are missing)."""
import os, subprocess, numpy as np
from scipy.signal import butter, sosfilt
SR = 48000; R = np.random.default_rng(3)
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'sfx'); os.makedirs(OUT, exist_ok=True)
def tt(d): return np.arange(int(d * SR)) / SR
def noise(d): return R.normal(0, 1, int(d * SR))
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lpf(x, f, o=2): return sosfilt(butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def hpf(x, f, o=2): return sosfilt(butter(o, f, 'highpass', fs=SR, output='sos'), x)
def env(t, a, d): return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(d, 1e-4))
def norm(x, p=.9): return x / (np.max(np.abs(x)) + 1e-9) * p
def fade(x, b=.03):
    n = int(b * SR); x = x.copy(); x[-n:] *= np.linspace(1, 0, n); return x
def chirp(f0, f1, d):
    t = tt(d); f = f0 * (f1 / f0) ** (t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR)

def pop():
    t = tt(.16); s = chirp(380, 1250, .16) * env(t, .002, .035) + bp(noise(.16), 1500, 5000) * env(t, .001, .006) * .4
    return s
def whoosh(d=1.0):
    t = tt(d); n = noise(d); sh = np.sin(np.pi * t / d) ** 2
    f = np.concatenate([bp(n[i:i + 2400], 300 + 2500 * (i / len(n)), 900 + 4000 * (i / len(n))) for i in range(0, len(n), 2400)])[:len(n)]
    return f * sh
def swoosh(d=.45, lo=600, hi=5000):
    t = tt(d); n = noise(d); sh = (t / d) ** 1.5 * np.exp(-((t / d - .7) ** 2) / .04)
    return hpf(bp(n, lo, hi), 300) * sh
def paper():
    d = .55; t = tt(d); n = noise(d)
    crack = np.zeros_like(n)
    for k in range(40):
        i = int(R.uniform(0, .45) * SR); L = int(.004 * SR); crack[i:i + L] += R.normal(0, 1, L) * np.exp(-np.arange(L) / 60)
    return bp(crack, 1500, 9000) * 1.2 + bp(n, 2000, 8000) * env(t, .02, .15) * .3
def impact(low=55, d=1.2):
    t = tt(d); thump = np.sin(2 * np.pi * np.cumsum(low + 90 * np.exp(-t / .04)) / SR) * env(t, .002, .25)
    return thump + lpf(noise(d), 900) * env(t, .001, .06) * .8 + bp(noise(d), 2000, 7000) * env(t, .001, .01) * .4
def sparkle(n=9, d=1.4, base=1800):
    t = tt(d); s = np.zeros_like(t)
    for k in range(n):
        st = k * d * .06 + R.uniform(0, .03); f = base * 2 ** (R.integers(0, 14) / 7); i = int(st * SR); tl = t[:len(t) - i]
        s[i:] += np.sin(2 * np.pi * f * tl) * env(tl, .002, .18) * (1 - k / (n + 2))
    return s
def bubble(n=7, d=1.4):
    t = tt(d); s = np.zeros_like(t)
    for k in range(n):
        i = int((k * .13 + R.uniform(0, .05)) * SR); L = int(.09 * SR); f0 = R.uniform(350, 800)
        s[i:i + L] += chirp(f0, f0 * 2.2, .09)[:len(s[i:i + L])] * env(tt(.09), .004, .03)[:len(s[i:i + L])]
    return s
def splash(d=1.4):
    t = tt(d); return bp(noise(d), 400, 7000) * env(t, .005, .25) + lpf(noise(d), 500) * env(t, .002, .08) * .8 + bubble(5, d) * .3
def scratch(d=1.2):
    t = tt(d); s = np.zeros_like(t)   # record-scratch: fast pitch wobble on filtered noise + tone
    f = 420 + 300 * np.sin(2 * np.pi * 3.2 * t) * np.exp(-t / .6)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * .5
    return (bp(noise(d), 800, 3500) * .7 + tone) * env(t, .005, .35) * (np.abs(np.sin(2 * np.pi * 3.2 * t)) * .7 + .3)
def ding(f=1320, d=1.6, two=True):
    t = tt(d); s = (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / .2)) * env(t, .002, .45)
    if two:
        i = int(.12 * SR); tl = t[:len(t) - i]; s[i:] += (np.sin(2 * np.pi * f * 1.5 * tl)) * env(tl, .002, .5)
    return s
def snip():
    d = .35; t = tt(d); s = np.zeros_like(t)
    for st in (0.0, .12):
        i = int(st * SR); L = int(.03 * SR); s[i:i + L] += bp(noise(.03), 2500, 9000) * np.exp(-np.arange(L) / 250)
    return s

FX = {'pop': pop, 'whoosh': lambda: whoosh(1.0), 'swoosh1': lambda: swoosh(.45), 'swoosh2': lambda: swoosh(.5, 400, 3500),
      'swoosh3': lambda: swoosh(.8, 300, 4000), 'paper': paper, 'impact1': impact, 'impact2': lambda: impact(42, 1.6),
      'sparkle1': sparkle, 'sparkle2': lambda: sparkle(12, 1.5, 2400), 'bubble': bubble, 'splash1': splash, 'splash2': lambda: splash(1.7),
      'scratch1': scratch, 'scratch2': lambda: scratch(1.0), 'ding1': ding, 'ding2': lambda: ding(1760, .7, False), 'snip': snip}
for n, fn in FX.items():
    p = os.path.join(OUT, n + '.mp3')
    if os.path.exists(p): continue
    x = norm(fade(fn())).astype(np.float32)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-b:a', '192k', p], input=x.tobytes(), check=True)
    print('sfx', n)
