// Episode 19 — What if gravity reversed for 10 seconds every day?  (v5.1 premium studio look + AI voiceover; continuous camera, structure from ep13/ep18)
// Everything is timed to the narration (vo.json from vo_lines.json). The flight numbers are computed below (simulate()), not guessed.
// Facts / physics (checked 2026-11-14):
//  - g = 9.81 m/s². Reversed for 10 s with air drag: belly-down human terminal speed ≈ 53 m/s (~190 km/h; Exploratorium via
//    hypertextbook.com/facts/1998/JianHuang.shtml). Quadratic-drag integration: 338 m and 50 m/s after 10 s, coast to a peak of ~431 m at 14.1 s,
//    land at ~25.9 s at ~52 m/s ≈ 186 km/h. (Without air it would be 490 m after 10 s, peak 981 m.)
//  - Eiffel Tower: 330 m since the March 2022 DAB antenna (toureiffel.paris "Eiffel Tower grows 330 meters tall") -> 338 m is higher.
//  - world population ≈ 8.2 billion (UN World Population Prospects 2024) -> "8 billion".
//  - gravity is by far the weakest fundamental force; a small magnet lifts a paper clip against the pull of the whole Earth (Vatican Observatory "Wimpy gravity").
//  - everything about how society copes ("hold on", cars and boats lifting) is labelled SPECULATION on screen and "our guess" in the voice.
import { THREE, RoundedBoxGeometry, scene, camera, clamp, lerp, eOut, eInOut, K, rimLight, makeCar } from './kit.js';
import { key, hemi, DOF, draw, renderer, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd } from './studio.js';
import { makeJeremy2 } from './jeremy2.js';

await bootStudio('WHAT IF GRAVITY FLIPPED?', 'EP. 19');
const VO = await (await fetch('./vo.json')).json(), LN = VO.lines, total = VO.total;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const $ = id => document.getElementById(id);
floorScale(1);
$('ui').insertAdjacentHTML('afterbegin', '<div id="v5fade" style="position:absolute;inset:0;background:#0a0a0c;opacity:0"></div>');

// ---------------------------------------------------------------- physics: reversed gravity for 10 s, quadratic air drag (vt = 53 m/s)
const G = 9.81, VT = 53, KD = G / VT / VT, SIM = []; // [tau, y, v]
{ let y = 0, v = 0, tau = 0; const dt = .002; while (true) { const a = (tau < 10 ? G : -G) - KD * v * Math.abs(v); v += a * dt; y += v * dt; tau += dt; SIM.push([tau, y, v]); if (tau > 11 && y <= 0) break; } }
const TLAND = SIM[SIM.length - 1][0];
const simAt = tau => { if (tau <= 0) return [0, 0]; const k = Math.min(SIM.length - 1, Math.floor(tau / .002)); return [SIM[k][1], SIM[k][2]]; };
const PEAK = Math.max(...SIM.map(s => s[1]));

// ---------------------------------------------------------------- materials / helpers
const marbleTex = canvasTex(512, 512, (ctx, w, h) => { const r = rand(8); ctx.fillStyle = '#e9e6e0'; ctx.fillRect(0, 0, w, h);
  for (let i = 0; i < 26; i++) { ctx.strokeStyle = `rgba(120,116,112,${.05 + r() * .12})`; ctx.lineWidth = .6 + r() * 2.2; ctx.beginPath(); let x = r() * w, y = r() * h; ctx.moveTo(x, y); for (let k = 0; k < 9; k++) { x += (r() - .5) * 120; y += (r() - .3) * 90; ctx.lineTo(x, y); } ctx.stroke(); } }).tex;
const marble = new THREE.MeshPhysicalMaterial({ map: marbleTex, roughness: .28, clearcoat: .5, clearcoatRoughness: .3 });
const brass = new THREE.MeshStandardMaterial({ color: 0xb8894a, metalness: 1, roughness: .3 });
const steel = new THREE.MeshStandardMaterial({ color: 0xc9ccd3, metalness: 1, roughness: .18 });
const accentM = new THREE.MeshBasicMaterial({ color: ACCENT, toneMapped: false });
const shadowAll = g => { g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };
function plinth(w, d, h) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, .03), marble); m.position.y = h / 2; m.castShadow = m.receiveShadow = true; return m; }
const ball = (r, col, seed) => { const tx = canvasTex(256, 128, (ctx, w, h) => { const cs = col; for (let i = 0; i < 6; i++) { ctx.fillStyle = cs[i % cs.length]; ctx.fillRect(i * w / 6, 0, w / 6 + 1, h); } }).tex;
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 32), new THREE.MeshPhysicalMaterial({ map: tx, roughness: .35, clearcoat: .6 })); m.castShadow = true; return m; };

