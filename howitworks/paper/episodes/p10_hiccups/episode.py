"""P10 — Why do we get hiccups? (PAPER-CUTOUT format) — educational only, not medical advice.
Facts (plain words, no studies): a hiccup is a sudden, involuntary contraction (spasm) of the diaphragm, the big muscle
under the lungs that helps you breathe; it pulls air in suddenly and a split second later the vocal cords snap shut,
which makes the "hic" sound. Common triggers: eating too much or too fast, fizzy/carbonated drinks, alcohol, excitement or
stress, sudden temperature changes. Most hiccups stop on their own within minutes; common home tricks include sipping
cold water or briefly holding your breath. Hiccups lasting more than 48 hours should be checked by a doctor (caption).
Sources: Mayo Clinic "Hiccups — symptoms & causes"; NHS "Hiccups"; healthdirect Australia "Hiccups"; Better Health
Channel (Victoria) "Hiccups"; MedlinePlus "Hiccups".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['mint', 'coral', 'blue', 'red', 'orange', 'teal'], shakes=[S[2] + 0.5, S[3] + 1.1, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
SKY = (.55, .85, 1.0)

def hic(t, t0, every=0.9):
    """little hiccup jump: 0..1 spike every `every` s after t0"""
    if t < t0: return 0
    ph = ((t - t0) % every) / every
    return max(0, 1 - ph*6)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook
        rays(c, W/2, 1100, 1100, WHT, tq*12, f.k(0.05, 0.45))
        j = -60*hic(tq, 0.4, 0.8)
        stk(c, 'fizzy_glass', W*0.46 + jx, 1100 + jy + j, 1.05, jr - 8, f.k(0.0, 0.3), maxd=600)
        stk(c, 'burger', W*0.74 + jx, 1560 + jy, 0.75, 10 + jr, f.k(0.5, 0.75), maxd=400)
        glyph(c, '?', 170, 760, 140, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 900, 860, 120, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "why do we get", W/2 + jx*.4, 330, 90, -3 + jr*.5, k=f.k(0.1, 0.35), seed=1)
        label(c, "HICCUPS?!", W/2 + 10, 470, 116, 2 - jr*.5, bgcol=YEL, k=f.k(0.5, 0.75), seed=2)
    elif b == 1:  # breathing muscle under lungs
        s0 = S[1]
        stk(c, 'lungs2', W/2 + jx, 1080 + jy, 1.05, -3 + jr, f.k(B[1] + 0.1, B[1] + 0.4), maxd=580)
        # the muscle: a red paper band under the lungs
        if tq > s0 + 1.0:
            kk = eo(f.k(s0 + 1.0, s0 + 1.3)); p = skia.Path(); y0 = 1420
            p.moveTo(W/2 - 360*kk, y0 + 40); p.quadTo(W/2, y0 - 120*kk, W/2 + 360*kk, y0 + 40)
            c.drawPath(p, skia.Paint(Color=skia.Color4f(.98, .98, .96, 1), Style=skia.Paint.kStroke_Style, StrokeWidth=86, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
            c.drawPath(p, skia.Paint(Color=skia.Color4f(*RED, 1), Style=skia.Paint.kStroke_Style, StrokeWidth=58, StrokeCap=skia.Paint.kRound_Cap, AntiAlias=True))
            arrow(c, W*0.80, 1640, 170, -115, f.k(s0 + 1.4, s0 + 1.7), col=YEL)
        label(c, "BLAME this MUSCLE!", W/2, 330, 88, -2 + jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 0.1, s0 + 0.35), seed=3)
        label(c, "right UNDER your LUNGS", W/2 + 15, 470, 74, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.2, s0 + 1.45), seed=4)
    elif b == 2:  # twitches, gulp in air
        s0 = S[2]
        j = -50*hic(tq, s0 + 0.5, 0.7)
        stk(c, 'lungs2', W*0.40 + jx, 1100 + jy + j, 0.9 + 0.1*hic(tq, s0 + 0.5, 0.7), -6 + jr, f.k(B[2] + 0.1, B[2] + 0.4), maxd=520)
        stk(c, 'electric_fan', W*0.78 + jx, 1580 + jy, 0.85, 8 + jr, f.k(s0 + 1.8, s0 + 2.05), maxd=340)
        if tq > s0 + 0.5: bolt(c, W*0.80, 980, 0.9, 15 + jr*3, f.k(s0 + 0.5, s0 + 0.7))
        arrow(c, W*0.66, 1520, 220, -150, f.k(s0 + 1.9, s0 + 2.3), col=SKY)
        label(c, "it suddenly TWITCHES", W/2, 330, 80, -2 + jr*.5, k=f.k(s0 + 0.5, s0 + 0.75), seed=5)
        label(c, "GULP! air rushes in", W/2 + 15, 470, 84, 3 - jr*.5, bgcol=SKY, k=f.k(s0 + 1.8, s0 + 2.05), seed=6)
    elif b == 3:  # vocal cords slam shut -> HIC
        s0 = S[3]
        sw = 1 - eo(f.k(s0 + 0.5, s0 + 1.0))
        stk(c, 'door', W*0.42 + jx, 1150 + jy, 1.0, -4 + jr + 25*sw, f.k(B[3] + 0.1, B[3] + 0.4), maxd=640)
        if tq > s0 + 1.1: stamp(c, "HIC!", W*0.62, 1500, 200, -10, f.k(s0 + 1.1, s0 + 1.35))
        label(c, "VOCAL CORDS", W/2, 330, 100, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=7)
        label(c, "SLAM SHUT!", W/2 + 15, 470, 104, 3 - jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 0.6, s0 + 0.85), seed=8)
    elif b == 4:  # triggers
        s0 = S[4]
        stk(c, 'burger', W*0.28 + jx, 1000 + jy, 0.85, -8 + jr, f.k(s0 + 0.3, s0 + 0.55), maxd=420)
        stk(c, 'fizzy_glass', W*0.72 + jx, 1060 + jy, 0.85, 10 + jr, f.k(s0 + 1.3, s0 + 1.55), maxd=440)
        stk(c, 'stopwatch', W*0.30 + jx, 1440 + jy, 0.8, -4 + jr, f.k(s0 + 0.6, s0 + 0.85), maxd=340)
        if tq > s0 + 2.1: glyph(c, '!', W*0.68, 1560, 280, 10 + jr*2, f.k(s0 + 2.1, s0 + 2.35), col=RED)
        label(c, "EAT too FAST", W/2, 330, 96, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.3, s0 + 0.55), seed=9)
        label(c, "FIZZY + EXCITED", W/2 + 15, 470, 92, 3 - jr*.5, k=f.k(s0 + 1.3, s0 + 1.55), seed=10)
    else:         # stops in minutes; sip cold water
        s0 = S[5]
        rays(c, W/2, 1150, 1100, WHT, tq*8, f.k(B[5] + 0.2, B[5] + 0.6), a=0.3)
        stk(c, 'alarm_clock', W*0.28 + jx, 1000 + jy, 0.75, -8 + jr, f.k(s0 + 0.3, s0 + 0.55), maxd=400)
        stk(c, 'water_glass', W*0.62 + jx, 1250 + jy, 1.0, 6 + jr, f.k(s0 + 2.0, s0 + 2.25), maxd=520)
        stk(c, 'ice_cube', W*0.86 + jx, 1500 + jy, 0.5, 14 + jr, f.k(s0 + 2.3, s0 + 2.55), maxd=260)
        label(c, "STOPS in MINUTES", W/2, 330, 92, -2 + jr*.5, k=f.k(s0 + 0.3, s0 + 0.55), seed=11)
        label(c, "slow sips of COLD water", W/2 + 15, 470, 74, 3 - jr*.5, bgcol=SKY, k=f.k(s0 + 2.0, s0 + 2.25), seed=12)
        if tq > DUR - 1.5: stamp(c, "BYE HICCUPS!", W*0.46, 1640, 96, -6, f.k(DUR - 1.5, DUR - 1.25), col=(.1, .6, .3))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.5); K.sfx(0.1, 'pop', 0.6); K.sfx(0.35, 'pop', 0.6); K.sfx(0.5, 'pop', 0.7); K.sfx(0.55, 'pop', 0.6); K.sfx(0.4, 'bubble', 0.5)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 1.0, 'snip', 0.6); K.sfx(S[1] + 1.2, 'pop', 0.6); K.sfx(S[1] + 1.4, 'swoosh3', 0.5)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.5, 'impact2', 0.8); K.sfx(S[2] + 0.55, 'pop', 0.6); K.sfx(S[2] + 1.8, 'whoosh', 0.6); K.sfx(S[2] + 1.85, 'pop', 0.6)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.2, 'pop', 0.6); K.sfx(S[3] + 0.6, 'pop', 0.6); K.sfx(S[3] + 1.0, 'impact1', 1.0); K.sfx(S[3] + 1.1, 'scratch2', 0.5)
K.sfx(S[4] + 0.3, 'pop', 0.7); K.sfx(S[4] + 1.3, 'pop', 0.7); K.sfx(S[4] + 1.35, 'bubble', 0.5); K.sfx(S[4] + 2.1, 'pop', 0.7); K.sfx(S[4] + 2.15, 'sparkle1', 0.4)
K.sfx(S[5] + 0.3, 'pop', 0.7); K.sfx(S[5] + 0.35, 'ding1', 0.4); K.sfx(S[5] + 2.0, 'pop', 0.7); K.sfx(S[5] + 2.05, 'splash1', 0.35); K.sfx(S[5] + 2.3, 'pop', 0.6)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p10_hiccups')
