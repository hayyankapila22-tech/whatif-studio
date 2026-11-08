// Episode 4 — What if Earth stopped spinning?
import {
  THREE, RoundedBoxGeometry, scene, camera, draw, key, flash as flashLight, M, canvasTex, loadFont, text3d,
  makeJeremy, renderCaptions, clamp, prog, eOut, eInOut, eIn, lerp, rand, popS, floor
} from './engine.js';
import { setTitle, intro, counter, stageAt, keyframes, flash } from './hud.js';

await document.fonts.load('80px IDB'); await document.fonts.load('80px IDBo'); await document.fonts.load('40px IM');
await loadFont();

const TOTAL = 48;
setTitle('WHAT IF EARTH STOPPED SPINNING?', 'EP. 4');
const REEL = ['(x)', 'YOU DOUBLED 1¢', 'GRAVITY DOUBLED', '0 DISAPPEARED', 'THE MOON VANISHED', 'YOU FELL THROUGH EARTH', 'EARTH STOPPED SPINNING?'];
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const look = new THREE.Vector3();
function setCam(p, l, roll = 0) { camera.position.copy(p); look.copy(l); camera.lookAt(look); camera.rotateZ(roll); }
function rbox(w, h, d, r, mat) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, r), mat); m.castShadow = m.receiveShadow = true; return m; }
function group(...k) { const g = new THREE.Group(); k.forEach(x => g.add(x)); scene.add(g); return g; }
const J = makeJeremy(); const jPivot = new THREE.Group(); jPivot.add(J); scene.add(jPivot);
const sceneBg = scene.background.clone(); const sceneFog = scene.fog;
const dm = new THREE.Object3D();

// ---------- globe ----------
function earthCanvas(superK) {
  return canvasTex(2048, 1024, (ctx, w, h) => {
    const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#1d4f9a'); g.addColorStop(.5, '#1565c0'); g.addColorStop(1, '#1d4f9a'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    const r = rand(23); const blob = (cx, cy, s, col) => { for (let i = 0; i < 70; i++) { ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(cx + (r() - .5) * s * 1.6, cy + (r() - .5) * s, s * (.15 + r() * .3), s * (.12 + r() * .25), r() * 3, 0, 7); ctx.fill(); } };
    if (!superK) { [[330, 330, 260], [520, 640, 200], [1060, 330, 230], [1120, 600, 220], [1500, 380, 320], [1700, 700, 140], [1000, 900, 300]].forEach(([x, y, s]) => { blob(x, y, s, '#3f8a3c'); blob(x + 20, y + 10, s * .6, '#7a8b45'); }); ctx.fillStyle = '#f2f6ff'; ctx.fillRect(0, 0, w, 50); ctx.fillRect(0, h - 70, w, 70); }
    else { // one continent wrapping the equator, oceans at the poles
      const band = ctx.createLinearGradient(0, h * .22, 0, h * .78); band.addColorStop(0, '#6e8f45'); band.addColorStop(.3, '#a8915a'); band.addColorStop(.5, '#c9a86a'); band.addColorStop(.7, '#a8915a'); band.addColorStop(1, '#6e8f45');
      ctx.fillStyle = band; ctx.beginPath(); ctx.moveTo(0, h * .28); for (let x = 0; x <= w; x += 32) ctx.lineTo(x, h * .26 + Math.sin(x * .011) * 26 + (r() - .5) * 18); for (let x = w; x >= 0; x -= 32) ctx.lineTo(x, h * .74 + Math.sin(x * .013 + 2) * 26 + (r() - .5) * 18); ctx.fill();
      for (let i = 0; i < 40; i++) blob(r() * w, h * (.4 + r() * .2), 60, 'rgba(160,120,70,.5)');
    }
  });
}
const ER = 6;
const earth = new THREE.Mesh(new THREE.SphereGeometry(ER, 96, 64), new THREE.MeshStandardMaterial({ map: earthCanvas(false).tex, roughness: .7 }));
const superE = new THREE.Mesh(new THREE.SphereGeometry(ER * 1.002, 96, 64), new THREE.MeshStandardMaterial({ map: earthCanvas(true).tex, roughness: .7, transparent: true, opacity: 0 }));
const cloudTex = canvasTex(2048, 1024, (ctx, w, h) => { const r = rand(77); for (let i = 0; i < 150; i++) { ctx.fillStyle = `rgba(255,255,255,${.12 + r() * .3})`; ctx.beginPath(); ctx.ellipse(r() * w, h * (.15 + r() * .7), 30 + r() * 120, 10 + r() * 30, (r() - .5) * .3, 0, 7); ctx.fill(); } });
const clouds = new THREE.Mesh(new THREE.SphereGeometry(ER * 1.03, 96, 64), new THREE.MeshStandardMaterial({ map: cloudTex.tex, transparent: true, depthWrite: false, roughness: 1 }));
const atmo = new THREE.Mesh(new THREE.SphereGeometry(ER * 1.07, 64, 48), new THREE.MeshBasicMaterial({ color: 0x5ab0ff, transparent: true, opacity: .15, side: THREE.BackSide, blending: THREE.AdditiveBlending }));
const axisLine = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, ER * 2.6, 8), new THREE.MeshBasicMaterial({ color: 0xffc444, toneMapped: false }));
const stars = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute((() => { const r = rand(5), a = []; for (let i = 0; i < 2500; i++) { const th = r() * 6.283, ph = Math.acos(2 * r() - 1), d = 300; a.push(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d, Math.sin(ph) * Math.sin(th) * d); } return a; })(), 3)), new THREE.PointsMaterial({ color: 0xffffff, size: 1.2, sizeAttenuation: false }));
const sunLight = new THREE.DirectionalLight(0xfff4e0, 2.2); sunLight.position.set(-20, 6, 12);
const globeSpin = new THREE.Group(); globeSpin.add(earth, superE, clouds); globeSpin.rotation.z = 0.41;
const globeG = group(globeSpin, atmo, axisLine, stars, sunLight);

