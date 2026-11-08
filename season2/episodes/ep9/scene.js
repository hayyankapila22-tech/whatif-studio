// Episode 9 — What if pigeons doubled every minute?  (1 pigeon × 2^minute; every number checked)
import { tag, THREE, scene, camera, canvasTex, rand, clamp, prog, lerp, eOut, eInOut, V, K, boot, mode, cam, dolly, shake, bubble, headPos, run, fmtBig, earthCanvas } from './kit.js';
import { key, hemi, renderer } from './engine.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

await boot('WHAT IF PIGEONS KEPT DOUBLING?', 'EP. 9');
const J = K.J;

// ---------- pigeon geometry (vertex coloured, ~0.32 m long, faces +z) ----------
function part(geo, col, [x, y, z], [sx, sy, sz] = [1, 1, 1], rx = 0) { geo.scale(sx, sy, sz); if (rx) geo.rotateX(rx); geo.translate(x, y, z); const c = new THREE.Color(col), n = geo.attributes.position.count, a = new Float32Array(n * 3); for (let i = 0; i < n; i++) { a[i * 3] = c.r; a[i * 3 + 1] = c.g; a[i * 3 + 2] = c.b; } geo.setAttribute('color', new THREE.BufferAttribute(a, 3)); geo.deleteAttribute('uv'); return geo; }
function pigeonGeo(flying) {
  const g = [
    part(new THREE.SphereGeometry(1, 12, 9), 0x8d96aa, [0, .1, 0], [.08, .075, .145]),
    part(new THREE.SphereGeometry(1, 10, 8), 0x4f7d6e, [0, .15, .09], [.055, .05, .055]),          // iridescent neck
    part(new THREE.SphereGeometry(1, 10, 8), 0x6e7790, [0, .195, .13], [.042, .042, .046]),
    part(new THREE.ConeGeometry(.012, .04, 6), 0xd9c6a0, [0, .19, .18], [1, 1, 1], Math.PI / 2),
    part(new THREE.SphereGeometry(1, 6, 4), 0xff6a2a, [.026, .205, .158], [.008, .008, .008]),
    part(new THREE.SphereGeometry(1, 6, 4), 0xff6a2a, [-.026, .205, .158], [.008, .008, .008]),
    part(new THREE.BoxGeometry(.11, .02, .12), 0x3d4252, [0, .1, -.17], [1, 1, 1], .25),
  ];
  if (flying) for (const s of [-1, 1]) { const w = part(new THREE.BoxGeometry(.3, .012, .12), 0x7c859b, [s * .2, .13, 0]); g.push(w); const tip = part(new THREE.BoxGeometry(.12, .01, .1), 0x2f3340, [s * .38, .13, -.01]); g.push(tip); }
  else { for (const s of [-1, 1]) { g.push(part(new THREE.SphereGeometry(1, 8, 6), 0x7a8398, [s * .06, .11, -.02], [.03, .055, .12])); g.push(part(new THREE.SphereGeometry(1, 6, 4), 0x2f3340, [s * .065, .095, -.1], [.025, .02, .05])); g.push(part(new THREE.CylinderGeometry(.006, .006, .05, 5), 0xd9567a, [s * .025, .025, .01])); } }
  return mergeGeometries(g);
}
const pMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .55, metalness: .05 });
const NG = 7000, NF = 6000;
const ground = new THREE.InstancedMesh(pigeonGeo(false), pMat, NG); ground.receiveShadow = true; ground.castShadow = true; ground.frustumCulled = false; scene.add(ground);
const flock = new THREE.InstancedMesh(pigeonGeo(true), pMat, NF); flock.frustumCulled = false; scene.add(flock);
const r = rand(41), GA = Math.PI * (3 - Math.sqrt(5));
const gp = Array.from({ length: NG }, (_, i) => { const rr = Math.sqrt(i / (Math.PI * 5)) * 1.25 + .6, a = i * GA; return { x: Math.cos(a) * rr * 1.9, z: Math.sin(a) * rr * .5, ry: r() * 6.283, ph: r() * 9, s: .9 + r() * .25 }; });
const fp = Array.from({ length: NF }, () => ({ a: r() * 6.283, rr: 4 + Math.sqrt(r()) * 70, y: 9 + r() * 38, ph: r() * 9, sp: .25 + r() * .25, s: 1.6 + r() * .6 }));
const dm = new THREE.Object3D();
function placeGround(n, cx, cz, t, peck = 1) { const c = Math.min(n, NG); ground.count = c; for (let i = 0; i < c; i++) { const p = gp[i]; const pk = Math.max(0, Math.sin(t * 5 + p.ph)) ** 6 * peck; dm.position.set(cx + p.x, .18, Math.max(-7.6, Math.min(7.6, cz + p.z))); dm.rotation.set(pk * .5, p.ry + Math.sin(t * .7 + p.ph) * .3, 0); dm.scale.setScalar(p.s); dm.updateMatrix(); ground.setMatrixAt(i, dm.matrix); } ground.instanceMatrix.needsUpdate = true; ground.visible = c > 0; }
function placeFlock(n, cx, cz, t, yMul = 1) { const c = Math.min(n, NF); flock.count = c; for (let i = 0; i < c; i++) { const p = fp[i]; const a = p.a + t * p.sp; dm.position.set(cx + Math.cos(a) * p.rr * 1.6, p.y * yMul + Math.sin(t * 2 + p.ph) * 1.2, cz + Math.sin(a) * p.rr * .6); dm.rotation.set(Math.sin(t * 9 + p.ph) * .25, a + Math.PI, Math.sin(t * 9 + p.ph) * .35); dm.scale.set(p.s, p.s * (1 + .3 * Math.sin(t * 14 + p.ph)), p.s); dm.updateMatrix(); flock.setMatrixAt(i, dm.matrix); } flock.instanceMatrix.needsUpdate = true; flock.visible = c > 0; }
// one hero pigeon (larger, for close-ups) and one that ends up on Jeremy's head
const hero = new THREE.Mesh(pigeonGeo(false), pMat); hero.castShadow = true; scene.add(hero);

