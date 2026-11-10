// Season 2 v3 "world" kit: time-of-day, night lights, decay over years, snow, nature, animals, collapse, props.
// Reusable for any TIMELINE episode on Jeremy's Street: call setAge(years) + setSky(preset) per shot.
import { THREE, RoundedBoxGeometry, scene, canvasTex, rand, clamp, lerp, eOut, LOOK, GRADE } from './kit.js';
import { key, hemi, renderer, INK } from './engine.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { crown, grassGeo, grassMat, leafMats } from './foliage.js';
import { setEnv } from './engine.js';

const V = (x, y, z) => new THREE.Vector3(x, y, z);
export const W = {}; // handles

// ------------------------------------------------------------------ sky / light presets
export const SKY = {
  day:     { hdri: 'sky', zen: '#2f6fd0', hor: '#bcd6f2', gnd: '#9fb6cf', sun: '#fff1cf', key: 3.4, keyCol: '#ffe4c0', hemi: .6, exp: .52, env: .6, fog: [70, 300] },
  golden:  { hdri: 'sunset', zen: '#3d5fb0', hor: '#ffc98e', gnd: '#c99a86', sun: '#ffd28a', key: 3.2, keyCol: '#ffb879', hemi: .7, exp: .7, env: .6, fog: [60, 280] },
  dusk:    { hdri: 'sunset', zen: '#1b2a6b', hor: '#f08a6a', gnd: '#6a4a6a', sun: '#ff9a6a', key: 1.5, keyCol: '#ff9a7a', hemi: .5, exp: .62, env: .4, fog: [50, 260] },
  night:   { hdri: 'night', zen: '#060b24', hor: '#1d2c5c', gnd: '#141a33', sun: '#000000', key: .5, keyCol: '#8fa8ff', hemi: .32, exp: .8, env: .3, fog: [40, 220] },
  overcast:{ hdri: 'city', zen: '#7d8ea8', hor: '#c9d2dc', gnd: '#a8afb8', sun: '#000000', key: 1.4, keyCol: '#e8eef8', hemi: .8, exp: .55, env: .5, fog: [40, 220] },
  ominous: { hdri: 'sunset', zen: '#3a2a3a', hor: '#e07a4a', gnd: '#5a3a3a', sun: '#ff7a3a', key: 1.6, keyCol: '#ffa070', hemi: .35, exp: .52, env: .3, fog: [50, 400] },
  winter:  { hdri: 'dawn', zen: '#8aa4c8', hor: '#e6edf5', gnd: '#dfe6ee', sun: '#ffffff', key: 1.8, keyCol: '#f2f6ff', hemi: .9, exp: .5, env: .55, fog: [25, 160] },
};
const cA = new THREE.Color(), cB = new THREE.Color();
export function setSky(a, b = null, k = 0) {
  const A = SKY[a], B = b ? SKY[b] : A, m = (x, y) => lerp(x, y, k);
  const col = (p) => cA.set(A[p]).lerp(cB.set(B[p]), k);
  LOOK.zenith.copy(col('zen')); LOOK.horizon.copy(col('hor')); LOOK.ground.copy(col('gnd')); LOOK.sunGlow.copy(col('sun'));
  key.intensity = m(A.key, B.key); key.color.copy(col('keyCol')); hemi.intensity = m(A.hemi, B.hemi);
  renderer.toneMappingExposure = m(A.exp, B.exp); scene.environmentIntensity = m(A.env, B.env) * 1.15;
  setEnv(k < .5 ? A.hdri : B.hdri);
  if (scene.fog) { scene.fog.color.copy(LOOK.horizon); scene.fog.near = m(A.fog[0], B.fog[0]); scene.fog.far = m(A.fog[1], B.fog[1]); }
}

