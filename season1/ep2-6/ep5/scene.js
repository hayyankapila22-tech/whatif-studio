// Episode 5 — What if Jeremy's car never stopped accelerating?
import {
  THREE, RoundedBoxGeometry, scene, camera, draw, key, flash as flashLight, M, canvasTex, loadFont, text3d,
  makeJeremy, renderCaptions, clamp, prog, eOut, eInOut, eIn, lerp, rand, popS, floor
} from './engine.js';
import { setTitle, intro, counter, stageAt, keyframes, flash } from './hud.js';

await document.fonts.load('80px IDB'); await document.fonts.load('80px IDBo'); await document.fonts.load('40px IM');
await loadFont();

const TOTAL = 50;
setTitle('WHAT IF YOUR CAR NEVER STOPPED?', 'EP. 5');
const REEL = ['(x)', 'EARTH STOPPED', 'YOU DOUBLED 1¢', 'GRAVITY DOUBLED', 'YOU FELL THROUGH EARTH', '0 DISAPPEARED', 'YOUR CAR NEVER STOPPED?'];
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const look = new THREE.Vector3();
function setCam(p, l, roll = 0) { camera.position.copy(p); look.copy(l); camera.lookAt(look); camera.rotateZ(roll); }
function rbox(w, h, d, r, mat) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, r), mat); m.castShadow = m.receiveShadow = true; return m; }
function group(...k) { const g = new THREE.Group(); k.forEach(x => g.add(x)); scene.add(g); return g; }
const sceneBg = scene.background.clone(); const sceneFog = scene.fog;
const dm = new THREE.Object3D();

// ---------- the car (convertible, Jeremy driving) ----------
const paint = new THREE.MeshPhysicalMaterial({ color: 0xe8364e, metalness: .6, roughness: .22, clearcoat: 1, emissive: 0xff3300, emissiveIntensity: 0 });
const car = new THREE.Group();
{ const body = rbox(3.4, 0.7, 1.6, 0.28, paint); body.position.y = 0.62; const nose = rbox(1.2, 0.45, 1.5, 0.22, paint); nose.position.set(1.5, 0.5, 0);
  const wind = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.45, 1.4), new THREE.MeshPhysicalMaterial({ color: 0xaad8ff, transparent: true, opacity: .35, roughness: 0 })); wind.position.set(0.55, 1.15, 0); wind.rotation.z = -0.4;
  const spoiler = rbox(0.5, 0.08, 1.6, 0.03, M.dark); spoiler.position.set(-1.6, 1.25, 0); const sp1 = rbox(0.08, 0.3, 0.08, 0.02, M.dark); sp1.position.set(-1.6, 1.05, .6); const sp2 = sp1.clone(); sp2.position.z = -.6;
  car.add(body, nose, wind, spoiler, sp1, sp2);
  const tyre = new THREE.MeshStandardMaterial({ color: 0x111, roughness: .7 });
  car.wheels = [];
  for (const x of [-1.1, 1.2]) for (const z of [-0.78, 0.78]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.28, 28), tyre); w.rotation.x = Math.PI / 2; w.position.set(x, 0.38, z); const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.3, 6), M.chrome); hub.rotation.x = Math.PI / 2; hub.position.copy(w.position); car.add(w, hub); car.wheels.push(w, hub); }
  const tail = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.12, 1.3), new THREE.MeshBasicMaterial({ color: 0xff2030, toneMapped: false })); tail.position.set(-1.72, 0.75, 0); car.add(tail); }