// ---------- wind set ----------
const poleM = new THREE.MeshStandardMaterial({ color: 0x9aa3b8, metalness: .8, roughness: .3 });
const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 3.4, 16), poleM); pole.position.set(-0.9, 1.7, 0); pole.castShadow = true;
const lamp = rbox(0.5, 0.18, 0.3, 0.06, poleM); lamp.position.set(-0.75, 3.4, 0);
const STR = 160; const strM = new THREE.MeshBasicMaterial({ color: 0xdfe8ff, transparent: true, opacity: .55, toneMapped: false });
const streaks = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.02, 0.02), strM, STR); streaks.frustumCulled = false;
const sP = []; { const r = rand(4); for (let i = 0; i < STR; i++) sP.push([r() * 30, r() * 6, -6 + r() * 9, .5 + r()]); }
const debM = [new THREE.MeshStandardMaterial({ color: 0xc8a06a, roughness: .7 }), new THREE.MeshStandardMaterial({ color: 0x3f8a3c, roughness: .7 }), new THREE.MeshStandardMaterial({ color: 0xe8364e, roughness: .5 }), M.white];
const DEB = 40; const debris = []; { const r = rand(9); for (let i = 0; i < DEB; i++) { const kind = i % 4; const geo = kind === 0 ? new THREE.BoxGeometry(.4, .3, .3) : kind === 1 ? new THREE.ConeGeometry(.25, .6, 8) : kind === 2 ? new THREE.BoxGeometry(.6, .05, .4) : new THREE.SphereGeometry(.18, 12, 8);
  const m = new THREE.Mesh(geo, debM[kind]); m.castShadow = true; m.userData = { x0: -14 - r() * 12, y: .3 + r() * 4, z: -3 + r() * 5, sp: .7 + r() * .6, rot: r() * 9, ph: r() * 30 }; debris.push(m); } }