// ------------------------------------------------------------------ setup (call once after boot)
export function buildWorld(K) {
  const S = K.street.group, U = S.userData;
  W.S = S; W.blocks = U.blocks; W.lamps = U.lamps; W.cars = U.cars;
  const r = rand(404);
  // remember original material colours (moss / rust tint)
  W.facades = []; S.traverse(o => { if (o.isMesh && o.material && o.material.map && o.material.color && !W.facades.includes(o.material)) { o.material.userData.c0 = o.material.color.clone(); W.facades.push(o.material); } });
  W.carPaint = W.cars.map(c => { let m = null; c.traverse(o => { if (o.isMesh && o.material.isMeshPhysicalMaterial && o.material.clearcoat > .5 && !m) m = o.material; }); if (m) m.userData.c0 = m.color.clone(); return m; });
  // ---- window lights (night) + broken window state per glass instance
  W.win = [];
  const litGeo = new THREE.PlaneGeometry(1.05, 1.5), litMat = new THREE.MeshBasicMaterial({ color: 0xffd58a, toneMapped: false });
  const m4 = new THREE.Matrix4(), p = new THREE.Vector3(), q = new THREE.Quaternion(), sc = new THREE.Vector3();
  for (const b of W.blocks) {
    const g = b.userData.glass; if (!g) continue;
    const n = g.count, lit = new THREE.InstancedMesh(litGeo, litMat, n); lit.frustumCulled = false;
    const side = b.userData.side, base = [];
    for (let i = 0; i < n; i++) { g.getMatrixAt(i, m4); m4.decompose(p, q, sc); base.push({ m: m4.clone(), p: p.clone(), on: r(), br: r() });
      g.setColorAt(i, new THREE.Color(1, 1, 1)); }
    g.instanceColor.needsUpdate = true;
    lit.userData = { base, side }; b.add(lit); lit.visible = false; W.win.push({ g, lit, base, side });
  }
  // ---- grass tufts (instanced, grow with age)
  const blade = (h, rz, ry) => { const gg = new THREE.ConeGeometry(.035, h, 3); gg.translate(0, h / 2, 0); gg.rotateZ(rz); gg.rotateY(ry); return gg; };
  const tuftGeo = mergeGeometries([blade(.34, .25, 0), blade(.28, -.3, 1.2), blade(.36, .1, 2.4), blade(.26, -.2, 3.5), blade(.3, .35, 4.6), blade(.22, .5, 5.5)]);
  const NG = 7000; W.grass = new THREE.InstancedMesh(grassGeo, grassMat, NG); W.grass.frustumCulled = false; W.grass.castShadow = false; W.grass.receiveShadow = true;
  W.grassD = [];
  const gc = new THREE.Color();
  for (let i = 0; i < NG; i++) {
    // concentrated along cracks/curbs early (birth small), meadow later
    const crack = i < 900; const x = -10 + r() * 90;
    const z = crack ? (r() < .5 ? 4.5 : -4.5) + (r() - .5) * .5 : (r() - .5) * 16;
    W.grassD.push({ x, z, birth: crack ? r() * .4 : .4 + Math.pow(r(), .7) * 25, s: .5 + r() * .6, ry: r() * 6.28 });
    W.grass.setColorAt(i, gc.setHSL(.22 + r() * .1, .55 + r() * .2, .32 + r() * .14));
  }
  scene.add(W.grass);
  // ---- moss / meadow overlay on the road + sidewalks
  const meadowTex = canvasTex(1024, 256, (ctx, w, h) => { const q2 = rand(3); ctx.clearRect(0, 0, w, h); for (let i = 0; i < 2600; i++) { ctx.fillStyle = `hsla(${85 + q2() * 40},${45 + q2() * 25}%,${28 + q2() * 18}%,${.5 + q2() * .5})`; ctx.beginPath(); ctx.ellipse(q2() * w, q2() * h, 6 + q2() * 26, 4 + q2() * 14, q2() * 3, 0, 7); ctx.fill(); } }).tex;
  meadowTex.wrapS = meadowTex.wrapT = THREE.RepeatWrapping; meadowTex.repeat.set(6, 1.5);
  W.meadow = new THREE.Mesh(new THREE.PlaneGeometry(140, 17), new THREE.MeshStandardMaterial({ map: meadowTex, transparent: true, opacity: 0, roughness: 1, depthWrite: false }));
  W.meadow.rotation.x = -Math.PI / 2; W.meadow.position.set(20, .2, 0); W.meadow.renderOrder = 2; scene.add(W.meadow);
  // ---- snow cover
  W.snow = new THREE.Mesh(new THREE.PlaneGeometry(220, 26), new THREE.MeshStandardMaterial({ color: 0xf4f8ff, roughness: .7, transparent: true, opacity: 0, depthWrite: false }));
  W.snow.rotation.x = -Math.PI / 2; W.snow.position.set(0, .21, 0); W.snow.renderOrder = 3; scene.add(W.snow);
  const fl = []; for (let i = 0; i < 5000; i++) fl.push(r() * 60 - 30, r() * 20, r() * 30 - 15);
  W.flakes = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(fl, 3)), new THREE.PointsMaterial({ color: 0xffffff, size: .09, transparent: true, opacity: .9, depthWrite: false }));
  W.flakes.visible = false; W.flakeBase = fl.slice(); scene.add(W.flakes);
  // ---- vines climbing the facades (instanced leaves)
  const leafGeo = new THREE.PlaneGeometry(.75, .75);
  const NV = 9000; W.vines = new THREE.InstancedMesh(leafGeo, leafMats[2], NV); W.vines.frustumCulled = false;
  W.vineD = [];
  for (let i = 0; i < NV; i++) {
    const bi = Math.floor(r() * W.blocks.length), b = W.blocks[bi].userData; const col = Math.floor(r() * 6);
    const x = b.x + (col / 5 - .5) * b.w * .9 + (r() - .5) * 1.4, y = Math.pow(r(), 1.3) * b.h, z = b.front + (b.side) * (.06 + r() * .15);
    W.vineD.push({ x, y, z, h: b.h, rz: r() * 6.28, s: .6 + r() * .8, side: b.side, blk: W.blocks[bi] });
    W.vines.setColorAt(i, gc.setHSL(.24 + r() * .1, .5 + r() * .25, .25 + r() * .15));
  }
  W.vines.count = 0; scene.add(W.vines);
  // ---- crack decals on north + south fronts
  const crackTex = canvasTex(512, 512, (ctx, w, h) => { ctx.clearRect(0, 0, w, h); ctx.strokeStyle = 'rgba(30,20,25,.85)'; ctx.lineCap = 'round'; const q3 = rand(12);
    const br = (x, y, a, l, wd) => { if (l < 8) return; ctx.lineWidth = wd; ctx.beginPath(); ctx.moveTo(x, y); let cx = x, cy = y; for (let k = 0; k < 6; k++) { cx += Math.cos(a) * l / 6 + (q3() - .5) * 10; cy += Math.sin(a) * l / 6 + (q3() - .5) * 10; ctx.lineTo(cx, cy); } ctx.stroke(); br(cx, cy, a + (q3() - .5) * 1.4, l * .6, wd * .7); if (q3() > .4) br(cx, cy, a + (q3() - .5) * 2, l * .5, wd * .6); };
    br(w / 2, 0, Math.PI / 2, 300, 7); br(w / 2, 0, Math.PI / 2 + .6, 200, 5); }).tex;
  W.cracks = [];
  for (const b of W.blocks) { const u = b.userData; for (let k = 0; k < 3; k++) { const c = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 3.4), new THREE.MeshBasicMaterial({ map: crackTex, transparent: true, opacity: 0, depthWrite: false, color: 0x5a4a50 }));
    c.position.set(u.x + (r() - .5) * u.w * .7, 3 + r() * (u.h - 5), u.front + u.side * .03); c.rotation.set(0, u.side > 0 ? 0 : Math.PI, (r() - .5) * .8); scene.add(c); W.cracks.push(c); } }
  { const hero = W.blocks.find(b => b.userData.side < 0 && Math.abs(b.userData.x - 44) < 1); if (hero) { const u = hero.userData;
    [[-2.5, 5.5, .3, 4.2], [2.2, 8.5, -.4, 3.6], [-.5, 3.4, .9, 2.8], [3.4, 4.6, .1, 3]].forEach(([dx, y, rz, s2]) => { const c = new THREE.Mesh(new THREE.PlaneGeometry(s2, s2), new THREE.MeshBasicMaterial({ map: crackTex, transparent: true, opacity: 0, depthWrite: false, color: 0x3a2a30 }));
      c.position.set(u.x + dx, y, u.front - .04); c.rotation.set(0, Math.PI, rz); scene.add(c); W.cracks.unshift(c); }); } }
  // ---- young/grown trees reclaiming the street
  W.wild = [];
  const trunkM = new THREE.MeshStandardMaterial({ color: 0x6a4a34, roughness: .95 });
  const leafMs = [0x3f9a3a, 0x58ad45, 0x2f8a3c, 0x6fb84a].map(c => new THREE.MeshStandardMaterial({ color: c, roughness: .85, flatShading: true }));
  const spots = [[24, 2.0], [16, 2.6], [9, -2.2], [4, 1.5], [20, 6.1], [28, -6.4], [13, -5.9], [48, 6.6], [52, -1.8], [58, 2.4], [62, -3], [55, 5.2], [50, -6.2], [26, -2.8], [19, -1.0], [46, 3.2], [66, .5], [1, -4.8], [30, -3.6], [57, -5.6]];
  spots.forEach(([x, z], i) => {
    const g = new THREE.Group(); const hh = 4 + r() * 4;
    const tr = new THREE.Mesh(new THREE.CylinderGeometry(.12, .3, hh, 8), trunkM); tr.position.y = hh / 2; tr.castShadow = true; g.add(tr);
    for (let k = 0; k < 4; k++) { const rad = 1.3 + r() * .9; const lb = crown(rad, i * 13 + k, (i + k) % 3); lb.position.set((r() - .5) * 2.2, hh - .2 + r() * 2 + k * .3, (r() - .5) * 2.2); g.add(lb); }
    g.position.set(x, 0, z); g.userData = { birth: i === 0 ? 8 : 9 + i * 1.2 + r() * 4, full: i === 0 ? 28 : 45 + r() * 30 }; g.visible = false; scene.add(g); W.wild.push(g);
  });
  // ---- props
  W.cup = coffeeCup(); scene.add(W.cup); W.cup.visible = false;
  W.lid = cupLid(); scene.add(W.lid); W.lid.visible = false;
  W.splash = new THREE.Mesh(new THREE.CircleGeometry(.28, 24), new THREE.MeshStandardMaterial({ color: 0x4a2a16, roughness: .2, transparent: true, opacity: .9, depthWrite: false })); W.splash.rotation.x = -Math.PI / 2; W.splash.visible = false; scene.add(W.splash);
  W.sparkle = sparkles(); scene.add(W.sparkle);
  W.subway = subwayEntrance(); W.subway.position.set(43.5, .18, 6.3); scene.add(W.subway);
  W.towers = coolingTowers(); scene.add(W.towers);
  W.dust = dustCloud(); scene.add(W.dust);
  W.debris = null;
  INK.skip.push(W.grass, W.vines, W.flakes, W.sparkle, W.meadow, W.snow, W.dust);
  setAge(0);
  return W;
}

