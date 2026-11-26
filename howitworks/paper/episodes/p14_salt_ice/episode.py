"""P14 — Why does salt melt ice on the road? (PAPER-CUTOUT format)
Facts (plain words, no studies): salt doesn't heat anything. Ice always has a thin film of liquid water on its surface,
where molecules constantly melt off and refreeze. Salt dissolves into that water and gets in the way of it freezing again
(it lowers the freezing point of the water), so melting wins over freezing and the ice turns to slush even below 0 °C.
Rock salt gets much less effective when it's colder than about -10 °C (around 15 °F), so road crews switch to other
chemicals or add sand / grit for traction.
Sources: Scientific American "Salt Doesn't Melt Ice—Here's How It Makes Winter Streets Safer"; HowStuffWorks "Why Does
Salt Melt Ice on the Roads in Winter?"; PBS NewsHour "Why does salt melt road ice?"; City of Greater Sudbury "How does
salt work?"; North Lanarkshire Council "Salt and how it works".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['teal', 'orange', 'blue', 'purple', 'mint', 'coral'], shakes=[S[1] + 1.0, S[3] + 2.2, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
ICE = (.75, .9, 1.0)
def has(n): return os.path.exists(os.path.join(LIB, n + '.png'))

def grains(c, tq, t0, x, y, n=14, spread=70, fall=520, seed=0):
    """salt grains falling from (x, y)"""
    if tq < t0: return
    r = random.Random(seed)
    for i in range(n):
        ph = r.uniform(0, 1); dx = r.uniform(-spread, spread)
        p = ((tq - t0) * 1.6 + ph) % 1.0
        gx = x + dx * (0.3 + p); gy = y + p * fall
        c.save(); c.translate(gx, gy); c.rotate(r.uniform(0, 90) + tq * 200)
        c.drawRect(skia.Rect.MakeXYWH(-9, -9, 18, 18), skia.Paint(Color=skia.Color4f(.4, .45, .55, 1), AntiAlias=True))
        c.drawRect(skia.Rect.MakeXYWH(-7, -7, 14, 14), skia.Paint(Color=skia.Color4f(1, 1, 1, 1), AntiAlias=True))
        c.restore()

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook
        rays(c, W/2, 1200, 1100, WHT, tq*12, f.k(0.05, 0.45), a=0.25)
        stk(c, 'ice_cube', W*0.45 + jx, 1350 + jy, 1.0, -4 + jr, f.k(0.0, 0.3), maxd=560)
        sh = 18*math.sin(tq*30)
        stk(c, 'salt_shaker', W*0.70 + jx + sh, 860 + jy, 0.8, 160 + jr + sh*.3, f.k(0.3, 0.55), maxd=420)
        grains(c, tq, 0.6, W*0.66, 1000, seed=1, fall=300)
        glyph(c, '?', 150, 900, 140, -12 + jr*2, f.k(0.5, 0.75))
        label(c, "why does SALT", W/2 + jx*.4, 330, 96, -3 + jr*.5, k=f.k(0.1, 0.35), seed=1)
        label(c, "MELT ICE?", W/2 + 10, 470, 110, 2 - jr*.5, bgcol=ICE, k=f.k(0.7, 0.95), seed=2)
    elif b == 1:  # salt isn't hot
        s0 = S[1]
        stk(c, 'salt_shaker', W*0.34 + jx, 1100 + jy, 0.9, -8 + jr, f.k(B[1] + 0.1, B[1] + 0.35), maxd=480)
        stk(c, 'thermometer', W*0.72 + jx, 1050 + jy, 0.7, 12 + jr, f.k(s0 + 0.6, s0 + 0.85), maxd=400)
        if tq > s0 + 1.0: stamp(c, "NOT HOT!", W*0.5, 1560, 120, -6, f.k(s0 + 1.0, s0 + 1.25), col=(.1, .45, .95))
        label(c, "THE TWIST:", W/2, 330, 100, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.0, s0 + 0.25), seed=3)
        label(c, "salt ISN'T HOT!", W/2 + 15, 470, 100, 3 - jr*.5, k=f.k(s0 + 0.6, s0 + 0.85), seed=4)
    elif b == 2:  # thin water layer, melting + freezing
        s0 = S[2]
        stk(c, 'ice_cube', W*0.5 + jx, 1250 + jy, 1.15, jr, f.k(B[2] + 0.1, B[2] + 0.35), maxd=580)
        for i, (dx, dy) in enumerate([(-200, -230), (40, -280), (230, -200), (-90, 40)]):
            if tq > s0 + 1.0 + i*0.12: drop(c, W*0.5 + dx + jx, 1250 + dy + jy + 10*math.sin(tq*8 + i), 34, 8*math.sin(tq*20 + i), seed=i)
        a = f.k(s0 + 2.0, s0 + 2.4)
        arrow(c, W*0.14, 1500, 300, -90, a, col=(1, .5, .2)); arrow(c, W*0.86, 1200, 300, 90, a, col=ICE)
        label(c, "ICE has a WATER layer", W/2, 330, 80, -2 + jr*.5, bgcol=ICE, k=f.k(s0 + 0.9, s0 + 1.15), seed=5)
        label(c, "MELTING + FREEZING", W/2 + 15, 470, 84, 3 - jr*.5, k=f.k(s0 + 2.0, s0 + 2.25), seed=6)
    elif b == 3:  # salt gets in the way
        s0 = S[3]
        stk(c, 'ice_cube', W*0.48 + jx, 1400 + jy, 1.0, jr, f.k(B[3] + 0.1, B[3] + 0.35), maxd=560)
        sh = 18*math.sin(tq*30)
        stk(c, 'salt_shaker', W*0.62 + jx + sh, 820 + jy, 0.75, 160 + jr + sh*.3, f.k(s0 + 0.1, s0 + 0.35), maxd=400)
        grains(c, tq, s0 + 0.4, W*0.58, 950, n=18, fall=420, seed=2)
        if tq > s0 + 2.2: stamp(c, "BLOCKED!", W*0.5, 1700, 110, -6, f.k(s0 + 2.2, s0 + 2.45))
        label(c, "SALT mixes in", W/2, 330, 100, -2 + jr*.5, k=f.k(s0 + 0.1, s0 + 0.35), seed=7)
        label(c, "NO freezing back!", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.6, s0 + 1.85), seed=8)
    elif b == 4:  # more melts than freezes, below zero
        s0 = S[4]
        water(c, lerp(1750, 1350, eo(f.k(s0 + 0.3, s0 + 2.0))), tq)
        kk = 1 - f.k(s0 + 0.8, s0 + 2.0)
        if kk > 0: stk(c, 'ice_cube', W*0.45 + jx, 1180 + jy, 1.0*max(0.35, kk), jr, 1, maxd=520, alpha=min(1, max(0, kk*1.5)))
        stk(c, 'thermometer', W*0.24 + jx, 860 + jy, 0.6, -10 + jr, f.k(s0 + 1.4, s0 + 1.65), maxd=360)
        if tq > s0 + 1.9: stamp(c, "-5°C", W*0.24, 1080, 80, -8, f.k(s0 + 1.9, s0 + 2.15), col=(.1, .45, .95))
        if tq > s0 + 2.4: stamp(c, "MELTED!", W*0.55, 1150, 100, 5, f.k(s0 + 2.4, s0 + 2.65))
        stk(c, 'snowflake', W*0.76 + jx, 860 + jy, 0.75, tq*20, f.k(s0 + 1.4, s0 + 1.65), maxd=380)
        label(c, "MORE MELTS", W/2, 330, 104, -2 + jr*.5, bgcol=ICE, k=f.k(s0 + 0.2, s0 + 0.45), seed=9)
        label(c, "even BELOW ZERO!", W/2 + 15, 470, 92, 3 - jr*.5, k=f.k(s0 + 1.4, s0 + 1.65), seed=10)
    else:         # colder than -10 -> sand
        s0 = S[5]
        stk(c, 'car', W*0.32 + jx, 1080 + jy, 0.95, -6 + jr, f.k(s0 + 0.1, s0 + 0.35), maxd=480)
        stk(c, 'thermometer', W*0.78 + jx, 820 + jy, 0.7, 10 + jr, f.k(s0 + 0.6, s0 + 0.85), maxd=360)
        if tq > s0 + 1.3: stamp(c, "-10°C", W*0.78, 1080, 90, 8, f.k(s0 + 1.3, s0 + 1.55), col=(.1, .45, .95))
        stk(c, 'sand_pile', W*0.62 + jx, 1400 + jy, 1.1, 4 + jr, f.k(s0 + 3.0, s0 + 3.25), maxd=480)
        label(c, "colder than -10°C?", W/2, 330, 88, -2 + jr*.5, bgcol=ICE, k=f.k(s0 + 0.6, s0 + 0.85), seed=11)
        label(c, "SAND for GRIP!", W/2 + 15, 470, 100, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 3.0, s0 + 3.25), seed=12)
        if tq > DUR - 1.5: stamp(c, "TIP!", W*0.22, 1560, 120, -8, f.k(DUR - 1.5, DUR - 1.25), col=(.1, .6, .3))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.4); K.sfx(0.1, 'pop', 0.6); K.sfx(0.3, 'pop', 0.6); K.sfx(0.5, 'pop', 0.6); K.sfx(0.6, 'scratch2', 0.4); K.sfx(0.7, 'pop', 0.7)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.0, 'pop', 0.6); K.sfx(S[1] + 0.6, 'pop', 0.6); K.sfx(S[1] + 1.0, 'impact1', 0.9); K.sfx(S[1] + 1.05, 'ding2', 0.4)
K.sfx(B[2] + 0.1, 'pop', 0.7)
for i in range(4): K.sfx(S[2] + 1.0 + i*0.12, 'bubble' if i % 2 else 'splash2', 0.35)
K.sfx(S[2] + 0.9, 'pop', 0.6); K.sfx(S[2] + 2.0, 'swoosh3', 0.5); K.sfx(S[2] + 2.0, 'pop', 0.6)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.1, 'pop', 0.6); K.sfx(S[3] + 0.4, 'scratch2', 0.5); K.sfx(S[3] + 1.6, 'pop', 0.6); K.sfx(S[3] + 2.2, 'impact1', 0.9)
K.sfx(S[4] + 0.2, 'pop', 0.7); K.sfx(S[4] + 0.3, 'splash1', 0.5); K.sfx(S[4] + 1.0, 'bubble', 0.4); K.sfx(S[4] + 1.4, "pop", 0.6); K.sfx(S[4] + 1.45, "sparkle1", 0.5); K.sfx(S[4] + 1.9, "impact2", 0.6); K.sfx(S[4] + 2.4, "impact1", 0.8)
K.sfx(S[5] + 0.1, 'pop', 0.7); K.sfx(S[5] + 0.6, 'pop', 0.6); K.sfx(S[5] + 1.3, 'impact2', 0.7); K.sfx(S[5] + 3.0, 'pop', 0.7); K.sfx(S[5] + 3.05, 'scratch1', 0.4)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle2', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p14_salt_ice')
