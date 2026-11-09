// Episode 10 — What if all humans vanished?  TIMELINE: counter = time since every human disappeared.
// Facts (checked 2026-11-09):
//  - fossil-fuel power plants fail "within hours" without operators -> grid cascades (xkcd What If "Lights Out")
//  - NYC subway floods within ~36-48 h once the pumps stop (Weisman via LiveScience 36 h; Scientific American 48 h; BBC Science Focus "after two days")
//  - ~7 days: emergency generators run out of fuel at nuclear plants (BBC Science Focus timeline)
//  - roads crack and buckle "in a matter of months" (Scientific American, Weisman interview)
//  - year 1: human head/body lice go extinct; city cockroaches freeze in cold regions (BBC Science Focus)
//  - year 3: pipes burst in colder regions, buildings weaken (BBC Science Focus)
//  - streets crater "within a couple of decades" (Scientific American)
//  - Chernobyl: wolves ~7x more abundant than in nearby reserves ~30 years after people left (Deryabina et al. 2015, Current Biology; UGA SREL)
//  - houses/office buildings collapse "over the following decades" (Scientific American)
//  - plastics persist for thousands of years (LiveScience / Weisman)
import { THREE, scene, camera, clamp, prog, lerp, eOut, eInOut, V, K, boot, mode, cam, dolly, shake, bubble, headPos, run, makeCar, focus, noFocus, RIM, GRADE, INK, rimLight } from './kit.js';
import { buildWorld, W, setAge, setSky, poof, flood, towers, collapse, debrisPile, resetCollapse, makeAnimal } from './world.js';

await boot('WHAT IF ALL HUMANS VANISHED?', 'EP. 10');
const J = K.J;
buildWorld(K);

// ---------- cast of animals + the rolling car ----------
const dogs = ['dog', 'dog2', 'dog'].map(k => { const a = makeAnimal(k); scene.add(a); rimLight(a); return a; });
const deer = ['deer', 'doe', 'doe'].map(k => { const a = makeAnimal(k); scene.add(a); rimLight(a); return a; });
const wolves = ['wolf', 'wolf', 'wolf'].map(k => { const a = makeAnimal(k); scene.add(a); rimLight(a); return a; });
const rollCar = makeCar(0xe8364e); scene.add(rollCar);
const hazard = [-1, 1].flatMap(s => [[2.08, s], [-2.08, s]]).map(([x, s]) => { const m = new THREE.Mesh(new THREE.SphereGeometry(.09, 12, 8), new THREE.MeshBasicMaterial({ color: 0xffa020, toneMapped: false })); m.position.set(x, .75, s * .72); rollCar.add(m); return m; });
const ALL = [...dogs, ...deer, ...wolves];

