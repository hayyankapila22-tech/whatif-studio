// Episode 6 — What if gravity doubled every minute?
import {
  THREE, RoundedBoxGeometry, scene, camera, draw, key, flash as flashLight, M, canvasTex, loadFont, text3d,
  makeJeremy, renderCaptions, clamp, prog, eOut, eInOut, eIn, lerp, rand, popS, floor, shards
} from './engine.js';
import { setTitle, intro, counter, stageAt, keyframes, flash } from './hud.js';

await document.fonts.load('80px IDB'); await document.fonts.load('80px IDBo'); await document.fonts.load('40px IM');
await loadFont();

const TOTAL = 47.5;
setTitle('WHAT IF GRAVITY KEPT DOUBLING?', 'EP. 6');
const REEL = ['(x)', 'YOUR CAR NEVER STOPPED', 'EARTH STOPPED', 'YOU DOUBLED 1¢', '0 DISAPPEARED', 'THE MOON VANISHED', 'GRAVITY DOUBLED EVERY MINUTE?'];
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const look = new THREE.Vector3();
function setCam(p, l, roll = 0) { camera.position.copy(p); look.copy(l); camera.lookAt(look); camera.rotateZ(roll); }
function rbox(w, h, d, r, mat) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, r), mat); m.castShadow = m.receiveShadow = true; return m; }
function group(...k) { const g = new THREE.Group(); k.forEach(x => g.add(x)); scene.add(g); return g; }
const sceneBg = scene.background.clone(); const sceneFog = scene.fog;
const J = makeJeremy(); const jG = new THREE.Group(); jG.add(J); scene.add(jG);

// ---------- bathroom scale ----------
const scaleDisp = canvasTex(400, 140, (ctx, w, h, kg) => { ctx.fillStyle = '#0b1a12'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#6dffb0'; ctx.shadowColor = '#3dff90'; ctx.shadowBlur = 16; ctx.font = 'bold 92px monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(kg, w / 2, h / 2 + 6); });
const scaleG = new THREE.Group(); { const base = rbox(1.6, 0.18, 1.4, 0.08, new THREE.MeshPhysicalMaterial({ color: 0xeef1f8, roughness: .2, clearcoat: 1 })); base.position.y = 0.09;
  const disp = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.22), new THREE.MeshBasicMaterial({ map: scaleDisp.tex, toneMapped: false })); disp.rotation.x = -Math.PI / 2 + 0.0; disp.position.set(0, 0.185, 0.48); scaleG.add(base, disp); }
scene.add(scaleG);

// ---------- planes / city / mountain ----------
function makePlane() { const g = new THREE.Group(); const w = new THREE.MeshStandardMaterial({ color: 0xf2f4fa, roughness: .35, metalness: .3 });
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.25, 2.2, 8, 16), w); body.rotation.z = Math.PI / 2; const wing = rbox(0.6, 0.06, 3.2, 0.03, w); const tail = rbox(0.4, 0.5, 0.06, 0.03, w); tail.position.set(-1.2, 0.3, 0); const tw = rbox(0.35, 0.05, 1.1, 0.02, w); tw.position.set(-1.2, 0.1, 0);
  const stripe = new THREE.Mesh(new THREE.CapsuleGeometry(0.255, 2.0, 8, 16, 1), new THREE.MeshStandardMaterial({ color: 0x3a7bff })); stripe.rotation.z = Math.PI / 2; stripe.scale.set(1, 1, .2); g.add(body, wing, tail, tw, stripe); g.traverse(o => o.castShadow = true); return g; }
