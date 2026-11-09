# sfx2.py — richer synthesized sound design for Season 2 v3 (all generated here; no third-party samples).
# Event names used by episodes in spec.sfx: [{t, name, gain?, pan?, d?}] and spec.beds: [{t0, t1, name, gain?}].
import numpy as np
from scipy.signal import butter, sosfilt
SR = 44100
R = np.random.default_rng(7)

def tt(d): return np.arange(int(d * SR)) / SR
def noise(d): return R.normal(0, 1, int(d * SR))
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lpf(x, f, o=2): return sosfilt(butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def hpf(x, f, o=2): return sosfilt(butter(o, f, 'highpass', fs=SR, output='sos'), x)
def env(t, a, d): return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(d, 1e-4))
def fade(x, a=.02, b=.05):
    n = len(x); e = np.ones(n); ia, ib = int(a * SR), int(b * SR)
    if ia: e[:ia] = np.linspace(0, 1, ia)
    if ib: e[-ib:] = np.linspace(1, 0, ib)
    return x * e
def norm(x, p=.9): m = np.max(np.abs(x)) + 1e-9; return x / m * p

# ---------------------------------------------------------------- one-shots
def poof():      # magical vanish: airy burst + sparkly chime cluster
    d = 1.2; t = tt(d); air = bp(noise(d), 1500, 9000) * env(t, .01, .18)
    ch = sum(np.sin(2 * np.pi * f * t) * np.exp(-(t - o).clip(0) * 7) * (t > o) for f, o in zip([2349, 2794, 3520, 4186, 5274], [0, .04, .08, .12, .17]))
    sub = np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t * 8) + 60) / SR) * env(t, .005, .12)
    return norm(air * .7 + ch * .25 + sub * .6)
def clatter():   # paper cup hits pavement and rolls
    d = .9; t = tt(d); x = np.zeros(len(t))
    for o, g in [(0, 1), (.09, .55), (.17, .35), (.24, .22)]:
        i = int(o * SR); n = int(.06 * SR); x[i:i + n] += bp(noise(.06), 900, 5000) * np.exp(-tt(.06) * 60) * g
    roll = bp(noise(d), 300, 1800) * (t > .25) * np.exp(-(t - .25).clip(0) * 4) * .15
    return norm(x + roll)
def splash():
    d = .7; t = tt(d); return norm(bp(noise(d), 400, 4000) * env(t, .005, .12) + bp(noise(d), 2000, 8000) * env(t, .02, .25) * .4)
def car_roll():  # tyres on asphalt slowing + soft bump
    d = 2.6; t = tt(d); sp = np.clip(1 - t / 2.2, 0, 1)
    tyre = lpf(noise(d), 300) * sp * 3 + bp(noise(d), 600, 1400) * sp * .3
    bump = np.sin(2 * np.pi * np.cumsum(70 + 40 * np.exp(-(t - 2.15).clip(0) * 20)) / SR) * (t > 2.15) * np.exp(-(t - 2.15).clip(0) * 9)
    return norm(tyre * .6 + bump * 1.2)
def hazard(n=6):  # blinker relay ticks
    d = n * .4; x = np.zeros(int(d * SR))
    for k in range(n):
        for o, f in [(0, 2600), (.2, 1900)]:
            i = int((k * .4 + o) * SR); m = int(.03 * SR); x[i:i + m] += np.sin(2 * np.pi * f * tt(.03)) * np.exp(-tt(.03) * 120)
    return norm(x, .6)
