import numpy as np, wave, subprocess, sys
SR = 44100; T = 59.0; N = int(SR * T)
mix = np.zeros((N, 2)); rng = np.random.default_rng(0)

def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[:j - i] * gain
    mix[i:j, 0] += s * np.sqrt((1 - pan) / 2) * 1.41
    mix[i:j, 1] += s * np.sqrt((1 + pan) / 2) * 1.41
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, k):
    k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, 'same')

def whoosh(d=0.5):
    t = tt(d); s = rng.normal(0, 1, len(t)); out = np.zeros(len(t))
    ks = np.linspace(30, 4, len(t))
    for i in range(0, len(t), 512):
        seg = s[max(0, i - 64):i + 576]; f = lp(seg, ks[i]) - lp(seg, ks[i] * 5)
        out[i:i + 512] = f[min(64, i):min(64, i) + 512][:len(out[i:i + 512])]
    return out * np.sin(np.pi * t / d) ** 2 * 2.5
def pop(f=900):
    t = tt(0.09); fr = f * (1 + 0.8 * np.exp(-t * 60)); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 45)
def shatter(d=1.3):
    t = tt(d); s = rng.normal(0, 1, len(t)) * np.exp(-t * 4.5)
    tinks = sum(np.sin(2 * np.pi * rng.uniform(2500, 7000) * t) * np.exp(-np.maximum(0, t - x) * 22) * (t > x) for x in rng.uniform(0, .7, 18)) * 0.13
    boom = np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-t * 10)) / SR) * np.exp(-t * 5)
    return s * 0.3 + tinks + boom * 0.9
def riser(d):
    t = tt(d); return (np.sin(2 * np.pi * np.cumsum(180 + 1100 * (t / d) ** 2) / SR) * 0.5 + lp(rng.normal(0, 1, len(t)), 3) * 0.3) * (t / d) ** 2
def tick():
    t = tt(0.05); return rng.normal(0, 1, len(t)) * np.exp(-t * 140) * 0.8 + np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 90) * .5
def buzz(d=0.5, f=110):
    t = tt(d); return np.sign(np.sin(2 * np.pi * f * t)) * 0.35 * np.minimum(1, (d - t) * 20)
def beep(f=2000, d=0.12):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.minimum(1, (d - t) * 60) * 0.5
def dtmf(a, b, d=0.13):
    t = tt(d); return (np.sin(2 * np.pi * a * t) + np.sin(2 * np.pi * b * t)) * 0.3 * np.minimum(1, (d - t) * 60)
def glitch(d=0.8):
    t = tt(d); sq = np.sign(np.sin(2 * np.pi * 140 * t * (1 + 2 * (rng.random(len(t)) > .97))))
    gate = (np.floor(t * 30) % 3 != 0); return (sq * 0.3 + rng.normal(0, .35, len(t))) * gate
def powerdown(d=0.9):
    t = tt(d); f = 600 * np.exp(-t * 4) + 30; return np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - t / d) * 0.6 + rng.normal(0, .1, len(t)) * (1 - t / d)
def ding(f=1318):
    t = tt(0.9); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 5) * .5
def chalk(d):
    t = tt(d); s = rng.normal(0, 1, len(t)); s = s - lp(s, 6)
    g = (np.sin(2 * np.pi * 7 * t) > -0.2) * (0.6 + 0.4 * np.sin(2 * np.pi * 2.3 * t)); return s * g * 0.12
def rumble(d=1.2):
    t = tt(d); return lp(rng.normal(0, 1, len(t)), 60) * 3 * np.minimum(1, t * 4) * np.exp(-t * 1.5)