car.traverse(o => { if (o.isMesh) o.castShadow = true; });
const J = makeJeremy(); J.scale.setScalar(0.55); J.position.set(-0.35, 0.35, 0); J.rotation.y = Math.PI / 2; car.add(J);
// sonic cone + heat flames
const cone = new THREE.Mesh(new THREE.ConeGeometry(2.6, 7, 48, 1, true), new THREE.MeshBasicMaterial({ color: 0xdff0ff, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
cone.rotation.z = Math.PI / 2; cone.position.set(-1.6, 0.8, 0); car.add(cone);
const flameM = new THREE.MeshBasicMaterial({ color: 0xff8a20, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false });
const flame = new THREE.Mesh(new THREE.ConeGeometry(1.0, 5, 32, 1, true), flameM); flame.rotation.z = Math.PI / 2; flame.position.set(-3.6, 0.7, 0); car.add(flame);
const shell = new THREE.Mesh(new THREE.SphereGeometry(2.4, 48, 32), new THREE.MeshBasicMaterial({ color: 0xff7a30, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false })); shell.scale.set(1.3, .6, .8); shell.position.set(0.6, 0.7, 0); car.add(shell);
scene.add(car);

// ---------- road ----------
const roadTex = canvasTex(256, 512, (ctx, w, h) => { ctx.fillStyle = '#23252e'; ctx.fillRect(0, 0, w, h); const r = rand(3); for (let i = 0; i < 900; i++) { ctx.fillStyle = `rgba(255,255,255,${r() * .06})`; ctx.fillRect(r() * w, r() * h, 2, 2); }
  ctx.fillStyle = '#f2f2f2'; ctx.fillRect(10, 0, 8, h); ctx.fillRect(w - 18, 0, 8, h); ctx.fillStyle = '#ffc444'; ctx.fillRect(w / 2 - 5, 0, 10, h * .5); });
roadTex.tex.wrapS = roadTex.tex.wrapT = THREE.RepeatWrapping; roadTex.tex.repeat.set(1, 40);
const road = new THREE.Mesh(new THREE.PlaneGeometry(8, 400), new THREE.MeshStandardMaterial({ map: roadTex.tex, roughness: .8 })); road.rotation.x = -Math.PI / 2; road.rotation.z = Math.PI / 2; road.position.y = 0.02; road.receiveShadow = true;
const POST = 40; const posts = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.06, 0.06, 1.4, 8), new THREE.MeshStandardMaterial({ color: 0xdfe3ee, emissive: 0xffffff, emissiveIntensity: .2 }), POST); posts.castShadow = true;
const STR = 120; const strM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .5, toneMapped: false });
const streaks = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.02, 0.02), strM, STR); streaks.frustumCulled = false;
const sP = []; { const r = rand(4); for (let i = 0; i < STR; i++) sP.push([r() * 60, .1 + r() * 4, -6 + r() * 10, .5 + r()]); }
const roadG = group(road, posts, streaks);

// ---------- space ----------
const earthTex = canvasTex(2048, 1024, (ctx, w, h) => { const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#1d4f9a'); g.addColorStop(.5, '#1565c0'); g.addColorStop(1, '#1d4f9a'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  const r = rand(23); const blob = (cx, cy, s, col) => { for (let i = 0; i < 70; i++) { ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(cx + (r() - .5) * s * 1.6, cy + (r() - .5) * s, s * (.15 + r() * .3), s * (.12 + r() * .25), r() * 3, 0, 7); ctx.fill(); } };
  [[330, 330, 260], [520, 640, 200], [1060, 330, 230], [1120, 600, 220], [1500, 380, 320], [1700, 700, 140], [1000, 900, 300]].forEach(([x, y, s]) => { blob(x, y, s, '#3f8a3c'); blob(x + 20, y + 10, s * .6, '#7a8b45'); });
  ctx.fillStyle = '#f2f6ff'; ctx.fillRect(0, 0, w, 50); ctx.fillRect(0, h - 70, w, 70); });