def power_down():  # mains hum dives + relay clunks
    d = 2.2; t = tt(d); f = 120 * np.exp(-t * 1.6) + 18
    hum = (np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * np.clip(1 - t / d, 0, 1)
    x = hum * .6
    for o in [.35, .7, 1.1, 1.5]:
        i = int(o * SR); n = int(.08 * SR); x[i:i + n] += lpf(noise(.08), 900) * np.exp(-tt(.08) * 50) * 2
    return norm(x)
def flicker():    # electrical buzz/zap
    d = .7; t = tt(d); g = (np.sin(2 * np.pi * 13 * t) > 0) * 1.0
    return norm((np.sign(np.sin(2 * np.pi * 60 * t)) * .3 + hpf(noise(d), 3000) * .2) * g * np.exp(-t * 2))
def water_gush(d=2.4):
    t = tt(d); x = lpf(noise(d), 1400) * np.minimum(1, t / .6) * .8
    bub = np.zeros(len(t))
    for o in R.uniform(0, d - .1, 40):
        i = int(o * SR); n = int(.05 * SR); f = R.uniform(300, 900)
        bub[i:i + n] += np.sin(2 * np.pi * np.cumsum(f * (1 + tt(.05) * 8)) / SR) * np.exp(-tt(.05) * 50)
    return norm(fade(x + bub * .3, .2, .4))
def siren(d=2.4):  # distant alarm wail
    t = tt(d); f = 700 + 250 * np.sin(2 * np.pi * .6 * t)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return norm(lpf(s, 2200) * np.minimum(1, t / .4) * np.minimum(1, (d - t) / .4))
def bark(f0=420):
    d = .28; t = tt(d); f = f0 * (1 + .6 * np.exp(-t * 25)) * (1 - t)
    v = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .4 + R.normal(0, .3, len(t))
    v = bp(v, 300, 2400) + bp(v, 900, 1600) * 1.5
    return norm(v * env(t, .01, .07))
def howl(d=2.0):
    t = tt(d); f = 380 + 160 * np.sin(np.pi * t / d) ** .7 + 6 * np.sin(2 * np.pi * 5.5 * t)
    v = sum(np.sin(2 * np.pi * k * np.cumsum(f) / SR) / k ** 1.4 for k in range(1, 6)) + R.normal(0, .05, len(t))
    v = bp(v, 300, 3000)
    return norm(v * np.sin(np.pi * t / d) ** .6)
def crack():      # concrete/wall crack
    d = .5; t = tt(d); x = hpf(noise(d), 1500) * np.exp(-t * 30) + lpf(noise(d), 400) * np.exp(-t * 12) * 2
    return norm(x)
def pipe_burst():
    return norm(np.concatenate([crack() * .8, hpf(noise(.9), 2500) * np.linspace(1, .3, int(.9 * SR)) * .6]))
def crumble(d=3.0):  # building collapse: rumble + debris hits
    t = tt(d); x = lpf(noise(d), 160) * 4 * np.minimum(1, t / .2) * np.exp(-t * .9)
    for o in R.uniform(0, d * .8, 60):
        i = int(o * SR); n = int(.08 * SR); x[i:i + n] += bp(noise(.08), 200, 3000) * np.exp(-tt(.08) * 40) * R.uniform(.2, .9)
    return norm(x)
def wind_gust(d=2.4):
    t = tt(d); m = .6 + .4 * np.sin(2 * np.pi * .5 * t + 1)
    return norm(bp(noise(d), 200, 1200) * m * np.sin(np.pi * t / d))
def rustle(d=.8):
    t = tt(d); return norm(bp(noise(d), 2000, 7000) * (np.sin(2 * np.pi * 9 * t) > .3) * np.sin(np.pi * t / d))
def chirp_bird(f=3200):
    d = .18; t = tt(d); fr = f * (1 + .35 * np.sin(2 * np.pi * 18 * t)) * (1 + .3 * t / d)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / d) ** 2
def sparkle_rev():  # magical reappear (reverse-ish swell + chime)
    d = 1.0; t = tt(d); sw = bp(noise(d), 2000, 9000) * (t / d) ** 2
    ch = sum(np.sin(2 * np.pi * f * t) * np.exp(-(t - .7).clip(0) * 6) * (t > .7) for f in [1568, 2093, 2637])
    return norm(sw * .8 + ch * .4)

# ---------------------------------------------------------------- ambience beds (loopable, any length)
def bed_city(d):
    t = tt(d); x = lpf(noise(d), 250) * 2 + bp(noise(d), 400, 1500) * .15
    for o in R.uniform(0, max(.1, d - .5), int(d / 2) + 1):  # distant horns
        i = int(o * SR); n = int(.25 * SR); f = R.choice([370, 440, 494])
        x[i:i + n] += lpf(np.sign(np.sin(2 * np.pi * f * tt(.25))), 1500) * .06 * np.sin(np.pi * tt(.25) / .25)
    return x