# ---- timeline ----
add(riser(1.6), 0.0, .5); add(beep(3000, .05), 1.5, .3); add(shatter(1.6), 2.0, .9)
for s0 in [3.5, 7, 12, 15.5, 19.5, 23, 27, 32, 34.5, 37, 39.5, 42.5, 45, 49.5, 55]: add(whoosh(.5), s0 - .25, .35)
add(pop(1000), 4.2, .4)
for i in range(4): add(pop(700 + 80 * i), 7.0 + .07 * i, .3)
add(shatter(.9), 8.25, .6)
for i in range(4): add(pop(800 + 120 * i), 9.3 + .2 * i, .35, (-1) ** i * .3)
for x in [12.0, 12.6, 13.2]: add(tick(), x, .7)
add(buzz(.6, 90), 13.8, .45)
for i in range(4): add(beep(1800, .1), 13.9 + i * .25, .35)
add(shatter(.5)[:int(.5 * SR)], 14.0, .35)
add(chalk(1.0), 16.2, .7); add(chalk(.5), 17.3, .7); add(chalk(.6), 18.0, .7); add(chalk(.6), 18.5, .6)
for i in range(4): add(pop(900), 19.5 + .08 * i, .3)
add(glitch(.6), 20.3, .3); add(shatter(.9), 21.7, .55)
add(shatter(.7), 23.6, .5); add(ding(1568), 23.7, .25); add(shatter(.8), 24.75, .55); add(buzz(.35, 160), 26.0, .4)
add(shatter(.8), 27.85, .55); add(pop(600), 28.2, .4); add(shatter(.7), 30.45, .5); add(buzz(.3, 140), 30.9, .3)
for i in range(7): add(beep(2400, .09), 32.7 + i * .25, .4); add(beep(2400, .09), 32.82 + i * .25, .4)
add(pop(500), 35.35, .4); add(pop(450), 35.45, .4); add(pop(400), 35.55, .35)
for i, (a, b) in enumerate([(770, 1336), (770, 1336), (770, 1336), (697, 1336), (697, 1209)]): add(dtmf(a, b), 37.0 + i * .16, .5)
add(pop(1200), 37.95, .45); add(shatter(.5), 38.0, .3); add(buzz(.4, 220), 38.1, .35)
add(pop(800), 39.5, .3); add(pop(900), 39.7, .3); add(glitch(.5), 41.3, .25)
add(buzz(.9, 110), 43.3, .35)
for i in range(10): add(beep(rng.uniform(1500, 4000), .04), 45.0 + i * .14, .15)
add(riser(1.0)[::-1], 46.6, .3); add(glitch(.8), 47.2, .45); add(powerdown(.9), 48.0, .6)
add(rumble(1.3), 49.5, .8); add(ding(1318), 50.9, .4); add(whoosh(.5), 51.8, .4); add(whoosh(.5), 52.4, .4)
for i in range(3): add(pop(1000 + 100 * i), 55.6 + .3 * i, .4)
add(ding(1568), 56.9, .35)
sfx = mix.copy()

def save(name, x):
    x = x / max(1e-6, np.max(np.abs(x))) * 0.92
    with wave.open(name, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())
save('sfx.wav', sfx)

# music bed from user's track: 0:00–0:59, silent during blackout, fade out at end
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', sys.argv[1], '-t', str(T), '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
mus = np.frombuffer(raw, np.int16).astype(float).reshape(-1, 2) / 32768
mus = np.pad(mus, ((0, max(0, N - len(mus))), (0, 0)))[:N]
t = np.arange(N) / SR
env = np.ones(N)
env *= np.clip(t / 0.3, 0, 1)                                         # quick fade-in
env *= np.where((t > 48.0) & (t < 49.3), 0, 1)                        # blackout silence
env *= np.clip((t - 47.6) / 0.4, 0, 1) * (t < 48.2) + (t >= 48.2)     # dip into blackout
env = np.where((t > 47.6) & (t < 48.0), np.clip((48.0 - t) / 0.4, 0, 1), env)
env *= np.clip((T - t) / 1.5, 0, 1)                                   # fade out
mus *= env[:, None]
full = mus * 0.62 + sfx / max(1e-6, np.max(np.abs(sfx))) * 0.55
save('mix_with_track.wav', np.tanh(full * 1.2))
print('ok')