// ------------------------------------------------------------------ the master "age" control (years since people vanished)
const dm = new THREE.Object3D(), m4b = new THREE.Matrix4(), pp = new THREE.Vector3(), qq = new THREE.Quaternion(), ss = new THREE.Vector3();
export function setAge(y, t = 0, opts = {}) {
  W.age = y;
  // window lights: on only in "night with power" (opts.lights 0..1 = fraction still on)
  const lights = opts.lights ?? 0, black = new THREE.Color(.05, .06, .08), white = new THREE.Color(1, 1, 1);
  const brokenF = clamp((y - 2) / 20) * .75;
  for (const w of W.win) {
    w.lit.visible = lights > 0;
    for (let i = 0; i < w.base.length; i++) {
      const b = w.base[i];
      if (lights > 0) { dm.matrix.copy(b.m); dm.matrix.decompose(pp, qq, ss); pp.z += w.side * .11; dm.position.copy(pp); dm.quaternion.copy(qq); dm.scale.setScalar(b.on < lights * .85 ? 1 : 0); if (w.side < 0) dm.rotateY(Math.PI); dm.updateMatrix(); w.lit.setMatrixAt(i, dm.matrix); }
      w.g.setColorAt(i, b.br < brokenF ? black : white);
    }
    if (lights > 0) w.lit.instanceMatrix.needsUpdate = true;
    w.g.instanceColor.needsUpdate = true;
  }
  for (const l of W.lamps) { const m = l.userData.bulb.material; m.emissiveIntensity = (opts.lamps ?? (y < .01 ? .8 : 0)) * 2.2; m.color.set(opts.lamps > 0 ? 0xfff6d8 : 0x55575e); }
  // grass
  let n = 0;
  for (const g of W.grassD) { const k = clamp((y - g.birth * .25) / Math.max(.2, g.birth * .4 + .3)); if (k <= 0) continue; dm.position.set(g.x, .18, g.z); dm.rotation.set(Math.sin(t * 1.3 + g.x) * .06, g.ry, 0); dm.scale.setScalar(g.s * eOut(k) * (1 + clamp((y - 10) / 60) * .4)); dm.updateMatrix(); W.grass.setMatrixAt(n, dm.matrix); W.grass.setColorAt && 0; n++; }
  W.grass.count = n; W.grass.instanceMatrix.needsUpdate = true; W.grass.visible = n > 0 && !(opts.snow > 0);
  W.meadow.material.opacity = clamp((y - 3) / 25) * .95;
  // vines climb ~ up to the roofline in ~80 years
  const vh = clamp((y - 3) / 80); let nv = 0;
  for (const v of W.vineD) { if (v.y > vh * v.h * 1.05 || !v.blk.visible) continue; dm.position.set(v.x, v.y, v.z); dm.rotation.set(0, v.side > 0 ? 0 : Math.PI, v.rz); dm.scale.setScalar(v.s * clamp((vh * v.h - v.y) / 1.5 + .3)); dm.updateMatrix(); W.vines.setMatrixAt(nv++, dm.matrix); }
  W.vines.count = nv; W.vines.instanceMatrix.needsUpdate = true;
  // cracks, moss, rust
  W.cracks.forEach((c, i) => c.material.opacity = clamp((y - 2.2 - Math.max(0, i - 4) * .4) / 1.2) * .95);
  const moss = clamp((y - 5) / 80) * .45, mossC = new THREE.Color(0x7d9a5a);
  W.facades.forEach(m => { if (m.userData.c0) m.color.copy(m.userData.c0).lerp(mossC, moss); });
  const rust = clamp((y - .5) / 30), rustC = new THREE.Color(0x7a4a2e);
  W.carPaint.forEach(m => { if (m) { m.color.copy(m.userData.c0).lerp(rustC, rust * .8); m.roughness = lerp(.25, 1, rust); m.metalness = lerp(.6, .1, rust); m.clearcoat = lerp(1, 0, rust); } });
  // wild trees
  for (const g of W.wild) { const k = clamp((y - g.userData.birth) / g.userData.full); g.visible = k > 0; g.scale.setScalar(.15 + .85 * eOut(k)); }
  // snow (opts.snow 0..1)
  const sn = opts.snow ?? 0; W.snow.material.opacity = sn * .92; W.flakes.visible = sn > 0;
  if (sn > 0) { const a = W.flakes.geometry.attributes.position; for (let i = 0; i < a.count; i++) { const b = W.flakeBase; a.setXYZ(i, b[i * 3] + Math.sin(t + i) * .3 + (opts.cx ?? 0), ((b[i * 3 + 1] - t * 1.2) % 20 + 20) % 20, b[i * 3 + 2] + (opts.cz ?? 0)); } a.needsUpdate = true; }
}