def bed_silence_wind(d): t = tt(d); return bp(noise(d), 150, 700) * (.5 + .5 * np.sin(2 * np.pi * .15 * t)) * .6
def bed_crickets(d):
    t = tt(d); x = np.zeros(len(t))
    for f, rate, ph in [(4400, 2.8, 0), (4700, 3.1, .5), (5100, 2.5, 1.1)]:
        g = (np.sin(2 * np.pi * rate * t + ph) > .3) * (np.sin(2 * np.pi * 30 * t) > 0)
        x += np.sin(2 * np.pi * f * t) * lpf(g.astype(float), 200) * .25
    return x + bed_silence_wind(d) * .3
def bed_birds(d, dens=2.5):
    x = bed_silence_wind(d) * .35
    for o in R.uniform(0, max(.1, d - .4), int(d * dens)):
        c = chirp_bird(R.uniform(2400, 4800)); i = int(o * SR); n = min(len(c), len(x) - i)
        if n > 0: x[i:i + n] += c[:n] * R.uniform(.15, .45)
    return x
def bed_rain_drip(d):
    x = bp(noise(d), 1500, 6000) * .08
    for o in R.uniform(0, max(.1, d - .1), int(d * 6)):
        i = int(o * SR); n = int(.04 * SR); x[i:i + n] += np.sin(2 * np.pi * R.uniform(900, 2000) * tt(.04)) * np.exp(-tt(.04) * 80) * .2
    return x
def bed_winter(d): t = tt(d); return bp(noise(d), 300, 2500) * (.5 + .5 * np.sin(2 * np.pi * .23 * t)) * .7
def bed_drone(d):  # ominous low pad
    t = tt(d); return (np.sin(2 * np.pi * 55 * t) + .6 * np.sin(2 * np.pi * 82.4 * t) + .3 * np.sin(2 * np.pi * 110.3 * t)) * .3 * (.7 + .3 * np.sin(2 * np.pi * .3 * t))

def pop():        # thought-cloud pop: soft bubbly blip rising in pitch
    d = .32; t = tt(d); f = 380 + 900 * (t / d) ** .6
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, .004, .07) + bp(noise(d), 2000, 6000) * env(t, .002, .015) * .3)
def chips():      # poker chips clacking onto a stack
    d = .8; t = tt(d); x = np.zeros(len(t))
    for o, g in [(0, 1), (.07, .7), (.13, .6), (.2, .45), (.26, .35), (.33, .25)]:
        i = int(o * SR); n = int(.03 * SR); x[i:i + n] += (bp(noise(.03), 2500, 7000) + np.sin(2 * np.pi * 3100 * tt(.03)) * .4) * np.exp(-tt(.03) * 140) * g
    return norm(x)
def ding():       # bright two-note chime
    d = 1.0; t = tt(d)
    return norm(sum(np.sin(2 * np.pi * f * t) * np.exp(-(t - o).clip(0) * 5) * (t > o) for f, o in [(1318, 0), (1760, .11)]))
def bed_murmur(d):  # crowd murmur: speech-band noise with syllable-rate wobble
    t = tt(d); x = 0
    for k in range(5):
        x = x + bp(noise(d), 250 + k * 90, 900 + k * 150) * (.55 + .45 * np.sin(2 * np.pi * (3.1 + k * .7) * t + k))
    return x * .25

ONESHOT = dict(pop=pop, chips=chips, ding=ding, poof=poof, clatter=clatter, splash=splash, car_roll=car_roll, hazard=hazard, power_down=power_down, flicker=flicker,
               water_gush=water_gush, siren=siren, bark=bark, bark_hi=lambda: bark(560), howl=howl, crack=crack, pipe_burst=pipe_burst,
               crumble=crumble, wind_gust=wind_gust, rustle=rustle, bird=lambda: chirp_bird(3600), sparkle_rev=sparkle_rev)
BEDS = dict(murmur=bed_murmur, city=bed_city, wind=bed_silence_wind, crickets=bed_crickets, birds=bed_birds, drip=bed_rain_drip, winter=bed_winter, drone=bed_drone)
