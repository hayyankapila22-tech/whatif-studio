"""P17 — How does sunscreen stop a sunburn? (PAPER-CUTOUT format) — educational only, not medical advice.
Facts (plain words, no studies): sunburn is caused by ultraviolet (UV) rays in sunlight, which we can't see. Most
sunscreens ("chemical" / organic filters) absorb UV and release it as a tiny amount of heat. Mineral sunscreens use
zinc oxide or titanium dioxide, fine white particles that sit on the skin and block UV (mostly absorbing, some
scattering). Sunscreen wears off with sweat, water and towelling, so reapply about every 2 hours and right after
swimming or sweating.
Sources: Cleveland Clinic "Mineral sunscreen explained"; Skin Cancer Foundation "Sunscreen & your skin";
Memorial Sloan Kettering "Understanding sunscreen"; Weill Cornell Medicine "How does sunscreen work?"; AAD sunscreen FAQs.
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['blue', 'purple', 'orange', 'teal', 'coral', 'mint'], shakes=[S[1] + 3.9, S[3] + 4.3, S[5] + 1.5], voice_files=VO, music=MUSIC)
B = K.B
UV = (.72, .35, 1.0); SKIN = (1.0, .78, .62); BURN = (.98, .45, .40)
def has(n): return os.path.exists(os.path.join(LIB, n + '.png'))

def bottle(c, x, y, s, rot, k):
    """sunscreen bottle = blank lotion bottle + paper SPF label"""
    if k <= 0: return
    stk(c, 'lotion', x, y, s, rot, k, maxd=520)
    c.save(); c.translate(x, y); c.rotate(rot); c.translate(-x, -y)
    label(c, "SPF 50", x, y + 60*s, 64*s, -4, bgcol=YEL, k=k, seed=21); c.restore()

def skin(c, y, k, col=SKIN, seed=0):
    """skin layer = torn paper strip across the bottom"""
    if k <= 0: return
    yy = lerp(H + 100, y, eo(min(1, k)))
    p = skia.Path(); p.moveTo(-60, H + 200); r = random.Random(seed); p.lineTo(-60, yy)
    for i in range(0, 40): p.lineTo(-60 + i * (W + 120) / 39, yy + 14 * math.sin(i * .7) + r.uniform(-4, 4))
    p.lineTo(W + 60, H + 200); p.close()
    c.drawPath(off(p, 0, -16), skia.Paint(Color=skia.Color4f(0, 0, 0, .25), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(.98, .98, .96, 1), Style=skia.Paint.kStroke_Style, StrokeWidth=40, AntiAlias=True))
    c.drawPath(p, skia.Paint(Color=skia.Color4f(*col, 1), AntiAlias=True))

def uvray(c, x0, y0, x1, y1, tq, k, col=UV):
    """wavy UV ray from (x0,y0) to (x1,y1), grows with k"""
    if k <= 0: return
    L = math.hypot(x1 - x0, y1 - y0) * eo(min(1, k)); ang = math.atan2(y1 - y0, x1 - x0)
    c.save(); c.translate(x0, y0); c.rotate(math.degrees(ang)); p = skia.Path(); p.moveTo(0, 0)
    for i in range(1, 60):
        x = L * i / 59; p.lineTo(x, 22 * math.sin(x / 30 - tq * 14))
    for w, cc in ((30, (.98, .98, .96)), (14, col)):
        c.drawPath(p, skia.Paint(Color=skia.Color4f(*cc, 1), Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
    c.restore()

def wiggle(c, x, y, tq, k):
    """little heat squiggles rising"""
    if k <= 0: return
    for i in range(3):
        p = skia.Path(); xx = x + (i - 1) * 60
        for j in range(20):
            yy = y - j * 9; (p.moveTo if j == 0 else p.lineTo)(xx + 12 * math.sin(j * .6 - tq * 10 + i), yy)
        c.drawPath(p, skia.Paint(Color=skia.Color4f(1, .45, .2, min(1, k)), Style=skia.Paint.kStroke_Style, StrokeWidth=12, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook
        rays(c, W/2, 1150, 1100, WHT, tq*12, f.k(0.05, 0.45), a=0.25)
        stk(c, 'sun', W*0.66 + jx, 900 + jy, 0.8, tq*8, f.k(0.0, 0.3), maxd=520)
        bottle(c, W*0.38 + jx, 1300 + jy, 1.0, -8 + jr, f.k(0.3, 0.55))
        glyph(c, '?', 880, 1500, 150, 12 + jr*2, f.k(0.6, 0.85))
        label(c, "how does SUNSCREEN", W/2 + jx*.4, 330, 84, -3 + jr*.5, k=f.k(0.1, 0.35), seed=1)
        label(c, "stop a SUNBURN?", W/2 + 10, 470, 96, 2 - jr*.5, bgcol=YEL, k=f.k(1.3, 1.55), seed=2)
    elif b == 1:  # invisible UV rays burn skin
        s0 = S[1]
        stk(c, 'sun', W*0.24 + jx, 800 + jy, 0.6, tq*8, f.k(B[1] + 0.1, B[1] + 0.35), maxd=440)
        for i in range(3):
            uvray(c, W*0.3 + i*40, 900 + i*20, W*(0.45 + i*0.18), 1440, tq, f.k(s0 + 1.0 + i*.15, s0 + 1.6 + i*.15))
        burn = f.k(s0 + 3.8, s0 + 4.3)
        skin(c, 1460, f.k(B[1] + 0.2, B[1] + 0.5), col=tuple(lerp(a, bb, burn) for a, bb in zip(SKIN, BURN)), seed=1)
        if tq > s0 + 3.9: stamp(c, "OUCH!", W*0.72, 1680, 120, 6, f.k(s0 + 3.9, s0 + 4.15))
        stk(c, 'sunglasses2', W*0.76 + jx, 860 + jy, 0.5, 10 + jr, f.k(s0 + 0.5, s0 + 0.75), maxd=380)
        label(c, "INVISIBLE UV rays", W/2, 330, 92, -2 + jr*.5, bgcol=(.85, .7, 1), k=f.k(s0 + 0.9, s0 + 1.15), seed=3)
        label(c, "they BURN your skin", W/2 + 15, 470, 86, 3 - jr*.5, k=f.k(s0 + 3.9, s0 + 4.15), seed=4)
    elif b == 2:  # most soak up the rays -> tiny bit of heat
        s0 = S[2]
        skin(c, 1420, f.k(s0 + 0.2, s0 + 0.5), col=(1, 1, .97), seed=3)   # cream layer on top of the skin
        skin(c, 1520, f.k(B[2] + 0.1, B[2] + 0.4), seed=2)
        bottle(c, W*0.78 + jx, 980 + jy, 0.75, 12 + jr, f.k(B[2] + 0.1, B[2] + 0.35))
        for i in range(3):
            kk = f.k(s0 + 0.6 + i*.15, s0 + 1.2 + i*.15)
            uvray(c, W*(0.1 + i*0.14), 760, W*(0.2 + i*0.14), 1400, tq, kk)
        wiggle(c, W*0.3, 1380, tq, f.k(s0 + 3.2, s0 + 3.5))
        stk(c, 'thermometer', W*0.6 + jx, 1180 + jy, 0.5, -10 + jr, f.k(s0 + 3.3, s0 + 3.55), maxd=360)
        label(c, "most SOAK UP the rays", W/2, 330, 82, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.9, s0 + 1.15), seed=5)
        label(c, "into a tiny bit of HEAT", W/2 + 15, 470, 84, 3 - jr*.5, k=f.k(s0 + 3.3, s0 + 3.55), seed=6)
    elif b == 3:  # mineral: white particles block
        s0 = S[3]
        skin(c, 1500, f.k(B[3] + 0.1, B[3] + 0.4), seed=4)
        r = random.Random(5)
        for i in range(16):
            x = 60 + i * 64 + r.uniform(-10, 10); y = 1440 + r.uniform(-20, 20)
            kk = f.k(s0 + 1.7 + i*0.04, s0 + 1.9 + i*0.04)
            if kk > 0:
                c.drawCircle(x + jx*.3, y, 30*back(min(1, kk)), skia.Paint(Color=skia.Color4f(.75, .75, .8, 1), AntiAlias=True))
                c.drawCircle(x + jx*.3, y, 24*back(min(1, kk)), skia.Paint(Color=skia.Color4f(1, 1, 1, 1), AntiAlias=True))
        for i in range(3):
            x = W*(0.2 + i*0.3); kk = f.k(s0 + 3.6 + i*.12, s0 + 4.0 + i*.12)
            uvray(c, x - 120, 800, x, 1380, tq, kk)
            if tq > s0 + 4.2 + i*.12: arrow(c, x, 1370, 200, -60 - i*20, f.k(s0 + 4.2 + i*.12, s0 + 4.4 + i*.12), col=UV)
        stk(c, 'sun', W*0.2 + jx, 760 + jy, 0.45, tq*8, f.k(B[3] + 0.1, B[3] + 0.35), maxd=420)
        stk(c, 'sun_hat2', W*0.68 + jx, 980 + jy, 0.95, 8 + jr, f.k(s0 + 0.3, s0 + 0.55), maxd=460)
        if tq > s0 + 4.3: stamp(c, "BLOCKED!", W*0.36, 1080, 100, -6, f.k(s0 + 4.3, s0 + 4.55))
        label(c, "MINERAL ones", W/2, 330, 100, -2 + jr*.5, k=f.k(s0 + 0.1, s0 + 0.35), seed=7)
        label(c, "tiny WHITE particles", W/2 + 15, 470, 84, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.7, s0 + 1.95), seed=8)
    elif b == 4:  # wears off: sweat, water, towels
        s0 = S[4]
        stk(c, 'sweat_drop', W*0.24 + jx, 900 + 10*math.sin(tq*5) + jy, 0.55, -8 + jr, f.k(s0 + 1.0, s0 + 1.25), maxd=340)
        stk(c, 'swim_ring2', W*0.72 + jx, 1000 + jy, 0.75, tq*10, f.k(s0 + 1.5, s0 + 1.75), maxd=420)
        stk(c, 'towel', W*0.42 + jx, 1440 + jy, 0.9, 5 + jr, f.k(s0 + 2.4, s0 + 2.65), maxd=520)
        label(c, "it WEARS OFF!", W/2, 330, 104, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.2, s0 + 0.45), seed=9)
        label(c, "SWEAT, WATER, TOWELS", W/2 + 15, 470, 80, 3 - jr*.5, k=f.k(s0 + 1.0, s0 + 1.25), seed=10)
    else:         # reapply every 2 h + after swimming
        s0 = S[5]
        bottle(c, W*0.26 + jx, 1240 + jy, 0.95, -8 + 4*math.sin(tq*6) + jr, f.k(s0 + 0.1, s0 + 0.35))
        stk(c, 'alarm_clock', W*0.74 + jx + 6*math.sin(tq*40)*f.k(s0 + 1.2, s0 + 2.2), 900 + jy, 0.6, 8 + jr, f.k(s0 + 1.0, s0 + 1.25), maxd=400)
        if tq > s0 + 1.5: stamp(c, "EVERY 2 HRS", W*0.7, 1150, 70, 6, f.k(s0 + 1.5, s0 + 1.75), col=(.1, .45, .95))
        stk(c, 'swim_ring2', W*0.74 + jx, 1500 + jy, 0.55, -tq*10, f.k(s0 + 3.0, s0 + 3.25), maxd=380)
        label(c, "put MORE ON", W/2, 330, 104, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.1, s0 + 0.35), seed=11)
        label(c, "+ after SWIMMING!", W/2 + 15, 470, 92, 3 - jr*.5, k=f.k(s0 + 3.0, s0 + 3.25), seed=12)

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.4); K.sfx(0.3, 'pop', 0.7); K.sfx(0.6, 'pop', 0.6); K.sfx(1.3, 'pop', 0.8); K.sfx(1.35, 'sparkle1', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.5, 'pop', 0.6); K.sfx(S[1] + 0.9, 'pop', 0.6); K.sfx(S[1] + 1.0, 'swoosh3', 0.5); K.sfx(S[1] + 1.3, 'scratch2', 0.3); K.sfx(S[1] + 3.9, 'impact1', 0.9)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.2, 'paper', 0.6); K.sfx(S[2] + 0.9, 'pop', 0.6); K.sfx(S[2] + 0.6, 'swoosh1', 0.4); K.sfx(S[2] + 3.2, 'sparkle2', 0.4); K.sfx(S[2] + 3.3, 'pop', 0.6)
K.sfx(B[3] + 0.1, 'pop', 0.6); K.sfx(S[3] + 0.1, 'pop', 0.6); K.sfx(S[3] + 0.3, 'pop', 0.5)
for i in range(4): K.sfx(S[3] + 1.7 + i * 0.16, 'pop', 0.45)
K.sfx(S[3] + 3.6, 'swoosh3', 0.5); K.sfx(S[3] + 4.3, 'impact1', 0.9); K.sfx(S[3] + 4.35, 'ding2', 0.4)
K.sfx(S[4] + 0.2, 'pop', 0.7); K.sfx(S[4] + 1.0, 'bubble', 0.5); K.sfx(S[4] + 1.5, 'splash1', 0.5); K.sfx(S[4] + 2.4, 'pop', 0.6); K.sfx(S[4] + 2.45, 'scratch1', 0.4)
K.sfx(S[5] + 0.1, 'pop', 0.7); K.sfx(S[5] + 1.0, 'pop', 0.6); K.sfx(S[5] + 1.2, 'ding1', 0.5); K.sfx(S[5] + 1.5, 'impact1', 0.8); K.sfx(S[5] + 3.0, 'pop', 0.7); K.sfx(S[5] + 3.05, 'splash2', 0.4)
K.sfx(S[5] + 3.3, 'sparkle2', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p17_sunscreen')