const earth = new THREE.Mesh(new THREE.SphereGeometry(60, 128, 96), new THREE.MeshStandardMaterial({ map: earthTex.tex, roughness: 1, metalness: 0, envMapIntensity: .2 }));
const atmo = new THREE.Mesh(new THREE.SphereGeometry(62.5, 96, 64), new THREE.MeshBasicMaterial({ color: 0x5ab0ff, transparent: true, opacity: .1, side: THREE.BackSide, blending: THREE.AdditiveBlending }));
const sun = new THREE.Mesh(new THREE.SphereGeometry(10, 48, 32), new THREE.MeshBasicMaterial({ color: 0xffe9a0, toneMapped: false }));
const sunL = new THREE.PointLight(0xfff0d0, 0, 400, 0);
const SN = 1400; const starPos = new Float32Array(SN * 3); { const r = rand(5); for (let i = 0; i < SN; i++) { starPos[i * 3] = (r() - .5) * 400; starPos[i * 3 + 1] = (r() - .5) * 300; starPos[i * 3 + 2] = (r() - .5) * 300; } }
const WARP = 260; const warpM = new THREE.MeshBasicMaterial({ color: 0xbfe0ff, transparent: true, opacity: .8, toneMapped: false });
const warp = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.05, 0.05), warpM, WARP); warp.frustumCulled = false;
const wP = []; { const r = rand(8); for (let i = 0; i < WARP; i++) { const a = r() * 6.28, d = 3 + r() * 30; wP.push([r() * 300, Math.cos(a) * d, Math.sin(a) * d, .5 + r()]); } }
const spaceG = group(earth, atmo, sun, sunL, warp);

// ---------- relativity props ----------
const clockFace = canvasTex(512, 512, (ctx, w, h) => { ctx.fillStyle = '#f5f2ea'; ctx.beginPath(); ctx.arc(w / 2, h / 2, w / 2 - 6, 0, 7); ctx.fill(); ctx.strokeStyle = '#1a1d2a'; ctx.lineWidth = 14; ctx.stroke();
  ctx.fillStyle = '#1a1d2a'; ctx.font = '60px IDB'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; for (let k = 1; k <= 12; k++) { const a = k / 12 * 6.283 - Math.PI / 2; ctx.fillText(k, w / 2 + Math.cos(a) * 190, h / 2 + Math.sin(a) * 190); } });
const clockG = new THREE.Group(); { const disc = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 0.2, 64), [M.gold, new THREE.MeshBasicMaterial({ map: clockFace.tex }), M.gold]); disc.rotation.x = Math.PI / 2; clockG.add(disc);
  const hand = (len, wdt) => { const p = new THREE.Group(); const m = new THREE.Mesh(new THREE.BoxGeometry(wdt, len, 0.04), M.dark); m.position.y = len / 2; p.add(m); p.position.z = 0.13; clockG.add(p); return p; }; clockG.hour = hand(0.6, 0.08); clockG.min = hand(0.95, 0.05); }
scene.add(clockG);
const yearSign = new THREE.Group(); scene.add(yearSign);

// ---------- CTA ----------
const ctaG = group();

// =================== TIMELINE ===================
const C = 1079252849;
const st = [
  { t: 3.0, v: 0, cap: 'Jeremy floors it… and NEVER stops.', hi: ['NEVER'], mode: 'road' },
  { t: 5.6, v: 120, cap: '120 km/h: highway speed.', hi: ['highway'], mode: 'road' },
  { t: 8.2, v: 320, cap: '320 km/h: bullet-train speed.', hi: ['bullet-train'], mode: 'road' },
  { t: 10.8, v: 1235, cap: '1,235 km/h: SONIC BOOM.', hi: ['SONIC', 'BOOM'], mode: 'road' },
  { t: 13.4, v: 3400, cap: '3,400 km/h: faster than a rifle bullet.', hi: ['rifle', 'bullet'], mode: 'road' },
  { t: 16.0, v: 6200, cap: 'Mach 5: the air heats the car RED-HOT.', hi: ['RED-HOT'], mode: 'road' },
  { t: 18.6, v: 28000, cap: '28,000 km/h: orbital speed. The road falls away.', hi: ['orbital'], mode: 'orbit' },
  { t: 21.2, v: 40320, cap: '40,320 km/h: ESCAPE VELOCITY. Bye, Earth.', hi: ['ESCAPE', 'VELOCITY'], mode: 'space' },
  { t: 23.8, v: 107000, cap: 'Faster than Earth flies around the Sun.', hi: ['Sun'], mode: 'space' },
  { t: 26.4, v: 692000, cap: 'Faster than anything humans ever built.', hi: ['anything'], mode: 'space' },
  { t: 29.4, v: C * 0.9999, cap: 'LIGHT SPEED?', hi: ['LIGHT', 'SPEED'], mode: 'warp' },
  { t: 32.0, v: C * 0.9999, cap: 'Physics says NO: it’d take infinite energy.', hi: ['infinite'], mode: 'warp', err: true },
  { t: 35.0, v: C * 0.9999, cap: 'But at 99.99% of light speed…', hi: ['99.99%'], mode: 'time' },
  { t: 37.6, v: C * 0.9999, cap: '…time slows down for Jeremy.', hi: ['time', 'slows'], mode: 'time' },
  { t: 40.2, v: C * 0.9999, cap: '1 year in the car = 70 years on Earth.', hi: ['70', 'years'], mode: 'time', years: true },
  { t: 43.2, v: C * 0.9999, cap: 'He gets home… in 2096.', hi: ['2096'], mode: 'home', years: true },
  { t: 46.0, v: 0, cap: 'Would you take the ride?', hi: ['ride'], mode: 'cta' },
];
const vKF = []; st.forEach((s, i) => { if (i > 0 && s.v !== st[i - 1].v && i < 16) vKF.push([s.t - (i === 10 ? 2.2 : 1.2), st[i - 1].v]); vKF.push([s.t, s.v]); });
const speedAt = t => t >= 46 ? C * 0.9999 : keyframes(vKF.filter(k => k[0] < 46), t, x => x * x);
const sevV = v => v < 300 ? 0 : v < 1235 ? 1 : v < 6000 ? 2 : v < 40320 ? 3 : v < 692000 ? 4 : 5;
const yearKF = [[40.2, 2026], [42.6, 2096]];

