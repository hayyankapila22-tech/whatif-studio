# autosfx.py <epdir> : builds sfx.wav from spec.json (written by `node render.cjs spec`). Sound effects sit above the music.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sfxlib as L
ep = sys.argv[1]; S = json.load(open(os.path.join(ep, 'spec.json')))
T = S['total']; L.init(T); add = L.add
n = S.get('reel', 7) - 1
for k in range(1, n + 1): add(L.tick(), (1 - (1 - k / n) ** (1 / 3.2)) * 2.1, .9)
add(L.riser(2.0), 0.1, .25); add(L.ding(1568), 2.1, .55); add(L.whoosh(.5), 2.75, .45)
def thud(f=60):
    t = L.tt(.6); return np.sin(2 * np.pi * np.cumsum(f + 40 * np.exp(-t * 20)) / L.SR) * np.exp(-t * 8)
beats = S['beats']; cta = S.get('ctaAt', T - 5)
for i, b in enumerate(beats):
    t0 = b['t']; prev = beats[i - 1] if i else None
    add(L.whoosh(.35), max(0, t0 - .18), .32, pan=(-.3 if i % 2 else .3))
    if t0 < cta:
        add(L.pop(700 + 40 * i), t0, .35)
        for k in range(6): add(L.tick(), t0 + .05 + k * .1, .22 * (1 - k / 7))   # counter rolling
    if b.get('big'):
        add(L.boom(1.4 if b.get('space') else 1.1), t0, .85); add(thud(55), t0, .7); add(L.bong(110 if b.get('space') else 160), t0 + .02, .3)
    if b.get('space') and not (prev and prev.get('space')): add(L.whoosh(1.0), t0 - .4, .6); add(L.riser(1.2), t0 - 1.2, .3)
    if b.get('bubble'): add(L.pop(1500), t0 + .2, .5); add(L.pop(1900), t0 + .26, .3)
    nb = beats[i + 1]['t'] if i + 1 < len(beats) else T
    if nb - t0 > 2 and i + 1 < len(beats) and beats[i + 1].get('big'): add(L.riser(1.4), nb - 1.4, .28)
add(L.ding(1318), cta, .5); add(L.chaching(), cta + 2.3, .4)
import wave
x = L.mix / max(1e-6, np.max(np.abs(L.mix))) * 0.92
with wave.open(os.path.join(ep, 'sfx.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(L.SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
print('sfx ok', ep, T)