const car = new THREE.Group(); { const red = new THREE.MeshPhysicalMaterial({ color: 0x3a7bff, metalness: .5, roughness: .25, clearcoat: 1 }); const body = rbox(2.2, .55, 1.0, .18, red); body.position.y = .45; const cab = rbox(1.1, .45, .9, .16, new THREE.MeshPhysicalMaterial({ color: 0x223, roughness: .05, clearcoat: 1 })); cab.position.set(-.1, .9, 0); car.add(body, cab);
  for (const x of [-.7, .7]) for (const z of [-.5, .5]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(.22, .22, .18, 20), new THREE.MeshStandardMaterial({ color: 0x111 })); w.rotation.x = Math.PI / 2; w.position.set(x, .22, z); car.add(w); } }
const windG = group(pole, lamp, streaks, ...debris, car);

// ---------- tsunami ----------
const city = new THREE.Group(); { const r = rand(17); const winTex = canvasTex(128, 256, (ctx, w, h) => { ctx.fillStyle = '#1a2040'; ctx.fillRect(0, 0, w, h); for (let y = 6; y < h; y += 16) for (let x = 6; x < w; x += 16) { ctx.fillStyle = r() > .45 ? '#ffd98a' : '#2a3366'; ctx.fillRect(x, y, 8, 9); } }).tex;
  const bm = new THREE.MeshStandardMaterial({ color: 0x8890b0, map: winTex, emissive: 0xffffff, emissiveMap: winTex, emissiveIntensity: .4, roughness: .4 });
  for (let i = 0; i < 40; i++) { const h = 1.5 + r() * 6, w = 1 + r() * 1.5; const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, w), bm); b.position.set(-2 + r() * 16, h / 2, -10 + r() * 12); b.castShadow = b.receiveShadow = true; city.add(b); } }
const waveGeo = new THREE.PlaneGeometry(60, 30, 120, 60); const waveBase = waveGeo.attributes.position.array.slice();
const waveM = new THREE.MeshPhysicalMaterial({ color: 0x1a6fb0, roughness: .15, clearcoat: 1, side: THREE.DoubleSide, emissive: 0x0a3060, emissiveIntensity: .3 });
const wave = new THREE.Mesh(waveGeo, waveM); wave.rotation.x = -Math.PI / 2;
const foam = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 60, 16, 1), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .9 })); foam.rotation.x = Math.PI / 2;
const tsuG = group(city, wave, foam);

// ---------- sun / night ----------
const sunBall = new THREE.Mesh(new THREE.SphereGeometry(3, 48, 32), new THREE.MeshBasicMaterial({ color: 0xffe08a, toneMapped: false }));
const sunGlow = new THREE.PointLight(0xffc860, 400, 80);
const dryM = new THREE.MeshStandardMaterial({ color: 0xb58a55, roughness: .9 });
const ground = new THREE.Mesh(new THREE.CircleGeometry(40, 64), new THREE.MeshStandardMaterial({ roughness: .95, map: canvasTex(1024, 1024, (ctx, w, h) => { ctx.fillStyle = '#c49a64'; ctx.fillRect(0, 0, w, h); ctx.strokeStyle = 'rgba(70,40,20,.55)'; ctx.lineWidth = 3; const r = rand(2); for (let i = 0; i < 160; i++) { ctx.beginPath(); let x = r() * w, y = r() * h; ctx.moveTo(x, y); for (let k = 0; k < 5; k++) { x += (r() - .5) * 90; y += (r() - .5) * 90; ctx.lineTo(x, y); } ctx.stroke(); } }).tex }));
ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; ground.position.y = 0.01;
const nightStars = stars.clone();
const sunG = group(sunBall, sunGlow, ground, nightStars);

