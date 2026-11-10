// Episode 12 — What if popcorn doubled every minute?  (v5 premium studio look; one continuous shot)
// Facts (checked 2026-11-10):
//  - one popcorn kernel ~0.13 g (10 kernels ≈ 1.3 g; PMC10287524 table 5); popping (expansion) volume ~41-47 cm³/g
//    for commercial hybrids (Cereal Chemistry 68:464, 1991) -> one popped piece ≈ 0.13 × 44 ≈ 5.7 cm³ of popcorn (bulk).
//  - volume after m minutes = 5.7 cm³ × 2^m (heap shown as a cone at a ~30° angle of repose).
//  - bathtub ~150-300 L; car ~4.5 × 1.8 × 1.5 m ≈ 12 m³; Olympic pool ≥ 50 × 25 × 2 m = 2,500 m³;
//    Great Pyramid ≈ 2.6 million m³ (Wikipedia); Burj Khalifa 828 m; Moon 2.196e10 km³, Earth 1.083e12 km³ (NASA fact sheets).
import { THREE, scene, camera, clamp, lerp, eOut, eInOut, K, makeCar } from './kit.js';
import { key, hemi, LOOK, GRADE, DOF, setEnv, draw, sky } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd, jeremy, bathtub, pool, pyramid, planets } from './studio.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { canvasTex, rand } from './engine.js';

await bootStudio('WHAT IF POPCORN DOUBLED?', 'EP. 12');
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const PIECE_DETAIL = 2; const PIECE = 5.7e-6;                          // m³ per popped piece (bulk)
const vol = m => PIECE * Math.pow(2, m);
const CONE = Math.PI / 3 * Math.tan(Math.PI / 6); // V = CONE · R³  (30° heap)
const heapR = m => Math.cbrt(vol(m) / CONE), heapH = R => R * Math.tan(Math.PI / 6);

// ---------- popcorn piece (smooth lumpy cluster, cream with a few brown hull flecks) ----------
function pieceGeo(seed) {
  const r = rand(seed), parts = [];
  const add = (x, y, z, s, col) => { const g = new THREE.IcosahedronGeometry(s, PIECE_DETAIL); const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) { const v = V(p.getX(i), p.getY(i), p.getZ(i)); const n = 1 + .18 * Math.sin(v.x * 300 + seed) * Math.sin(v.y * 260) * Math.sin(v.z * 280 + 1); p.setXYZ(i, v.x * n, v.y * n, v.z * n); }
    g.computeVertexNormals(); g.translate(x, y, z); const c = new THREE.Color(col), a = new Float32Array(p.count * 3); for (let i = 0; i < p.count; i++) { a[i * 3] = c.r; a[i * 3 + 1] = c.g; a[i * 3 + 2] = c.b; } g.setAttribute('color', new THREE.BufferAttribute(a, 3)); parts.push(g); };
  for (let k = 0; k < 6; k++) add((r() - .5) * .018, (r() - .3) * .012, (r() - .5) * .018, .006 + r() * .005, k % 3 ? 0xfff3cf : 0xf7dc95);
  add((r() - .5) * .008, -.004, (r() - .5) * .008, .0035, 0x8a5a2a);
  return mergeGeometries(parts);
}
const pMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .6, emissive: 0x3a2a10, emissiveIntensity: .25 });
const PG = [pieceGeo(1), pieceGeo(2), pieceGeo(3)];
const NP = 2048, pieces = PG.map(g => { const m = new THREE.InstancedMesh(g, pMat, NP); m.castShadow = m.receiveShadow = true; m.frustumCulled = false; scene.add(m); return m; });
// positions inside a 30° cone, ordered so the first n always form a smaller similar heap
const RMAX = heapR(11) * 1.02, HMAX = heapH(RMAX), pts = [];
{ const r = rand(9); while (pts.length < NP * 3) { const x = (r() * 2 - 1) * RMAX, z = (r() * 2 - 1) * RMAX, y = r() * HMAX, rr = Math.hypot(x, z); if (rr / RMAX + y / HMAX > 1) continue;
    pts.push({ p: V(x, y + .011, z), k: rr / RMAX + y / HMAX, rot: [r() * 6, r() * 6, r() * 6], s: .85 + r() * .35 }); }
  pts.sort((a, b) => a.k - b.k); pts.length = NP * 3; }
