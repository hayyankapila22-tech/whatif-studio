// Episode 8 — What if Jeremy doubled in height every minute?  (1.8 m × 2^minute; every number checked)
import { tag, THREE, scene, camera, canvasTex, rand, clamp, prog, lerp, eOut, eInOut, V, K, boot, mode, cam, dolly, shake, bubble, headPos, run, fmtBig, earthCanvas, RoundedBoxGeometry } from './kit.js';
import { sky } from './engine.js';

await boot('WHAT IF JEREMY KEPT GROWING?', 'EP. 8');
const J = K.J, HJ = 2.7;              // model height in its own units
sky.scale.setScalar(4e5); camera.far = 3e5; camera.updateProjectionMatrix();
function range(near, far) { camera.near = near; camera.far = far; camera.updateProjectionMatrix(); }
function fog(n, f) { if (scene.fog) { scene.fog.near = n; scene.fog.far = f; } }
function box(w, h, d, mat) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.castShadow = m.receiveShadow = true; return m; }

// ---------- landmarks (real heights, metres) ----------
const stone = new THREE.MeshStandardMaterial({ color: 0xd9c9a3, roughness: .8 }), gold = new THREE.MeshStandardMaterial({ color: 0xd8b25a, metalness: .7, roughness: .3 }), dark = new THREE.MeshStandardMaterial({ color: 0x3b3f4a, roughness: .6 });
const clockTex = canvasTex(256, 256, (ctx, w, h) => { ctx.fillStyle = '#f4eedc'; ctx.beginPath(); ctx.arc(128, 128, 120, 0, 7); ctx.fill(); ctx.strokeStyle = '#222'; ctx.lineWidth = 8; ctx.stroke(); for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283; ctx.fillStyle = '#222'; ctx.fillRect(128 + Math.cos(a) * 95 - 4, 128 + Math.sin(a) * 95 - 4, 8, 8); } ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(128, 128); ctx.lineTo(128, 50); ctx.moveTo(128, 128); ctx.lineTo(180, 128); ctx.stroke(); }).tex;
const bigBen = new THREE.Group(); { const shaft = box(12, 55, 12, stone); shaft.position.y = 27.5; const clk = box(13.5, 16, 13.5, stone); clk.position.y = 63; const bel = box(11, 10, 11, gold); bel.position.y = 76;
  const spire = new THREE.Mesh(new THREE.ConeGeometry(8, 15, 4), dark); spire.rotation.y = Math.PI / 4; spire.position.y = 88.5; bigBen.add(shaft, clk, bel, spire);
  for (let k = 0; k < 4; k++) { const f = new THREE.Mesh(new THREE.CircleGeometry(5, 48), new THREE.MeshBasicMaterial({ map: clockTex })); const a = k * Math.PI / 2; f.position.set(Math.sin(a) * 6.8, 63, Math.cos(a) * 6.8); f.rotation.y = a; bigBen.add(f); } }
bigBen.position.set(64, 0, 26); scene.add(bigBen);
const glass = new THREE.MeshPhysicalMaterial({ color: 0x9fc4e8, metalness: .8, roughness: .12, clearcoat: 1 });
const burj = new THREE.Group(); { let y = 0; const tiers = [[45, 160], [38, 140], [31, 120], [24, 110], [17, 90], [11, 70]]; tiers.forEach(([r, h]) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(r * .82, r, h, 24), glass); c.position.y = y + h / 2; c.castShadow = true; burj.add(c); y += h; });
  const sp = new THREE.Mesh(new THREE.CylinderGeometry(.8, 6, 828 - y, 16), glass); sp.position.y = y + (828 - y) / 2; burj.add(sp); }
