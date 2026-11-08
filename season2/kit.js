// Season 2 episode kit: street + space sets, Jeremy, shot helpers, speech bubble, spec-driven runner.
// An episode = spec (title, reel, beats) + build() for its own props + shot(t, beat, lt) per beat.
import { THREE, RoundedBoxGeometry, scene, camera, draw, setSun, aimSun, sky, bloom, renderer, canvasTex, rand, loadFont, renderCaptions, clamp, prog, lerp, eOut, eInOut } from './engine.js';
import { buildStreet, makePOVHands, makeCar } from './street.js';
import { makeJeremy2 } from './jeremy2.js';
import { setTitle, intro, counter, stageAt, flash } from './hud.js';
export { THREE, RoundedBoxGeometry, scene, camera, canvasTex, rand, clamp, prog, lerp, eOut, eInOut, makeCar, flash, aimSun, bloom };

export const V = (x, y, z) => new THREE.Vector3(x, y, z);
const $ = id => document.getElementById(id);
export const K = {}; // shared handles

// ---------- number formatting ----------
const BIG = [[1e30, 'nonillion'], [1e27, 'octillion'], [1e24, 'septillion'], [1e21, 'sextillion'], [1e18, 'quintillion'], [1e15, 'quadrillion'], [1e12, 'trillion'], [1e9, 'billion'], [1e6, 'million']];
export function fmtBig(v, unit = '', dec = 1) {
  for (const [d, w] of BIG) if (v >= d) { const x = v / d; return (x >= 100 ? Math.round(x) : x.toFixed(dec).replace(/\.0$/, '')) + ' ' + w + (unit ? ' ' + unit : ''); }
  if (v >= 100) return Math.round(v).toLocaleString('en-US') + (unit ? ' ' + unit : '');
  return (v >= 10 ? v.toFixed(1) : v.toFixed(2)).replace(/\.?0+$/, '') + (unit ? ' ' + unit : '');
}

// ---------- sets ----------
export async function boot(title, ep) {
  await document.fonts.load('80px IDB'); await document.fonts.load('80px IDBo'); await document.fonts.load('40px IM'); await loadFont();
  setTitle(title, ep);
  setSun(34, 215, 3.5, 1.2);
  K.street = buildStreet(scene);
  K.J = makeJeremy2(); scene.add(K.J); K.J.scale.setScalar(.75);
  K.hands = makePOVHands(); camera.add(K.hands); scene.add(camera);
  K.fog = scene.fog;
  buildSpace();
  return K;
}