// ---------------------------------------------------------------- A. the flight set: Jeremy, a car, beach balls, and a 330 m tower 110 m away
const TX = -110; // tower centre x
const tower = new THREE.Group();
{ const iron = new THREE.MeshStandardMaterial({ color: 0x6b5a45, roughness: .62, metalness: .35 });
  const half = h => 62.5 * Math.exp(-h / 75) + 3; // leg half-spread vs height (base 125 m square, platforms at 57 / 116 / 276 m)
  for (const [sx, sz] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) { const pts = []; for (let k = 0; k <= 40; k++) { const h = k / 40 * 276; const w = half(h); pts.push(V(sx * w, h, sz * w)); }
    const leg = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, 3.2, 16), iron); tower.add(leg);
    const foot = new THREE.Mesh(new RoundedBoxGeometry(14, 6, 14, 2, 1), new THREE.MeshStandardMaterial({ color: 0x9a9184, roughness: .9 })); foot.position.set(sx * 62.5, 3, sz * 62.5); tower.add(foot); }
  // arches between the legs at the base
  for (let f = 0; f < 4; f++) { const a = new THREE.Mesh(new THREE.TorusGeometry(37, 1.6, 12, 64, Math.PI), iron); a.position.set(0, 2, 0); a.rotation.y = f * Math.PI / 2; a.translateZ(52); a.scale.y = .95; tower.add(a); }
  // platforms
  for (const [h, th] of [[57, 5], [116, 3.5], [276, 3]]) { const w = half(h) * 2 + 8; const p = new THREE.Mesh(new RoundedBoxGeometry(w, th, w, 2, .8), iron); p.position.y = h; tower.add(p);
    const rail = new THREE.Mesh(new THREE.BoxGeometry(w + 1, 1.2, w + 1), new THREE.MeshStandardMaterial({ color: 0x55483a, roughness: .7, transparent: true, opacity: .5 })); rail.position.y = h + th / 2 + .6; tower.add(rail); }
  // cross bracing between legs (X braces per face, three tiers)
  for (const [h0, h1] of [[8, 57], [57, 116], [116, 200], [200, 276]]) for (let f = 0; f < 4; f++) { const ang = f * Math.PI / 2;
    for (const s of [-1, 1]) { const w0 = half(h0), w1 = half(h1); const p0 = V(-s * w0, h0, w0), p1 = V(s * w1, h1, w1); const len = p0.distanceTo(p1);
      const b = new THREE.Mesh(new THREE.CylinderGeometry(.8, .8, len, 10), iron); b.position.copy(p0).add(p1).multiplyScalar(.5); b.lookAt(p1); b.rotateX(Math.PI / 2);
      const g = new THREE.Group(); g.add(b); g.rotation.y = ang; tower.add(g); } }
  const top = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 3, 300 - 276, 16), iron); top.position.y = 288; const ant = new THREE.Mesh(new THREE.CylinderGeometry(.35, .6, 30, 10), new THREE.MeshStandardMaterial({ color: 0xdedede, metalness: .6, roughness: .3 })); ant.position.y = 315;
  tower.add(top, ant); tower.position.set(TX, 0, -40); scene.add(shadowAll(tower)); }