burj.position.set(420, 0, 160); scene.add(burj);
const bigGround = new THREE.Mesh(new THREE.PlaneGeometry(2e5, 2e5), new THREE.MeshStandardMaterial({ color: 0x7f8a78, roughness: 1 })); bigGround.rotation.x = -Math.PI / 2; bigGround.position.y = -.05; bigGround.receiveShadow = true; scene.add(bigGround);
// cloud deck at 1.5 km
const cloudM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, emissive: 0xffffff, emissiveIntensity: .12 });
const clouds = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 3), cloudM, 700); { const d = new THREE.Object3D(), r = rand(31); for (let i = 0; i < 700; i++) { const a = r() * 6.283, rr = 200 + Math.sqrt(r()) * 9000; d.position.set(21 + Math.cos(a) * rr, 1150 + r() * 120, 6 + Math.sin(a) * rr); d.scale.set(120 + r() * 260, 40 + r() * 60, 120 + r() * 260); d.updateMatrix(); clouds.setMatrixAt(i, d.matrix); } } scene.add(clouds);
function makePlane() { const g = new THREE.Group(); const w = new THREE.MeshStandardMaterial({ color: 0xf2f4fa, roughness: .35, metalness: .3 });
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(.25, 2.2, 8, 16), w); body.rotation.z = Math.PI / 2; const wing = new THREE.Mesh(new RoundedBoxGeometry(.6, .06, 3.2, 2, .03), w); const tail = new THREE.Mesh(new RoundedBoxGeometry(.4, .5, .06, 2, .03), w); tail.position.set(-1.2, .3, 0);
  const stripe = new THREE.Mesh(new THREE.CapsuleGeometry(.255, 2.0, 8, 16), new THREE.MeshStandardMaterial({ color: 0xff3d6e })); stripe.rotation.z = Math.PI / 2; stripe.scale.set(1, 1, .2); g.add(body, wing, tail, stripe); return g; }
const planes = [0, 1].map(() => { const p = makePlane(); p.scale.setScalar(420); scene.add(p); return p; });

// ---------- planet scale (km): Earth, ISS, Moon, Mars, Sun ----------
const P = new THREE.Group(); K.space.add(P);
const bigEarth = new THREE.Mesh(new THREE.SphereGeometry(6371, 160, 120), new THREE.MeshStandardMaterial({ map: earthCanvas(), roughness: .85 })); bigEarth.position.y = -6371; P.add(bigEarth);
const bigAtmo = new THREE.Mesh(new THREE.SphereGeometry(6471, 160, 120), new THREE.MeshBasicMaterial({ color: 0x5aa8ff, transparent: true, opacity: .22, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.BackSide })); bigAtmo.position.y = -6371; P.add(bigAtmo);
const iss = new THREE.Group(); { const m = new THREE.MeshStandardMaterial({ color: 0xdfe3ea, metalness: .6, roughness: .4 }), pan = new THREE.MeshStandardMaterial({ color: 0x23306b, metalness: .5, roughness: .3, emissive: 0x101840 });
  iss.add(box(10, .5, .5, m)); for (const x of [-4.5, -3, 3, 4.5]) for (const z of [-1.6, 1.6]) { const p = box(1.2, .05, 2.6, pan); p.position.set(x, 0, z); iss.add(p); } const mod = box(1, .9, 3, m); iss.add(mod); }
iss.scale.setScalar(2.6); P.add(iss);
const moonTex = K.moon.material.map;
const bigMoon = new THREE.Mesh(new THREE.SphereGeometry(1737, 96, 64), new THREE.MeshStandardMaterial({ map: moonTex, roughness: 1 })); P.add(bigMoon);
const glowTex = canvasTex(256, 256, (ctx, w, h) => { const g = ctx.createRadialGradient(128, 128, 0, 128, 128, 128); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.25, 'rgba(255,255,255,.9)'); g.addColorStop(.5, 'rgba(255,255,255,.25)'); g.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex;
const dot = (col) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: col, transparent: true, depthWrite: false, toneMapped: false })); P.add(s); return s; };
const sunS = dot(0xffd36a), marsS = dot(0xff6a3d), earthS = dot(0x5ab0ff), moonS = dot(0xdddddd);

