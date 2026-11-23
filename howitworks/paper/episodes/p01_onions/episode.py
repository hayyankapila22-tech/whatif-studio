"""P01 — Why do onions make you cry? (PAPER-CUTOUT reference episode)
Facts (plain words, no studies): cutting breaks onion cells; enzymes turn sulphur compounds into an irritating gas
(syn-propanethial-S-oxide) that drifts up to the eyes; the eyes' nerves sense the sting and make tears to flush it;
it is the onion's chemical defence against animals; chilling slows the reaction, a sharp knife crushes fewer cells.
Sources: Library of Congress "Everyday Mysteries: Why does chopping an onion make you cry?";
Nature 419, 685 (2002) Imai et al. (lachrymatory-factor synthase); Scientific American "Why do onions make us cry?".
Run:  python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
K = Kit(S, DUR, ['blue', 'purple', 'pink', 'orange', 'mint', 'navy'], shakes=[S[3] + 0.35, DUR - 1.6], voice_files=VO)
B = K.B
GAS = (.72, .93, .35)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook: onion + tears + question marks
        rays(c, W/2, 1050, 1100, WHT, tq*12, f.k(0.05, 0.45))
        stk(c, 'onion', W/2 + jx, 1060 + jy, 1.25, jr - 4, f.k(0.0, 0.35), maxd=560)
        stk(c, 'tissues', W*0.20 + jx, 1500 + jy, 0.75, -10 + jr, f.k(0.7, 1.0), maxd=420)
        glyph(c, '?', 180, 760, 150, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 900, 700, 120, 14 - jr*2, f.k(0.6, 0.85)); glyph(c, '?', 880, 1420, 100, 8, f.k(0.85, 1.1), col=WHT)
        for i in range(4):
            ph = (tq - 0.9 - i*0.35)
            if ph > 0: drop(c, [330, 760, 450, 650][i] + jx, 650 + (ph % 1.2) * 700, 26, jr*3, seed=i)
        label(c, "WHY do ONIONS", W/2 + jx*.4, 330, 92, -3 + jr*.5, k=f.k(0.15, 0.4), seed=1)
        label(c, "make you CRY?", W/2 + 10, 470, 92, 2 - jr*.5, bgcol=YEL, k=f.k(0.9, 1.15), seed=2)
    elif b == 1:  # knife bursts cells
        s0 = S[1]
        rays(c, W/2, 1100, 1000, WHT, -tq*10, f.k(B[1] + 0.2, B[1] + 0.6))
        stk(c, 'onion_half', W/2 + jx, 1180 + jy, 1.1, jr, f.k(B[1] + 0.2, B[1] + 0.5), maxd=560)
        chop = abs(math.sin((tq - s0) * 7)) if tq > s0 + 0.3 else 1
        stk(c, 'knife', W*0.62 + jx, lerp(760, 920, 1 - chop) + jy, 1.0, -35 + jr, f.k(B[1] + 0.35, B[1] + 0.6), maxd=620)
        for i in range(14):
            tp = s0 + 0.9 + i*0.13
            if tq < tp: continue
            x = 260 + (i*137) % 560; y = 1000 + (i*89) % 380; kk = prog(tq, tp, tp + 0.35)
            col = GAS if kk > 0.5 else (1, .95, .85)
            c.drawCircle(x, y, lerp(10, 34, eo(kk)), skia.Paint(Color=skia.Color4f(.98, .98, .96, 1 - kk*0.6), Style=skia.Paint.kStroke_Style, StrokeWidth=lerp(10, 3, kk), AntiAlias=True))
            c.drawCircle(x, y, lerp(10, 26, eo(kk)), skia.Paint(Color=skia.Color4f(*col, (1 - kk)*0.8), AntiAlias=True))
        label(c, "you BURST", W/2, 330, 96, -2 + jr*.5, k=f.k(s0 + 0.5, s0 + 0.75), seed=3)
        label(c, "1000s of tiny CELLS", W/2 + 15, 470, 80, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.4, s0 + 1.65), seed=4)
    elif b == 2:  # gas floats up to the eyes
        s0 = S[2]
        stk(c, 'onion_half', W/2 + jx, 1500 + jy, 0.95, jr, 1, maxd=560)
        stk(c, 'eye', W/2 + jx*.5, 700 + jy*.5, 0.9 + 0.03*math.sin(tq*6), jr, f.k(s0 + 1.4, s0 + 1.7), maxd=520)
        for i in range(9):
            tp = B[2] + 0.2 + i*0.22; ph = tq - tp
            if ph <= 0: continue
            ph = ph % 2.4; y = lerp(1380, 820, eo(min(1, ph/2.0))); x = W/2 + 120*math.sin(i*1.7 + ph*2)
            cloud(c, x + jx, y, 70 + (i % 3)*18, GAS, min(1, ph*3), seed=i, a=max(0, 1 - max(0, ph - 1.7)*2))
        label(c, "a GAS floats UP", W/2, 330, 92, -2 + jr*.5, k=f.k(s0 + 0.6, s0 + 0.85), seed=5)
        label(c, "into your EYES", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=GAS, k=f.k(s0 + 2.0, s0 + 2.25), seed=6)
    elif b == 3:  # sting -> tears flood
        s0 = S[3]
        rays(c, W/2, 950, 1100, YEL, tq*20, f.k(B[3] + 0.1, B[3] + 0.5))
        stk(c, 'eye', W/2 + jx, 950 + jy, 1.2, jr, 1, maxd=520)
        for i, (bx, by, rt) in enumerate([(170, 760, -20), (920, 800, 25), (200, 1200, 200), (900, 1180, 160)]):
            bolt(c, bx, by, 0.5, rt + jr*3, f.k(s0 + 0.3 + i*0.1, s0 + 0.5 + i*0.1))
        if tq < s0 + 1.9: stamp(c, "STING!", W/2, 1350, 150, -8, f.k(s0 + 0.3, s0 + 0.55))
        for i in range(6):
            ph = tq - (s0 + 1.8 + i*0.2)
            if ph > 0: drop(c, W/2 + (-1)**i*(90 + i*20) + jx, 1050 + (ph % 1.0)*520, 30 + (i % 3)*6, jr*4, seed=i)
        lvl = lerp(H + 150, 1480, eo(f.k(s0 + 2.4, s0 + 3.4)))
        if lvl < H + 100: water(c, lvl, tq)
        label(c, "your eyes feel the STING", W/2, 330, 70, -2 + jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 0.3, s0 + 0.55), seed=7)
        label(c, "TEARS wash it out", W/2 + 15, 465, 88, 3 - jr*.5, bgcol=WHT, k=f.k(s0 + 2.3, s0 + 2.55), seed=8)
    elif b == 4:  # the onion's defence vs a rabbit
        s0 = S[4]
        stk(c, 'onion', W*0.62 + jx, 1180 + jy, 1.0, jr, f.k(B[4] + 0.15, B[4] + 0.45), maxd=520)
        hop = abs(math.sin(tq*8))*40
        rx = lerp(-250, W*0.24, eo(f.k(B[4] + 0.3, s0 + 1.0))); rx = lerp(rx, -300, eio(f.k(s0 + 2.1, s0 + 2.6)))
        stk(c, 'rabbit', rx + jx, 1330 - hop + jy, 0.95, -6 + jr, 1, maxd=440)
        for i in range(4):
            cloud(c, W*0.45 + i*40 + jx, 1050 - i*60, 80 + i*12, GAS, f.k(s0 + 1.4 + i*0.1, s0 + 1.7 + i*0.1), seed=20 + i, a=0.95)
        if tq > s0 + 1.6: glyph(c, '!', W*0.22, 1000, 160, -10 + jr*3, f.k(s0 + 1.6, s0 + 1.8), col=RED)
        label(c, "it's the onion's", W/2, 330, 80, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=9)
        label(c, "SECRET DEFENCE", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 0.9, s0 + 1.15), seed=10)
    else:         # tips: chill 30 min + sharp knife
        s0 = S[5]
        rays(c, W/2, 1150, 1100, (.5, .4, 1), tq*8, f.k(B[5] + 0.2, B[5] + 0.6))
        stk(c, 'fridge', W*0.28 + jx, 1150 + jy, 1.0, -6 + jr, f.k(s0 + 0.7, s0 + 1.0), maxd=560)
        stk(c, 'ice_cube', W*0.18 + jx, 1560 + jy, 0.8, 12 + jr, f.k(s0 + 1.0, s0 + 1.25), maxd=280)
        stk(c, 'onion', W*0.47 + jx, 1500 + jy, 0.6, jr, f.k(s0 + 1.0, s0 + 1.25), maxd=360)
        stk(c, 'knife', W*0.72 + jx, 1130 + jy, 1.0, -60 + jr, f.k(s0 + 2.4, s0 + 2.7), maxd=620)
        if tq > s0 + 2.7: rays(c, W*0.80, 880, 160, WHT, tq*60, 1, n=8, a=0.9)
        label(c, "CHILL it 30 MIN", W/2, 330, 92, -2 + jr*.5, bgcol=(.55, .85, 1), k=f.k(s0 + 1.0, s0 + 1.25), seed=11)
        label(c, "use a SHARP knife", W/2 + 15, 470, 86, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.5, s0 + 2.75), seed=12)
        if tq > DUR - 1.6: stamp(c, "NO TEARS!", W/2, 1720, 110, -6, f.k(DUR - 1.6, DUR - 1.35), col=RED)

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.0, 'sparkle1', 0.5); K.sfx(0.35, 'pop', 0.6); K.sfx(0.6, 'pop', 0.6); K.sfx(0.85, 'pop', 0.6); K.sfx(0.7, 'pop', 0.7); K.sfx(0.9, 'ding2', 0.6)
for i in range(6): K.sfx(S[1] + 0.3 + i*0.45, 'impact1', 0.25)
for i in range(0, 14, 2): K.sfx(S[1] + 0.9 + i*0.13, 'pop', 0.45)
K.sfx(S[1] + 1.4, 'pop', 0.7)
K.sfx(B[2] + 0.2, 'whoosh', 0.6); K.sfx(B[2] + 0.4, 'bubble', 0.5); K.sfx(S[2] + 1.4, 'pop', 0.8); K.sfx(S[2] + 2.0, 'pop', 0.7)
K.sfx(S[3] + 0.3, 'impact1', 0.9); K.sfx(S[3] + 0.35, 'sparkle1', 0.4); K.sfx(S[3] + 2.4, 'splash2', 0.7); K.sfx(S[3] + 2.3, 'pop', 0.7)
K.sfx(S[4] + 0.2, 'pop', 0.7); K.sfx(S[4] + 0.9, 'pop', 0.7); K.sfx(S[4] + 1.4, 'whoosh', 0.5); K.sfx(S[4] + 1.6, 'scratch1', 0.8); K.sfx(S[4] + 2.1, 'swoosh3', 0.6)
K.sfx(S[5] + 0.7, 'pop', 0.7); K.sfx(S[5] + 1.0, 'pop', 0.7); K.sfx(S[5] + 1.0, 'ding1', 0.5); K.sfx(S[5] + 2.4, 'swoosh2', 0.6); K.sfx(S[5] + 2.7, 'sparkle1', 0.6)
K.sfx(DUR - 1.6, 'impact1', 0.8); K.sfx(DUR - 0.9, 'sparkle1', 0.4)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p01_onions')