const dm = new THREE.Object3D();
function showPieces(n, fall = 1) {
  const c = [0, 0, 0];
  for (let i = 0; i < Math.min(n, NP * 3); i++) { const q = pts[i], b = i % 3, f = i === Math.floor(n) - 1 ? fall : 1;
    dm.position.copy(q.p); dm.position.y += (1 - f) * .25; dm.rotation.set(...q.rot); dm.scale.setScalar(q.s); dm.updateMatrix(); pieces[b].setMatrixAt(c[b]++, dm.matrix); }
  pieces.forEach((m, b) => { m.count = c[b]; m.instanceMatrix.needsUpdate = true; m.visible = c[b] > 0; });
}
// ---------- the big heap (volume-true cone with a popcorn texture) ----------
const popTex = canvasTex(1024, 1024, (ctx, w, h) => { const r = rand(31); ctx.fillStyle = '#e9dcbc'; ctx.fillRect(0, 0, w, h);
  for (let i = 0; i < 2600; i++) { const x = r() * w, y = r() * h, s = 10 + r() * 16, l = 82 + r() * 12; const g = ctx.createRadialGradient(x - s * .3, y - s * .3, 1, x, y, s);
    g.addColorStop(0, `hsl(44,70%,${l + 6}%)`); g.addColorStop(.7, `hsl(42,55%,${l - 8}%)`); g.addColorStop(1, 'hsla(35,40%,45%,.0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, s, 0, 7); ctx.fill();
    if (r() < .12) { ctx.fillStyle = 'rgba(120,75,35,.7)'; ctx.beginPath(); ctx.ellipse(x + s * .3, y + s * .2, s * .25, s * .15, r() * 3, 0, 7); ctx.fill(); } } }).tex;
popTex.wrapS = popTex.wrapT = THREE.RepeatWrapping;
const heapGeo = (() => { const p = []; for (let i = 0; i <= 24; i++) { const u = i / 24; const rr = 1 - u; const y = u + .06 * Math.sin(u * Math.PI) - (u > .92 ? (u - .92) * 1.6 : 0); p.push(new THREE.Vector2(Math.max(0, rr) * 1, y * Math.tan(Math.PI / 6))); } return new THREE.LatheGeometry(p, 96); })();
{ const p = heapGeo.attributes.position, r = rand(3); for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i); const n = 1 + .008 * Math.sin(x * 37 + z * 23) * Math.sin(z * 41 - x * 13); p.setXYZ(i, x * n, y * (1 + .008 * Math.sin(x * 50)), z * n); } heapGeo.computeVertexNormals(); }
const heap = new THREE.Mesh(heapGeo, new THREE.MeshStandardMaterial({ map: popTex, bumpMap: popTex, bumpScale: 2, roughness: .8 })); heap.castShadow = heap.receiveShadow = true; scene.add(heap);
const ball = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), new THREE.MeshStandardMaterial({ map: popTex, bumpMap: popTex, bumpScale: 2, roughness: .85 })); scene.add(ball);

// ---------- scale references ----------
const bowl = (() => { const p = []; for (let i = 0; i <= 16; i++) { const a = i / 16 * Math.PI / 2; p.push(new THREE.Vector2(.075 * Math.sin(a) + .005, .07 * (1 - Math.cos(a)))); } p.push(new THREE.Vector2(.074, .07)); for (let i = 16; i >= 0; i--) { const a = i / 16 * Math.PI / 2; p.push(new THREE.Vector2(.069 * Math.sin(a), .006 + .066 * (1 - Math.cos(a)))); }
  const m = new THREE.Mesh(new THREE.LatheGeometry(p, 64), new THREE.MeshPhysicalMaterial({ color: 0x2f5e7a, roughness: .25, clearcoat: .6, side: THREE.DoubleSide })); m.castShadow = m.receiveShadow = true; return m; })();
const tub = bathtub(), car = makeCar(0x9fb3cc), olympic = pool(), pyr = pyramid();
const burj = (() => { const g = new THREE.Group(), glass = new THREE.MeshPhysicalMaterial({ color: 0x9fb4c8, metalness: .6, roughness: .15, clearcoat: 1 });
  [[0, 300, 32], [300, 520, 22], [520, 650, 14], [650, 700, 8], [700, 828, 2]].forEach(([a, b, r]) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r * .8, r, b - a, 24), glass); m.position.y = (a + b) / 2; m.castShadow = true; g.add(m); });
  return g; })();