const planes = [0, 1, 2].map(() => makePlane());
const cloudsM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, transparent: true, opacity: .9 });
const cloudBits = []; { const r = rand(3); for (let i = 0; i < 18; i++) { const c = new THREE.Mesh(new THREE.SphereGeometry(1 + r() * 1.5, 16, 12), cloudsM); c.scale.y = .45; c.position.set((r() - .5) * 30, 2 + r() * 10, -8 - r() * 12); cloudBits.push(c); } }
const skyG = group(...planes, ...cloudBits);
const city = new THREE.Group(); const bldgs = []; { const r = rand(17); const winTex = canvasTex(128, 256, (ctx, w, h) => { ctx.fillStyle = '#1a2040'; ctx.fillRect(0, 0, w, h); for (let y = 6; y < h; y += 16) for (let x = 6; x < w; x += 16) { ctx.fillStyle = r() > .45 ? '#ffd98a' : '#2a3366'; ctx.fillRect(x, y, 8, 9); } }).tex;
  const bm = new THREE.MeshStandardMaterial({ color: 0x8890b0, map: winTex, emissive: 0xffffff, emissiveMap: winTex, emissiveIntensity: .4, roughness: .4 });
  for (let i = 0; i < 30; i++) { const h = 2 + r() * 7, w = 1 + r() * 1.4; const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, w), bm); b.geometry.translate(0, h / 2, 0); b.position.set((r() - .5) * 16, 0, -2 - r() * 12); b.castShadow = b.receiveShadow = true; b.userData = { h, d: r() * .6, tilt: (r() - .5) * .6 }; bldgs.push(b); city.add(b); } }
const dust = shards(80, new THREE.MeshStandardMaterial({ color: 0xa89a88, roughness: 1 }), .25, 6);
const cityG = group(city, dust);
const mountain = new THREE.Group(); { const rock = new THREE.Mesh(new THREE.ConeGeometry(6, 8, 7, 4), new THREE.MeshStandardMaterial({ color: 0x6d6a72, roughness: .9, flatShading: true })); rock.position.y = 4;
  const snow = new THREE.Mesh(new THREE.ConeGeometry(2.3, 3.1, 7, 2), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .6, flatShading: true })); snow.position.y = 6.5; mountain.add(rock, snow); mountain.traverse(o => { o.castShadow = o.receiveShadow = true; }); }
const flag = new THREE.Group(); { const p = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, 1.2, 8), M.chrome); p.position.y = .6; const f = new THREE.Mesh(new THREE.PlaneGeometry(.6, .35), new THREE.MeshBasicMaterial({ color: 0xff3b55, side: THREE.DoubleSide })); f.position.set(.3, 1.0, 0); flag.add(p, f); }
const mtnG = group(mountain, flag);

// ---------- space: globe, seesaw, black hole ----------
const earthTex = canvasTex(2048, 1024, (ctx, w, h) => { const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#1d4f9a'); g.addColorStop(.5, '#1565c0'); g.addColorStop(1, '#1d4f9a'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  const r = rand(23); const blob = (cx, cy, s, col) => { for (let i = 0; i < 70; i++) { ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(cx + (r() - .5) * s * 1.6, cy + (r() - .5) * s, s * (.15 + r() * .3), s * (.12 + r() * .25), r() * 3, 0, 7); ctx.fill(); } };
  [[330, 330, 260], [520, 640, 200], [1060, 330, 230], [1120, 600, 220], [1500, 380, 320], [1700, 700, 140], [1000, 900, 300]].forEach(([x, y, s]) => { blob(x, y, s, '#3f8a3c'); blob(x + 20, y + 10, s * .6, '#7a8b45'); });
  ctx.fillStyle = '#f2f6ff'; ctx.fillRect(0, 0, w, 50); ctx.fillRect(0, h - 70, w, 70); });
