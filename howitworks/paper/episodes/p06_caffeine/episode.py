"""P06 — How does coffee keep you awake? (PAPER-CUTOUT format) — educational only, not medical advice.
Facts (plain words, no studies): caffeine adds no energy (no calories in black coffee); while you're awake a chemical
called adenosine builds up in the brain and makes you feel sleepy; caffeine is shaped like adenosine and sits in the
same receptors ("parking spots"), blocking the sleepy signal; adenosine keeps building up behind it, so when caffeine
wears off you can feel a "crash"; caffeine's half-life is about 5 hours (range ~3–7), so an afternoon coffee is still
in your system at bedtime; sleep experts suggest stopping caffeine roughly 8 hours before bed.
Sources: Sleep Foundation "Caffeine and sleep"; Univ. of Newcastle Hippocampus "Coffee won't give you extra energy";
CSPI "Is caffeine messing with your sleep?"; Examine.com "How does caffeine work in your brain?".
Run:  /home/claude/cbx/bin/python3 ../../tts_voice.py  ->  python3 episode.py stills  ->  python3 episode.py all
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from paperkit import *

VO = [f'vo_{i}.wav' for i in range(6)]
S, DUR = timeline(VO)
MUSIC = os.environ.get('PAPER_MUSIC', 'quirky' if os.path.exists(os.path.join(MUS, 'quirky.mp3')) else 'timeless')
K = Kit(S, DUR, ['coral', 'navy', 'purple', 'teal', 'red', 'yellow'], shakes=[S[1] + 1.6, S[3] + 2.4, S[4] + 2.6, DUR - 1.5], voice_files=VO, music=MUSIC)
B = K.B
SLEEPY = (.62, .55, 1.0)

def zzz(c, x, y, size, rot, k):
    glyph(c, 'Z', x, y, size, rot, k, col=SLEEPY)

def scene(c, t, f):
    tq, jx, jy, jr, b = f.tq, f.jx, f.jy, f.jr, f.beat
    if b == 0:   # hook: coffee cup + alarm clock
        rays(c, W/2, 1080, 1100, WHT, tq*12, f.k(0.05, 0.45))
        stk(c, 'coffee_cup', W/2 + jx, 1060 + jy, 1.25, jr - 3, f.k(0.0, 0.3), maxd=640)
        stk(c, 'alarm_clock', W*0.74 + jx, 1520 + jy, 0.85 + 0.04*abs(math.sin(tq*30)), 10 + jr*2, f.k(0.7, 0.95), maxd=420)
        glyph(c, '?', 170, 760, 140, -12 + jr*2, f.k(0.35, 0.6)); glyph(c, '?', 920, 720, 120, 14 - jr*2, f.k(0.55, 0.8))
        label(c, "HOW does COFFEE", W/2 + jx*.4, 330, 92, -3 + jr*.5, k=f.k(0.15, 0.4), seed=1)
        label(c, "keep you AWAKE?", W/2 + 10, 470, 96, 2 - jr*.5, bgcol=YEL, k=f.k(0.8, 1.05), seed=2)
    elif b == 1:  # plot twist: no energy
        s0 = S[1]
        stk(c, 'battery', W*0.42 + jx, 1080 + jy, 1.1, -8 + jr, f.k(B[1] + 0.1, B[1] + 0.4), maxd=520)
        stk(c, 'coffee_beans', W*0.70 + jx, 1530 + jy, 0.95, 12 + jr, f.k(s0 + 0.8, s0 + 1.05), maxd=460)
        if tq > s0 + 1.6: stamp(c, "ZERO ENERGY!", W*0.44, 1120, 110, -10, f.k(s0 + 1.6, s0 + 1.85))
        label(c, "PLOT TWIST...", W/2, 330, 96, -2 + jr*.5, k=f.k(s0 + 0.2, s0 + 0.45), seed=3)
        label(c, "it adds NO ENERGY!", W/2 + 15, 470, 86, 3 - jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 1.6, s0 + 1.85), seed=4)
    elif b == 2:  # sleepy chemical builds up in your brain
        s0 = S[2]
        rays(c, W/2, 1100, 1000, SLEEPY, -tq*8, f.k(B[2] + 0.2, B[2] + 0.6), a=0.3)
        stk(c, 'brain', W/2 + jx, 1060 + jy, 1.1, -4 + jr, f.k(B[2] + 0.1, B[2] + 0.4), maxd=600)
        for i in range(7):   # sleepy puffs piling up around the brain
            ph = s0 + 0.9 + i*0.35
            ang = i/7*2*math.pi + 0.3
            cloud(c, W/2 + 330*math.cos(ang) + jx, 1060 + 300*math.sin(ang) + jy, 70, SLEEPY, f.k(ph, ph + 0.25), seed=i)
        stk(c, 'pillow', W*0.24 + jx, 1600 + jy, 0.8, -10 + jr, f.k(s0 + 2.4, s0 + 2.65), maxd=400)
        zzz(c, 860, 1560, 130, 12 + jr*2, f.k(s0 + 2.6, s0 + 2.85))
        label(c, "a SLEEPY chemical", W/2, 330, 86, -2 + jr*.5, k=f.k(s0 + 0.5, s0 + 0.75), seed=5)
        label(c, "BUILDS UP all day", W/2 + 15, 470, 88, 3 - jr*.5, bgcol=SLEEPY, k=f.k(s0 + 1.2, s0 + 1.45), seed=6)
    elif b == 3:  # caffeine steals its parking spots -> blocked
        s0 = S[3]
        stk(c, 'brain', W*0.30 + jx, 1000 + jy, 0.75, -6 + jr, f.k(B[3] + 0.1, B[3] + 0.4), maxd=480)
        stk(c, 'traffic_cone', W*0.78 + jx, 920 + jy, 0.7, 8 + jr, f.k(s0 + 0.9, s0 + 1.1), maxd=360)
        drive = eio(f.k(s0 + 1.0, s0 + 1.9))
        stk(c, 'coffee_beans', lerp(W + 250, W*0.62, drive) + jx, 1420 + jy, 1.0, -6 + jr, f.k(s0 + 0.95, s0 + 1.1), maxd=460)
        if tq > s0 + 2.0:
            cloud(c, W*0.22 + jx, 1520, 80, SLEEPY, f.k(s0 + 2.0, s0 + 2.2), seed=3)
            zzz(c, W*0.22, 1520, 90, -8, f.k(s0 + 2.0, s0 + 2.2))
        stk(c, 'padlock', W*0.50 + jx, 1700 + jy, 0.6, 10 + jr, f.k(s0 + 2.4, s0 + 2.6), maxd=360)
        if tq > s0 + 2.4: stamp(c, "BLOCKED!", W*0.62, 1180, 130, 8, f.k(s0 + 2.4, s0 + 2.65))
        label(c, "caffeine STEALS its SPOT", W/2, 330, 74, -2 + jr*.5, k=f.k(s0 + 1.0, s0 + 1.25), seed=7)
        label(c, "message BLOCKED!", W/2 + 15, 470, 90, 3 - jr*.5, bgcol=YEL, k=f.k(s0 + 2.4, s0 + 2.65), seed=8)
    elif b == 4:  # sleepy stuff piles up -> crash
        s0 = S[4]
        n = int(clamp((tq - s0 - 0.4) / 0.22, 0, 12))
        for i in range(n):   # pile of sleepy puffs
            row = i // 4; col = i % 4
            cloud(c, 230 + col*210 + (row % 2)*100 + jx, 1650 - row*150 + jy, 95, SLEEPY, 1, seed=i)
        stk(c, 'coffee_cup', W*0.70 + jx, 1000 + jy, 0.8, 10 + jr - (25 if tq > s0 + 2.6 else 0), f.k(B[4] + 0.1, B[4] + 0.4), maxd=440)
        stk(c, 'pillow', W*0.30 + jx, 1010 + jy, 0.9, -8 + jr, f.k(s0 + 2.5, s0 + 2.7), maxd=420)
        if tq > s0 + 2.6: stamp(c, "CRASH!", W/2, 1260, 160, -8, f.k(s0 + 2.6, s0 + 2.85))
        label(c, "the sleepy stuff PILES UP", W/2, 330, 70, -2 + jr*.5, k=f.k(s0 + 0.4, s0 + 0.65), seed=9)
        label(c, "then... CRASH!", W/2 + 15, 470, 100, 3 - jr*.5, bgcol=RED, fg=WHT, k=f.k(s0 + 2.6, s0 + 2.85), seed=10)
    else:         # tip: last coffee ~8 h before bed
        s0 = S[5]
        rays(c, W/2, 1150, 1100, WHT, tq*8, f.k(B[5] + 0.2, B[5] + 0.6), a=0.3)
        stk(c, 'alarm_clock', W*0.30 + jx, 1060 + jy, 0.95, -10 + jr, f.k(s0 + 0.3, s0 + 0.55), maxd=440)
        stk(c, 'coffee_cup', W*0.72 + jx, 1100 + jy, 0.85, 8 + jr, f.k(s0 + 1.6, s0 + 1.85), maxd=420)
        stk(c, 'pillow', W*0.50 + jx, 1580 + jy, 0.75, -4 + jr, f.k(s0 + 2.6, s0 + 2.85), maxd=380)
        label(c, "it lasts for HOURS", W/2, 330, 92, -2 + jr*.5, k=f.k(s0 + 0.4, s0 + 0.65), seed=11)
        label(c, "last coffee: 8 h before BED", W/2 + 15, 470, 66, 3 - jr*.5, bgcol=BLK, fg=YEL, k=f.k(s0 + 1.7, s0 + 1.95), seed=12)
        if tq > DUR - 1.5: stamp(c, "SWEET DREAMS!", W/2, 1300, 100, -6, f.k(DUR - 1.5, DUR - 1.25), col=(.45, .3, .95))

# ---------- sound design ----------
K.default_sfx()
K.sfx(0.02, 'pop', 0.9); K.sfx(0.05, 'impact2', 0.5); K.sfx(0.35, 'pop', 0.6); K.sfx(0.55, 'pop', 0.6); K.sfx(0.7, 'ding1', 0.5); K.sfx(0.8, 'pop', 0.7); K.sfx(1.0, 'ding2', 0.4)
K.sfx(B[1] + 0.1, 'pop', 0.7); K.sfx(S[1] + 0.2, 'pop', 0.7); K.sfx(S[1] + 0.8, 'pop', 0.6); K.sfx(S[1] + 1.6, 'impact1', 0.9); K.sfx(S[1] + 1.65, 'scratch1', 0.6)
K.sfx(B[2] + 0.1, 'pop', 0.7); K.sfx(S[2] + 0.5, 'pop', 0.6); K.sfx(S[2] + 1.2, 'pop', 0.6)
for i in range(7): K.sfx(S[2] + 0.9 + i*0.35, 'bubble' if i % 2 else 'pop', 0.4)
K.sfx(S[2] + 2.4, 'pop', 0.7); K.sfx(S[2] + 2.6, 'sparkle2', 0.4)
K.sfx(B[3] + 0.1, 'pop', 0.7); K.sfx(S[3] + 0.9, 'pop', 0.6); K.sfx(S[3] + 1.0, 'swoosh3', 0.7); K.sfx(S[3] + 1.0, 'pop', 0.6); K.sfx(S[3] + 2.0, 'bubble', 0.5)
K.sfx(S[3] + 2.4, 'impact1', 0.9); K.sfx(S[3] + 2.45, 'snip', 0.5)
K.sfx(B[4] + 0.1, 'pop', 0.7); K.sfx(S[4] + 0.4, 'pop', 0.6)
for i in range(0, 12, 3): K.sfx(S[4] + 0.4 + i*0.22, 'bubble', 0.35)
K.sfx(S[4] + 2.5, 'pop', 0.7); K.sfx(S[4] + 2.6, 'impact2', 1.0); K.sfx(S[4] + 2.65, 'scratch2', 0.5)
K.sfx(S[5] + 0.3, 'pop', 0.7); K.sfx(S[5] + 0.4, 'pop', 0.6); K.sfx(S[5] + 0.45, 'ding1', 0.4); K.sfx(S[5] + 1.6, 'pop', 0.7); K.sfx(S[5] + 1.7, 'pop', 0.6); K.sfx(S[5] + 2.6, 'pop', 0.6)
K.sfx(DUR - 1.5, 'impact1', 0.8); K.sfx(DUR - 1.45, 'sparkle1', 0.5)

if __name__ == '__main__':
    K.run(scene, sys.argv, name='p06_caffeine')
