"""P11 — How does your phone know it's your finger? (PAPER-CUTOUT format)
Facts (plain words, no studies): phones use capacitive touchscreens: under the glass is a transparent grid of electrodes
holding a small electric charge/field; your body conducts electricity, so a fingertip draws a little charge away and changes
the charge at that spot; the phone's controller measures where it changed and works out the touch position. Ordinary gloves
are insulators, so nothing changes -> no touch; a sausage is salty and full of water, so it conducts like a finger (famous
Korean winter trick). Water drops are conductive too and can cause "ghost" touches -> dry the screen.
Sources: TED-Ed "Why a sausage can do what your gloves cannot"; ScienceAlert "How does a touchscreen actually work?";
Cosmos "Swipe, tap, scroll: how touchscreens follow your finger"; McGill OSS; Scienceline "How do touch screens work?".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['purple', 'orange', 'navy', 'teal', 'pink', 'blue'], shakes=[S[1] + 0.5, S[4] + 2.2, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
ELEC = (.35, .95, 1.0)

def grid(c, cx, cy, w, h, k, hot=None, tq=0, rot=35):
    """glowing paper-tape grid of electrodes drawn along the tilted phone screen; hot = (u, v) in screen coords (-0.5..0.5)"""
    if k <= 0: return
    n, m = 8, 4; a = min(1, k); L = eo(min(1, k))
    c.save(); c.translate(cx, cy); c.rotate(rot)
    pw = skia.Paint(Color=skia.Color4f(.98, .98, .96, a), Style=skia.Paint.kStroke_Style, StrokeWidth=14, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True)
    pc = skia.Paint(Color=skia.Color4f(*ELEC, a), Style=skia.Paint.kStroke_Style, StrokeWidth=7, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True)
    for p in (pw, pc):
        for i in range(n):
            x = -w/2 + w*(i + .5)/n; c.drawLine(x, -h/2, x, -h/2 + h*L, p)
        for j in range(m):
            y = -h/2 + h*(j + .5)/m; c.drawLine(-w/2, y, -w/2 + w*L, y, p)
    if hot:
        r = 46 + 16*math.sin(tq*20)
        c.drawCircle(hot[0]*w, hot[1]*h, r, skia.Paint(Color=skia.Color4f(1, .85, .1, .75), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12)))
    c.restore()

def rotp(cx, cy, u, v, rot=35):
    a = math.radians(rot); return cx + u*math.cos(a) - v*math.sin(a), cy + u*math.sin(a) + v*math.cos(a)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook
        rays(c, W/2, 1100, 1100, WHT, tq*12, f.k(0.05, 0.45))
        stk(c, 'phone2', W*0.45 + jx, 1100 + jy, 1.05, jr - 6, f.k(0.0, 0.3), maxd=640)
        tap = 30*abs(math.sin(tq*5))
        stk(c, 'hand_pointing', W*0.70 + jx - tap*.5, 1480 + jy + tap, 1.0, -30 + jr, f.k(0.6, 0.85), maxd=440)
        glyph(c, '?', 170, 760, 140, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 920, 820, 120, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "how does your PHONE", W/2 + jx*.4, 330, 80, -3 + jr*.5, k=f.k(0.1, 0.35), seed=1)
        label(c, "know it's your FINGER?", W/2 + 10, 470, 78, 2 - jr*.5, bgcol=YEL, k=f.k(0.7, 0.95), seed=2)
    elif b == 1:  # body carries electricity
        s0 = S[1]
        stk(c, 'hand_pointing', W*0.42 + jx, 1150 + jy, 1.05, -10 + jr, f.k(B[1] + 0.1, B[1] + 0.4), maxd=560)
        for i in range(3):
            if tq > s0 + 0.5 + i*0.15: bolt(c, W*0.78 + (i - 1)*30, 900 + i*200, 0.75, 15 - i*12 + jr*3, f.k(s0 + 0.5 + i*0.15, s0 + 0.7 + i*0.15))
        stk(c, 'battery', W*0.26 + jx, 1560 + jy, 0.85, -14 + jr, f.k(s0 + 1.0, s0 + 1.25), maxd=340)
        label(c, "YOUR BODY carries", W/2, 330, 90, -2 + jr*.5, k=f.k(s0 + 0.1, s0 + 0.35), seed=3)
        label(c, "ELECTRICITY!", W/2 + 15, 470, 104, 3 - jr*.5, bgcol=ELEC, k=f.k(s0 + 0.5, s0 + 0.75), seed=4)
    elif b == 2:  # invisible grid under the glass
        s0 = S[2]
        stk(c, 'phone2', W/2 + jx, 1120 + jy, 1.1, -3 + jr, f.k(B[2] + 0.1, B[2] + 0.4), maxd=660)
        grid(c, W/2, 1110, 520, 220, f.k(s0 + 1.0, s0 + 1.6))
        stk(c, 'magnifier', W*0.82 + jx, 1580 + jy, 0.6, 14 + jr, f.k(s0 + 0.6, s0 + 0.85), maxd=340)
        label(c, "an INVISIBLE GRID", W/2, 330, 92, -2 + jr*.5, k=f.k(s0 + 0.6, s0 + 0.85), seed=5)
        label(c, "with a TINY charge", W/2 + 15, 470, 88, 3 - jr*.5, bgcol=ELEC, k=f.k(s0 + 2.4, s0 + 2.65), seed=6)
    elif b == 3:  # finger soaks up charge -> location
        s0 = S[3]
        hx, hy = rotp(W/2, 1110, 0.12*520, -0.1*220)
        stk(c, 'phone2', W/2 + jx, 1120 + jy, 1.1, -3 + jr, f.k(B[3] + 0.1, B[3] + 0.4), maxd=660)
        grid(c, W/2, 1110, 520, 220, 1, hot=(0.12, -0.1) if tq > s0 + 1.0 else None, tq=tq)
        dn = 1 - eo(f.k(s0 + 0.4, s0 + 1.0))
        stk(c, 'hand_pointing', hx + 150 + jx + 200*dn, hy + 95 + jy + 300*dn, 0.85, -20 + jr, f.k(s0 + 0.2, s0 + 0.4), maxd=440)
        if tq > s0 + 2.8: stamp(c, "RIGHT HERE!", W*0.46, 1640, 92, -6, f.k(s0 + 2.8, s0 + 3.05), col=(.1, .45, .95))
        label(c, "your finger SOAKS UP", W/2, 330, 80, -2 + jr*.5, k=f.k(s0 + 0.4, s0 + 0.65), seed=7)
        label(c, "a little CHARGE", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.0, s0 + 1.25), seed=8)
    elif b == 4:  # gloves no, sausage yes
        s0 = S[4]
        stk(c, 'gloves', W*0.30 + jx, 840 + jy, 0.85, -8 + jr, f.k(s0 + 0.4, s0 + 0.65), maxd=460)
        if tq > s0 + 1.1: stamp(c, "NOPE!", W*0.30, 1090, 110, -10, f.k(s0 + 1.1, s0 + 1.35))
        stk(c, 'sausage2', W*0.62 + jx, 1340 + jy, 1.2, 12 + jr, f.k(s0 + 2.0, s0 + 2.25), maxd=480)
        if tq > s0 + 2.3: stamp(c, "YEP!", W*0.74, 1590, 120, 8, f.k(s0 + 2.3, s0 + 2.55), col=(.1, .6, .3))
        label(c, "GLOVES don't work...", W/2, 330, 86, -2 + jr*.5, k=f.k(s0 + 0.4, s0 + 0.65), seed=9)
        label(c, "but a SAUSAGE does!", W/2 + 15, 470, 88, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.0, s0 + 2.25), seed=10)
    else:         # water drops fool it -> dry screen
        s0 = S[5]
        rays(c, W/2, 1150, 1100, WHT, tq*8, f.k(B[5] + 0.2, B[5] + 0.6), a=0.3)
        stk(c, 'phone2', W*0.40 + jx, 1100 + jy, 1.05, -6 + jr, f.k(s0 + 0.1, s0 + 0.35), maxd=600)
        for i, (dx, dy) in enumerate([(-90, -150), (60, -20), (-40, 140)]):
            if tq > s0 + 0.9 + i*0.15: drop(c, W*0.40 + dx + jx, 1120 + dy + jy, 34, 10*math.sin(tq*30 + i), seed=i)
        stk(c, 'towel', W*0.76 + jx, 1500 + jy, 1.0, 12 + jr, f.k(s0 + 2.6, s0 + 2.85), maxd=400)
        label(c, "WATER DROPS fool it!", W/2, 330, 84, -2 + jr*.5, bgcol=ELEC, k=f.k(s0 + 0.9, s0 + 1.15), seed=11)
        label(c, "DRY your screen", W/2 + 15, 470, 92, 3 - jr*.5, k=f.k(s0 + 2.6, s0 + 2.85), seed=12)
        if tq > DUR - 1.5: stamp(c, "TIP!", W*0.30, 1640, 130, -6, f.k(DUR - 1.5, DUR - 1.25), col=(.1, .6, .3))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.5); K.sfx(0.1, 'pop', 0.6); K.sfx(0.35, 'pop', 0.6); K.sfx(0.55, 'pop', 0.6); K.sfx(0.6, 'pop', 0.7); K.sfx(0.7, 'pop', 0.7); K.sfx(0.75, 'ding1', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.1, 'pop', 0.7)
for i in range(3): K.sfx(S[1] + 0.5 + i*0.15, 'sparkle1' if i % 2 else 'impact2', 0.45)
K.sfx(S[1] + 1.0, 'pop', 0.6)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.6, 'pop', 0.6); K.sfx(S[2] + 1.0, 'swoosh3', 0.5); K.sfx(S[2] + 1.3, 'sparkle2', 0.5); K.sfx(S[2] + 2.4, 'pop', 0.6)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.2, 'pop', 0.6); K.sfx(S[3] + 0.4, 'pop', 0.6); K.sfx(S[3] + 1.0, 'ding2', 0.6); K.sfx(S[3] + 1.0, 'pop', 0.6); K.sfx(S[3] + 2.8, 'impact1', 0.9)
K.sfx(S[4] + 0.4, 'pop', 0.7); K.sfx(S[4] + 1.1, 'impact1', 0.9); K.sfx(S[4] + 1.15, 'scratch1', 0.5); K.sfx(S[4] + 2.0, 'pop', 0.7); K.sfx(S[4] + 2.3, 'impact2', 0.9); K.sfx(S[4] + 2.35, 'sparkle1', 0.5)
K.sfx(S[5] + 0.1, 'pop', 0.7)
for i in range(3): K.sfx(S[5] + 0.9 + i*0.15, 'splash2' if i == 0 else 'bubble', 0.4)
K.sfx(S[5] + 1.0, 'pop', 0.6); K.sfx(S[5] + 2.6, 'pop', 0.7); K.sfx(S[5] + 2.65, 'swoosh3', 0.4)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p11_touchscreen')