// ---------- timeline (v = days since humans vanished) ----------
const D = 1, H = 1 / 24, Y = 365.25;
const B = [
  { t: 3.2, v: 1 / 86400, cap: 'Every human on Earth just vanished. Even Jeremy.', hi: ['Every', 'human'], red: ['vanished.'], size: 62 },
  { t: 5.6, v: 1 * H, cap: 'Hour 1: cars roll to a stop. Nobody is driving.', hi: ['Nobody'] },
  { t: 8.0, v: 12 * H, cap: 'Within hours, power plants shut down. Lights out.', hi: ['Lights', 'out.'], size: 62 },
  { t: 10.4, v: 2 * D, cap: 'Day 2: the subway floods. The pumps stopped.', hi: ['floods.'] },
  { t: 12.8, v: 7 * D, cap: 'Day 7: backup power runs dry. Nuclear plants overheat.', red: ['overheat.'], size: 60 },
  { t: 15.2, v: 30 * D, cap: 'Month 1: pets go wild. Dogs roam in packs.', hi: ['packs.'] },
  { t: 17.6, v: 91 * D, cap: 'Month 3: weeds split the sidewalks.', hi: ['weeds'] },
  { t: 20.0, v: 1 * Y, cap: 'Year 1: head lice go extinct. Roaches freeze.', hi: ['lice'] },
  { t: 22.4, v: 3 * Y, cap: 'Year 3: frozen pipes burst. Walls crack.', hi: ['crack.'] },
  { t: 24.8, v: 10 * Y, cap: "Year 10: deer graze on Jeremy's street.", hi: ['deer'] },
  { t: 27.2, v: 20 * Y, cap: 'Year 20: trees burst through the road.', hi: ['trees'] },
  { t: 29.6, v: 30 * Y, cap: 'Year 30: wolves move in.', hi: ['wolves'], note: 'Real life: Chernobyl has ~7× more wolves than nearby reserves' },
  { t: 32.0, v: 50 * Y, cap: 'Year 50: the buildings start to fall.', red: ['fall.'], big: true },
  { t: 34.4, v: 100 * Y, cap: "Year 100: Jeremy's street is a FOREST.", hi: ['FOREST.'], big: true },
  { t: 36.8, v: 100 * Y, cap: "Jeremy's back. Only his plastic lid survived.", hi: ['plastic', 'lid'], bubble: '...HELLO?' },
  { t: 39.2, v: 100 * Y, cap: 'What should vanish next? 👇', hi: ['vanish', 'next?'] },
];
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;
function fmt(v) {
  const s = v * 86400;
  if (s < 59.5) return plural(Math.max(1, Math.round(s)), 'second');
  if (s < 3600) return plural(Math.round(s / 60), 'minute');
  if (v < 1) return plural(Math.max(1, Math.round(v * 24)), 'hour');
  if (v < 45) return plural(Math.round(v), 'day');
  if (v < 360) return plural(Math.round(v / 30.44), 'month');
  return plural(Math.round(v / Y), 'year');
}

// ---------- helpers ----------
const JX = 34.5, JZ = 5.6, SOUTH = W.blocks.find(b => b.userData.side > 0 && Math.abs(b.userData.x - 44) < 1);
function jer(x, z, ry, pose, cup = false) {
  J.visible = true; J.position.set(x, .18, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose);
  if (cup) { J.arms[1].rotation.x = -1.15; J.arms[1].add(W.cup); W.cup.position.set(-.02, -.74, .05); W.cup.rotation.set(1.15, 0, 0); W.cup.visible = true; }
}
function hideAll() {
  J.visible = false; J.arms[1].rotation.x = 0; if (W.cup.parent !== scene) scene.add(W.cup); W.cup.visible = false; W.lid.visible = false; W.splash.visible = false; W.sparkle.visible = false;
  ALL.forEach(a => a.visible = false); rollCar.visible = false; towers(false); flood(0); resetCollapse();
  noFocus(); RIM.k = .55; INK.on = true; GRADE.split = .08;
}
const cupOnGround = (t) => { W.cup.visible = true; W.cup.position.set(JX + .35, .27, JZ - .55); W.cup.rotation.set(0, .4, Math.PI / 2); W.splash.visible = true; W.splash.position.set(JX + .55, .19, JZ - .75); W.splash.scale.setScalar(1.6); };
function walk(a, x, z, ry, t, speed = 1, extra = {}) { a.visible = true; a.position.set(x, .18, z); a.rotation.set(0, ry, 0); a.pose({ walk: speed > 0 ? 1 : 0, ph: t * 1.6 * speed, t, ...extra }); }