window.renderAt = (T) => {
  flashLight.intensity = 0; flash(0); document.getElementById('small').textContent = ''; document.querySelector('canvas').style.filter = ''; document.querySelector('canvas').style.transform = '';
  intro(T, REEL, 3.0);
  const { i, lt, s } = stageAt(st, T);
  const mode = T < 3 ? 'intro' : s.mode;
  const v = speedAt(T);
  const stageLook = mode === 'intro' || mode === 'cta' || mode === 'home';
  floor.visible = stageLook; scene.fog = stageLook ? sceneFog : null;
  roadG.visible = mode === 'road'; spaceG.visible = ['orbit', 'space', 'warp', 'time'].includes(mode); clockG.visible = mode === 'time'; yearSign.visible = mode === 'home';
  scene.background = mode === 'road' ? new THREE.Color(0x0b1028) : stageLook ? sceneBg : new THREE.Color(0x000004);
  car.visible = mode !== 'intro'; car.position.set(0, 0, 0); car.rotation.set(0, 0, 0);
  paint.emissiveIntensity = 0; cone.material.opacity = 0; flameM.opacity = 0; shell.material.opacity = 0;
  J.pose({ expr: 'happy', armL: 0.4, armR: 0.4 });

  if (mode === 'intro') setCam(V(0, 3.0, 9), V(0, 2.4, 0));
  const k = Math.log10(Math.max(1, v)) / 6; // 0..1 visual speed
  if (mode === 'road') {
    const vis = Math.min(1, Math.log10(1 + v) / Math.log10(6200));
    const scroll = keyframes([[3, 0], [8, 3], [13, 14], [18.6, 40]], T, x => x * x);
    roadTex.tex.offset.y = -scroll * 10;
    car.wheels.forEach(w => w.rotation.y = -scroll * 40);
    for (let n = 0; n < POST; n++) { const x = (((n * 6 - scroll * 60) % 240) + 240) % 240 - 120; dm.position.set(x, 0.7, n % 2 ? 4.4 : -4.4); dm.rotation.set(0, 0, 0); dm.scale.setScalar(1); dm.updateMatrix(); posts.setMatrixAt(n, dm.matrix); } posts.instanceMatrix.needsUpdate = true;
    for (let n = 0; n < STR; n++) { const p = sP[n]; const x = ((p[0] - scroll * 90 * p[3]) % 60 + 60) % 60 - 30; dm.position.set(x, p[1], p[2]); dm.scale.set(.3 + vis * 6, 1, 1); dm.rotation.set(0, 0, 0); dm.updateMatrix(); streaks.setMatrixAt(n, dm.matrix); } streaks.instanceMatrix.needsUpdate = true; strM.opacity = vis * .6;
    cone.material.opacity = v >= 1235 ? .12 + .05 * Math.sin(T * 30) : 0; cone.scale.set(1, 1, 1);
    if (v >= 1235 && T < 11.2) flash(.5 * (1 - (T - 10.8) / .4));
    const heat = clamp((v - 3400) / 2800); paint.emissiveIntensity = heat * 1.6; shell.material.opacity = heat * .35; flameM.opacity = heat * .6;
    const sh = (Math.random() - .5) * .05 * vis;
    car.position.y = Math.abs(Math.sin(T * 30)) * .02 * vis;
    J.pose({ expr: v < 150 ? 'happy' : v < 1235 ? 'shocked' : 'panic', armL: v < 300 ? .5 : 2.6, armR: v < 300 ? .5 : 2.6, sweatK: heat > 0 ? T : 0, look: .3 });
    setCam(V(lerp(6.5, 4.8, vis) + sh, 2.7 + sh, 11 - vis * 1.2), V(0.3, 1.1, 0), -0.05 + sh);
  }
  if (mode === 'orbit') { // car lifts off the curving Earth
    earth.position.set(0, -60, 0); atmo.position.copy(earth.position); earth.rotation.set(Math.PI / 2 - 0.3, 0, T * .05); sun.visible = false; sunL.intensity = 0; warp.visible = false;
    const up = eInOut(prog(lt, 0.3, 2.6)); car.position.set(0, 0.2 + up * 3.5, 0); car.rotation.z = up * .2;
    paint.emissiveIntensity = 1.6 * (1 - up); shell.material.opacity = .35 * (1 - up);
    J.pose({ expr: 'shocked', armL: 2.6, armR: 2.6, look: -.5 });
    setCam(V(lerp(6, 10, up), lerp(3, 5.5, up), lerp(10, 14, up)), V(0, up * 2.4, 0));
    key.intensity = 1.2;
  }
  if (mode === 'space' || mode === 'warp' || mode === 'time') {
    sun.visible = s.t === 23.8 || s.t === 26.4; sunL.intensity = sun.visible ? 3 : 0;
    const away = T - 21.2; earth.position.set(-20 - away * 18, -40 - away * 4, -30 - away * 30); atmo.position.copy(earth.position);
    sun.position.set(lerp(80, -120, prog(T, 23.8, 29.4)), 20, -80); sunL.position.copy(sun.position);
    warp.visible = true; const wk = mode === 'space' ? .25 + .15 * (i - 7) : mode === 'warp' ? 1 : .6;
    for (let n = 0; n < WARP; n++) { const p = wP[n]; const x = ((p[0] - T * 120 * wk * p[3]) % 300 + 300) % 300 - 150; dm.position.set(x, p[1], p[2]); dm.scale.set(1 + wk * 30, 1, 1); dm.rotation.set(0, 0, 0); dm.updateMatrix(); warp.setMatrixAt(n, dm.matrix); } warp.instanceMatrix.needsUpdate = true;
    warpM.color.set(mode === 'warp' ? 0xd0e8ff : 0xffffff); warpM.opacity = mode === 'time' ? .5 : .85;
    car.position.set(0, 0, 0); car.rotation.set(Math.sin(T) * .05, Math.sin(T * .7) * .1, Math.sin(T * .9) * .05);
    J.pose({ expr: mode === 'warp' ? 'panic' : mode === 'time' ? 'confused' : 'shocked', armL: mode === 'time' ? 1 : 2.6, armR: mode === 'time' ? 1.6 : 2.6, look: .2, sweatK: mode === 'warp' ? T : 0 });
    const sh = mode === 'warp' ? (Math.random() - .5) * .3 : 0;
    if (mode === 'time') {
      clockG.position.set(0, 3.6, -1); clockG.scale.setScalar(popS(T, 35.0, .4)); clockG.rotation.set(0, Math.sin(T * .6) * .25, 0);
      const slow = T < 37.6 ? 1 : 1 / 70; clockG.min.rotation.z = -((T - 35) * (T < 37.6 ? 2.5 : 0.04)); clockG.hour.rotation.z = clockG.min.rotation.z / 12;
      setCam(V(lerp(3, -2, eInOut(prog(T, 35, 43.2))), 2.6, 11.5), V(0, 2.2, 0));
    } else setCam(V(lerp(5, 3, k) + sh, 2.4 + sh, 10 + sh), V(0, 0.9, 0), sh * .1);
    if (s.err) { document.querySelector('canvas').style.filter = Math.floor(T * 12) % 3 === 0 ? 'hue-rotate(160deg) saturate(2)' : ''; document.querySelector('canvas').style.transform = `translateX(${(Math.random() - .5) * 30}px)`; if (lt < .3) flash(.6 * (1 - lt / .3)); }
    if (mode === 'warp' && lt < .25 && !s.err) flash(.8 * (1 - lt / .25));
  }
  if (mode === 'home') {
    yearSign.clear(); const yr = text3d('2096', 1.2, M.goldGlow); yr.position.set(0, 3.5, -2.5); yearSign.add(yr); yearSign.scale.setScalar(popS(lt, .2, .5)); yearSign.rotation.y = Math.sin(T) * .15;
    car.position.set(1.4, 0, 0.5); car.rotation.y = -0.5; J.pose({ expr: 'shocked', armL: 2.4, armR: 2.4, sweatK: lt });
    setCam(V(-1, 2.8, 11), V(0.4, 2.6, 0));
  }
  if (mode === 'cta') {
    car.position.set(0.6, 0, 0.6); car.rotation.y = -0.6 + Math.sin(T * .5) * .1;
    J.pose({ expr: 'happy', armL: .4, armR: 2.5 + Math.sin(T * 10) * .3, look: .8 });
    setCam(V(lerp(-.6, .6, eInOut(prog(lt, 0, 4))), 2.6, 9.4), V(0.4, 1.2, 0));
    const sm = document.getElementById('small'); sm.style.top = '1525px'; sm.style.opacity = clamp((lt - 1.2) / .4); sm.textContent = 'Purely hypothetical · for entertainment';
  }
  // counter: speed, then light-speed %, then calendar
  if (T >= 40.2 && T < 46) counter(T, { on: true, valueAt: t => keyframes(yearKF, t), fmt: v => 'YEAR ' + Math.round(v), label: 'ON EARTH', sub: 'Jeremy aged 1 year', sev: 5 });
  else if (T >= 29.4 && T < 40.2) { const err = T >= 32.0 && T < 35.0;
    counter(T, { on: true, valueAt: t => t < 32 ? speedAt(t) : C * 0.9999, fmt: x => err && Math.floor(T * 10) % 4 === 0 ? 'ERROR' : (T >= 35 ? '99.99% LIGHT SPEED' : Math.round(x).toLocaleString('en-US') + ' km/h'), label: 'SPEED', sub: T >= 35 ? 'time runs 70× slower' : 'light: 1,079,252,849 km/h', sev: 5, shake: err ? 1 : 0.3 }); }
  else counter(T, { on: T >= 3.0 && T < 46, valueAt: t => speedAt(Math.max(3, t)), fmt: x => Math.round(x).toLocaleString('en-US') + ' km/h', label: 'SPEED', sub: '', sev: sevV(v), shake: v >= 6000 ? .4 : 0 });
  const caps = [];
  if (T >= 3.0) { const end = i + 1 < st.length ? st[i + 1].t - 0.15 : TOTAL; caps.push({ t0: s.t + 0.05, t1: end, text: s.cap, y: 1330, size: s.cap.length > 32 ? 66 : 80, g: s.hi.map(x => x.replace(/[,.?!…:]/g, '')) }); }
  if (mode === 'cta') caps.push({ t0: s.t + 1.0, t1: TOTAL, text: 'Comment below ↓', y: 1440, size: 66, g: ['below', '↓'] });
  renderCaptions(caps, T);
  document.getElementById('fill').style.width = (clamp(T / TOTAL) * 100) + '%';
  draw();
};
window.TOTAL = TOTAL;
window.READY = true;