// =================== TIMELINE ===================
const st = [
  { t: 3.0, w: 0, cap: 'Earth suddenly STOPS spinning.', hi: ['STOPS'], mode: 'globe' },
  { t: 5.6, w: 60, cap: 'But the air keeps moving.', hi: ['air'], mode: 'wind' },
  { t: 8.2, w: 120, cap: '120 km/h: hurricane-force winds.', hi: ['hurricane-force'], mode: 'wind' },
  { t: 10.8, w: 320, cap: '320 km/h: like the worst tornadoes.', hi: ['worst', 'tornadoes'], mode: 'wind' },
  { t: 13.4, w: 408, cap: '408 km/h: beats the fastest gust EVER.', hi: ['EVER'], mode: 'wind' },
  { t: 16.0, w: 1235, cap: '1,235 km/h: FASTER THAN SOUND.', hi: ['SOUND'], mode: 'wind' },
  { t: 18.6, w: 1670, cap: '1,670 km/h at the equator.', hi: ['1670'], mode: 'wind' },
  { t: 21.2, w: 1670, cap: 'Anything not bolted down flies east.', hi: ['flies', 'east'], mode: 'wind' },
  { t: 23.8, w: 1670, cap: 'The oceans keep moving too: MEGA-TSUNAMIS.', hi: ['MEGA-TSUNAMIS'], mode: 'tsunami' },
  { t: 26.8, w: 1670, cap: 'And then it gets weirder…', hi: ['weirder'], mode: 'globe', day: true },
  { t: 29.4, w: 1670, cap: 'With no spin, ONE day lasts a whole YEAR.', hi: ['YEAR'], mode: 'globe', day: true },
  { t: 32.4, w: 1670, cap: '6 months of nonstop sun…', hi: ['sun'], mode: 'sun', day: true },
  { t: 35.0, w: 1670, cap: '…then 6 months of night.', hi: ['night'], mode: 'night', day: true },
  { t: 37.6, w: 1670, cap: 'The oceans drain toward the poles…', hi: ['poles'], mode: 'globe', day: true, morph: true },
  { t: 40.4, w: 1670, cap: '…leaving ONE supercontinent around the middle.', hi: ['ONE', 'supercontinent'], mode: 'globe', day: true, morph: true },
  { t: 43.4, w: 1670, cap: 'Where would you hide?', hi: ['hide'], mode: 'cta', day: true },
];
const windKF = []; st.forEach((s, i) => { if (i > 0 && s.w !== st[i - 1].w) windKF.push([s.t - 1.2, st[i - 1].w]); windKF.push([s.t, s.w]); });
const windAt = t => keyframes(windKF, t);
const dayKF = [[0, 24], [26.8, 24], [29.4, 8766]];
const sevW = w => w < 100 ? 0 : w < 300 ? 1 : w < 408 ? 2 : w < 1235 ? 3 : w < 1670 ? 4 : 5;