// ------------------------------------------------------------------ props
function std(c, o = {}) { return new THREE.MeshStandardMaterial({ color: c, roughness: .6, ...o }); }
function coffeeCup() {
  const g = new THREE.Group();
  const c = new THREE.Mesh(new THREE.CylinderGeometry(.075, .055, .2, 32), std(0xf6f4ee, { roughness: .4 }));
  const sl = new THREE.Mesh(new THREE.CylinderGeometry(.078, .066, .08, 32), std(0x1d6b52, { roughness: .8 })); sl.position.y = -.01;
  const lid = new THREE.Mesh(new THREE.CylinderGeometry(.082, .08, .025, 32), std(0x2a2a2e, { roughness: .35 })); lid.position.y = .11;
  g.add(c, sl, lid); g.traverse(o => { if (o.isMesh) o.castShadow = true; }); return g;
}
function cupLid() {
  const g = new THREE.Group(); const l = new THREE.Mesh(new THREE.CylinderGeometry(.082, .08, .025, 32), std(0xf2f2f2, { roughness: .35 }));
  const sip = new THREE.Mesh(new THREE.CylinderGeometry(.04, .045, .02, 20), std(0x2a2a2e)); sip.position.set(.03, .02, 0); g.add(l, sip); g.scale.setScalar(2.2); return g;
}
function sparkles() {
  const n = 60, a = []; const r = rand(31); for (let i = 0; i < n; i++) a.push(0, 0, 0);
  const pts = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(a, 3)), new THREE.PointsMaterial({ color: 0xfff1b0, size: .12, transparent: true, depthWrite: false, toneMapped: false }));
  pts.userData.dir = Array.from({ length: n }, () => V(r() - .5, r() * .9, r() - .5).normalize().multiplyScalar(.8 + r() * 1.4)); pts.visible = false; return pts;
}
export function poof(center, k) { // k: 0..1 seconds-ish progress
  const p = W.sparkle; p.visible = k > 0 && k < 1; if (!p.visible) return;
  const a = p.geometry.attributes.position; p.userData.dir.forEach((d, i) => a.setXYZ(i, center.x + d.x * eOut(k) * 1.4, center.y + d.y * eOut(k) * 1.4, center.z + d.z * eOut(k) * 1.4)); a.needsUpdate = true;
  p.material.opacity = 1 - k; p.material.size = .16 * (1 - k * .5);
}
function subwayEntrance() {
  const g = new THREE.Group();
  const rail = std(0x2e7d4f, { roughness: .4, metalness: .5 });
  const stepTex = canvasTex(256, 512, (ctx, w, h) => { for (let i = 0; i < 16; i++) { const v = 70 - i * 4; ctx.fillStyle = `rgb(${v},${v + 2},${v + 8})`; ctx.fillRect(0, i * h / 16, w, h / 16 - 3); ctx.fillStyle = '#c9a23a'; ctx.fillRect(0, i * h / 16 + h / 16 - 6, w, 3); } }).tex;
  const pit = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 3.4), new THREE.MeshStandardMaterial({ map: stepTex, roughness: .9 })); pit.rotation.x = -Math.PI / 2; pit.position.y = .012; g.add(pit);
  const rails = [[0, .5, 1.75, 1.9, .05], [.95, .5, 0, .05, 3.5], [-.95, .5, 0, .05, 3.5]];
  rails.forEach(([x, y, z, w, d]) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, .06, d), rail); m.position.set(x, y + .5, z); g.add(m); const m2 = m.clone(); m2.position.y = .55; g.add(m2); });
  for (const [x, z] of [[.95, 1.75], [-.95, 1.75], [.95, -1.7], [-.95, -1.7], [.95, 0], [-.95, 0]]) { const po = new THREE.Mesh(new THREE.CylinderGeometry(.04, .04, 1.05, 10), rail); po.position.set(x, .52, z); g.add(po); }
  for (const x of [.95, -.95]) { const p = new THREE.Mesh(new THREE.CylinderGeometry(.05, .06, 2.4, 12), rail); p.position.set(x, 1.2, -1.7); g.add(p); const gl = new THREE.Mesh(new THREE.SphereGeometry(.2, 24, 16), new THREE.MeshStandardMaterial({ color: 0x9ff0b0, emissive: 0x5adf7a, emissiveIntensity: .6 })); gl.position.set(x, 2.5, -1.7); g.add(gl); g.userData.globes = (g.userData.globes || []).concat(gl); }
  const signT = canvasTex(512, 128, (ctx, w, h) => { ctx.fillStyle = '#1b1d24'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#fff'; ctx.font = `${h * .55}px IDB`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('SUBWAY', w / 2, h / 2 + 4); ctx.fillStyle = '#2e7d4f'; ctx.beginPath(); ctx.arc(60, h / 2, 34, 0, 7); ctx.fill(); ctx.fillStyle = '#fff'; ctx.font = `${h * .45}px IDB`; ctx.fillText('4', 60, h / 2 + 3); }).tex;
  const sign = new THREE.Mesh(new THREE.BoxGeometry(2.1, .5, .08), [std(0x1b1d24), std(0x1b1d24), std(0x1b1d24), std(0x1b1d24), new THREE.MeshStandardMaterial({ map: signT, emissive: 0xffffff, emissiveMap: signT, emissiveIntensity: .25 }), std(0x1b1d24)]);
  sign.position.set(0, 2.15, -1.7); sign.rotation.y = Math.PI; g.add(sign);
  // water: rises in the pit, then spills onto the sidewalk and street
  g.userData.water = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 3.4), new THREE.MeshPhysicalMaterial({ color: 0x3a6a7a, roughness: .05, metalness: .1, clearcoat: 1, transparent: true, opacity: .85 })); g.userData.water.rotation.x = -Math.PI / 2; g.add(g.userData.water);
  g.userData.puddle = new THREE.Mesh(new THREE.CircleGeometry(1, 48), g.userData.water.material); g.userData.puddle.rotation.x = -Math.PI / 2; g.userData.puddle.position.y = .03; g.add(g.userData.puddle);
  g.traverse(o => { if (o.isMesh) o.castShadow = o.receiveShadow = true; });
  return g;
}
export function flood(k, t) { // 0..1
  const w = W.subway.userData.water, p = W.subway.userData.puddle;
  w.visible = k > 0; w.position.y = lerp(.0, .03, clamp(k * 2)); w.material.opacity = clamp(k * 3) * .85;
  const sp = clamp((k - .35) / .65); p.visible = sp > 0; p.scale.set(1 + sp * 5, 1 + sp * 3.2, 1); p.position.set(-sp * .6, .03, -sp * 2.2);
}
function coolingTowers() {
  const g = new THREE.Group();
  const pts = []; for (let i = 0; i <= 20; i++) { const y = i / 20; const r = 1 - .42 * Math.sin(Math.min(1, y / .78) * Math.PI * .5) + (y > .78 ? (y - .78) * .6 : 0); pts.push(new THREE.Vector2(r * 22, y * 60)); }
  const geo = new THREE.LatheGeometry(pts, 48); const mat = std(0xcfc8bf, { roughness: .9, side: THREE.DoubleSide });
  for (const [x, z] of [[300, -40], [340, -12]]) { const t = new THREE.Mesh(geo, mat); t.position.set(x, 0, z); t.scale.setScalar(1.3); g.add(t); }
  // steam puffs (billboards)
  const puffTex = canvasTex(256, 256, (ctx, w, h) => { const gr = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); gr.addColorStop(0, 'rgba(255,255,255,.95)'); gr.addColorStop(.6, 'rgba(240,240,245,.6)'); gr.addColorStop(1, 'rgba(240,240,245,0)'); ctx.fillStyle = gr; ctx.fillRect(0, 0, w, h); }).tex;
  g.userData.puffs = [];
  for (let i = 0; i < 26; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTex, transparent: true, depthWrite: false, color: 0xf0eeea })); g.add(s); g.userData.puffs.push({ s, x: i % 2 ? 300 : 340, z: i % 2 ? -40 : -12, ph: i / 26 }); }
  g.visible = false; return g;
}
export function towers(on, t, glow = 0) {
  W.towers.visible = on; if (!on) return;
  for (const p of W.towers.userData.puffs) { const k = (p.ph + t * .08) % 1; p.s.position.set(p.x + k * 22, 80 + k * 80, p.z + Math.sin(p.ph * 9) * 8); p.s.scale.setScalar(26 + k * 60); p.s.material.opacity = (1 - k) * .9; p.s.material.color.setRGB(1, 1 - glow * .3 * (1 - k), 1 - glow * .5 * (1 - k)); }
}
function dustCloud() {
  const tex = canvasTex(256, 256, (ctx, w, h) => { const gr = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); gr.addColorStop(0, 'rgba(210,190,170,.9)'); gr.addColorStop(1, 'rgba(210,190,170,0)'); ctx.fillStyle = gr; ctx.fillRect(0, 0, w, h); }).tex;
  const g = new THREE.Group(); const r = rand(77); g.userData.p = [];
  for (let i = 0; i < 40; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false })); g.add(s); g.userData.p.push({ s, d: V(r() - .5, r() * .5, r() - .5).normalize(), sp: 4 + r() * 10, sz: 4 + r() * 6 }); }
  g.visible = false; return g;
}

