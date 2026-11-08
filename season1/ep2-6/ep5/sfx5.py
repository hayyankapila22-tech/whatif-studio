import sys; sys.path.insert(0, '..')
import numpy as np
import sfxlib as L
L.init(50.0); add=L.add
n=6
for k in range(1,n+1):
    p = 1-(1-k/n)**(1/3.2); add(L.tick(), p*2.1, .9)
add(L.riser(2.0), 0.1, .25); add(L.ding(1568), 2.1, .55); add(L.whoosh(.5), 2.75, .4)
def engine(d, f0, f1, a=.5):
    t = L.tt(d); f = np.linspace(f0, f1, len(t)); ph = 2*np.pi*np.cumsum(f)/L.SR
    return (np.sign(np.sin(ph))*.3 + np.sin(ph*2)*.4 + L.rng.normal(0,.08,len(t))) * a
# rev + gear shifts
add(engine(2.6, 60, 160), 3.0, .5); add(engine(2.6, 90, 200), 5.6, .45); add(engine(2.6, 110, 240), 8.2, .45)
add(L.boom(1.4), 10.8, 1.0); add(L.shatter(.6), 10.8, .4)
def roar(d, a0, a1):
    t = L.tt(d); s = L.rng.normal(0,1,len(t)); return (L.lp(s, 12) - L.lp(s, 80)) * np.linspace(a0, a1, len(t)) * 3
add(roar(7.8, .4, 1.0), 10.8, .6)
add(L.whoosh(.5), 13.2, .4); add(L.rumble(2.4), 16.0, .7)
add(L.riser(2.4), 18.6, .45); add(L.whoosh(.8), 21.0, .6); add(L.boom(1.6), 21.2, .6)
for t0 in [23.8, 26.4]: add(L.whoosh(.6), t0-.3, .5); add(L.pop(700), t0, .3)
add(L.riser(2.2), 27.2, .6); add(L.boom(2.0), 29.4, 1.0); add(L.shatter(1.2), 29.4, .5)
add(L.glitch(1.0), 32.0, .5); add(L.buzz(.6, 90), 32.3, .4); add(L.glitch(.6), 33.6, .3)
for k in range(10): add(L.tick(), 37.8+k*.25, .5)
add(L.bong(147), 37.6, .5)
for k in range(24): add(L.tick(), 40.2+k*.1, .3)
add(L.ding(1318), 42.6, .5); add(L.whoosh(.5), 43.0, .4); add(L.bong(110), 43.2, .6)
add(L.whoosh(.5), 45.8, .4); add(L.pop(900), 47.0, .4)
L.finish(sys.argv[1], 'sfx.wav', 'mix.wav')
print('ok')
