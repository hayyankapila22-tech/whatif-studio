import sys; sys.path.insert(0, '..')
import numpy as np
import sfxlib as L
L.init(48.0); add=L.add
n=6
for k in range(1,n+1):
    p = 1-(1-k/n)**(1/3.2); add(L.tick(), p*2.1, .9)
add(L.riser(2.0), 0.1, .25); add(L.ding(1568), 2.1, .55); add(L.whoosh(.5), 2.75, .4)
def wind(d, a0, a1, hi=18):
    t = L.tt(d); s = L.rng.normal(0,1,len(t)); out = L.lp(s, hi) - L.lp(s, 120)
    g = np.linspace(a0, a1, len(t)) * (1 + .25*np.sin(2*np.pi*.7*t)); return out * g * 3
# stop: screech + thud
t=L.tt(.7); add(np.sin(2*np.pi*np.cumsum(900-600*t/.7)/L.SR)*np.exp(-t*2)*.4, 3.5, .5); add(L.boom(1.4), 3.6, .7)
add(wind(15.6, .05, 1.0), 5.6, .7)
add(wind(2.6, 1.0, 1.0, 10), 21.2, .7)
for t0 in [8.2,10.8,13.4]: add(L.whoosh(.5), t0-.25, .4)
add(L.boom(1.2), 16.0, 1.0); add(L.shatter(.5), 16.0, .4)   # sonic boom
add(L.whoosh(.6), 18.4, .5)
for k in range(6): add(L.pop(300+50*k), 21.8+k*.3, .3)
add(L.rumble(3.0), 23.8, 1.0); t=L.tt(2.6); add(L.lp(L.rng.normal(0,1,len(t)),6)*np.minimum(1,t)*np.exp(-np.maximum(0,t-1.8)*3), 24.2, .8)
add(L.whoosh(.6), 26.6, .4); add(L.bong(147), 29.4, .6)
for k in range(20): add(L.tick(), 27.6+k*.09, .3)
add(L.riser(1.5), 31.0, .25); add(L.ding(1760), 32.4, .3)
add(L.bong(110), 35.0, .5)
add(L.rumble(2.5), 37.6, .5); add(L.whoosh(.7), 40.2, .4); add(L.ding(1318), 40.4, .4)
add(L.whoosh(.5), 43.2, .4); add(L.pop(900), 44.4, .4)
L.finish(sys.argv[1], 'sfx.wav', 'mix.wav')
print('ok')