// ---------- timeline ----------
const H = m => 1.8 * Math.pow(2, m);
const B = [
  { t: 3.2, m: 0, cap: 'Jeremy is 1.8 m tall. Then he starts doubling.', hi: ['doubling.'] },
  { t: 5.6, m: 1, cap: 'Minute 1: 3.6 m. Doorways are now a problem.', hi: ['3.6', 'm.'] },
  { t: 8.0, m: 2, cap: 'Minute 2: 7.2 m. He’s peeking into upstairs windows.', hi: ['upstairs'] },
  { t: 10.4, m: 3, cap: 'Minute 3: 14.4 m. Taller than the café.', hi: ['14.4', 'm.'], bubble: 'OMG!' },
  { t: 12.8, m: 3, cap: 'Reality check: he weighs ×512, but his bones are only ×64 stronger.', hi: ['×512,'], red: ['×64'], big: true, size: 60, bubble: 'OUCH!' },
  { t: 15.4, m: 6, cap: 'Minute 6: 115 m. Taller than Big Ben.', hi: ['Big', 'Ben.'], big: true },
  { t: 17.8, m: 9, cap: 'Minute 9: 922 m. Taller than the Burj Khalifa.', hi: ['Burj', 'Khalifa.'] },
  { t: 20.2, m: 10, cap: 'Minute 10: his head is in the clouds. Literally.', hi: ['clouds.'] },
  { t: 22.6, m: 13, cap: 'Minute 13: 14.7 km. Planes fly past his chest.', hi: ['Planes'] },
  { t: 25.0, m: 16, cap: 'Minute 16: 118 km. His head is in SPACE.', red: ['SPACE.'], big: true, space: true },
  { t: 27.4, m: 18, cap: 'Minute 18: the space station flies past his face.', hi: ['space', 'station'], space: true, bubble: 'HI!' },
  { t: 29.8, m: 21, cap: 'Minute 21: he’s taller than the Moon is wide.', hi: ['Moon'], space: true },
  { t: 32.2, m: 23, cap: 'Minute 23: taller than Earth is wide.', red: ['Earth'], big: true, space: true },
  { t: 34.6, m: 28, cap: 'Minute 28: his head passes the Moon.', hi: ['Moon.'], space: true },
  { t: 37.0, m: 35, cap: 'Minute 35: taller than the distance to Mars.', red: ['Mars.'], space: true },
  { t: 39.4, m: 37, cap: 'Minute 37: his head passes the SUN.', red: ['SUN.'], big: true, space: true },
  { t: 41.8, m: 37, cap: 'All of that… in 37 minutes. ⏱️', hi: ['37', 'minutes.'] },
  { t: 44.0, m: 37, cap: 'What should double next? 👇', hi: ['double', 'next?'] },
].map(b => ({ ...b, v: H(b.m) }));
const fmtLen = v => v < 1000 ? (v < 100 ? v.toFixed(1) : Math.round(v)) + ' m' : v < 1e4 ? (v / 1000).toFixed(2) + ' km' : fmtBig(v / 1000, 'km');

let curH = 1.8;
function heightAt(t, i, lt) { const b = B[i], pv = i ? B[i - 1].v : b.v; return Math.exp(lerp(Math.log(pv), Math.log(b.v), eOut(clamp(lt / .7)))); }
function jer(x, y, z, ry, h, pose) { J.visible = true; J.position.set(x, y, z); J.rotation.set(0, ry, 0); J.scale.setScalar(h / HJ); J.pose(pose); }
function hideAll() { bigGround.visible = true; bigBen.visible = burj.visible = clouds.visible = false; planes.forEach(p => p.visible = false); P.visible = false; [K.earth, K.clouds, K.atmo, K.moon].forEach(o => o.visible = false); }
const JX = 21, JZ = 5.6, GY = .18;