const car = makeCar(0xc8442f); car.position.set(1.0, 0, -5.5); car.rotation.y = .2; scene.add(shadowAll(car));
const balls = [ball(.35, ['#f2f2f2', '#e8493b', '#f5c242', '#3a8de0'], 1), ball(.3, ['#ffffff', '#2fb36b'], 2), ball(.22, ['#f5c242', '#ffffff'], 3)];
const BP = [V(-1.3, .35, .7), V(1.3, .3, 1.0), V(-.9, .22, -2.2)]; balls.forEach((b, n) => { b.position.copy(BP[n]); scene.add(b); });
const J = K.J; // the flying Jeremy
// altitude marker: thin orange trail from the ground + glowing dot (Jeremy is a few pixels tall at 400 m)
const trail = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 1, 12), new THREE.MeshBasicMaterial({ color: ACCENT, toneMapped: false, transparent: true, opacity: .85 })); scene.add(trail);
const dotTex = canvasTex(128, 128, (ctx, w, h) => { const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.25, 'rgba(255,170,120,.95)'); g.addColorStop(.6, 'rgba(240,116,60,.35)'); g.addColorStop(1, 'rgba(240,116,60,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex;
const dot = new THREE.Sprite(new THREE.SpriteMaterial({ map: dotTex, transparent: true, depthWrite: false, toneMapped: false })); scene.add(dot);

// ---------------------------------------------------------------- B. "every day" set (speculation): Jeremy holding a bolted rail; car + boat lift off
const BX = 60; const J2 = makeJeremy2(); scene.add(J2); rimLight(J2);
const car2 = makeCar(0x3a6fd8); car2.position.set(BX + 1.6, 0, -4.6); car2.rotation.y = -.3; scene.add(shadowAll(car2));
const boat = new THREE.Group();
{ const shp = new THREE.Shape(); shp.moveTo(-2.2, .2); shp.quadraticCurveTo(-2.1, -.55, 0, -.6); shp.quadraticCurveTo(2.1, -.55, 2.4, .25); shp.lineTo(-2.2, .2);
  const hull = new THREE.Mesh(new THREE.ExtrudeGeometry(shp, { depth: 1.5, bevelEnabled: true, bevelSize: .12, bevelThickness: .12, bevelSegments: 4, curveSegments: 24 }), new THREE.MeshPhysicalMaterial({ color: 0xf3f1ec, roughness: .3, clearcoat: .8 })); hull.position.z = -.75;
  const stripe = new THREE.Mesh(new THREE.BoxGeometry(4.3, .1, 1.78), accentM); stripe.position.set(.1, .12, 0);
  const deck = new THREE.Mesh(new RoundedBoxGeometry(3.6, .08, 1.4, 2, .03), new THREE.MeshStandardMaterial({ color: 0x9b6b43, roughness: .7 })); deck.position.set(0, .2, 0);
  const trailer = new THREE.Mesh(new RoundedBoxGeometry(4.2, .12, .9, 2, .04), new THREE.MeshStandardMaterial({ color: 0x2a2b30, metalness: .7, roughness: .4 })); trailer.position.y = -.85;
  boat.add(hull, stripe, deck); boat.position.set(BX - .2, .9, -9.5); boat.rotation.y = .12; scene.add(shadowAll(boat));
  const tr = new THREE.Group(); tr.add(trailer); for (const x of [-1.2, 1.2]) for (const z of [-.5, .5]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(.28, .28, .2, 24), new THREE.MeshStandardMaterial({ color: 0x15161a, roughness: .8 })); w.rotation.x = Math.PI / 2; w.position.set(x, -.97 + .1, z); tr.add(w); }
  tr.position.copy(boat.position); tr.rotation.y = .12; scene.add(shadowAll(tr)); }
const balls2 = [ball(.35, ['#f2f2f2', '#e8493b', '#f5c242', '#3a8de0'], 4), ball(.25, ['#ffffff', '#7a4fd6'], 5)]; const BP2 = [V(BX - 1.5, .35, 1.0), V(BX + 1.5, .25, 1.0)]; balls2.forEach((b, n) => { b.position.copy(BP2[n]); scene.add(b); });
// bolted rail: two orange posts with a bar, base plates with bolts
const railG = new THREE.Group();
{ const postM = new THREE.MeshStandardMaterial({ color: ACCENT, roughness: .4, metalness: .3 });
  for (const x of [-.7, .7]) { const p = new THREE.Mesh(new THREE.CylinderGeometry(.05, .05, 2.4, 24), postM); p.position.set(x, 1.2, 0); const pl = new THREE.Mesh(new THREE.CylinderGeometry(.22, .22, .04, 32), steel); pl.position.set(x, .02, 0); railG.add(p, pl);
    for (let k = 0; k < 4; k++) { const b = new THREE.Mesh(new THREE.CylinderGeometry(.025, .025, .04, 12), steel); b.position.set(x + Math.cos(k * 1.57 + .78) * .15, .05, Math.sin(k * 1.57 + .78) * .15); railG.add(b); } }
  const bar = new THREE.Mesh(new THREE.CylinderGeometry(.045, .045, 1.5, 24), postM); bar.rotation.z = Math.PI / 2; bar.position.y = 2.4; railG.add(bar);
  railG.position.set(BX, 0, -.25); scene.add(shadowAll(railG)); }

// ---------------------------------------------------------------- C. the twist: a horseshoe magnet holding a steel ball up against the whole planet
const MX = BX + 9; const magG = new THREE.Group(); let held;
{ magG.add(plinth(1.6, 1.2, .9));
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, 1.5, 16), brass); pole.position.set(-.55, .9 + .75, 0);
  const arm = new THREE.Mesh(new THREE.CylinderGeometry(.025, .025, .6, 12), brass); arm.rotation.z = Math.PI / 2; arm.position.set(-.25, 2.4, 0);
  const red = new THREE.MeshPhysicalMaterial({ color: 0xc8281f, roughness: .3, clearcoat: .8 });
  const mag = new THREE.Group(); const hs = new THREE.Mesh(new THREE.TorusGeometry(.14, .055, 24, 64, Math.PI), red); hs.rotation.z = 0;
  const legL = new THREE.Mesh(new THREE.CylinderGeometry(.055, .055, .14, 24), red), legR = legL.clone(); legL.position.set(-.14, -.07, 0); legR.position.set(.14, -.07, 0);
  const tipL = new THREE.Mesh(new THREE.CylinderGeometry(.056, .056, .07, 24), steel), tipR = tipL.clone(); tipL.position.set(-.14, -.175, 0); tipR.position.set(.14, -.175, 0);
  mag.add(hs, legL, legR, tipL, tipR); mag.rotation.z = 0; mag.position.set(0, 2.3, 0);
  const hook = new THREE.Mesh(new THREE.CylinderGeometry(.008, .008, .08, 8), steel); hook.position.set(0, 2.4, 0);
  held = new THREE.Mesh(new THREE.SphereGeometry(.09, 48, 32), steel); held.position.set(0, 2.3 - .21 - .09, 0);
  const clips = new THREE.Group(); for (let k = 0; k < 3; k++) { const c = new THREE.Mesh(new THREE.TorusGeometry(.025, .005, 8, 24), steel); c.scale.y = 2; c.position.set(0, held.position.y - .1 - k * .1, 0); clips.add(c); }
  magG.add(pole, arm, hook, mag, held, clips); magG.position.set(MX, 0, -.2); scene.add(shadowAll(magG)); }
