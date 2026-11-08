// Episode 3 — What if you jumped into a hole through the Earth?
import {
  THREE, RoundedBoxGeometry, renderer, scene, camera, draw, flash as flashLight, M, canvasTex, loadFont, text3d,
  makeJeremy, renderCaptions, clamp, prog, eOut, eInOut, eBack, lerp, rand, popS, floor, shards
} from './engine.js';
import { setTitle, intro, counter, stageAt, keyframes, flash } from './hud.js';

await document.fonts.load('80px IDB'); await document.fonts.load('80px IDBo'); await document.fonts.load('40px IM');
await loadFont();
renderer.localClippingEnabled = true;

const TOTAL = 50;
setTitle('WHAT IF YOU FELL THROUGH EARTH?', 'EP. 3');
const REEL = ['(x)', 'GRAVITY DOUBLED', 'THE MOON VANISHED', '0 DISAPPEARED', 'YOU DOUBLED 1¢', 'EARTH STOPPED', 'YOU FELL THROUGH EARTH?'];
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const look = new THREE.Vector3();
function setCam(p, l, roll = 0) { camera.position.copy(p); look.copy(l); camera.lookAt(look); camera.rotateZ(roll); }
function group(...k) { const g = new THREE.Group(); k.forEach(x => g.add(x)); scene.add(g); return g; }
const J = makeJeremy(); scene.add(J);
const sceneBg = scene.background.clone(); const sceneFog = scene.fog;

// ---------- depth model ----------
const R = 6371, D = 12742;
const tempTable = [[0, 15], [4, 60], [12.3, 180], [35, 500], [100, 1300], [660, 1900], [2900, 4000], [5150, 5400], [6371, 5400]];
const tempAt = d => { const x = d <= R ? d : D - d; return Math.round(keyframes(tempTable, x) / 10) * 10; };
const layerAt = d => { const x = d <= R ? d : D - d; return x < 35 ? 0 : x < 2900 ? 1 : x < 5150 ? 2 : 3; };

// ---------- shaft (close-up fall) ----------
const strata = canvasTex(512, 1024, (ctx, w, h) => {
  ctx.fillStyle = '#7a6250'; ctx.fillRect(0, 0, w, h); const r = rand(31);
  for (let y = 0; y < h; y += 4 + r() * 18) { const v = 90 + r() * 70; ctx.fillStyle = `rgb(${v},${v * .8},${v * .62})`; ctx.fillRect(0, y, w, 3 + r() * 14); }
  for (let i = 0; i < 260; i++) { ctx.fillStyle = `rgba(0,0,0,${r() * .35})`; ctx.fillRect(r() * w, r() * h, 2 + r() * 30, 1 + r() * 4); }
  ctx.strokeStyle = 'rgba(20,10,5,.6)'; ctx.lineWidth = 2; for (let i = 0; i < 26; i++) { ctx.beginPath(); let x = r() * w, y = r() * h; ctx.moveTo(x, y); for (let k = 0; k < 8; k++) { x += (r() - .5) * 40; y += 10 + r() * 20; ctx.lineTo(x, y); } ctx.stroke(); }
});
strata.tex.wrapS = strata.tex.wrapT = THREE.RepeatWrapping; strata.tex.repeat.set(3, 4);
const emTex = strata.tex.clone(); emTex.needsUpdate = true;
const shaftMat = new THREE.MeshStandardMaterial({ map: strata.tex, side: THREE.BackSide, roughness: .85, emissive: 0xff5a10, emissiveMap: strata.tex, emissiveIntensity: 0 });
const shaft = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 2.4, 90, 48, 1, true), shaftMat); shaft.position.y = -30;
const glow = new THREE.PointLight(0xff7a20, 0, 60); glow.position.set(0, -14, 0);
const headL = new THREE.PointLight(0xbfd4ff, 25, 20); headL.position.set(0, 4, 2);
const STREAK = 90; const streakM = new THREE.MeshBasicMaterial({ color: 0xffb060, transparent: true, opacity: .8, toneMapped: false });
const streaks = new THREE.InstancedMesh(new THREE.BoxGeometry(0.04, 1.6, 0.04), streakM, STREAK); streaks.frustumCulled = false;
const sp = []; { const r = rand(12); for (let i = 0; i < STREAK; i++) { const a = r() * 6.28, d = 0.5 + r() * 1.7; sp.push([Math.cos(a) * d, r() * 40, Math.sin(a) * d, 0.6 + r()]); } }
const shaftG = group(shaft, glow, headL, streaks);
const dm = new THREE.Object3D();