// ------------------------------------------------------------------ building collapse
export function collapse(block, k, t) { // k: 0..1 progress (0 = standing)
  const u = block.userData;
  if (!W.debris || W.debris.userData.block !== block) {
    if (W.debris) scene.remove(W.debris);
    const g = new THREE.Group(); g.userData.block = block; const r = rand(9); g.userData.ch = [];
    const nx = 5, ny = 7, nz = 3, cw = u.w / nx, chh = u.h / ny, cd = u.d / nz;
    for (let ix = 0; ix < nx; ix++) for (let iy = 0; iy < ny; iy++) for (let iz = 0; iz < nz; iz++) {
      const m = new THREE.Mesh(new THREE.BoxGeometry(cw * .98, chh * .98, cd * .98), u.facade); m.castShadow = m.receiveShadow = true;
      const p0 = V(u.x + (ix + .5) * cw - u.w / 2, (iy + .5) * chh, u.z + (iz + .5) * cd - u.d / 2);
      const p1 = V(p0.x + (r() - .5) * 4, .4 + r() * 1.2 + iy * .3 + iz * .2, p0.z + u.side * (r() * 3.5));
      g.add(m); g.userData.ch.push({ m, p0, p1, delay: (ny - iy) / ny * .3 + r() * .15, rot: V(r() - .5, r() - .5, r() - .5).multiplyScalar(3) });
    }
    W.debris = g; scene.add(g);
  }
  block.visible = k <= 0; W.debris.visible = k > 0;
  for (const c of W.debris.userData.ch) { const q = eOut(clamp((k - c.delay) / (1 - c.delay + .001))); const fall = q * q; c.m.position.lerpVectors(c.p0, c.p1, q); c.m.position.y = lerp(c.p0.y, c.p1.y, fall); c.m.rotation.set(c.rot.x * q, c.rot.y * q, c.rot.z * q); }
  // dust
  W.dust.visible = k > .05 && k < 1.6;
  if (W.dust.visible) W.dust.userData.p.forEach(p => { const q = clamp((k - .05) / 1.2); p.s.position.set(u.x + p.d.x * p.sp * q * 1.5, 1 + p.d.y * p.sp * q + q * 3, u.z + u.side * 6 + p.d.z * p.sp * q); p.s.scale.setScalar(p.sz * (.5 + q * 1.5)); p.s.material.opacity = .85 * (1 - clamp((k - .6) / 1)); });
}
export function debrisPile(block) { collapse(block, 1, 0); W.dust.visible = false; }
export function resetCollapse() { if (W.debris) { W.debris.userData.block.visible = true; W.debris.visible = false; } W.dust.visible = false; }