const earthMat = new THREE.MeshStandardMaterial({ map: earthTex.tex, roughness: .9 });
const earth = new THREE.Mesh(new THREE.SphereGeometry(3, 96, 64), earthMat);
const atmoShell = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshBasicMaterial({ color: 0x6ab8ff, transparent: true, opacity: .28, depthWrite: false, blending: THREE.AdditiveBlending }));
const sunMat = new THREE.MeshBasicMaterial({ color: 0xffd36a, toneMapped: false });
const sun = new THREE.Mesh(new THREE.SphereGeometry(2.2, 48, 32), sunMat);
const SUNS = 100; const suns = new THREE.InstancedMesh(new THREE.SphereGeometry(0.32, 16, 12), sunMat, SUNS);
const plank = rbox(7.4, 0.22, 1.2, 0.1, M.chrome); const pivotTri = new THREE.Mesh(new THREE.ConeGeometry(0.7, 1.4, 3), M.gold); pivotTri.position.y = -0.85;
const seesaw = new THREE.Group(); const beam = new THREE.Group(); beam.add(plank); seesaw.add(beam, pivotTri);
const disk = new THREE.Mesh(new THREE.RingGeometry(3.6, 9, 128, 1), new THREE.MeshBasicMaterial({ transparent: true, side: THREE.DoubleSide, toneMapped: false, depthWrite: false, blending: THREE.AdditiveBlending,
  map: canvasTex(1024, 64, (ctx, w, h) => { const g = ctx.createLinearGradient(0, 0, w, 0); g.addColorStop(0, '#fff2c0'); g.addColorStop(.3, '#ffae40'); g.addColorStop(.7, '#ff5a10'); g.addColorStop(1, 'rgba(120,20,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex }));
{ const pos = disk.geometry.attributes.position, uv = disk.geometry.attributes.uv; for (let i = 0; i < pos.count; i++) { const r = Math.hypot(pos.getX(i), pos.getY(i)); uv.setXY(i, (r - 3.6) / 5.4, .5); } }
const photon = new THREE.Mesh(new THREE.TorusGeometry(3.25, 0.08, 12, 128), new THREE.MeshBasicMaterial({ color: 0xfff0d0, toneMapped: false }));
const stars = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute((() => { const r = rand(5), a = []; for (let i = 0; i < 2500; i++) { const th = r() * 6.283, ph = Math.acos(2 * r() - 1), d = 300; a.push(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d, Math.sin(ph) * Math.sin(th) * d); } return a; })(), 3)), new THREE.PointsMaterial({ color: 0xffffff, size: 1.2, sizeAttenuation: false }));
const spaceL = new THREE.PointLight(0xfff0d0, 0, 100, 0);
const spaceG = group(earth, atmoShell, sun, suns, seesaw, disk, photon, stars, spaceL);
const dm = new THREE.Object3D();

// =================== TIMELINE ===================
const st = [
  { t: 3.0, m: 0, cap: 'Gravity starts doubling every minute.', hi: ['doubling'], mode: 'jer' },
  { t: 5.6, m: 1, cap: 'Minute 1: 2g. Jeremy weighs double.', hi: ['double'], mode: 'jer' },
  { t: 8.2, m: 2, cap: 'Minute 2: 4g. He can’t stand up.', hi: ['can’t', 'stand'], mode: 'jer' },
  { t: 10.8, m: 3, cap: 'Minute 3: 8g. Fighter-pilot territory: he blacks out.', hi: ['blacks', 'out'], mode: 'jer' },
  { t: 13.4, m: 4, cap: 'Minute 4: planes drop out of the sky.', hi: ['planes'], mode: 'sky' },
  { t: 16.0, m: 5, cap: 'Minute 5: buildings collapse.', hi: ['collapse'], mode: 'city' },
  { t: 18.6, m: 6, cap: 'Minute 6: Everest slumps to ~140 m.', hi: ['~140', 'm'], mode: 'mtn' },
  { t: 21.2, m: 10, cap: 'Minute 10: the whole sky squashes to ~8 m thick.', hi: ['~8', 'm'], mode: 'atmo' },
  { t: 23.8, m: 19, cap: 'Minute 19: Earth now outweighs the SUN.', hi: ['SUN'], mode: 'seesaw' },
  { t: 26.6, m: 19, cap: 'So the Sun starts orbiting US.', hi: ['US'], mode: 'orbit' },
  { t: 29.4, m: 25, cap: 'Minute 25: heavier than 100 Suns.', hi: ['100', 'Suns'], mode: 'seesaw100' },
  { t: 32.2, m: 29, cap: 'Minute 29: space itself starts to bend…', hi: ['bend'], mode: 'bend' },
  { t: 35.0, m: 30, cap: 'Minute 30: Earth becomes a BLACK HOLE.', hi: ['BLACK', 'HOLE'], mode: 'bh' },
  { t: 38.0, m: 30, cap: 'Not even light can escape.', hi: ['light'], mode: 'bh' },
  { t: 40.8, m: 30, cap: 'Total time: just 30 minutes.', hi: ['30', 'minutes'], mode: 'bh' },
  { t: 43.4, m: 30, cap: 'What should double next?', hi: ['double'], mode: 'cta' },
];
const mKF = []; st.forEach((s, i) => { if (i > 0 && s.m !== st[i - 1].m) mKF.push([s.t - 1.1, st[i - 1].m]); mKF.push([s.t, s.m]); });
const minuteAt = t => Math.floor(keyframes(mKF, t) + 1e-6);
const gAt = t => Math.pow(2, minuteAt(t));
const sevG = g => g < 2 ? 0 : g < 4 ? 1 : g < 16 ? 2 : g < 1024 ? 3 : g < 1e6 ? 4 : 5;
const fmtG = g => g.toLocaleString('en-US') + ' g';

window.renderAt = (T) => {
  flashLight.intensity = 0; flash(0); document.getElementById('small').textContent = '';
  intro(T, REEL, 3.0);
  const { i, lt, s } = stageAt(st, T);
  const mode = T < 3 ? 'intro' : s.mode;
  const g = gAt(T), m = minuteAt(T);
  const stageLook = ['intro', 'jer', 'cta'].includes(mode);
  const world = ['sky', 'city', 'mtn'].includes(mode);
  floor.visible = stageLook || mode === 'city' || mode === 'mtn'; scene.fog = stageLook ? sceneFog : null;
  scene.background = mode === 'sky' ? new THREE.Color(0x7cc0ff) : (mode === 'city' || mode === 'mtn') ? new THREE.Color(0x0b1028) : stageLook ? sceneBg : new THREE.Color(0x01020a);
  jG.visible = mode === 'jer' || mode === 'cta'; scaleG.visible = mode === 'jer';
  skyG.visible = mode === 'sky'; cityG.visible = mode === 'city'; mtnG.visible = mode === 'mtn'; spaceG.visible = ['atmo', 'seesaw', 'orbit', 'seesaw100', 'bend', 'bh'].includes(mode);
  J.position.set(0, 0, 0); J.rotation.set(0, 0, 0); J.scale.set(1, 1, 1); jG.position.set(0, 0, 0); jG.rotation.set(0, 0, 0);
  key.intensity = 2.0;

  if (mode === 'intro') setCam(V(0, 3.0, 9), V(0, 2.4, 0));
  if (mode === 'jer') {
    scaleG.position.set(0, 0, 0.6); scaleDisp.draw((80 * g).toLocaleString('en-US') + ' kg');
    jG.position.set(0, 0.18, 0.6);
    const squash = m === 0 ? 1 : m === 1 ? 0.9 : m === 2 ? 0.72 : 1;
    if (m < 3) { J.scale.set(1 + (1 - squash) * .4, squash, 1); J.pose({ expr: m === 0 ? 'happy' : m === 1 ? 'worried' : 'panic', armL: m === 0 ? .3 : .05, armR: m === 0 ? .3 : .05, sweatK: m > 0 ? T : 0, look: .4, bob: m === 2 ? -0.25 : 0 }); }
    else { const fall = eOut(prog(lt, 0, .5)); jG.rotation.x = -fall * Math.PI / 2; jG.position.set(0, 0.18 + fall * 0.15, 0.6 + fall * 0.2); J.scale.set(1.15, 0.6, 1); J.pose({ expr: 'sleep', armL: .1, armR: .1 }); }
    const sh = m >= 2 ? (Math.random() - .5) * .03 : 0;
    setCam(V(lerp(-.5, .5, eInOut(prog(T, 3, 13.4))) + sh, 2.6 + sh, 7.6), V(0, 1.3, 0));
  }
  if (mode === 'sky') {
    planes.forEach((p, k) => { const u = lt; p.scale.setScalar(1.7); p.position.set(-6 + k * 5, 9 - u * u * (2.2 + k * .6) - k * 1.5, -6 - k * 3); p.rotation.set(0, k * .4 - .2, -0.2 - u * .55); });
    cloudBits.forEach((c, k) => c.position.y += 0);
    setCam(V(0, 5, 9), V(0, 4.5, -6));
  }
  if (mode === 'city') {
    bldgs.forEach(b => { const u = clamp((lt - b.userData.d) / 1.4); b.scale.y = Math.max(.12, 1 - eIn(u) * .88); b.rotation.z = b.userData.tilt * eIn(u) * .5; b.position.y = 0; });
    dust.burst(V(0, .2, -6), lt - .4, 6, .3, 2.6);
    const sh = (Math.random() - .5) * .12 * clamp(lt);
    setCam(V(2 + sh, 6 + sh, 16), V(0, 3, -6));
  }
  if (mode === 'mtn') {
    const sq = eInOut(prog(lt, .9, 2.4)); mountain.scale.set(1 + sq * .9, Math.max(0.016, 1 - sq * .984), 1 + sq * .9);
    flag.position.set(0, 8 * mountain.scale.y + 0.05, 0); flag.rotation.z = sq * .3;
    setCam(V(lerp(4, 6, sq), lerp(7, 4, sq), 20), V(0, lerp(4, 1.5, sq), 0));
  }
  if (spaceG.visible) {
    earth.visible = true; earth.position.set(0, 0, 0); earth.scale.setScalar(1); earth.rotation.y = T * .15; earthMat.color.set(0xffffff); earthMat.map = earthTex.tex;
    atmoShell.visible = mode === 'atmo'; sun.visible = false; suns.visible = false; seesaw.visible = false; disk.visible = false; photon.visible = false; spaceL.intensity = 0;
    key.intensity = 2.2; stars.rotation.y = T * .01;
    if (mode === 'atmo') { const sq = eInOut(prog(lt, .3, 2.0)); atmoShell.scale.setScalar(3 * (1.35 - sq * .33)); atmoShell.material.opacity = .22 + sq * .3; setCam(V(0, 1.5, 17), V(0, 0, 0)); }
    if (mode === 'seesaw' || mode === 'seesaw100') {
      seesaw.visible = true; seesaw.position.set(0, -1.2, 0);
      const tilt = mode === 'seesaw' ? -0.22 * eOut(prog(lt, .3, 1.4)) : -0.22 + 0.3 * eOut(prog(lt, .3, 1.6));
      beam.rotation.z = tilt;
      const L = V(-2.9, 0.12, 0).applyAxisAngle(V(0, 0, 1), tilt), Rr = V(2.9, 0.12, 0).applyAxisAngle(V(0, 0, 1), tilt);
      earth.scale.setScalar(.38); earth.position.set(L.x, L.y - 1.2 + 1.27, 0);
      if (mode === 'seesaw') { sun.visible = true; sun.scale.setScalar(.6); sun.position.set(Rr.x, Rr.y - 1.2 + 1.45, 0); }
      else { suns.visible = true; suns.count = SUNS; let n = 0; for (let a = 0; a < 6 && n < SUNS; a++) for (let b = 0; b < 17 && n < SUNS; b++) { dm.position.set(Rr.x - .9 + (b % 6) * .36 + (a % 2) * .18, Rr.y - 1.2 + .32 + a * .34, -.5 + Math.floor(b / 6) * .5); dm.scale.setScalar(.7 * popS(lt, n * .008, .3)); dm.rotation.set(0, 0, 0); dm.updateMatrix(); suns.setMatrixAt(n++, dm.matrix); } suns.instanceMatrix.needsUpdate = true; }
      spaceL.intensity = 2; spaceL.position.set(4, 3, 4);
      setCam(V(0, 1.4, 16), V(0, 0.5, 0));
    }
    if (mode === 'orbit') { sun.visible = true; const a = lt * 1.6; sun.scale.setScalar(.8); sun.position.set(Math.cos(a) * 7, Math.sin(a) * 1.2, Math.sin(a) * 7); spaceL.intensity = 3; spaceL.position.copy(sun.position);
      const trail = 0; setCam(V(0, 5, 19), V(0, 0, 0)); }
    if (mode === 'bend') { const k = prog(lt, 0, 2.8); earthMat.color.setRGB(1 - k * .85, 1 - k * .85, 1 - k * .85); photon.visible = k > .4; photon.material.opacity = 1; photon.scale.setScalar(1); photon.rotation.set(Math.PI / 2 - .25, 0, 0);
      const sh = (Math.random() - .5) * .1 * k; setCam(V(sh, 1 + sh, 17 - k * 2), V(0, 0, 0), Math.sin(T * 10) * .01 * k); }
    if (mode === 'bh') { earthMat.color.set(0x000000); earthMat.map = null; earthMat.needsUpdate = true; disk.visible = true; photon.visible = true; disk.rotation.set(Math.PI / 2 - .28, 0, T * .6); photon.rotation.set(0, 0, 0);
      photon.lookAt(camera.position); if (s.t === 35.0 && lt < .4) flash(.8 * (1 - lt / .4));
      const k = eInOut(prog(T, 35, 43.4)); setCam(V(lerp(0, 3, k), lerp(2.2, 3.4, k), lerp(16, 19, k)), V(0, 0, 0)); }
  } else { earthMat.map = earthTex.tex; }
  if (mode === 'cta') {
    jG.position.set(0, 0, 1); J.pose({ expr: 'confused', look: Math.sin(T * 2), tilt: .12, armL: .3, armR: 1.3 });
    setCam(V(lerp(-.4, .4, eInOut(prog(lt, 0, 4))), 2.6, 8.4), V(0, 2.0, 0));
    const sm = document.getElementById('small'); sm.style.top = '1525px'; sm.style.opacity = clamp((lt - 1.2) / .4); sm.textContent = 'Purely hypothetical · for entertainment';
  }
  counter(T, { on: T >= 3.0 && mode !== 'cta', valueAt: t => gAt(Math.max(3, t)), fmt: fmtG, label: `MINUTE ${m}`, sub: `Jeremy: ${(80 * g).toLocaleString('en-US')} kg`, sev: sevG(g), shake: g >= 1e6 ? .6 : 0 });
  const caps = [];
  if (T >= 3.0) { const end = i + 1 < st.length ? st[i + 1].t - 0.15 : TOTAL; caps.push({ t0: s.t + 0.05, t1: end, text: s.cap, y: mode === 'cta' ? 1300 : 1330, size: mode === 'cta' ? 70 : s.cap.length > 32 ? 66 : 80, g: s.hi.map(x => x.replace(/[,.?!…:]/g, '')) }); }
  if (mode === 'cta') caps.push({ t0: s.t + 1.0, t1: TOTAL, text: 'Comment below ↓', y: 1440, size: 66, g: ['below', '↓'] });
  renderCaptions(caps, T);
  document.getElementById('fill').style.width = (clamp(T / TOTAL) * 100) + '%';
  draw();
};
window.TOTAL = TOTAL;
window.READY = true;