// ---------- cutaway Earth ----------
const clip = [new THREE.Plane(V(-1, 0, 0), 0), new THREE.Plane(V(0, 0, -1), 0)];
function layer(r, color, emissive, ei, map) { const m = new THREE.MeshStandardMaterial({ color, emissive, emissiveIntensity: ei, roughness: .6, side: THREE.DoubleSide, clippingPlanes: clip, clipIntersection: true, map: map || null });
  const s = new THREE.Mesh(new THREE.SphereGeometry(r, 96, 64), m); return s; }
const earthTex = canvasTex(2048, 1024, (ctx, w, h) => {
  const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#1d4f9a'); g.addColorStop(.5, '#1565c0'); g.addColorStop(1, '#1d4f9a'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  const r = rand(23); const blob = (cx, cy, s, col) => { for (let i = 0; i < 70; i++) { ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(cx + (r() - .5) * s * 1.6, cy + (r() - .5) * s, s * (.15 + r() * .3), s * (.12 + r() * .25), r() * 3, 0, 7); ctx.fill(); } };
  [[330, 330, 260], [520, 640, 200], [1060, 330, 230], [1120, 600, 220], [1500, 380, 320], [1700, 700, 140], [1000, 900, 300]].forEach(([x, y, s]) => { blob(x, y, s, '#3f8a3c'); blob(x + 20, y + 10, s * .6, '#7a8b45'); });
  ctx.fillStyle = '#f2f6ff'; ctx.fillRect(0, 0, w, 50); ctx.fillRect(0, h - 70, w, 70);
});
const ER = 6;
const crust = layer(ER, 0xffffff, 0x000000, 0, earthTex.tex);
const crustIn = layer(ER * 0.985, 0x8a6a4a, 0x000000, 0);
const mantle = layer(ER * 0.95, 0xd8582a, 0xff4a10, 0.35);
const outer = layer(ER * 3480 / R, 0xffa030, 0xff8a10, 0.9);
const inner = layer(ER * 1220 / R, 0xfff0b0, 0xffd060, 1.6);
const tunnel = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, ER * 2.02, 12), new THREE.MeshBasicMaterial({ color: 0x5ee0ff, toneMapped: false })); tunnel.position.set(0.12, 0, 0.12);
const marker = new THREE.Mesh(new THREE.SphereGeometry(0.22, 24, 16), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }));
const markRing = new THREE.Mesh(new THREE.TorusGeometry(0.4, 0.04, 8, 40), new THREE.MeshBasicMaterial({ color: 0x5ee0ff, toneMapped: false }));
const labels = [['CRUST', 5.6], ['MANTLE', 4.3], ['OUTER CORE', 2.2], ['INNER CORE', 0.3]].map(([s, y]) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 0.5), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false, depthTest: false,
  map: canvasTex(520, 100, (ctx, w, h) => { ctx.fillStyle = 'rgba(8,10,30,.75)'; ctx.beginPath(); ctx.roundRect(0, 0, w, h, 50); ctx.fill(); ctx.fillStyle = '#fff'; ctx.font = '56px IDB'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(s, w / 2, h / 2 + 3); }).tex })); m.position.set(-2.4, y, 3.5); m.renderOrder = 5; return m; });
const stars = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute((() => { const r = rand(5), a = []; for (let i = 0; i < 2500; i++) { const th = r() * 6.283, ph = Math.acos(2 * r() - 1), d = 300; a.push(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d, Math.sin(ph) * Math.sin(th) * d); } return a; })(), 3)), new THREE.PointsMaterial({ color: 0xffffff, size: 1.2, sizeAttenuation: false }));
const earthG = group(crust, crustIn, mantle, outer, inner, tunnel, marker, markRing, ...labels, stars);