window.renderAt = (T) => {
  flashLight.intensity = 0; flash(0); document.getElementById('small').textContent = '';
  intro(T, REEL, 3.0);
  const { i, lt, s } = stageAt(st, T);
  const mode = T < 3 ? 'intro' : s.mode;
  const w = windAt(T);
  const onStage = mode === 'intro' || mode === 'wind' || mode === 'cta';
  floor.visible = onStage; scene.fog = onStage ? sceneFog : null;
  scene.background = mode === 'sun' ? new THREE.Color(0xffb366) : mode === 'night' ? new THREE.Color(0x02030a) : onStage ? sceneBg : new THREE.Color(0x01020a);
  key.intensity = mode === 'night' ? 0.15 : mode === 'globe' ? 0.4 : 2.0;
  globeG.visible = mode === 'globe'; windG.visible = mode === 'wind'; tsuG.visible = mode === 'tsunami'; sunG.visible = mode === 'sun' || mode === 'night';
  jPivot.visible = mode === 'wind' || mode === 'sun' || mode === 'night' || mode === 'cta';
  jPivot.rotation.set(0, 0, 0); jPivot.position.set(0, 0, 0); J.position.set(0, 0, 0); J.rotation.set(0, 0, 0); J.scale.setScalar(1);

  if (mode === 'intro') setCam(V(0, 3.0, 9), V(0, 2.4, 0));
  if (mode === 'globe') {
    // spins fast until it stops at 3.6s; clouds keep drifting a little after
    const spinT = Math.min(T, 3.6); globeSpin.children[0].rotation.y = spinT * 2.2; superE.rotation.y = earth.rotation.y;
    clouds.rotation.y = earth.rotation.y + Math.max(0, Math.min(T, 8) - 3.6) * 0.25;
    superE.material.opacity = s.morph ? (s.t === 37.6 ? eInOut(prog(lt, .4, 2.6)) : 1) : 0;
    clouds.material.opacity = s.morph ? 1 - superE.material.opacity * .85 : 1;
    stars.rotation.y = T * .01;
    if (s.t === 3.0) { const k = eInOut(prog(lt, 0, 2.6)); setCam(V(0, 2, lerp(28, 22, k)), V(0, 0, 0), T < 3.6 ? 0 : (lt < 1 ? Math.sin(T * 60) * .01 * (1 - lt) : 0)); if (lt > 0.6 && lt < 0.85) flash(.35 * (1 - (lt - .6) / .25)); }
    else { const k = eInOut(prog(lt, 0, 3)); setCam(V(lerp(-4, 4, k), lerp(4, 2, k), lerp(28, 26, k)), V(0, 0, 0)); }
    sunLight.intensity = s.day ? 2.4 : 2.2; axisLine.visible = false; sunLight.position.set(-20, 4, s.day ? 6 : 12);
  }
  if (mode === 'wind') {
    const k = clamp(w / 1670); const letGo = s.t === 21.2;
    for (let n = 0; n < STR; n++) { const p = sP[n]; const len = .5 + k * 4; const x = ((p[0] + T * (4 + 60 * k) * p[3]) % 30) - 15; dm.position.set(x, p[1], p[2]); dm.scale.set(len, 1, 1); dm.rotation.set(0, 0, 0); dm.updateMatrix(); streaks.setMatrixAt(n, dm.matrix); }
    streaks.instanceMatrix.needsUpdate = true; strM.opacity = .15 + .6 * k; streaks.count = Math.floor(30 + 130 * k);
    debris.forEach((d, n) => { const u = d.userData; d.visible = k > 0.05 && n < 8 + 32 * k; const x = ((u.ph + T * (3 + 30 * k) * u.sp) % 30) - 15; d.position.set(x, u.y + Math.sin(T * 3 + n) * .3 * k, u.z); d.rotation.set(T * u.rot * k, T * u.rot * .7 * k, 0); });
    car.visible = w >= 1235; if (car.visible) { const u = (T - 16.0); car.position.set(-12 + ((u * 9) % 26), 0.4 + Math.abs(Math.sin(u * 4)) * 1.2, -2.5); car.rotation.set(u * 2, 0, u * 3); }
    // Jeremy clinging to the lamp post, body blown sideways
    jPivot.position.set(-0.9, 3.05, 0.25);
    J.position.set(0, -2.6, 0); J.scale.setScalar(0.95);
    const ang = Math.min(1.45, k * 2.2) + Math.sin(T * (6 + 20 * k)) * 0.08 * (k > .05 ? 1 : 0);
    jPivot.rotation.z = ang;
    if (letGo && lt > 0.6) { const u = lt - 0.6; jPivot.position.set(-0.9 + u * u * 14 + u * 3, 3.05 + Math.sin(u * 3) * .6, 0.25); jPivot.rotation.z = 1.4 + u * 6; }
    J.pose({ expr: k < 0.05 ? 'confused' : k < 0.3 ? 'worried' : 'panic', armL: 3.0, armR: 3.0, sweatK: k > .2 ? T : 0, look: -0.5 });
    const sh = (Math.random() - .5) * 0.05 * k;
    setCam(V(-0.3 + sh, 2.4 + sh, 9.5), V(0.2, 2.0, 0), sh * .5);
  }
  if (mode === 'tsunami') {
    // a wall of water rolling east (left → right) over the city
    const front = lerp(-8, 16, eIn(prog(lt, 0, 3.0)) * 0.5 + prog(lt, 0, 3.0) * 0.5); const H = 10;
    const p = waveGeo.attributes.position.array;
    for (let n = 0; n < p.length; n += 3) { const x = waveBase[n], yy = waveBase[n + 1]; const dx = x - (front - 0); const h = dx < 0 ? H * Math.exp(-(dx * dx) / 60) + 0.3 : H * Math.exp(-(dx * dx) / 2.5); p[n + 2] = Math.max(0, h) + Math.sin(x * .8 + T * 3 + yy) * .15; }
    waveGeo.attributes.position.needsUpdate = true; waveGeo.computeVertexNormals();
    wave.position.set(0, 0, -4); foam.position.set(front - 30 + 30, H - 0.2, -4); foam.position.x = front; foam.visible = true;
    city.children.forEach(b => { b.visible = b.position.x > front - 1; });
    setCam(V(16, 6, 26), V(3, 4.5, -4), Math.sin(T * 30) * .004);
  }
  if (mode === 'sun' || mode === 'night') {
    const day = mode === 'sun';
    sunBall.visible = day; sunGlow.visible = day; sunBall.position.set(-7, 11, -30); sunGlow.position.set(2, 10, -10);
    ground.material.color.set(day ? 0xffffff : 0x4a5a80); nightStars.visible = !day;
    J.scale.setScalar(1); jPivot.position.set(0, 0, 1.0); J.rotation.y = 0.2;
    J.pose({ expr: day ? 'worried' : 'worried', sweatK: day ? T : 0, armL: day ? 2.2 : 0.5, armR: day ? 2.2 : 0.5, look: day ? 0.6 : -0.4, tilt: day ? 0 : Math.sin(T * 40) * .03 });
    if (!day) J.position.x = Math.sin(T * 50) * .02;
    setCam(V(lerp(-1, 1, eInOut(prog(lt, 0, 2.6))), 2.2, 8.5), V(0.5, 3.0, 0));
    key.intensity = day ? 3.2 : 0.12; key.color.set(day ? 0xffe0b0 : 0x8090ff);
  } else key.color.set(0xfff1dd);
  if (mode === 'cta') {
    J.scale.setScalar(.9); jPivot.position.set(0, 0, 1.0); J.rotation.y = 0;
    J.pose({ expr: 'confused', look: Math.sin(T * 2), tilt: .12, armL: .3, armR: 1.3 });
    setCam(V(lerp(-.4, .4, eInOut(prog(lt, 0, 4.6))), 2.6, 8.4), V(0, 2.0, 0));
    const sm = document.getElementById('small'); sm.style.top = '1525px'; sm.style.opacity = clamp((lt - 1.2) / .4); sm.textContent = 'Purely hypothetical · for entertainment';
  }
  const dayPhase = T >= 26.8;
  if (!dayPhase) counter(T, { on: T >= 3.0, valueAt: t => windAt(Math.max(3, t)), fmt: v => Math.round(v).toLocaleString('en-US') + ' km/h', label: 'WIND SPEED', sub: w >= 1235 ? 'speed of sound: 1,235 km/h' : '', sev: sevW(w), shake: w >= 1235 && mode === 'wind' ? 0.5 : 0 });
  else counter(T, { on: true, valueAt: t => keyframes(dayKF, t), fmt: v => Math.round(v).toLocaleString('en-US') + ' hours', label: 'LENGTH OF ONE DAY', sub: T >= 29.4 ? '= 1 whole year' : '', sev: T < 29.4 ? 1 : 5 });
  const caps = [];
  if (T >= 3.0) { const end = i + 1 < st.length ? st[i + 1].t - 0.15 : TOTAL; caps.push({ t0: s.t + 0.05, t1: end, text: s.cap, y: 1330, size: s.cap.length > 32 ? 66 : 80, g: s.hi.map(x => x.replace(/[,.?!…:]/g, '')) }); }
  if (mode === 'cta') caps.push({ t0: s.t + 1.0, t1: TOTAL, text: 'Comment below ↓', y: 1440, size: 66, g: ['below', '↓'] });
  renderCaptions(caps, T);
  document.getElementById('fill').style.width = (clamp(T / TOTAL) * 100) + '%';
  draw();
};
window.TOTAL = TOTAL;
window.READY = true;