run({
  total: 46.5, ctaAt: 41.8, sub: 'Jeremy’s height',
  reel: ['(x)', 'YOUR COFFEE DOUBLED', 'GRAVITY DOUBLED', 'EARTH STOPPED', 'YOU DOUBLED 1¢', 'YOUR CAR NEVER STOPPED', 'JEREMY DOUBLED IN HEIGHT?'],
  beats: B, label: b => 'MINUTE ' + b.m, fmt: fmtLen,
  introShot(t) { mode('street'); hideAll(); range(.05, 3e5); fog(70, 300); jer(16 + t * .9, GY, JZ, -Math.PI / 2, 1.8, { expr: 'happy', bob: Math.abs(Math.sin(t * 6)) * .03 }); dolly(V(10, 9, -4), V(13, 6, -1), V(20, 1.5, 6), V(20, 1.2, 6), t / 3.2); },
  shot(t, b, lt, i) {
    hideAll(); const h = heightAt(t, i, lt); const k = clamp(lt / 2.4);
    if (b.space && i < 16) { mode('space'); P.visible = true; bigGround.visible = false; } else { mode('street'); range(.05, 3e5); }
    const grow = lt < .7 ? Math.sin(lt / .7 * Math.PI) * .25 : 0; // arms fling while growing
    if (i === 0) { fog(70, 300); jer(lerp(19, 20.5, k), GY, JZ, -Math.PI / 2 + .6, h, { expr: 'happy', bob: Math.abs(Math.sin(t * 6)) * .03, look: .3 }); dolly(V(16, 1.6, 2.0), V(16.6, 1.6, 2.4), V(20.5, 1.2, 5.8), V(20.5, 1.2, 5.8), k); }
    else if (i === 1) { fog(70, 300); jer(18, GY, 6.1, Math.PI + .2, h, { expr: 'confused', armL: .3 + grow * 6, armR: .3 + grow * 6, look: .4 }); dolly(V(16.4, 1.1, 1.2), V(16.6, 1.2, 1.6), V(18, 2.4, 6.5), V(18, 2.4, 6.5), k); }
    else if (i === 2) { fog(70, 300); jer(19, GY, 6.3, .9, h, { expr: 'happy', armL: .3 + grow * 6, armR: .3, look: -.6, tilt: .1 }); dolly(V(10.5, 4.5, -.5), V(11, 5, 0), V(19, 5, 7), V(19, 5.2, 7), k); }
    else if (i === 3 || i === 4) { fog(100, 600);
      const snap = i === 4 ? eOut(clamp((lt - .1) / .5)) : 0;
      jer(20, GY, 6.4, Math.PI + .15, h, { expr: i === 4 ? 'panic' : 'shocked', armL: 2.4 + grow * 2, armR: 2.4, look: .2, sweatK: lt, tilt: snap * .35 });
      J.scale.y = h / HJ * (1 - .38 * snap); J.position.y = GY;
      dolly(V(15.5, 1.0, -4.5), V(15.2, .9, -5), V(20, 8.5, 6.4), V(20, 8, 6.4), k, 0, 62);
      if (i === 4) document.getElementById('flash').style.background = lt < .5 ? '#ff2d4a' : '#fff';
      bubble(t, b.bubble, b.t + .15, V(20, h * (1 - .38 * snap) + .2, 6.4));
    } else if (i === 5) { fog(400, 3000); bigBen.visible = true; jer(JX, GY, JZ, Math.PI + .5, h, { expr: 'happy', armL: .3 + grow * 4, armR: 2.6, look: .5 }); dolly(V(-110, 95, -150), V(-130, 100, -175), V(40, 55, 10), V(40, 58, 10), k); tag('BIG BEN 96 m', V(64, 100, 26), '#ffe08a'); }
    else if (i === 6) { fog(3000, 20000); burj.visible = true; jer(JX, GY, JZ, Math.PI + .6, h, { expr: 'shocked', armL: .3 + grow * 4, armR: .4, look: .6 }); dolly(V(-900, 330, -1500), V(-1000, 380, -1650), V(200, 450, 60), V(200, 470, 60), k); tag('BURJ KHALIFA 828 m', V(420, 860, 160), '#9fdcff'); }
    else if (i === 7) { fog(4000, 30000); clouds.visible = true; jer(JX, GY, JZ, Math.PI + .3, h, { expr: 'confused', armL: .3, armR: .3, look: .3, blink: (t % 2) < .1 }); dolly(V(-1300, 1650, -2700), V(-1400, 1680, -2850), V(21, 1450, 6), V(21, 1480, 6), k); }
    else if (i === 8) { fog(8000, 80000); clouds.visible = true; jer(JX, GY, JZ, Math.PI + .2, h, { expr: 'shocked', armL: .4, armR: 1.5, look: .7 });
      planes.forEach((p, j) => { p.visible = true; p.position.set(lerp(-9000, 9000, (lt / 2.4 + j * .45) % 1), 10600 + j * 900, -3600 - j * 1500); p.rotation.set(0, 0, 0); });
      dolly(V(-8000, 11500, -19000), V(-8500, 11600, -20000), V(0, 9200, 0), V(0, 9400, 0), k); }
    else if (i >= 9 && i <= 15) { // km units on the planet; Jeremy stands on top of Earth at the origin
      const hk = h / 1000; bigEarth.rotation.set(1.2, t * .002, 0); jer(0, 0, 0, .25, hk, { expr: i === 15 ? 'happy' : 'shocked', armL: .4, armR: i === 10 ? 2.6 + Math.sin(t * 10) * .3 : .4, look: .4 });
      bigMoon.visible = sunS.visible = marsS.visible = earthS.visible = moonS.visible = iss.visible = false; bigEarth.visible = bigAtmo.visible = true;
      if (i === 9) { range(1, 1e5); dolly(V(170, 60, 250), V(185, 70, 270), V(0, 62, 0), V(0, 68, 0), k); tag('SPACE ↑ 100 km', V(-60, 104, 0), '#9fdcff'); }
      if (i === 10) { range(1, 1e5); iss.visible = true; iss.position.set(lerp(-160, 160, k), 420, 160); iss.rotation.set(.3, t * .4, .2); dolly(V(260, 470, 640), V(275, 475, 670), V(0, 400, 0), V(0, 405, 0), k); bubble(t, b.bubble, b.t + .4, V(0, hk * .95, 0)); }
      if (i === 11) { range(10, 1e6); bigMoon.visible = true; bigMoon.position.set(3600, 1737, 400); dolly(V(1200, 2400, 14500), V(1300, 2500, 15500), V(1800, 1900, 0), V(1800, 1900, 0), k); tag('MOON', V(3600, -400, 400), '#dddddd'); tag('JEREMY', V(0, hk * 1.06, 0), '#ffc444'); }
      if (i === 12) { range(10, 1e6); dolly(V(0, 3000, 52000), V(0, 3200, 56000), V(0, 2500, 0), V(0, 2700, 0), k); tag('EARTH', V(0, -13800, 0), '#7fd0ff'); }
      if (i >= 13) { const D = hk * 1.7; range(D / 2e4, D * 4); bigEarth.visible = bigAtmo.visible = false;
        earthS.visible = true; earthS.position.set(0, 0, 0); earthS.scale.setScalar(D * .03);
        if (i === 13) { moonS.visible = true; moonS.position.set(-hk * .25, 384400, 0); moonS.scale.setScalar(D * .022); tag('MOON', V(-hk * .25, 384400 - D * .05, 0), '#dddddd'); }
        if (i === 14) { marsS.visible = true; marsS.position.set(-hk * .25, 5.46e7, 0); marsS.scale.setScalar(D * .025); tag('MARS', V(-hk * .25, 5.46e7 - D * .055, 0), '#ff8a5c'); }
        if (i === 15) { sunS.visible = true; sunS.position.set(-hk * .3, 1.496e8, 0); sunS.scale.setScalar(D * .1 * (1 + .05 * Math.sin(t * 6))); tag('SUN', V(-hk * .3, 1.496e8 - D * .09, 0), '#ffd36a'); }
        dolly(V(0, hk * .5, D * .95), V(0, hk * .52, D * 1.03), V(0, hk * .5, 0), V(0, hk * .51, 0), k, 0, 55); tag('EARTH', V(hk * .2, -D * .02, 0), '#7fd0ff', .9); }
    } else { // back to normal for the outro
      fog(70, 300); jer(21.5, GY, 5.8, Math.PI + .1, 1.8, { expr: 'happy', armL: .2 + Math.abs(Math.sin(t * 5)) * 2.6, armR: .3, bob: Math.abs(Math.sin(t * 5)) * .03, look: .1 });
      dolly(V(21.4, 1.5, 3.4), V(21.4, 1.45, 3.7), V(21.5, 1.35, 6), V(21.5, 1.35, 6), k);
    }
    if (i !== 4) document.getElementById('flash').style.background = '#fff';
    if (b.big && lt < .35) shake((i >= 9 ? 2 : .08) * (1 - lt / .35) * (i >= 9 ? h / 1000 / 60 : 1), t);
  },
});