// ---------- ocean ----------
const oceanTex = canvasTex(512, 512, (ctx, w, h) => { ctx.fillStyle = '#0b4f8a'; ctx.fillRect(0, 0, w, h); const r = rand(4); for (let i = 0; i < 300; i++) { ctx.strokeStyle = `rgba(255,255,255,${r() * .25})`; ctx.lineWidth = 2; ctx.beginPath(); const x = r() * w, y = r() * h; ctx.arc(x, y, 6 + r() * 30, Math.PI * 1.1, Math.PI * 1.9); ctx.stroke(); } });
oceanTex.tex.wrapS = oceanTex.tex.wrapT = THREE.RepeatWrapping; oceanTex.tex.repeat.set(14, 14);
const ocean = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshPhysicalMaterial({ map: oceanTex.tex, roughness: .12, clearcoat: 1, metalness: .1 })); ocean.rotation.x = -Math.PI / 2; ocean.receiveShadow = true;
const splashM = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .05, transmission: 0, transparent: true, opacity: .85, clearcoat: 1 });
const splash = shards(70, splashM, 0.12, 9);
const oceanG = group(ocean, splash);

// ---------- CTA: hole in the stage ----------
const hole = new THREE.Mesh(new THREE.CircleGeometry(1.3, 64), new THREE.MeshBasicMaterial({ color: 0x000000 })); hole.rotation.x = -Math.PI / 2; hole.position.y = 0.02;
const holeRim = new THREE.Mesh(new THREE.TorusGeometry(1.32, 0.07, 12, 80), new THREE.MeshStandardMaterial({ color: 0xff7a20, emissive: 0xff5a10, emissiveIntensity: 2 })); holeRim.rotation.x = -Math.PI / 2; holeRim.position.y = 0.05;
const holeGlow = new THREE.PointLight(0xff6a10, 25, 8); holeGlow.position.set(0, -0.5, 0);
const ctaG = group(hole, holeRim, holeGlow);

// =================== TIMELINE ===================
const st = [
  { t: 3.0, d: 0, cap: 'Jeremy jumps into a tunnel through Earth.', hi: ['tunnel'], mode: 'cut' },
  { t: 5.6, d: 4, cap: '4 km: deeper than the deepest mine.', hi: ['deepest'] },
  { t: 8.2, d: 12.3, cap: '12 km: the deepest hole humans ever dug.', hi: ['ever', 'dug'] },
  { t: 10.8, d: 35, cap: '35 km: out of the crust. The rock glows.', hi: ['glows'] },
  { t: 13.4, d: 100, cap: '100 km: 1,300 °C. Solid rock that slowly flows.', hi: ['1300'] },
  { t: 16.0, d: 660, cap: '660 km: 235,000× the air pressure.', hi: ['235000×'] },
  { t: 18.6, d: 2900, cap: '2,900 km: an ocean of liquid metal.', hi: ['liquid', 'metal'] },
  { t: 21.2, d: 4000, cap: 'This iron ocean makes Earth’s magnetic field.', hi: ['magnetic', 'field'] },
  { t: 23.8, d: 5150, cap: '5,150 km: the inner core. Solid iron.', hi: ['inner', 'core'] },
  { t: 26.4, d: 6371, cap: 'THE CENTER: as hot as the Sun’s surface.', hi: ['Sun’s', 'surface'], mode: 'cut' },
  { t: 29.4, d: 6371, cap: 'Here, Jeremy is weightless.', hi: ['weightless'], mode: 'float' },
  { t: 32.4, d: 7200, cap: 'But he’s doing 8+ km/s… so he shoots past.', hi: ['8+', 'km/s'] },
  { t: 35.0, d: 9500, cap: 'Now gravity slows him down…', hi: ['slows'] },
  { t: 37.6, d: 12300, cap: 'Almost there…', hi: ['Almost'] },
  { t: 40.0, d: 12742, cap: '38 minutes later: out the other side!', hi: ['38', 'minutes'], mode: 'cut' },
  { t: 43.0, d: 12742, cap: '…and from most land, that’s the OCEAN.', hi: ['OCEAN'], mode: 'ocean' },
  { t: 46.0, d: 12742, cap: 'Would you jump?', hi: ['jump'], mode: 'cta' },
];
const depthKF = []; st.forEach((s, i) => { if (i > 0 && s.d !== st[i - 1].d) depthKF.push([s.t - 1.2, st[i - 1].d]); depthKF.push([s.t, s.d]); });
const depthAt = t => keyframes(depthKF, t);
const fmtKm = v => Math.round(v).toLocaleString('en-US') + ' km';
const sevAt = temp => temp < 100 ? 0 : temp < 600 ? 1 : temp < 1500 ? 2 : temp < 3000 ? 3 : temp < 5000 ? 4 : 5;
const layerCols = [[0x8a6a4a, 0x000000, 0], [0xc0582a, 0xff4a10, .6], [0xff9a30, 0xff7a10, 1.6], [0xfff0b0, 0xffc040, 2.4]];
const cA = new THREE.Color(), cB = new THREE.Color();