run({
  total: 43.5, ctaAt: 39.2, sub: 'without humans',
  reel: ['(x)', 'PIGEONS DOUBLED', 'YOUR COFFEE DOUBLED', 'JEREMY KEPT GROWING', 'GRAVITY DOUBLED', 'EARTH STOPPED', 'ALL HUMANS VANISHED?'],
  beats: B, label: () => 'HUMANS GONE FOR', fmt,
  beds: [{ t0: 0, t1: 3.8, name: 'city', gain: .32 }, { t0: 3.75, t1: 8.2, name: 'wind', gain: .18 }, { t0: 8.5, t1: 10.5, name: 'crickets', gain: .22 },
    { t0: 10.4, t1: 12.9, name: 'drip', gain: .25 }, { t0: 12.8, t1: 15.3, name: 'drone', gain: .32 }, { t0: 15.2, t1: 20.1, name: 'birds', gain: .18 },
    { t0: 20.0, t1: 22.5, name: 'winter', gain: .35 }, { t0: 22.4, t1: 24.9, name: 'wind', gain: .18 }, { t0: 24.8, t1: 29.7, name: 'birds', gain: .2 },
    { t0: 29.6, t1: 32.1, name: 'crickets', gain: .2 }, { t0: 32.0, t1: 34.5, name: 'wind', gain: .2 }, { t0: 34.4, t1: 43.5, name: 'birds', gain: .28 }],
  sfx: [{ t: 3.75, name: 'poof', gain: .8 }, { t: 4.2, name: 'clatter', gain: .55 }, { t: 4.25, name: 'splash', gain: .35 },
    { t: 5.6, name: 'car_roll', gain: .6 }, { t: 5.7, name: 'hazard', gain: .22 }, { t: 8.4, name: 'flicker', gain: .3 }, { t: 8.5, name: 'power_down', gain: .7 },
    { t: 10.4, name: 'water_gush', gain: .55 }, { t: 12.9, name: 'siren', gain: .3, pan: .3 }, { t: 15.6, name: 'bark', gain: .5, pan: -.2 }, { t: 15.95, name: 'bark_hi', gain: .45, pan: .2 },
    { t: 16.6, name: 'bark', gain: .4 }, { t: 17.7, name: 'rustle', gain: .3 }, { t: 20.1, name: 'wind_gust', gain: .35 }, { t: 22.6, name: 'pipe_burst', gain: .5 },
    { t: 23.2, name: 'crack', gain: .55, pan: -.3 }, { t: 23.7, name: 'crack', gain: .4, pan: .3 }, { t: 25.2, name: 'rustle', gain: .25 }, { t: 27.3, name: 'wind_gust', gain: .25 },
    { t: 27.4, name: 'rustle', gain: .35 }, { t: 30.0, name: 'howl', gain: .6 }, { t: 32.2, name: 'crumble', gain: .95 }, { t: 36.75, name: 'sparkle_rev', gain: .6 }],
  introShot(t) {
    mode('street'); hideAll(); setSky('day'); setAge(0, t, { lamps: 0 });
    jer(28 + t * 1.6, JZ, Math.PI / 2, { expr: 'happy', bob: Math.abs(Math.sin(t * 6)) * .03, armL: .25 }, true);
    dolly(V(26, 7, -3), V(30, 5, -1), V(33, 1.4, 5.6), V(34, 1.3, 5.6), t / 3.2);
  },
  shot(t, b, lt, i) {
    mode('street'); hideAll(); const k = clamp(lt / 2.4);
    if (i === 0) { // the vanishing
      setSky('day'); setAge(0, t, { lamps: 0 });
      const gone = lt > .55;
      if (!gone) jer(JX, JZ, Math.PI + .25, { expr: 'happy', look: .2, armL: .2, bob: Math.sin(lt * 9) * .01 }, true);
      else { J.visible = false; poof(V(JX, 1.3, JZ), (lt - .55) / .9);
        const f = clamp((lt - .55) / .45), cx = JX + .35, cz = JZ - .55; W.cup.visible = true; W.cup.position.set(cx, lerp(1.25, .27, f * f), cz); W.cup.rotation.set(0, .4, f * Math.PI / 2);
        if (f >= 1) { W.splash.visible = true; W.splash.position.set(cx + .2, .19, cz - .2); W.splash.scale.setScalar(.2 + eOut(clamp((lt - 1) / .5)) * 1.4); } }
      dolly(V(JX + 2.6, 1.7, JZ - 5.2), V(JX + 1.7, 1.0, JZ - 3.0), V(JX, 1.25, JZ), V(JX + .4, .45, JZ - .6), eInOut(k));
      focus(V(JX, 1.1, JZ), 1.1, 12);
    } else if (i === 1) { // driverless car rolls to a stop at the curb
      setSky('day'); setAge(H / Y, t); cupOnGround(t);
      const p = eOut(clamp(lt / 2.0)); rollCar.visible = true; rollCar.position.set(lerp(12, 31.5, p), 0, lerp(-1.4, 2.9, p * p)); rollCar.rotation.set(0, -lerp(0, .22, p), 0);
      hazard.forEach(h => h.visible = Math.floor(t * 2.5) % 2 === 0);
      if (lt > 2.0) shake(.02 * (1 - (lt - 2) / .4), t);
      dolly(V(JX + 4, .5, JZ - .4), V(JX + 3.6, .55, JZ - .6), V(26, .8, 1), V(29, .7, 2), k, 0, 50);
      focus(V(lerp(12, 31.5, p), .8, 1), .9, 12);
    } else if (i === 2) { // the lights go out (dusk -> night)
      const off = clamp((lt - .5) / 1.6);
      setSky('dusk', 'night', clamp(lt / 1.2)); setAge(.5 / Y, t, { lights: 1 - off, lamps: (1 - off) * (lt > .4 && lt < 1.1 ? (Math.sin(t * 60) > 0 ? 1 : .2) : 1) });
      dolly(V(21.6, 1.6, -6.3), V(23, 1.8, -6.1), V(40, 7, 9), V(41, 7.4, 9), k, .03, 58);
    } else if (i === 3) { // subway floods
      setSky('overcast'); setAge(2 / Y, t, { lamps: 0 });
      flood(clamp(lt / 2.2), t);
      dolly(V(48.5, 6.2, 1.2), V(48, 5.8, 1.6), V(43.2, .3, 6.2), V(43.2, .3, 6.2), k, 0, 52);
      focus(V(43.5, .2, 6), .9, 12);
    } else if (i === 4) { // nuclear plants on their own
      setSky('ominous'); setAge(7 / Y, t); towers(true, t, clamp(lt / 1.5)); flood(1, t); GRADE.split = .14;
      dolly(V(52, 2.0, .6), V(56, 2.3, .4), V(320, 70, -26), V(320, 76, -26), k, 0, 42);
    } else if (i === 5) { // dogs go wild
      setSky('day'); setAge(30 / Y, t); flood(1, t);
      dogs.forEach((d, j) => walk(d, lerp(52, 38, k) + [0, 1.4, -1.2][j], [0, -1.1, .9][j], -Math.PI / 2, t + j * .3, 1.2, { wag: .5 }));
      dolly(V(33, .45, .6), V(33.5, .45, .5), V(42, .5, 0), V(41, .55, 0), k, 0, 48);
      focus(V(lerp(52, 38, k), .5, 0), .8, 12);
    } else if (i === 6) { // weeds split the sidewalk
      setSky('day'); setAge(.25 + lt * .04, t); cupOnGround(t);
      dolly(V(JX + 3.2, .9, JZ - 2.2), V(JX + 2.7, .8, JZ - 1.9), V(JX, .2, 4.6), V(JX - .4, .2, 4.6), k, 0, 45);
      focus(V(JX + .3, .25, 4.6), 1.1, 14);
    } else if (i === 7) { // year 1: winter
      setSky('winter'); setAge(1, t, { snow: 1, cx: JX, cz: 0 }); GRADE.split = .04;
      dolly(V(JX - 6, 2.2, -3.4), V(JX - 5.4, 2.0, -3.2), V(JX + 6, 1.4, 4), V(JX + 6.4, 1.4, 4), k, 0, 55);
    } else if (i === 8) { // pipes burst, walls crack
      setSky('overcast'); setAge(3, t); cupOnGround(t); W.splash.visible = false;
      dolly(V(37, 1.6, .4), V(37.8, 1.8, .8), V(45, 6, 7.9), V(46, 6.4, 7.9), k, -.02, 55);
    } else if (i === 9) { // deer graze
      setSky('day'); setAge(10, t);
      walk(deer[0], 39, -1, -Math.PI / 2 + .5, t, 0, { graze: .8 + .2 * Math.sin(t * 2) });
      walk(deer[1], 42.5, 1.6, -2.2, t, 0, { graze: lt > 1 ? 0 : 1 });
      walk(deer[2], 45, -2.6, -1.2, t, 0, { graze: 1 });
      dolly(V(30.5, 1.2, 2.2), V(31, 1.2, 2.0), V(37, 1.0, -.2), V(37.4, 1.0, -.2), k, 0, 45);
      focus(V(39, .9, -1), 1.0, 14);
    } else if (i === 10) { // trees burst through the road
      setSky('golden'); setAge(20, t);
      dolly(V(15.5, 1.0, -4.2), V(16, 6.5, -5.2), V(24, 2.5, 2.0), V(24, 8, 2.0), eInOut(k), 0, 58);
    } else if (i === 11) { // wolves
      setSky('dusk'); setAge(30, t);
      walk(wolves[0], 37, .2, Math.PI + .25, t, 0, { howl: eOut(clamp((lt - .4) / .6)) });
      walk(wolves[1], lerp(46, 40, k), 1.8, -Math.PI / 2, t, 1);
      walk(wolves[2], lerp(47, 41.5, k), -1.6, -Math.PI / 2 + .2, t + .4, 1);
      dolly(V(32, 1.1, 2.4), V(32.5, 1.1, 2.2), V(38, 1.0, 0), V(38, 1.1, 0), k, 0, 46);
      focus(V(37, 1, .2), .9, 14);
    } else if (i === 12) { // collapse
      setSky('overcast'); collapse(SOUTH, clamp((lt - .2) / 1.7), t); setAge(50, t);
      if (lt > .25 && lt < 1.4) shake(.08 * (1 - (lt - .25) / 1.15), t);
      dolly(V(33.4, 4.2, 6.5), V(33.8, 4.4, 6.7), V(44, 8, -11), V(44, 6.5, -11), k, 0, 72);
    } else if (i === 13) { // year 100 forest
      setSky('golden'); debrisPile(SOUTH); setAge(100, t);
      walk(deer[0], 30, -1, .8, t, 0, { graze: 1 }); walk(deer[1], 33, 1.5, -.6, t, 0, { graze: .3 });
      dolly(V(16, 19, 0), V(21, 15, .4), V(42, 1.5, 0), V(42, 1.5, 0), eInOut(k), 0, 52);
    } else { // Jeremy returns, holding the lid
      setSky('golden'); debrisPile(SOUTH); setAge(100, t);
      walk(deer[1], 39, 2.2, -2.4, t, 0, { graze: lt > 1.4 ? 0 : 1 });
      const back = i === 14 ? lt > .25 : true;
      if (i === 14) poof(V(JX, 1.3, JZ), (lt - .1) / .9);
      if (back) {
        const wave = i === 15 ? .3 + Math.abs(Math.sin(t * 5)) * 2.4 : .3;
        jer(JX, JZ - .4, Math.PI + .15, { expr: i === 14 ? (lt < 1.4 ? 'shocked' : 'confused') : 'happy', look: Math.sin(t * 1.5) * .6, armL: wave, armR: .3 }, false);
        J.arms[1].rotation.x = -1.0; J.arms[1].add(W.lid); W.lid.position.set(0, -.8, .1); W.lid.rotation.set(1.0 - Math.PI / 2, 0, 0); W.lid.visible = true;
      }
      if (i === 14) dolly(V(JX + 1.4, 1.4, JZ - 4.6), V(JX + 1.2, 1.35, JZ - 4.2), V(JX, 1.5, JZ), V(JX, 1.5, JZ), k);
      else dolly(V(JX + 1.2, 1.35, JZ - 4.2), V(JX + 1.6, 2.4, JZ - 5.6), V(JX, 1.5, JZ), V(JX, 1.7, JZ), eInOut(k));
      if (back && i === 14) bubble(t, b.bubble, b.t + 1.5, headPos());
      focus(V(JX, 1.1, JZ - .4), 1.0, 12);
    }
    const sm = document.getElementById('small'); sm.style.top = '1290px'; sm.style.fontSize = '42px'; sm.style.fontFamily = 'IDB'; sm.style.color = '#ffe08a'; sm.style.webkitTextStroke = '5px #0a0b18'; sm.style.paintOrder = 'stroke fill'; sm.style.left = '60px'; sm.style.right = '150px';
    sm.textContent = b.note || ''; sm.style.opacity = b.note ? clamp((lt - .3) / .3) : 0;
    if (b.big && lt < .35 && i !== 12) shake(.06 * (1 - lt / .35), t);
  },
});