// ---------- space extras ----------
const featherTex = canvasTex(1024, 512, (ctx, w, h) => { ctx.fillStyle = '#7f889c'; ctx.fillRect(0, 0, w, h); const q = rand(9); for (let i = 0; i < 9000; i++) { const c = ['#8d96aa', '#6e7790', '#4f7d6e', '#5b4f78', '#a5adbf', '#3d4252'][Math.floor(q() * 6)]; ctx.fillStyle = c; ctx.beginPath(); ctx.ellipse(q() * w, q() * h, 3 + q() * 5, 2 + q() * 3, q() * 3, 0, 7); ctx.fill(); } }).tex;
const greyEarth = new THREE.Mesh(new THREE.SphereGeometry(3.006, 128, 96), new THREE.MeshStandardMaterial({ map: featherTex, roughness: .7, transparent: true, opacity: 0 })); K.space.add(greyEarth);
const layer = new THREE.Mesh(new THREE.SphereGeometry(3.03, 128, 96), new THREE.MeshStandardMaterial({ map: featherTex, roughness: .7, displacementMap: featherTex, displacementScale: .04 })); K.space.add(layer);
const ball = new THREE.Mesh(new THREE.SphereGeometry(1, 128, 96), new THREE.MeshStandardMaterial({ map: featherTex, roughness: .6 })); K.space.add(ball);

// ---------- timeline ----------
const B = [
  { t: 3.2, m: 0, cap: 'One pigeon lands next to Jeremy.', hi: ['One', 'pigeon'] },
  { t: 5.6, m: 3, cap: 'It doubles every minute. Minute 3: 8 pigeons. Cute.', hi: ['8', 'pigeons.'], size: 62 },
  { t: 8.0, m: 6, cap: 'Minute 6: 64. They want his coffee.', hi: ['coffee.'], bubble: 'SHOO!' },
  { t: 10.4, m: 9, cap: 'Minute 9: 512 pigeons on the street.', hi: ['512'] },
  { t: 12.8, m: 12, cap: 'Minute 12: 4,096. The sky fills with wings.', hi: ['wings.'] },
  { t: 15.2, m: 16, cap: 'Minute 16: 65,536. A packed stadium of pigeons.', hi: ['stadium'] },
  { t: 17.6, m: 20, cap: 'Minute 20: a MILLION. They block out the Sun.', red: ['MILLION.'], big: true, bubble: 'UH OH' },
  { t: 20.0, m: 25, cap: 'Minute 25: more pigeons than people in Australia.', hi: ['Australia.'] },
  { t: 22.4, m: 29, cap: 'Minute 29: more than every pigeon on Earth today.', hi: ['every', 'pigeon'] },
  { t: 24.8, m: 33, cap: 'Minute 33: more pigeons than HUMANS.', red: ['HUMANS.'], big: true, bubble: 'NOPE!' },
  { t: 27.2, m: 41, cap: 'Minute 41: they outweigh every human alive.', hi: ['outweigh'] },
  { t: 29.6, m: 54, cap: 'Minute 54: pigeons carpet the ENTIRE planet.', red: ['ENTIRE'], big: true, space: true },
  { t: 32.0, m: 60, cap: 'Minute 60: Earth is buried 20 m deep.', hi: ['20', 'm'], space: true },
  { t: 34.4, m: 85, cap: 'Minute 85: the pigeons outweigh EARTH.', red: ['EARTH.'], big: true, space: true },
  { t: 36.8, m: 85, cap: 'All from ONE pigeon. 🐦', hi: ['ONE', 'pigeon.'] },
  { t: 39.2, m: 85, cap: 'What should double next? 👇', hi: ['double', 'next?'] },
].map(b => ({ ...b, v: Math.pow(2, b.m) }));
const fmtN = v => v < 1e6 ? Math.round(v).toLocaleString('en-US') : fmtBig(v);
function shown(i, lt) { const b = B[i], pv = i ? B[i - 1].v : 1; return Math.exp(lerp(Math.log(pv), Math.log(b.v), eOut(clamp(lt / .7)))); }
function jer(x, z, ry, pose) { J.visible = true; J.position.set(x, .18, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose); }
function hideAll() { ground.visible = flock.visible = hero.visible = false; greyEarth.material.opacity = 0; layer.visible = ball.visible = false; key.intensity = 3.4; hemi.intensity = .6; renderer.toneMappingExposure = .52; }
const JX = 34.5, JZ = 5.6;