window.renderAt = (T) => {
  flashLight.intensity = 0; flash(0); document.getElementById('small').textContent = '';
  intro(T, REEL, 3.0);
  const { i, lt, s } = stageAt(st, T);
  const mode = T < 3 ? 'intro' : s.mode || 'shaft';
  const d = depthAt(T), temp = tempAt(d);
  const stageMode = mode === 'intro' || mode === 'cta';
  floor.visible = stageMode; scene.fog = stageMode ? sceneFog : null;
  scene.background = mode === 'ocean' ? new THREE.Color(0x6fb6ff) : stageMode ? sceneBg : new THREE.Color(mode === 'cut' ? 0x01020a : 0x050302);
  shaftG.visible = mode === 'shaft' || mode === 'float'; earthG.visible = mode === 'cut'; oceanG.visible = mode === 'ocean'; ctaG.visible = mode === 'cta' || mode === 'intro';
  J.visible = mode !== 'cut';

  if (mode === 'intro') { J.visible = false; setCam(V(0, 3.0, 9), V(0, 2.4, 0)); }
  if (mode === 'shaft' || mode === 'float') {
    // wall colour by layer, glow by temperature
    const L = layerAt(d), nxt = Math.min(3, L + 1);
    const lc = layerCols[L]; cA.set(lc[0]); shaftMat.color.copy(cA); shaftMat.emissive.set(lc[1]); shaftMat.emissiveIntensity = lc[2] * (0.6 + 0.4 * Math.sin(T * 3) ** 2);
    glow.intensity = clamp(temp / 5400) * 160; glow.color.set(L === 3 ? 0xffd080 : 0xff7a20);
    // visual speed: grows to the center, shrinks after
    const v = mode === 'float' ? 0.15 : d <= R ? 0.8 + 6 * Math.sqrt(clamp(d / R)) : 0.8 + 6 * Math.sqrt(clamp((D - d) / R));
    const off = (window.__off = (window.__off ?? 0)); // not used for determinism
    const scroll = keyframes([[3, 0], [10, 3], [20, 18], [26.4, 34], [29.4, 35], [32.4, 38], [40, 70]], T);
    strata.tex.offset.y = scroll;
    for (let k = 0; k < STREAK; k++) { const p = sp[k]; dm.position.set(p[0], ((p[1] + scroll * 8 * p[3]) % 40) - 30, p[2]); dm.scale.set(1, v * 0.4, 1); dm.rotation.set(0, 0, 0); dm.updateMatrix(); streaks.setMatrixAt(k, dm.matrix); }
    streaks.instanceMatrix.needsUpdate = true; streakM.color.set(L === 0 ? 0xd8c8b0 : L === 3 ? 0xfff0b0 : 0xffa050);
    const spin = mode === 'float' ? T * 0.6 : T * 0.9;
    J.scale.setScalar(0.8); J.position.set(0, -2.5 + (mode === 'float' ? Math.sin(T * 1.5) * .25 : 0), 0); J.rotation.set(mode === 'float' ? -0.9 : -1.15, 0, mode === 'float' ? Math.sin(T) * .4 : Math.sin(T * .7) * .25); J.rotateOnWorldAxis(V(0, 1, 0), Math.sin(spin * .5) * .5);
    const scared = temp > 400;
    J.pose({ expr: mode === 'float' ? 'confused' : scared ? 'panic' : 'shocked', armL: mode === 'float' ? 1.6 + Math.sin(T * 2) * .3 : 2.7 + Math.sin(T * 14) * .2, armR: mode === 'float' ? 1.6 - Math.sin(T * 2) * .3 : 2.7 + Math.cos(T * 14) * .2, sweatK: temp > 1000 ? T : 0, look: Math.sin(T * 2) * .4 });
    const sh = mode === 'shaft' ? (Math.random() - .5) * 0.06 * v / 6 : 0;
    setCam(V(Math.sin(T * .3) * 0.5 + sh, 6.4, 1.5 + sh), V(0, -3.6, -0.3), Math.sin(T * .5) * .08);
  }
  if (mode === 'cut') {
    const y = ER - (Math.min(d, D) / D) * 2 * ER;
    marker.position.set(0.12, y, 0.12); markRing.position.copy(marker.position); markRing.rotation.set(Math.PI / 2, 0, 0); markRing.scale.setScalar(1 + 0.3 * Math.sin(T * 8));
    earthG.rotation.y = 0; stars.rotation.y = T * .01;
    labels.forEach((l, k) => { l.visible = false; l.scale.setScalar(popS(lt, 0.5 + k * 0.2, .35)); l.position.x = 2.0; l.position.z = 4.2; l.lookAt(camera.position); });
    if (s.t === 3.0) { const k = eInOut(prog(lt, 0, 2.6)); setCam(V(lerp(21, 16.5, k), lerp(11, 7.5, k), lerp(27, 21.5, k)), V(0, lerp(0.5, -0.5, k), 0)); }
    else if (s.t === 26.4) { const k = eInOut(prog(lt, 0, 3)); setCam(V(lerp(8, 4.2, k), lerp(3, 1.2, k), lerp(10, 5.2, k)), V(0, 0, 0)); }
    else { const k = eInOut(prog(lt, 0, 3)); setCam(V(lerp(16, 13, k), lerp(-5, -8, k), lerp(21, 17, k)), V(0, -3.5, 0)); }
  }
  if (mode === 'ocean') {
    const up = eOut(prog(lt, 0, .8)); J.scale.setScalar(1); J.position.set(0, lerp(-2.5, 1.2, up) - 0.9 * eInOut(prog(lt, 1.2, 2.6)), 0); J.rotation.set(0, T * .6, 0);
    J.pose({ expr: 'panic', armL: 2.7, armR: 2.7, sweatK: lt });
    splash.burst(V(0, 0.1, 0), lt, 0.6, 5, 2.2);
    oceanTex.tex.offset.set(T * 0.01, T * 0.006);
    setCam(V(Math.sin(lt * .3) * 2, 3.0, 11.5), V(0, 1.7, 0));
  }
  if (mode === 'cta') {
    J.scale.setScalar(0.9); J.position.set(-1.0, 0, 0.9); J.rotation.y = 0.9; J.rotation.x = 0;
    J.pose({ expr: 'worried', look: 0.9, tilt: 0.2, armL: 0.3, armR: 1.2, sweatK: lt });
    holeGlow.intensity = 25 + Math.sin(T * 6) * 8;
    setCam(V(lerp(-0.5, 0.6, eInOut(prog(lt, 0, 4))), 4.2, 8.2), V(0, 0.9, 0));
    const sm = document.getElementById('small'); sm.style.top = '1525px'; sm.style.opacity = clamp((lt - 1.2) / .4); sm.textContent = 'Purely hypothetical · airless, heat-proof tunnel · for entertainment';
  }
  counter(T, { on: T >= 3.0, valueAt: t => depthAt(Math.max(3, t)), fmt: fmtKm, label: 'DISTANCE FALLEN', sub: `${temp.toLocaleString('en-US')} °C`, sev: sevAt(temp), shake: mode === 'shaft' && temp > 3000 ? 0.4 : 0 });
  const caps = [];
  if (T >= 3.0) { const end = i + 1 < st.length ? st[i + 1].t - 0.15 : TOTAL; caps.push({ t0: s.t + 0.05, t1: end, text: s.cap, y: 1330, size: s.cap.length > 32 ? 66 : 80, g: s.hi.map(w => w.replace(/[,.?!…:]/g, '')) }); }
  if (mode === 'cta') caps.push({ t0: s.t + 1.0, t1: TOTAL, text: 'Comment below ↓', y: 1440, size: 66, g: ['below', '↓'] });
  renderCaptions(caps, T);
  document.getElementById('fill').style.width = (clamp(T / TOTAL) * 100) + '%';
  draw();
};
window.TOTAL = TOTAL;
window.READY = true;
