import sys; sys.path.insert(0, '..')
import numpy as np
import sfxlib as L
L.init(50.0)
add=L.add
# intro: reel ticks (6 items), land
n=6
for k in range(1,n+1):
    p = 1-(1-k/n)**(1/3.2); add(L.tick(), p*2.1, .9)
add(L.riser(2.0), 0.1, .25); add(L.ding(1568), 2.1, .55); add(L.whoosh(.5), 2.75, .4)
stages=[3.0,5.6,8.2,10.8,13.4,16.0,18.6,21.2,23.8,26.4,29.4,32.4,34.6,37.2,40.0,43.0,46.2]
for i,t in enumerate(stages):
    if i<=9:
        add(L.chaching(), t, .5 + .04*i)
        if i>0:
            for k in range(14): add(L.tick(), t-0.9+k*0.064, .35)
add(L.pop(1100), 8.3, .3); add(L.pop(1100), 13.5, .3); add(L.pop(1100), 18.7, .3); add(L.pop(1100), 23.9, .3)
add(L.bong(196), 29.4, .6)
add(L.riser(2.2), 32.4, .5)
for k in range(30): add(L.tick(), 32.6+k*0.066, .3)
add(L.boom(), 34.6, .7); add(L.chaching(), 34.6, .5)
for k in range(14): add(L.tick(), 36.3+k*0.064, .35)
add(L.boom(), 37.2, .8); add(L.whoosh(.6), 37.0, .4)
for k in range(14): add(L.tick(), 39.1+k*0.064, .35)
add(L.boom(2.0), 40.0, .9); add(L.whoosh(.7), 39.8, .5)
for k in range(14): add(L.tick(), 42.1+k*0.064, .4)
add(L.shatter(1.6), 43.0, .9); add(L.boom(2.2), 43.0, 1.0); add(L.glitch(.8), 43.2, .3)
add(L.whoosh(.5), 46.0, .4)
for i in range(3): add(L.pop(900+150*i), 46.2+0.22*i, .45)
add(L.ding(1318), 47.4, .35)
L.finish(sys.argv[1], 'sfx.wav', 'mix.wav')
print('ok')
