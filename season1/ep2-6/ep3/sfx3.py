import sys; sys.path.insert(0, '..')
import numpy as np
import sfxlib as L
L.init(50.0); add=L.add
n=6
for k in range(1,n+1):
    p = 1-(1-k/n)**(1/3.2); add(L.tick(), p*2.1, .9)
add(L.riser(2.0), 0.1, .25); add(L.ding(1568), 2.1, .55); add(L.whoosh(.5), 2.75, .4)
def wind(d, a0, a1):
    t = L.tt(d); s = L.rng.normal(0,1,len(t)); out = L.lp(s, 18) - L.lp(s, 90)
    return out * np.linspace(a0, a1, len(t)) * 3
# jump + fall wind rising to the center, falling after
add(L.whoosh(.8), 3.6, .6)
add(wind(22.8, .15, 1.0), 3.6, .5)
add(wind(3.0, 1.0, .05), 26.4, .5)
add(wind(8.0, .9, .2), 32.0, .5)
stages=[5.6,8.2,10.8,13.4,16.0,18.6,21.2,23.8]
for i,t in enumerate(stages): add(L.whoosh(.5), t-.25, .35); add(L.pop(500+60*i), t, .25)
for t in [10.8, 13.4]: add(L.rumble(1.4), t, .6)
add(L.boom(1.8), 18.6, .6); add(L.boom(1.8), 23.8, .6)
add(L.ding(1046), 26.4, .5); add(L.bong(130), 26.4, .7)
add(L.riser(2.6), 29.6, .3)
add(L.boom(1.4), 32.4, .7); add(L.whoosh(.7), 32.3, .5)
for t in [35.0, 37.6]: add(L.whoosh(.5), t-.25, .3); add(L.pop(700), t, .25)
add(L.ding(1568), 40.0, .5); add(L.whoosh(.6), 39.8, .5)
# splash
t = L.tt(1.4); spl = L.lp(L.rng.normal(0,1,len(t)), 4) * np.exp(-t*3.5) * 1.2
add(spl, 43.0, .9); add(L.boom(1.0), 43.0, .4)
add(L.whoosh(.5), 45.8, .4); add(L.rumble(2.5), 46.0, .5); add(L.pop(900), 47.0, .4)
L.finish(sys.argv[1], 'sfx.wav', 'mix.wav')
print('ok')
