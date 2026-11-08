import sys; sys.path.insert(0, '..')
import numpy as np
import sfxlib as L
L.init(47.5); add=L.add
n=6
for k in range(1,n+1):
    p = 1-(1-k/n)**(1/3.2); add(L.tick(), p*2.1, .9)
add(L.riser(2.0), 0.1, .25); add(L.ding(1568), 2.1, .55); add(L.whoosh(.5), 2.75, .4)
def thud(f=60, a=1):
    t=L.tt(.6); return np.sin(2*np.pi*np.cumsum(f+40*np.exp(-t*20))/L.SR)*np.exp(-t*8)*a
for i,t0 in enumerate([3.0,5.6,8.2,10.8]): add(thud(70-8*i), t0, .9); add(L.bong(220-30*i), t0, .3)
add(L.bong(80), 11.2, .6)
t=L.tt(2.4); add(np.sin(2*np.pi*np.cumsum(1200-900*t/2.4)/L.SR)*.35*np.minimum(1,t*3), 13.5, .5); add(L.boom(1.4), 15.6, .7)
add(L.rumble(2.6), 16.0, 1.0); add(L.shatter(1.4), 16.4, .6)
add(L.rumble(2.6), 18.6, .9); add(L.boom(1.2), 20.3, .6)
add(L.whoosh(.8), 21.2, .5); add(L.bong(98), 21.4, .5)
add(thud(50), 23.8, 1.0); add(L.ding(1046), 24.4, .4)
add(L.whoosh(1.0), 26.6, .5); add(L.whoosh(1.0), 27.8, .5)
add(thud(45), 29.4, 1.0); [add(L.pop(1200), 29.5+k*.02, .05) for k in range(40)]
add(L.riser(2.8), 32.2, .6); add(L.rumble(2.8), 32.2, .6)
add(L.boom(2.6), 35.0, 1.2); add(L.glitch(.6), 35.1, .3)
t=L.tt(6.0); add(np.sin(2*np.pi*40*t)*.6*np.minimum(1,t)*np.minimum(1,(6-t)), 36.0, .6)
add(L.whoosh(.5), 43.2, .4); add(L.pop(900), 44.4, .4)
L.finish(sys.argv[1], 'sfx.wav', 'mix.wav')
print('ok')
