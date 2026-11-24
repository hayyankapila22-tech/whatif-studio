"""P08 — Does a microwave cook food from the inside out? (PAPER-CUTOUT format)
Facts (plain words, no studies): "inside out" is a myth; a microwave's waves make water (and some fat/sugar) molecules in
food flip back and forth billions of times a second (2.45 GHz), and that jiggling makes heat; the waves only reach about
2.5–4 cm (1–1.5 inches) into food, so the outer layer heats first and the centre heats more slowly by conduction from the
outside -> hot edges, cold middle; stirring halfway and letting food stand for a minute or two evens out the heat.
Sources: Cook's Illustrated / America's Test Kitchen "Your microwave questions answered" and "Getting the most from your
microwave"; HowStuffWorks "How microwave cooking works"; Today I Found Out "Microwaves don't cook from the inside out".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['teal', 'red', 'orange', 'purple', 'blue', 'mint'], shakes=[S[1] + 0.5, S[4] + 2.0, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
HOT = (1.0, .45, .12); ICE = (.55, .85, 1.0)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook: microwave + food
        rays(c, W/2, 1080, 1100, WHT, tq*12, f.k(0.05, 0.45))
        hum = 1 + 0.02*math.sin(tq*40)
        stk(c, 'microwave', W/2 + jx, 1040 + jy, 1.2*hum, jr - 3, f.k(0.0, 0.3), maxd=640)
        stk(c, 'pizza_slice', W*0.30 + jx, 1560 + jy, 0.8, -12 + jr, f.k(0.7, 0.95), maxd=420)
        glyph(c, '?', 170, 760, 140, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 920, 1560, 130, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "does a MICROWAVE cook", W/2 + jx*.4, 330, 76, -3 + jr*.5, k=f.k(0.15, 0.4), seed=1)
        label(c, "from the INSIDE OUT?", W/2 + 10, 470, 86, 2 - jr*.5, bgcol=YEL, k=f.k(0.8, 1.05), seed=2)
    elif b == 1:  # nope, myth
        s0 = S[1]
        stk(c, 'microwave', W*0.50 + jx, 1100 + jy, 0.95, -6 + jr, f.k(B[1] + 0.1, B[1] + 0.4), maxd=560)
        stk(c, 'soup_bowl', W*0.72 + jx, 1600 + jy, 0.75, 8 + jr, f.k(s0 + 0.9, s0 + 1.15), maxd=400)
        if tq > s0 + 0.5: stamp(c, "MYTH!", W*0.46, 1150, 170, -12, f.k(s0 + 0.5, s0 + 0.75))
        label(c, "NOPE!", W/2, 330, 110, -2 + jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 0.1, s0 + 0.35), seed=3)
        label(c, "a total MYTH!", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 0.8, s0 + 1.05), seed=4)
    elif b == 2:  # water wiggles billions of times a second -> heat
        s0 = S[2]
        rays(c, W/2, 1150, 1000, HOT, -tq*10, f.k(s0 + 3.0, s0 + 3.5), a=0.35)
        stk(c, 'soup_bowl', W/2 + jx, 1250 + jy, 1.05, -4 + jr, f.k(B[2] + 0.1, B[2] + 0.4), maxd=600)
        for i in range(6):
            ang = i/6*2*math.pi; wig = 18*math.sin(tq*60 + i*1.7)
            x = W/2 + 360*math.cos(ang) + wig; y = 1230 + 300*math.sin(ang)
            if prog(tq, s0 + 0.6 + i*0.15, s0 + 0.8 + i*0.15) > 0: drop(c, x + jx, y + jy, 34, 25*math.sin(tq*45 + i), seed=i)
        stk(c, 'thermometer', W*0.80 + jx, 1680 + jy, 0.6, 12 + jr, f.k(s0 + 3.0, s0 + 3.25), maxd=360)
        label(c, "the WATER WIGGLES", W/2, 330, 90, -2 + jr*.5, bgcol=ICE, k=f.k(s0 + 0.9, s0 + 1.15), seed=5)
        label(c, "BILLIONS of times a second", W/2 + 15, 470, 64, 3 - jr*.5, k=f.k(s0 + 1.8, s0 + 2.05), seed=6)
        if tq > s0 + 3.0: label(c, "= HEAT!", W*0.30, 1700, 100, -6, bgcol=HOT, fg=WHT, k=f.k(s0 + 3.0, s0 + 3.25), seed=13)
    elif b == 3:  # only a few cm in, the middle waits
        s0 = S[3]
        stk(c, 'pizza_slice', W/2 + jx, 1120 + jy, 1.25, -4 + jr, f.k(B[3] + 0.1, B[3] + 0.4), maxd=640)
        arrow(c, 70, 1120, 230, 0, f.k(s0 + 0.6, s0 + 1.0), col=HOT)
        arrow(c, W - 70, 1120, 230, 180, f.k(s0 + 0.8, s0 + 1.2), col=HOT)
        stk(c, 'ruler', W/2 + jx, 1560 + jy, 0.9, 4 + jr, f.k(s0 + 1.0, s0 + 1.25), maxd=560)
        if tq > s0 + 2.4: glyph(c, '?', W/2, 1110, 150, 8 + jr*2, f.k(s0 + 2.4, s0 + 2.6), col=ICE)
        label(c, "only a FEW CM in...", W/2, 330, 90, -2 + jr*.5, k=f.k(s0 + 0.5, s0 + 0.75), seed=7)
        label(c, "the MIDDLE has to WAIT!", W/2 + 15, 470, 74, 3 - jr*.5, bgcol=ICE, k=f.k(s0 + 2.3, s0 + 2.55), seed=8)
    elif b == 4:  # edges lava, middle frozen
        s0 = S[4]
        stk(c, 'volcano', W*0.32 + jx, 1000 + jy, 1.0, -6 + jr, f.k(s0 + 0.8, s0 + 1.05), maxd=520)
        stk(c, 'ice_cube', W*0.70 + jx, 1440 + jy, 0.9, 10 + jr, f.k(s0 + 1.9, s0 + 2.15), maxd=420)
        for i in range(3): cloud(c, W*0.30 + (i - 1)*90 + jx, 760 - i*20 + 10*math.sin(tq*6 + i), 55, (.9, .9, .9), f.k(s0 + 1.0 + i*0.1, s0 + 1.2 + i*0.1), seed=i)
        if tq > s0 + 2.0: stamp(c, "BRRR!", W*0.70, 1780, 110, 8, f.k(s0 + 2.0, s0 + 2.25), col=(.1, .45, .95))
        label(c, "EDGES = LAVA", W/2, 330, 100, -2 + jr*.5, bgcol=HOT, fg=WHT, k=f.k(s0 + 0.8, s0 + 1.05), seed=9)
        label(c, "MIDDLE = FROZEN", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=ICE, k=f.k(s0 + 1.9, s0 + 2.15), seed=10)
    else:         # tip: stir halfway, let it sit a minute
        s0 = S[5]
        rays(c, W/2, 1150, 1100, WHT, tq*8, f.k(B[5] + 0.2, B[5] + 0.6), a=0.3)
        stk(c, 'soup_bowl', W*0.38 + jx, 1180 + jy, 0.95, -4 + jr, f.k(s0 + 0.2, s0 + 0.45), maxd=480)
        stir = 20*math.sin(tq*12) if tq > s0 + 0.9 else 0
        stk(c, 'spoon', W*0.44 + jx + stir, 1000 + jy, 0.8, 35 + stir*0.5 + jr, f.k(s0 + 0.8, s0 + 1.05), maxd=440)
        stk(c, 'stopwatch', W*0.76 + jx, 1520 + jy, 0.7, 10 + jr, f.k(s0 + 2.0, s0 + 2.25), maxd=380)
        label(c, "STIR it halfway", W/2, 330, 96, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 0.8, s0 + 1.05), seed=11)
        label(c, "then WAIT 1 minute", W/2 + 15, 470, 88, 3 - jr*.5, k=f.k(s0 + 2.0, s0 + 2.25), seed=12)
        if tq > DUR - 1.5: stamp(c, "PERFECT!", W*0.42, 1640, 120, -6, f.k(DUR - 1.5, DUR - 1.25), col=(.1, .6, .3))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.5); K.sfx(0.35, 'pop', 0.6); K.sfx(0.55, 'pop', 0.6); K.sfx(0.7, 'pop', 0.7); K.sfx(0.8, 'pop', 0.7); K.sfx(1.0, 'ding1', 0.5)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.5, 'impact1', 1.0); K.sfx(S[1] + 0.55, 'scratch1', 0.6); K.sfx(S[1] + 0.9, 'pop', 0.6)
K.sfx(B[2] + 0.1, 'pop', 0.7)
for i in range(6): K.sfx(S[2] + 0.6 + i*0.15, 'bubble' if i % 2 else 'pop', 0.4)
K.sfx(S[2] + 0.9, 'pop', 0.6); K.sfx(S[2] + 1.8, 'pop', 0.6); K.sfx(S[2] + 3.0, 'pop', 0.7); K.sfx(S[2] + 3.05, 'sparkle2', 0.5)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.5, 'pop', 0.6); K.sfx(S[3] + 0.6, 'swoosh3', 0.5); K.sfx(S[3] + 1.0, 'pop', 0.6); K.sfx(S[3] + 2.3, 'pop', 0.6); K.sfx(S[3] + 2.4, 'ding2', 0.5)
K.sfx(S[4] + 0.8, 'pop', 0.7); K.sfx(S[4] + 1.0, 'scratch2', 0.4); K.sfx(S[4] + 1.9, 'pop', 0.7); K.sfx(S[4] + 2.0, 'impact2', 0.9); K.sfx(S[4] + 2.05, 'sparkle1', 0.5)
K.sfx(S[5] + 0.2, 'pop', 0.7); K.sfx(S[5] + 0.8, 'pop', 0.7); K.sfx(S[5] + 1.0, 'splash2', 0.35); K.sfx(S[5] + 2.0, 'pop', 0.7); K.sfx(S[5] + 2.1, 'ding1', 0.4)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p08_microwave')