car.traverse(o => { if (o.isMesh) o.castShadow = true; });
[bowl, tub, car, olympic, pyr, burj].forEach(o => scene.add(o));
const SPACE = planets(); scene.add(SPACE); SPACE.visible = false; const SPACE_BG = new THREE.Color(0x0a0a0c);
const stars = (() => { const a = [], r = rand(5); for (let i = 0; i < 3000; i++) { const th = r() * 6.283, ph = Math.acos(2 * r() - 1), d = 9e5; a.push(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d, Math.sin(ph) * Math.sin(th) * d); }
  return new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(a, 3)), new THREE.PointsMaterial({ color: 0xffffff, size: 1.4, sizeAttenuation: false, fog: false })); })();
scene.add(stars); stars.visible = false;

// ---------- timeline: minute as a continuous function of time ----------
const KEYS = [[0, 0], [2.2, 0], [4.6, 6], [7.0, 10], [10.0, 15], [13.0, 21], [16.0, 23], [19.4, 29], [23.0, 39], [26.6, 50], [30.0, 72], [33.4, 82], [36.4, 88], [43, 88]];
function minuteAt(t) { for (let i = 1; i < KEYS.length; i++) { const [t0, m0] = KEYS[i - 1], [t1, m1] = KEYS[i]; if (t <= t1) { const k = eInOut(clamp((t - t0) / (t1 - t0))); return lerp(m0, m1, k); } } return 88; }
const LINES = [[0, 'One piece of popcorn.'], [6, 'Minute 6: a bowlful.'], [10, 'Minute 10: a bucket.'], [15, 'Minute 15: a full bathtub.'], [21, 'Minute 21: as big as a car.'],
  [23, 'Minute 23: taller than Jeremy.'], [29, 'Minute 29: more than an Olympic pool.'], [39, 'Minute 39: more than the Great Pyramid.'], [50, 'Minute 50: taller than the Burj Khalifa.'],
  [72, 'Minute 72: a popcorn moon.'], [82, 'Minute 82: bigger than the Moon.'], [88, 'Minute 88: bigger than EARTH.']];
const lineAt = m => { let s = LINES[0], k = 0; for (const L of LINES) if (m >= L[0]) s = L; return s; };
const comma = n => Math.round(n).toLocaleString('en-US');
const WORDS = [[1e24, 'septillion'], [1e21, 'sextillion'], [1e18, 'quintillion'], [1e15, 'quadrillion'], [1e12, 'trillion'], [1e9, 'billion'], [1e6, 'million']];
const big = n => { for (const [d, w] of WORDS) if (n >= d) return (n / d).toFixed(n / d >= 100 ? 0 : 1).replace(/\.0$/, '') + ' ' + w; return comma(n); };
function fmtVol(v) {
  if (v < 1e-3) return (v * 1e6).toFixed(v < 1e-5 ? 1 : 0) + ' cm³';
  if (v < 1) return (v * 1000).toFixed(v < .01 ? 1 : 0) + ' litres';
  if (v < 1e7) return comma(v) + ' m³';
  if (v < 1e9) return big(v) + ' m³';
  return big(v / 1e9) + ' km³';
}

// smooth framing size (log-interpolated) so the camera never jumps
const REF = [[0, .045], [3, .06], [6, .22], [10, .4], [13, 1.2], [15, 1.7], [19, 3.6], [21, 4.4], [25, 9], [29, 46], [33, 60], [39, 230], [45, 420], [50, 800], [60, 3000]];
function refAt(m) { for (let i = 1; i < REF.length; i++) { const [m0, r0] = REF[i - 1], [m1, r1] = REF[i]; if (m <= m1) return Math.exp(lerp(Math.log(r0), Math.log(r1), eInOut(clamp((m - m0) / (m1 - m0))))); } return 3000; }
const total = 42.5, endAt = 38.6;
window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: 29.6, name: 'room', gain: .14 }, { t0: 29.4, t1: total, name: 'space', gain: .22 }],
  sfx: [{ t: .25, name: 'kpop', gain: .55 }, { t: 2.3, name: 'pops', gain: .4 }, { t: 5.2, name: 'pops', gain: .3 },
    ...[10.0, 13.0, 19.4, 23.0, 26.6, 33.4, 36.4].map(t => ({ t: t - .3, name: 'swell', gain: .28 })), { t: 29.3, name: 'wind_gust', gain: .18 }, { t: endAt, name: 'swell', gain: .35 }] };