run({
  total: 42.5, ctaAt: 36.8, sub: 'pigeons',
  reel: ['(x)', 'JEREMY KEPT GROWING', 'YOUR COFFEE DOUBLED', 'GRAVITY DOUBLED', 'EARTH STOPPED', 'YOU DOUBLED 1¢', 'PIGEONS DOUBLED EVERY MINUTE?'],
  beats: B, label: b => 'MINUTE ' + b.m, fmt: fmtN,
  introShot(t) { mode('street'); hideAll(); jer(16 + t * .9, JZ, -Math.PI / 2, { expr: 'happy', bob: Math.abs(Math.sin(t * 6)) * .03 }); dolly(V(10, 9, -4), V(13, 6, -1), V(20, 1.5, 6), V(20, 1.2, 6), t / 3.2); },
  shot(t, b, lt, i) {
    hideAll(); const n = shown(i, lt), k = clamp(lt / 2.4);
    if (b.space) mode('space'); else mode('street');
    if (i === 0) { // the first pigeon flutters down
      jer(JX, JZ + .3, Math.PI + .3, { expr: 'happy', look: .5, armL: .2, armR: .2 }); hero.visible = true;
      const land = eOut(clamp(lt / .9)); hero.position.set(JX + .8, .18 + (1 - land) * 2.2, JZ - .4); hero.rotation.set(0, -2.4, 0); hero.scale.setScalar(1.4);
      dolly(V(JX + 1.9, .32, JZ - 2.9), V(JX + 1.8, .3, JZ - 2.7), V(JX + .5, 1.05, JZ), V(JX + .5, 1.0, JZ), k);
    } else if (i <= 3) {
      placeGround(n, JX + .5, JZ - 1.2, t); const ex = ['happy', 'worried', 'shocked'][i - 1];
      jer(JX, JZ + .3, Math.PI + .3, { expr: ex, look: .4, armL: i === 2 ? 2.4 + Math.sin(t * 14) * .4 : .3, armR: i === 2 ? 2.4 - Math.sin(t * 14) * .4 : .3, sweatK: i === 3 ? lt : 0 });
      if (i === 1) dolly(V(JX + 2.4, .8, JZ - 3.2), V(JX + 2.2, .75, JZ - 3), V(JX + .4, .4, JZ - .8), V(JX + .4, .4, JZ - .8), k);
      if (i === 2) { dolly(V(JX + 2.8, 1.5, JZ - 4.4), V(JX + 2.6, 1.4, JZ - 4.1), V(JX, .9, JZ - .3), V(JX, .9, JZ - .3), k); bubble(t, b.bubble, b.t + .25, headPos()); }
      if (i === 3) dolly(V(JX - 9, 5.5, JZ - 9), V(JX - 9.5, 6, JZ - 9.5), V(JX + 1, .3, JZ - 1), V(JX + 1, .3, JZ - 1), k);
    } else if (i <= 6) { // into the sky
      placeGround(i === 4 ? 2048 : NG, JX + .5, JZ - 1.2, t); placeFlock(i === 4 ? n / 2 : n, JX, 0, t, i === 6 ? .8 : 1);
      jer(JX, JZ + .3, Math.PI + .2, { expr: i === 6 ? 'panic' : 'shocked', look: .2, armL: 2.3, armR: 2.3, sweatK: lt });
      if (i === 6) { const dk = eOut(clamp(lt / 1)); key.intensity = lerp(3.4, .35, dk); hemi.intensity = lerp(.6, .12, dk); renderer.toneMappingExposure = lerp(.52, .17, dk); }
      if (i === 4) dolly(V(JX - 4, 1.4, JZ - 6), V(JX - 4.2, 1.3, JZ - 6.3), V(JX + 2, 9, 2), V(JX + 2, 11, 2), k, 0, 62);
      if (i === 5) dolly(V(JX - 30, 18, -40), V(JX - 34, 22, -46), V(JX, 15, 0), V(JX, 16, 0), k);
      if (i === 6) { dolly(V(JX + .5, .9, JZ - 1.5), V(JX + .4, .8, JZ - 1.4), V(JX, 14, 2), V(JX, 18, 2), k, 0, 70); bubble(t, b.bubble, b.t + .3, headPos()); }
    } else if (i <= 10) { // the city disappears under pigeons
      placeGround(NG, JX + .5, JZ - 1.2, t, .6); placeFlock(NF, JX, 0, t, 1.2);
      jer(JX, JZ + .3, Math.PI + .2, { expr: i === 9 ? 'panic' : 'worried', look: .3, armL: 1.2, armR: 1.2, sweatK: lt });
      if (i === 7) dolly(V(JX - 60, 40, -70), V(JX - 70, 48, -80), V(JX, 6, 0), V(JX, 6, 0), k);
      if (i === 8) dolly(V(JX + 70, 60, -60), V(JX + 80, 70, -70), V(JX, 5, 0), V(JX, 5, 0), k);
      if (i === 9) { dolly(V(JX + 2.4, 1.6, JZ - 3), V(JX + 2.2, 1.5, JZ - 2.8), V(JX, 1.3, JZ), V(JX, 1.3, JZ), k); bubble(t, b.bubble, b.t + .25, headPos()); }
      if (i === 10) dolly(V(JX - 2, 25, -30), V(JX - 2, 60, -70), V(JX, 0, 4), V(JX, 0, 4), k);
    } else if (i <= 13) { // space
      const rot = t * .08; K.earth.rotation.y = rot; greyEarth.rotation.y = rot; layer.rotation.y = rot; K.clouds.rotation.y = rot * 1.2; K.clouds.visible = i === 11;
      if (i === 11) { greyEarth.material.opacity = eOut(clamp(lt / 1.4)); dolly(V(5, 2, 15), V(4.8, 1.8, 14.2), V(0, 0, 0), V(0, 0, 0), k, 0, 45); }
      if (i === 12) { greyEarth.material.opacity = 1; layer.visible = true; layer.scale.setScalar(lerp(1, 1.02, eOut(clamp(lt / 1)))); dolly(V(5, 3.6, 12), V(4.6, 3.4, 11.4), V(0, .8, 0), V(0, .8, 0), k, 0, 45); }
      if (i === 13) { greyEarth.material.opacity = 1; ball.visible = true; const R = lerp(1, 3 * Math.cbrt(14), eOut(k)); ball.scale.setScalar(R); ball.position.set(-(3 + R + 1), 0, -2); ball.rotation.y = t * .1;
        dolly(V(-5, 3, 48), V(-5.4, 3.2, 52), V(-5.5, 0, 0), V(-5.5, 0, 0), k, 0, 45); tag('EARTH', V(0, -4, 0), '#7fd0ff'); tag('PIGEONS', V(-(4 + R), -R - 1, -2), '#c9d1f5'); }
    } else { // outro: one pigeon sits on Jeremy's head
      jer(JX, JZ, Math.PI + .1, { expr: i === 14 ? 'confused' : 'happy', armL: i === 15 ? .2 + Math.abs(Math.sin(t * 5)) * 2.6 : .2, armR: .3, look: .1 });
      hero.visible = true; hero.scale.setScalar(1.1); hero.position.copy(headPos()).add(V(0, -.12 + (i === 14 ? (1 - eOut(clamp(lt / .8))) * 1.5 : 0), 0)); hero.rotation.set(0, Math.PI + .5 + Math.sin(t * 2) * .3, 0);
      dolly(V(JX + .4, 1.8, 2.0), V(JX + .3, 1.75, 2.4), V(JX, 1.55, 6), V(JX, 1.55, 6), k);
    }
    if (b.big && lt < .35) shake(.06 * (1 - lt / .35) * (b.space ? 2 : 1), t);
  },
});