// space set: Earth, Moon, stars, Sun light. Earth radius = 3 units.
export function earthCanvas(ocean = ['#1d4f9a', '#1565c0'], land = ['#3f8a3c', '#7a8b45']) {
  return canvasTex(2048, 1024, (ctx, w, h) => {
    const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, ocean[0]); g.addColorStop(.5, ocean[1]); g.addColorStop(1, ocean[0]); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    const r = rand(23); const blob = (cx, cy, s, col) => { for (let i = 0; i < 70; i++) { ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(cx + (r() - .5) * s * 1.6, cy + (r() - .5) * s, s * (.15 + r() * .3), s * (.12 + r() * .25), r() * 3, 0, 7); ctx.fill(); } };
    [[330, 330, 260], [520, 640, 200], [1060, 330, 230], [1120, 600, 220], [1500, 380, 320], [1700, 700, 140], [1000, 900, 300]].forEach(([x, y, s]) => { blob(x, y, s, land[0]); blob(x + 20, y + 10, s * .6, land[1]); });
    ctx.fillStyle = '#f2f6ff'; ctx.fillRect(0, 0, w, 50); ctx.fillRect(0, h - 70, w, 70);
  }).tex;
}
function buildSpace() {
  const G = new THREE.Group(); G.visible = false; scene.add(G); K.space = G;
  K.earthMat = new THREE.MeshStandardMaterial({ map: earthCanvas(), roughness: .85 });
  K.earth = new THREE.Mesh(new THREE.SphereGeometry(3, 128, 96), K.earthMat); G.add(K.earth);
  const cl = canvasTex(1024, 512, (ctx, w, h) => { const r = rand(77); for (let i = 0; i < 260; i++) { ctx.fillStyle = `rgba(255,255,255,${.15 + r() * .35})`; ctx.beginPath(); ctx.ellipse(r() * w, h * .1 + r() * h * .8, 10 + r() * 40, 3 + r() * 8, 0, 0, 7); ctx.fill(); } }).tex;
  K.clouds = new THREE.Mesh(new THREE.SphereGeometry(3.04, 96, 64), new THREE.MeshStandardMaterial({ map: cl, transparent: true, opacity: .55, depthWrite: false, roughness: 1 })); G.add(K.clouds);
  K.atmo = new THREE.Mesh(new THREE.SphereGeometry(3.25, 64, 48), new THREE.MeshBasicMaterial({ color: 0x6ab8ff, transparent: true, opacity: .16, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.BackSide })); G.add(K.atmo);
  const moonTex = canvasTex(512, 256, (ctx, w, h) => { ctx.fillStyle = '#a9a9b0'; ctx.fillRect(0, 0, w, h); const r = rand(8); for (let i = 0; i < 160; i++) { ctx.fillStyle = `rgba(${70 + r() * 60},${70 + r() * 60},${80 + r() * 60},.5)`; ctx.beginPath(); ctx.arc(r() * w, r() * h, 2 + r() * 16, 0, 7); ctx.fill(); } }).tex;
  K.moon = new THREE.Mesh(new THREE.SphereGeometry(.82, 64, 48), new THREE.MeshStandardMaterial({ map: moonTex, roughness: 1 })); K.moon.position.set(-14, 3, -20); G.add(K.moon);
  const a = [], r = rand(5); for (let i = 0; i < 4000; i++) { const th = r() * 6.283, ph = Math.acos(2 * r() - 1), d = 900; a.push(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d, Math.sin(ph) * Math.sin(th) * d); }
  K.stars = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(a, 3)), new THREE.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false })); G.add(K.stars);
  K.spaceSun = new THREE.DirectionalLight(0xfff4e0, 3.2); K.spaceSun.position.set(10, 4, 8); G.add(K.spaceSun);
}
const black = new THREE.Color(0x02030a);
let curMode = null;
export function mode(m) { // 'street' | 'space'
  if (curMode === m) { K.hands.visible = false; K.J.visible = m !== 'space'; return; } curMode = m;
  const sp = m === 'space';
  K.street.group.visible = !sp; sky.visible = !sp; K.space.visible = sp;
  scene.background = sp ? black : null; scene.fog = sp ? null : K.fog;
  scene.environmentIntensity = sp ? 0.08 : 0.6;
  scene.traverse(o => { if (o.isLight && o.parent === scene && !o.isAmbientLight) o.visible = !sp || o === K.spaceSun; });
  K.hands.visible = false; K.J.visible = !sp;
}

// ---------- camera ----------
const look = new THREE.Vector3();
export function cam(p, l, roll = 0, fov = 55) { camera.position.copy(p); look.copy(l); camera.lookAt(look); camera.rotateZ(roll); if (camera.fov !== fov) { camera.fov = fov; camera.updateProjectionMatrix(); } }
export function dolly(p0, p1, l0, l1, k, roll = 0, fov = 55) { cam(p0.clone().lerp(p1, eInOut(clamp(k))), l0.clone().lerp(l1, eInOut(clamp(k))), roll, fov); }
export function shake(amt, t) { camera.position.x += Math.sin(t * 71) * amt; camera.position.y += Math.cos(t * 59) * amt * .7; }

// ---------- POV ----------
export function pov(on) { $('pov').style.opacity = on ? 1 : 0; K.hands.visible = on; if (on) K.J.visible = false; }

