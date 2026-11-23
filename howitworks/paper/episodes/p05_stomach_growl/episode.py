"""P05 — Why does your stomach growl? (PAPER-CUTOUT format) — educational only.
Facts (plain words, no studies): the rumble (borborygmi) is made by the muscles of the stomach and intestines squeezing
in waves (peristalsis) to push food, fluid and gas along — it happens all the time, not only when hungry; with food
inside, the contents muffle the sound, so an empty stomach sounds louder; when the stomach and small intestine are
empty, a "housekeeping" wave (the migrating motor complex) sweeps through roughly every 90–120 minutes, starting a
couple of hours after a meal, and it can be loud; eating a little or drinking water usually quietens it.
Sources: Scientific American "Why does your stomach growl?"; Live Science "Why do our stomachs growl?";
Colorado State Univ. VIVO Pathophysiology "Migrating motor complex"; Cleveland Clinic "Stomach growling".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['orange', 'blue', 'pink', 'navy', 'teal', 'mint'], shakes=[S[1] + 1.4, S[3] + 2.0, S[4] + 2.4, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
GAS = (.72, .93, .35)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook: growling lion
        rays(c, W/2, 1050, 1100, WHT, tq*12, f.k(0.05, 0.45))
        roar = 1 + 0.04*abs(math.sin(tq*12))
        stk(c, 'lion', W/2 + jx, 1070 + jy, 1.15*roar, jr - 4, f.k(0.0, 0.35), maxd=600)
        stk(c, 'sandwich', W*0.22 + jx, 1580 + jy, 0.75, -10 + jr, f.k(0.8, 1.05), maxd=360)
        glyph(c, '?', 170, 800, 140, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 910, 760, 120, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "WHY does your", W/2 + jx*.4, 330, 92, -3 + jr*.5, k=f.k(0.15, 0.4), seed=1)
        label(c, "STOMACH GROWL?", W/2 + 10, 470, 92, 2 - jr*.5, bgcol=YEL, k=f.k(0.8, 1.05), seed=2)
    elif b == 1:  # not hunger talking: guts squeezing
        s0 = S[1]
        stk(c, 'burger', W*0.40 + jx, 1050 + jy, 1.25, -8 + jr, f.k(B[1] + 0.1, B[1] + 0.4), maxd=460)
        if s0 + 1.4 <= tq: stamp(c, "NOPE!", W*0.40, 1100, 140, -12, f.k(s0 + 1.4, s0 + 1.65))
        sq = 1 + 0.12*math.sin(tq*9) if tq > s0 + 2.0 else 1
        stk(c, 'toothpaste', W*0.68 + jx, 1520 + jy, 1.2 * sq, 18 + jr, f.k(s0 + 2.0, s0 + 2.25), maxd=520)
        label(c, "NOT hunger talking...", W/2, 330, 80, -2 + jr*.5, k=f.k(s0 + 0.3, s0 + 0.55), seed=3)
        label(c, "your GUTS SQUEEZING!", W/2 + 15, 470, 80, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.0, s0 + 2.25), seed=4)
    elif b == 2:  # muscles squeeze all day, push food gas juice like toothpaste
        s0 = S[2]
        rays(c, W/2, 1100, 1000, WHT, -tq*10, f.k(B[2] + 0.2, B[2] + 0.6))
        sq = 1 - 0.15*abs(math.sin(tq*5))
        stk(c, 'toothpaste', W/2 + jx, 1000 + jy, 1.15, -6 + jr, f.k(B[2] + 0.1, B[2] + 0.4), maxd=640)
        for i in range(6):   # stuff pushed along
            ph = tq - (s0 + 1.0 + i*0.3)
            if ph <= 0: continue
            x = 200 + ((ph * 420) % 760); y = 1420 + 40*math.sin(ph*4 + i)
            if i % 3 == 0: cloud(c, x + jx, y, 70, GAS, 1, seed=i)
            elif i % 3 == 1: blob(c, x + jx, y, 50, (.95, .62, .25), jr*3, 1, seed=i)
            else: drop(c, x + jx, y, 30, jr*3, seed=i)
        stk(c, 'clock', W*0.82 + jx, 1680 + jy, 0.55, 12 + jr, f.k(s0 + 0.8, s0 + 1.05), maxd=240)
        label(c, "muscles SQUEEZE all day", W/2, 330, 72, -2 + jr*.5, k=f.k(s0 + 0.4, s0 + 0.65), seed=5)
        label(c, "FOOD, GAS + JUICES", W/2 + 15, 470, 82, 3 - jr*.5, bgcol=GAS, k=f.k(s0 + 1.6, s0 + 1.85), seed=6)
    elif b == 3:  # empty stomach = nothing to muffle it = loud
        s0 = S[3]
        rays(c, W/2, 1100, 1100, WHT, tq*20, f.k(B[3] + 0.1, B[3] + 0.5), a=0.25)
        stk(c, 'empty_plate', W*0.34 + jx, 1180 + jy, 1.0, -4 + jr, f.k(B[3] + 0.1, B[3] + 0.4), maxd=520)
        stk(c, 'megaphone', W*0.68 + jx, 1480 + jy, 1.0 + 0.05*abs(math.sin(tq*14)), -14 + jr*2, f.k(s0 + 1.8, s0 + 2.05), maxd=480)
        for i, (bx, by, rt) in enumerate([(170, 1560, -20), (930, 1120, 25)]):
            bolt(c, bx, by, 0.5, rt + jr*3, f.k(s0 + 2.0 + i*0.1, s0 + 2.2 + i*0.1))
        label(c, "EMPTY = nothing to MUFFLE it", W/2, 330, 62, -2 + jr*.5, k=f.k(s0 + 0.6, s0 + 0.85), seed=7)
        label(c, "so it gets LOUD!", W/2 + 15, 470, 96, 3 - jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 2.0, s0 + 2.25), seed=8)
    elif b == 4:  # clean-up wave a couple of hours after eating
        s0 = S[4]
        stk(c, 'clock', W*0.28 + jx, 1000 + jy, 0.95, -8 + jr, f.k(B[4] + 0.1, B[4] + 0.4), maxd=400)
        sweep = eio(f.k(s0 + 1.4, s0 + 2.6))
        stk(c, 'broom', lerp(-150, W*0.62, sweep) + jx, 1450 + jy, 1.0, -20 + 12*math.sin(tq*9) + jr, f.k(s0 + 1.3, s0 + 1.5), maxd=480)
        if tq > s0 + 2.4: stamp(c, "GRRR!", W*0.70, 1000, 150, 8, f.k(s0 + 2.4, s0 + 2.65))
        label(c, "~2 HOURS after eating", W/2, 330, 80, -2 + jr*.5, k=f.k(s0 + 0.3, s0 + 0.55), seed=9)
        label(c, "a CLEAN-UP wave!", W/2 + 15, 470, 92, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 1.4, s0 + 1.65), seed=10)
    else:         # tip: small snack or water
        s0 = S[5]
        rays(c, W/2, 1150, 1100, (.5, .4, 1), tq*8, f.k(B[5] + 0.2, B[5] + 0.6))
        stk(c, 'banana', W*0.30 + jx, 1060 + jy, 0.9, -16 + jr, f.k(s0 + 0.9, s0 + 1.15), maxd=460)
        stk(c, 'water_glass', W*0.72 + jx, 1080 + jy, 0.9, 6 + jr, f.k(s0 + 1.7, s0 + 1.95), maxd=420)
        label(c, "a small SNACK", W/2, 330, 96, -2 + jr*.5, bgcol=YEL, k=f.k(s0 + 1.0, s0 + 1.25), seed=11)
        label(c, "or a glass of WATER", W/2 + 15, 470, 84, 3 - jr*.5, bgcol=(.55, .85, 1), k=f.k(s0 + 1.8, s0 + 2.05), seed=12)
        if tq > DUR - 1.5: stamp(c, "SHHH!", W/2, 1500, 120, -6, f.k(DUR - 1.5, DUR - 1.25), col=RED)

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.5); K.sfx(0.35, 'pop', 0.6); K.sfx(0.55, 'pop', 0.6); K.sfx(0.8, 'pop', 0.7); K.sfx(0.85, 'pop', 0.6); K.sfx(1.0, 'ding2', 0.5)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.3, 'pop', 0.7); K.sfx(S[1] + 1.4, 'impact1', 0.9); K.sfx(S[1] + 1.45, 'scratch1', 0.6); K.sfx(S[1] + 2.0, 'pop', 0.7); K.sfx(S[1] + 2.1, 'bubble', 0.5)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.4, 'pop', 0.6); K.sfx(S[2] + 0.8, 'pop', 0.5)
for i in range(6): K.sfx(S[2] + 1.0 + i*0.3, 'bubble' if i % 2 else 'pop', 0.4)
K.sfx(S[2] + 1.6, 'pop', 0.7)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.6, 'pop', 0.7); K.sfx(S[3] + 1.8, 'pop', 0.7); K.sfx(S[3] + 2.0, 'impact2', 0.9); K.sfx(S[3] + 2.05, 'sparkle1', 0.4)
K.sfx(B[4] + 0.1, 'pop', 0.7); K.sfx(B[4] + 0.2, 'ding2', 0.4); K.sfx(S[4] + 0.3, 'pop', 0.6); K.sfx(S[4] + 1.3, 'swoosh3', 0.7); K.sfx(S[4] + 1.4, 'pop', 0.7); K.sfx(S[4] + 2.4, 'impact1', 0.9); K.sfx(S[4] + 2.45, 'scratch2', 0.5)
K.sfx(S[5] + 0.9, 'pop', 0.7); K.sfx(S[5] + 1.0, 'pop', 0.6); K.sfx(S[5] + 1.7, 'pop', 0.7); K.sfx(S[5] + 1.8, 'splash1', 0.4); K.sfx(S[5] + 1.8, 'ding1', 0.4)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p05_stomach_growl')