// ------------------------------------------------------------------ animals (v4: smooth anatomy + fur texture)
let furTex = null;
function FUR() { if (furTex) return furTex; furTex = canvasTex(256, 256, (ctx, w, h) => { ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, w, h); const q = rand(55);
  for (let i = 0; i < 3500; i++) { const x = q() * w, y = q() * h, l = 4 + q() * 9, v = 170 + q() * 85; ctx.strokeStyle = `rgba(${v},${v},${v},.55)`; ctx.lineWidth = 1 + q(); ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + (q() - .5) * 3, y + l); ctx.stroke(); } }).tex;
  furTex.wrapS = furTex.wrapT = THREE.RepeatWrapping; furTex.repeat.set(3, 3); return furTex; }
export function makeAnimal(kind) {
  const P = {
    dog:  { len: .75, bh: .32, leg: .36, body: 0xc9884a, belly: 0xf0dcc0, head: .2, snout: .16, ear: 'flop', tail: .3, neck: .12 },
    dog2: { len: .7, bh: .3, leg: .32, body: 0x3a3536, belly: 0xe8e2da, head: .19, snout: .14, ear: 'up', tail: .28, neck: .12 },
    wolf: { len: 1.05, bh: .38, leg: .55, body: 0x8a8c94, belly: 0xd9d6d2, head: .23, snout: .2, ear: 'up', tail: .5, neck: .16 },
    deer: { len: 1.15, bh: .42, leg: .78, body: 0xa8703f, belly: 0xf2e6d2, head: .2, snout: .16, ear: 'big', tail: .12, neck: .5, antler: true },
    doe:  { len: 1.05, bh: .4, leg: .74, body: 0xb27a46, belly: 0xf2e6d2, head: .19, snout: .15, ear: 'big', tail: .12, neck: .45 },
  }[kind];
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const mb = new THREE.MeshStandardMaterial({ color: P.body, map: FUR(), roughness: .9 }), mbe = new THREE.MeshStandardMaterial({ color: P.belly, map: FUR(), roughness: .9 }), dark = std(0x1d1a1c, { roughness: .3 });
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(1, 1.6, 12, 24), mb); torso.rotation.x = Math.PI / 2; torso.scale.set(P.bh * .78, P.len / 3.6, P.bh * .85); torso.position.y = P.leg + P.bh * .6; body.add(torso);
  const belly = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), mbe); belly.scale.set(P.bh * .75, P.bh * .6, P.len * .4); belly.position.set(0, P.leg + P.bh * .35, 0); body.add(belly);
  const neckG = new THREE.Group(); neckG.position.set(0, P.leg + P.bh * .9, P.len * .42); body.add(neckG);
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(P.bh * .32, P.bh * .45, P.neck + .15, 12), mb); neck.position.y = (P.neck + .15) / 2; neck.rotation.x = .5; neckG.add(neck);
  const head = new THREE.Group(); head.position.set(0, P.neck + .12, (P.neck + .15) * .45); neckG.add(head);
  const hd = new THREE.Mesh(new THREE.SphereGeometry(P.head, 32, 24), mb); hd.scale.set(.85, .9, 1.05); head.add(hd);
  const sn = new THREE.Mesh(new THREE.CapsuleGeometry(P.head * .38, P.head * .7, 8, 16), mbe); sn.rotation.x = Math.PI / 2 - .15; sn.scale.set(1, 1, .85); sn.position.set(0, -P.head * .25, P.head * .85); head.add(sn);
  const nose = new THREE.Mesh(new THREE.SphereGeometry(P.head * .2, 12, 8), dark); nose.position.set(0, -P.head * .12, P.head * 1.55); head.add(nose);
  for (const s of [-1, 1]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(P.head * .17, 12, 8), dark); eye.position.set(s * P.head * .5, P.head * .2, P.head * .62); head.add(eye);
    const hl = new THREE.Mesh(new THREE.SphereGeometry(P.head * .06, 8, 6), std(0xffffff)); hl.position.set(s * P.head * .5 - .01, P.head * .27, P.head * .78); head.add(hl);
    let ear;
    if (P.ear === 'flop') { ear = new THREE.Mesh(new THREE.SphereGeometry(P.head * .45, 12, 8), std(0x8a5a30, { roughness: .8 })); ear.scale.set(.35, 1, .7); ear.position.set(s * P.head * .9, -P.head * .1, 0); }
    else { const sz = P.ear === 'big' ? 1.4 : 1; ear = new THREE.Mesh(new THREE.ConeGeometry(P.head * .3 * sz, P.head * .8 * sz, 8), mb); ear.position.set(s * P.head * .6, P.head * .85, -P.head * .1); ear.rotation.z = -s * (P.ear === 'big' ? .9 : .25); }
    head.add(ear);
    if (P.antler) { const am = std(0xd9c7a2, { roughness: .7 }); const a1 = new THREE.Mesh(new THREE.CylinderGeometry(.018, .028, .45, 6), am); a1.position.set(s * .1, P.head + .18, -.02); a1.rotation.z = -s * .4; head.add(a1);
      for (let k = 0; k < 3; k++) { const t2 = new THREE.Mesh(new THREE.CylinderGeometry(.012, .018, .2, 6), am); t2.position.set(s * (.14 + k * .05), P.head + .12 + k * .12, .05); t2.rotation.set(.6, 0, -s * .1); head.add(t2); } }
  }
  const legs = [];
  for (const [sx, sz] of [[-1, 1], [1, 1], [-1, -1], [1, -1]]) {
    const piv = new THREE.Group(); piv.position.set(sx * P.bh * .55, P.leg + P.bh * .3, sz * P.len * .32); body.add(piv);
    const lg = new THREE.Mesh(new THREE.CapsuleGeometry(P.bh * .13, P.leg + P.bh * .1, 6, 12), mb); lg.scale.set(1, 1, 1.25); lg.position.y = -(P.leg + P.bh * .3) / 2; piv.add(lg);
    const hoof = new THREE.Mesh(new THREE.SphereGeometry(P.bh * .15, 8, 6), kind.startsWith('d') && kind !== 'dog' && kind !== 'dog2' ? dark : mbe); hoof.position.y = -(P.leg + P.bh * .3); piv.add(hoof);
    legs.push(piv);
  }
  const tailP = new THREE.Group(); tailP.position.set(0, P.leg + P.bh * .9, -P.len * .48); body.add(tailP);
  const tail = new THREE.Mesh(new THREE.ConeGeometry(P.bh * .16, P.tail, 8), kind.startsWith('d') && P.antler !== undefined || kind === 'doe' ? mbe : mb); tail.position.y = P.tail / 2; tailP.add(tail); tailP.rotation.x = kind === 'wolf' ? -2.3 : -.7;
  g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  g.userData = { legs, head, neckG, tailP, kind, P };
  // pose: walk phase (0 = still), graze 0..1, howl 0..1, bark 0..1
  g.pose = ({ walk = 0, ph = 0, graze = 0, howl = 0, wag = 0, t = 0 } = {}) => {
    legs.forEach((l, i) => l.rotation.x = walk * .55 * Math.sin(ph * Math.PI * 2 + (i === 0 || i === 3 ? 0 : Math.PI)));
    body.position.y = walk * .03 * Math.abs(Math.sin(ph * Math.PI * 2));
    neckG.rotation.x = graze * 1.25 - howl * .9; head.rotation.x = -howl * .5 + graze * .2;
    tailP.rotation.z = Math.sin(t * 14) * wag * .6;
  };
  return g;
}