// ---------- speech bubble that follows Jeremy's head (clamped to the safe zone) ----------
const tmp = new THREE.Vector3();
export function bubble(t, text, t0, worldPos) {
  const el = $('bubble');
  if (!text || t < t0 || t > t0 + 1.6) { el.style.opacity = 0; return; }
  const k = t - t0, s = k < .25 ? 0.5 + 0.5 * Math.sin(k / .25 * Math.PI / 2) * 1.12 : 1 + 0.06 * Math.exp(-(k - .25) * 6);
  camera.updateMatrixWorld(); tmp.copy(worldPos).project(camera);
  const x = clamp((tmp.x * .5 + .5) * 1080, 230, 760), y = clamp((-tmp.y * .5 + .5) * 1920, 760, 1080);
  el.textContent = text; el.style.left = x + 'px'; el.style.top = y + 'px';
  el.style.opacity = 1 - prog(t, t0 + 1.35, t0 + 1.6); el.style.transform = `translate(-50%,-100%) scale(${s}) rotate(${Math.sin(k * 9) * 2}deg)`;
}
export function headPos() { return K.J.localToWorld(V(0, 2.75, 0)); }

// ---------- floating 3D labels (EARTH / JUPITER ...) ----------
let tagsUsed = 0;
export function tag(text, worldPos, color = '#ffffff', alpha = 1) {
  const el = $('tag' + tagsUsed++); camera.updateMatrixWorld(); tmp.copy(worldPos).project(camera);
  el.textContent = text; el.style.color = color; el.style.opacity = tmp.z < 1 ? alpha : 0;
  el.style.left = clamp((tmp.x * .5 + .5) * 1080, 170, 820) + 'px'; el.style.top = clamp((-tmp.y * .5 + .5) * 1920, 640, 1100) + 'px';
}
// ---------- runner ----------
// spec: { total, reel, unit, label(i,b), fmt(v), beats:[{t, v, cap, hi, sev, bubble}], introShot(t), shot(t, b, lt, i, next) }
export function run(spec) {
  const beats = spec.beats;
  window.SPEC = { total: spec.total, reel: spec.reel.length, ctaAt: spec.ctaAt, beats: beats.map(b => ({ t: b.t, big: !!b.big, space: !!b.space, bubble: !!b.bubble })) };
  window.renderAt = (t) => {
    K.hands.visible = false; $('pov').style.opacity = 0; $('bubble').style.opacity = 0; tagsUsed = 0;
    const inIntro = intro(t, spec.reel);
    const { i, lt, s: b } = stageAt(beats, t);
    if (t < beats[0].t) { spec.introShot(t); $('black').style.opacity = 0.5 * (1 - prog(t, 2.6, 3.2)); }
    else { $('black').style.opacity = 0; spec.shot(t, b, lt, i, beats[i + 1]); }
    // live counter: rolls from the previous value to this beat's value in log space
    const valueAt = (tt) => { const q = stageAt(beats, Math.max(tt, beats[0].t)); const pv = q.i ? beats[q.i - 1].v : q.s.v; const k = eOut(clamp((tt - q.s.t) / 0.7)); return pv > 0 && q.s.v > 0 ? Math.exp(lerp(Math.log(pv), Math.log(q.s.v), k)) : q.s.v; };
    const end = t > spec.ctaAt;
    counter(t, { on: t >= beats[0].t && !end, valueAt, fmt: spec.fmt, label: spec.label(b, i), sub: spec.sub, sev: b.sev ?? Math.min(5, i * 5 / (beats.length - 2)), shake: lt < .3 && b.big ? (1 - lt / .3) : 0 });
    const caps = [];
    if (t >= beats[0].t) caps.push({ t0: b.t, t1: (beats[i + 1]?.t ?? spec.total) - 0.05, text: b.cap, y: b.capY ?? 1160, size: b.size ?? 68, g: b.hi || [], r: b.red || [] });
    renderCaptions(caps, t);
    $('fill').style.width = (clamp(t / spec.total) * 100) + '%';
    if (!inIntro) $('flash').style.opacity = b.big ? 0.5 * (1 - clamp(lt / 0.18)) : 0;
    for (let q = tagsUsed; q < 3; q++) $('tag' + q).style.opacity = 0;
    draw();
  };
  window.READY = true;
}