const J3 = makeJeremy2(); scene.add(J3); rimLight(J3);

// ---------------------------------------------------------------- timeline
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), endAt = T0[9] + 1.2;
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const tFlip = T0[1] + .75, t10 = T1[3] - .25, tPeak = T1[4] - .2, tCut = T1[5] - .3; // video times of: flip, gravity back, peak, cut before touchdown
const TCUT_TAU = TLAND - .25; // physics time at the cut (still ~13 m up: we never show the impact)
const tauAt = t => { if (t < tFlip) return 0; if (t < t10) return (t - tFlip) / (t10 - tFlip) * 10; if (t < tPeak) return 10 + (t - t10) / (tPeak - t10) * 4.1; return Math.min(TCUT_TAU, 14.1 + (t - tPeak) / (tCut - tPeak) * (TCUT_TAU - 14.1)); };
const sceneB = t => t >= tCut;
const tDay2 = T0[7] + .25; // second flip ("anything loose would lift off")

window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: total, name: 'room', gain: .1 }, { t0: tFlip, t1: tCut, name: 'wind', gain: .22 }],
  sfx: [{ t: tFlip - .1, name: 'swell', gain: .32 }, { t: tFlip, name: 'wind_gust', gain: .3 }, { t: t10, name: 'chime', gain: .26 }, { t: tPeak - .3, name: 'swell', gain: .22 }, { t: tCut - .25, name: 'glide', gain: .3 },
    { t: tDay2, name: 'wind_gust', gain: .26 }, { t: T1[7] - .2, name: 'clatter', gain: .25 }, { t: T0[8] - .7, name: 'glide', gain: .28 }, { t: T0[8] + 3.2, name: 'ding', gain: .22 }, { t: endAt, name: 'chime', gain: .3 }] };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';