window.renderAt = (t) => {
  tagsReset();
  const m = minuteAt(t), mi = Math.floor(m + 1e-6), n = Math.pow(2, m), V3 = vol(m);
  const space = t > 29.6;
  // ---- ground world
  const R = heapR(m), Hh = heapH(R);
  S.floor.visible = !space; stars.visible = space; SPACE.visible = space;
  [pieces[0], pieces[1], pieces[2]].forEach(p => p.visible = false); heap.visible = false; ball.visible = false;
  [bowl, tub, car, olympic, pyr, burj].forEach(o => o.visible = false);
  if (!space) {
    sky.visible = true; scene.background = null; LOOK.zenith.set('#5d5a57'); LOOK.horizon.set('#bdb8b1');
    if (m < 11.2) { const nn = Math.max(1, Math.round(n)); showPieces(nn, t < 1.0 ? eOut(clamp(t / .6)) : 1); }
    if (m > 10.6) { heap.visible = true; heap.scale.set(R, R, R); heap.material.map.repeat.set(Math.max(1, R * 4), Math.max(1, R * 1.2)); heap.material.bumpMap = heap.material.map; }
    if (m > 10.6 && m < 11.2) heap.scale.multiplyScalar(lerp(.9, 1, (m - 10.6) / .6));
    // scale refs: placed beside the heap, swallowed once the heap outgrows them
    const place = (o, mRef, size, ang = -.85) => { const d = heapR(mRef) * 1.2 + size * .6; o.position.set(Math.cos(ang) * d, 0, Math.sin(ang) * d); o.visible = R < d - size * .2; return o.position; };
    if (m > 3 && m < 12) place(bowl, 6, .16);
    if (m > 12 && m < 18) { const p = place(tub, 15, 1.6); tub.rotation.y = .6; if (tub.visible && m > 14) tag3('BATHTUB', '~200 litres', p.clone().add(V(0, .8, 0))); }
    if (m > 18 && m < 26) { const p = place(car, 21, 4.6, -.85); car.rotation.y = 2.2; if (car.visible && m < 23) tag3('CAR', '4.5 m · ~12 m³', p.clone().add(V(0, 1.9, 0))); }
    if (m > 25 && m < 34) { const p = place(olympic, 29, 52, -.8); if (olympic.visible && m > 27) tag3('OLYMPIC POOL', '2,500 m³', p.clone().add(V(0, 3, 0))); }
    if (m > 33 && m < 44) { const p = place(pyr, 39, 230, -.85); if (pyr.visible && m > 36) tag3('GREAT PYRAMID', '146 m · 2.6 million m³', p.clone().add(V(0, 160, 0))); }
    if (m > 43) { const p = place(burj, 50, 60, -.8); if (burj.visible && m > 46) tag3('BURJ KHALIFA', '828 m', p.clone().add(V(0, 850, 0))); }
    // Jeremy steps back as the pile grows
    const jd = R + 1.3; if (m > 16.5) jeremy(V(Math.cos(-1.75) * jd, 0, Math.sin(-1.75) * jd), -.35, { expr: m > 20 ? 'shocked' : 'happy', look: -.6, armL: m > 20 ? 2.3 : .2, armR: m > 20 ? 2.3 : .2, blink: (t % 3.1) < .1 });
    if (m > 17 && m < 33) tag3('JEREMY', '1.75 m', K.J.position.clone().add(V(0, 2.25, 0)), clamp((33 - m) / 2));
    // heap tag
    if (m > 22) tag3(comma(Math.min(n, 1e15)).length > 15 ? big(n) + ' PIECES' : comma(n) + ' PIECES', Hh >= 1000 ? `${comma(Hh / 1000)} km tall` : `${Hh >= 10 ? Math.round(Hh) : Hh.toFixed(1)} m tall`, V(0, Hh * 1.05, 0));
    // camera: one continuous pull-back that keeps the heap and its reference in frame
    const subj = Math.max(R, .02), ref = refAt(m);
    const size = Math.max(subj * 1.5, ref);
    const dist = size * 2.9 + .35, tgt = V(0, Math.max(Hh * .55, .015) + size * .32, 0);
    orbit(tgt, dist, { yaw: -.55 + t * .012, pitch: lerp(.4, .3, clamp(m / 40)), fov: 36 });
    floorScale(m < 24 ? 1 : m < 36 ? 10 : m < 46 ? 100 : 1000, Math.max(1, dist / 400));
    shadowFit(V(0, 0, 0), size * 1.4);
    DOF.on = m < 12; DOF.focus = camera.position.distanceTo(V(0, Hh * .5, 0)); DOF.aperture = .9; DOF.maxR = 10;
    scene.background = null;
  } else {
    // ---- space: a popcorn planet next to the Moon and Earth (to scale)
    K.J.visible = false; DOF.on = false;
    const RE = 6371, RM = 1737.4; const Rb = Math.cbrt(3 * V3 / (4 * Math.PI)) / 1000; // km
    const E = SPACE.userData.earth, Mo = SPACE.userData.moon; const u = 1 / 1000; // 1 unit = 1000 km
    E.scale.setScalar(RE * u); Mo.scale.setScalar(RM * u); ball.visible = true; ball.scale.setScalar(Rb * u);
    const gap = 1.2; E.position.set(0, 0, 0); Mo.position.set(0, (RE + RM) * u + gap, 0); ball.position.set(0, -(RE + Rb) * u - gap, 0);
    E.rotation.y = t * .04; SPACE.userData.clouds.rotation.y = t * .01; ball.rotation.y = t * .03; Mo.rotation.y = t * .02;
    sky.visible = false; scene.background = SPACE_BG; scene.fog.near = 1e6; scene.fog.far = 2e6;
    key.position.set(40, 12, 30); key.target.position.set(0, 0, 0); key.target.updateMatrixWorld(); key.intensity = 3.2; hemi.intensity = .06;
    const top = Mo.position.y + RM * u, bot = ball.position.y - Rb * u, hgt = top - bot, mid = (top + bot) / 2;
    const dist = hgt / (2 * Math.tan(18 * Math.PI / 180)) * 1.75;
    camera.position.set(dist * .18, mid + hgt * .3, dist); camera.lookAt(0, mid + hgt * .3, 0); camera.fov = 36; camera.near = .01; camera.far = 1e7; camera.updateProjectionMatrix();
    const endK = clamp((t - endAt) / .5);
    if (m > 80) tag3('MOON', '3,474 km wide', Mo.position.clone().add(V(RM * u + 2.4, RM * u * .3 + .6, 0)), 1 - endK);
    tag3('EARTH', '12,742 km wide', E.position.clone().add(V(RE * u * .95, RE * u * .55, 0)), (1 - endK) * clamp((t - 30.6) / .5));
    tag3('POPCORN', Math.round(Rb * 2).toLocaleString('en-US') + ' km wide', ball.position.clone().add(V(Rb * u + 2.4, Rb * u * .3 + .6, 0)), 1 - clamp((t - endAt) / .5));
  }
  if (!space) { key.intensity = 1.7; hemi.intensity = .4; }
  tagsEnd();
  // ---- HUD
  const L = lineAt(mi), lineK = clamp((m - L[0]) * 3 + .35);
  setHUD({ q: 'What if popcorn <b>doubled every minute</b>?', qA: clamp((t - .3) / .4) * (1 - clamp((t - endAt) / .5)),
    l1: 'MINUTE', n1: String(mi), l2: 'PIECES', n2: n < 1e6 ? comma(n) : big(n), l3: 'VOLUME', val: fmtVol(V3), line: L[1], lineA: L[0] === 0 ? clamp((t - .6) / .4) : lineK,
    dataA: 1 - clamp((t - endAt) / .4),
    end: 'All from <b>ONE</b> piece of popcorn.<br>What should double next? 👇', endA: clamp((t - endAt) / .6) });
  const fd = document.getElementById('v5fade'); fd.style.opacity = clamp(1 - Math.abs(t - 29.6) / .28);
  draw();
};
document.getElementById('ui').insertAdjacentHTML('afterbegin', '<div id="v5fade" style="position:absolute;inset:0;background:#0a0a0c;opacity:0"></div>');
window.READY = true;