const wp = new THREE.Vector3();

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), lt = t - T0[i], ld = T1[i] - T0[i];
  const tau = tauAt(t), [alt, vel] = simAt(tau), B = sceneB(t);
  // ---- A: everything loose rises with the same motion (small offsets so it reads as separate objects)
  const lift = k => Math.max(0, alt * k);
  J.visible = !B; J.position.set(0, lift(1), 0); J.scale.setScalar(.75); J.rotation.set(Math.sin(tau * .6) * .35 * clamp(tau), -.35 + tau * .25, Math.sin(tau * .45) * .25 * clamp(tau));
  J.pose({ expr: tau > 14.1 ? 'panic' : tau > 0 ? 'shocked' : 'happy', look: tau > 0 ? .3 : -.2, armL: tau > 0 ? 2.6 : .25, armR: tau > 0 ? 2.6 : .25, blink: (t % 2.7) < .1 });
  car.position.y = lift(.985); car.rotation.set(Math.sin(tau * .3) * .2 * clamp(tau), .2 + tau * .04, Math.sin(tau * .25) * .15 * clamp(tau)); car.visible = !B;
  balls.forEach((b, n) => { b.position.set(BP[n].x, BP[n].y + lift(1.01 + n * .006), BP[n].z); b.rotation.set(tau * (1 + n), tau * .7, 0); b.visible = !B; });
  // ---- camera framing as a smooth function of altitude (frame height ≈ .61·dist; Jeremy sits just below the HUD)
  let tgt, dist, yaw, pitch;
  const aS = alt; // already smooth (physics)
  if (!B) { dist = 12 + 4.3 * aS; tgt = V(-Math.min(1, aS / 150) * 18, 1.0 + .235 * (dist - 12), 0); yaw = -.25 + .03 * clamp(t / 20); pitch = .08 + .04 * (1 - clamp(aS / 40)); }
  else { // B -> C: one continuous glide
    const cK = eInOut(clamp((t - (T0[8] - .8)) / 1.6)); const c0 = [BX, 1.6, 17, -.1, .12], c1 = [MX + .25, 1.5, 10.6, -.36, .1];
    const c = c0.map((v, j) => lerp(v, c1[j], cK)); const dr = clamp(lt / Math.max(ld, 1)); tgt = V(c[0], c[1], 0); dist = c[2] * (1 - .03 * dr); yaw = c[3] + .03 * dr; pitch = c[4]; }
  orbit(tgt, dist, { yaw, pitch, fov: 34, lookUp: B ? .075 : .075 * (1 - clamp(aS / 30)) });
  shadowFit(B ? tgt : V(0, 0, 0), B ? 6 : Math.max(5, Math.min(60, 4 + aS * .2)));
  DOF.on = dist < 25; DOF.focus = dist; DOF.aperture = .5; DOF.maxR = 8;
  // altitude marker (screen-constant thickness)
  const mOn = !B && alt > 3 ? clamp((alt - 3) / 6) : 0; trail.visible = dot.visible = mOn > 0;
  trail.scale.set(dist * .0011, Math.max(.01, alt), dist * .0011); trail.position.set(0, alt / 2, 0); trail.material.opacity = .8 * mOn;
  dot.position.set(0, alt + 1, 0); dot.scale.setScalar(dist * .02); dot.material.opacity = mOn;
  // ---- B: "every day": a second flip lifts the car, boat and balls a few metres; Jeremy hangs on to the bolted rail
  const d2 = t < tDay2 ? 0 : t < T1[7] - .5 ? eOut(clamp((t - tDay2) / 2.4)) * 3.2 : 3.2 * (1 - eInOut(clamp((t - (T1[7] - .5)) / .45)));
  [J2, car2, boat, ...balls2].forEach(o => o.visible = B);
  J2.position.set(BX, Math.min(.35, d2 * .4), .05); J2.rotation.set(0, -.3, 0); J2.scale.setScalar(.75); J2.pose({ expr: d2 > .1 ? 'worried' : 'happy', look: -.3, armL: 2.9, armR: 2.9, blink: (t % 3.1) < .1 });
  car2.position.y = d2 * .45; car2.rotation.set(d2 * .04, -.3, d2 * .05); boat.position.y = .9 + d2 * .4; boat.rotation.set(d2 * .05, .12, -d2 * .04);
  balls2.forEach((b, n) => { b.position.set(BP2[n].x, BP2[n].y + d2 * (.55 + n * .1), BP2[n].z); b.rotation.x = t * .5; });
  J3.visible = B; J3.position.set(MX + .9, 0, -1.2); J3.rotation.set(0, -.6, 0); J3.scale.setScalar(.75); J3.pose({ expr: i >= 9 ? 'confused' : 'happy', look: -.6, armL: .25, armR: i === 8 ? 1.3 : i >= 9 ? 1.3 : .25, tilt: i >= 9 ? .1 : 0, blink: (t % 2.3) < .1 });
  held.position.x = Math.sin(t * 1.3) * .004;
  // ---- dip to black at the change of world (we never show the touchdown)
  $('v5fade').style.opacity = clamp(1 - Math.abs(t - tCut) / .3);
  // ---- tags (after orbit)
  const A = (t0, t1) => clamp((t - t0) / .35) * clamp((t1 - t) / .3);
  if (i === 0) tag3('JEREMY', '1.75 m', V(-1.05, 1.5, 0), A(.6, tFlip));
  if (!B && tau > 0) tag3(tau < 10 ? 'GRAVITY ↑ REVERSED' : 'GRAVITY BACK ↓', 'Jeremy · ' + Math.round(alt) + ' m up', V(0, alt + 1, 0).addScaledVector(V(0, 1, 0), dist * .03), A(tFlip + .6, tCut - .35));
  if (!B && aS > 120) tag3('EIFFEL TOWER', '330 m', V(TX, 336, -40), clamp((aS - 120) / 40) * A(T0[3] + .8, tCut - .35));
  if (i === 6) tag3('SPECULATION', 'bolted down = safe', V(BX - .7, 2.6, -.25), A(T0[6] + .9, T0[7] - .3));
  if (i === 7) tag3('SPECULATION', 'loose = airborne', V(BX - 1.2, 1.7 + d2 * .4, -9.5), A(T0[7] + .5, T1[7]));
  if (i === 8) tag3('FRIDGE MAGNET', 'beats the whole Earth', V(MX - .3, 1.0, .5), A(T0[8] + 2.6, T0[9] - .2));
  tagsEnd();
  // ---- HUD
  const endK = clamp((t - endAt) / .35), endIn = clamp((t - endAt - .35) / .45);
  let l1 = 'SECONDS SINCE THE FLIP', n1 = tau.toFixed(1) + ' s', l2 = 'GRAVITY', n2 = tau > 0 && tau < 10 ? 'Reversed' : 'Normal', l3 = 'ALTITUDE', val = Math.round(alt) + ' m';
  if (i === 2) { l3 = 'SPEED'; val = Math.round(Math.abs(vel)) + ' m/s'; }
  if (i === 5) { l3 = vel < 0 ? 'FALLING AT' : 'ALTITUDE'; val = vel < 0 ? Math.round(-vel * 3.6) + ' km/h' : Math.round(alt) + ' m'; }
  if (i === 4 && t > tPeak - .1) val = Math.round(alt) + ' m';
  if (i >= 6) { l1 = 'EVERY DAY'; n1 = i === 8 ? 'Real life' : 'Day 2, 3, 4…'; l2 = 'THIS PART IS'; n2 = i >= 8 ? 'FACT' : 'SPECULATION'; l3 = i === 6 ? 'PEOPLE HOLDING ON' : i === 7 ? 'ANYTHING LOOSE' : 'STRONGER FORCE'; val = i === 6 ? '8 billion' : i === 7 ? 'Airborne' : 'Magnetism'; }
  if (i === 9) { l1 = 'EVERY DAY'; n1 = 'Real life'; l2 = 'THIS PART IS'; n2 = 'FACT'; l3 = 'STRONGER FORCE'; val = 'Magnetism'; }
  const fadeIn = clamp(lt / .25);
  setHUD({ q: 'What if gravity <b>flipped</b> for 10 seconds a day?', qA: clamp((t - .2) / .4) * (1 - endK), l1, n1, l2, n2, l3, val,
    line: i === 0 ? '' : LN[i].show, lineA: fadeIn * clamp((T1[i] + .25 - t) / .2 + (i === 9 ? 9 : 0)), dataA: (1 - endK),
    end: 'What would <b>you</b><br>hold on to? 👇', endA: endIn });
  $('v5n2').style.color = n2 === 'FACT' || n2 === 'Normal' ? '#fff' : ACCENT;
  draw();
};
window.READY = true;
