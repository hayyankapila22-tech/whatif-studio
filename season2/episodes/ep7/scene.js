// Episode 7 — What if your coffee doubled every minute?  (0.35 L cup, ×2 per minute)
import { tag, THREE, scene, camera, canvasTex, rand, clamp, prog, lerp, eOut, eInOut, makeCar, V, K, boot, mode, cam, dolly, shake, pov, bubble, headPos, run, fmtBig, earthCanvas } from './kit.js';

await boot('WHAT IF YOUR COFFEE KEPT DOUBLING?', 'EP. 7');
const J = K.J;

// ---------- coffee materials ----------
const ripple = canvasTex(512, 512, (ctx, w, h) => { const img = ctx.createImageData(w, h); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
  const u = x / w * 6.283, v = y / h * 6.283; const dx = Math.cos(u * 3 + v) * .5 + Math.cos(u * 7 - v * 2) * .3 + Math.sin(u * 2 + v * 5) * .2, dy = Math.sin(v * 3 - u) * .5 + Math.cos(v * 6 + u * 3) * .3 + Math.sin(u * 4 + v * 2) * .2;
  const i = (y * w + x) * 4; img.data[i] = 128 + dx * 40; img.data[i + 1] = 128 + dy * 40; img.data[i + 2] = 255; img.data[i + 3] = 255; } ctx.putImageData(img, 0, 0); });
ripple.tex.colorSpace = THREE.NoColorSpace; ripple.tex.wrapS = ripple.tex.wrapT = THREE.RepeatWrapping;
const coffee = new THREE.MeshPhysicalMaterial({ color: 0x5a2a10, roughness: .18, clearcoat: .35, clearcoatRoughness: .1, envMapIntensity: .45, normalMap: ripple.tex, normalScale: new THREE.Vector2(.35, .35), sheen: .3, sheenColor: 0x8a4a20 });
const flood = coffee.clone(); flood.normalMap = ripple.tex.clone(); flood.normalMap.repeat.set(40, 6); flood.normalMap.needsUpdate = true; flood.normalScale.set(.5, .5);
const cremaTex = canvasTex(512, 512, (ctx, w, h) => { const g = ctx.createRadialGradient(w / 2, h / 2, 10, w / 2, h / 2, w / 2); g.addColorStop(0, '#c99560'); g.addColorStop(.7, '#a86d3a'); g.addColorStop(1, '#6a3a18'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = 'rgba(240,210,170,.6)'; ctx.lineWidth = 10; ctx.beginPath(); for (let a = 0; a < 40; a += .05) { const r = a * 5.5; ctx.lineTo(w / 2 + Math.cos(a) * r, h / 2 + Math.sin(a) * r); } ctx.stroke(); }).tex;
const crema = new THREE.MeshPhysicalMaterial({ map: cremaTex, roughness: .35, clearcoat: .6 });
const ceramic = new THREE.MeshPhysicalMaterial({ color: 0xfafafa, roughness: .15, clearcoat: 1 });

// ---------- the cup on the café table ----------
const TABLE = V(22.8, 0.775, 6.6);
const cupG = new THREE.Group(); cupG.position.copy(TABLE); scene.add(cupG);
{ const body = new THREE.Mesh(new THREE.CylinderGeometry(.05, .04, .1, 48, 1, true), ceramic); body.position.y = .05; body.material.side = THREE.DoubleSide;
  const base = new THREE.Mesh(new THREE.CylinderGeometry(.04, .04, .006, 48), ceramic); base.position.y = .003;
  const rim = new THREE.Mesh(new THREE.TorusGeometry(.05, .003, 8, 48), ceramic); rim.rotation.x = Math.PI / 2; rim.position.y = .1;
  const handle = new THREE.Mesh(new THREE.TorusGeometry(.025, .007, 12, 32, Math.PI * 1.2), ceramic); handle.position.set(.056, .055, 0); handle.rotation.z = -Math.PI * .6;
  const saucer = new THREE.Mesh(new THREE.CylinderGeometry(.085, .06, .01, 48), ceramic); saucer.position.y = -.002;
  [body, base, rim, handle, saucer].forEach(m => { m.castShadow = m.receiveShadow = true; cupG.add(m); }); }
const surf = new THREE.Mesh(new THREE.CircleGeometry(.048, 48), crema); surf.rotation.x = -Math.PI / 2; surf.position.y = .092; cupG.add(surf);
const dome = new THREE.Mesh(new THREE.SphereGeometry(.05, 48, 24, 0, 6.283, 0, Math.PI / 2), coffee); dome.position.y = .095; cupG.add(dome);
const tPuddle = new THREE.Mesh(new THREE.CircleGeometry(1, 64), coffee); tPuddle.rotation.x = -Math.PI / 2; tPuddle.position.set(TABLE.x, TABLE.y + .002, TABLE.z); scene.add(tPuddle);
const stream = new THREE.Mesh(new THREE.CylinderGeometry(.022, .03, 1, 16), coffee); scene.add(stream);
const gPuddle = new THREE.Mesh(new THREE.CircleGeometry(1, 96), coffee); gPuddle.rotation.x = -Math.PI / 2; gPuddle.position.set(TABLE.x - .2, .185, TABLE.z - .3); gPuddle.receiveShadow = true; scene.add(gPuddle);
const mound = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 48, 0, 6.283, 0, Math.PI / 2), coffee); mound.position.set(TABLE.x, .18, TABLE.z - .4); mound.castShadow = true; scene.add(mound);
const lake = new THREE.Mesh(new THREE.PlaneGeometry(600, 200), flood); lake.rotation.x = -Math.PI / 2; lake.receiveShadow = true; scene.add(lake);
const floaters = [0xffc93a, 0x29b48a, 0xe8364e].map((c, i) => { const car = makeCar(c); car.position.set(16 + i * 6, 0, 1.5 - i * 1.5); car.rotation.y = .3 - i * .4; scene.add(car); return car; });
const moundR = (L) => Math.cbrt(L / 1000 / 1.152);   // half-ellipsoid, height = .55 R

// ---------- space extras ----------
const spot = new THREE.Mesh(new THREE.SphereGeometry(3.01, 96, 48, 0, 6.283, 0, .1), coffee); spot.rotation.set(1.15, 0, .5); K.space.add(spot);
const brownEarth = new THREE.Mesh(new THREE.SphereGeometry(3.006, 128, 96), new THREE.MeshPhysicalMaterial({ map: earthCanvas(['#2a1408', '#3d1d0b'], ['#3f8a3c', '#7a8b45']), roughness: .25, clearcoat: 1, transparent: true, opacity: 0 })); K.space.add(brownEarth);
const ballTex = canvasTex(1024, 512, (ctx, w, h) => { ctx.fillStyle = '#3a1c0c'; ctx.fillRect(0, 0, w, h); const r = rand(4); for (let i = 0; i < 90; i++) { ctx.strokeStyle = `rgba(${170 + r() * 60},${110 + r() * 40},${60 + r() * 30},${.25 + r() * .35})`; ctx.lineWidth = 4 + r() * 16; ctx.beginPath(); const y = r() * h; ctx.moveTo(0, y); for (let x = 0; x <= w; x += 32) ctx.lineTo(x, y + Math.sin(x / 90 + i) * 20 + Math.sin(x / 33) * 6); ctx.stroke(); } }).tex;
const ball = new THREE.Mesh(new THREE.SphereGeometry(1, 128, 96), new THREE.MeshPhysicalMaterial({ map: cremaTex, roughness: .2, clearcoat: .5, normalMap: ripple.tex, normalScale: new THREE.Vector2(.25, .25) })); K.space.add(ball);
const jupTex = canvasTex(1024, 512, (ctx, w, h) => { const cols = ['#d8c3a5', '#b58a5f', '#e8dcc6', '#a8724a', '#d9b98f', '#8f5e3a', '#efe3cf', '#c29a6b']; const r = rand(12); let y = 0; while (y < h) { const bh = 12 + r() * 40; ctx.fillStyle = cols[Math.floor(r() * cols.length)]; ctx.fillRect(0, y, w, bh); y += bh; }
  ctx.fillStyle = '#c0583a'; ctx.beginPath(); ctx.ellipse(w * .62, h * .62, 60, 28, 0, 0, 7); ctx.fill(); }).tex;
const jupiter = new THREE.Mesh(new THREE.SphereGeometry(1, 128, 96), new THREE.MeshStandardMaterial({ map: jupTex, roughness: .9 })); K.space.add(jupiter);

// ---------- timeline (0.35 L × 2^minute; every number checked) ----------
const L = m => 0.35 * Math.pow(2, m);
const B = [
  { t: 3.2, m: 0, cap: 'Jeremy grabs his usual coffee…', hi: ['coffee…'] },
  { t: 5.6, m: 1, cap: 'Minute 1: it doubles. The cup overflows.', hi: ['doubles.'] },
  { t: 8.0, m: 3, cap: 'Minute 3: it’s pouring off the table.', hi: ['pouring'] },
  { t: 10.4, m: 6, cap: 'Minute 6: 22 litres around his feet.', hi: ['22', 'litres'], bubble: 'OMG!' },
  { t: 12.8, m: 9, cap: 'Minute 9: a full bathtub of coffee.', hi: ['bathtub'] },
  { t: 15.2, m: 12, cap: 'Minute 12: a hot tub’s worth.', hi: ['hot', 'tub’s'], big: true },
  { t: 17.6, m: 16, cap: 'Minute 16: a whole tanker truck.', hi: ['tanker', 'truck.'], bubble: 'NOPE!' },
  { t: 20.0, m: 20, cap: 'Minute 20: the street floods.', hi: ['floods.'], big: true },
  { t: 22.4, m: 23, cap: 'Minute 23: more than an Olympic pool.', hi: ['Olympic', 'pool.'] },
  { t: 24.8, m: 27, cap: 'Minute 27: 7 metres deep. Cars float away.', hi: ['7', 'metres'], bubble: 'HELP!' },
  { t: 27.2, m: 33, cap: 'Minute 33: the whole city is a coffee lake.', hi: ['coffee', 'lake.'], big: true },
  { t: 29.6, m: 40, cap: 'Minute 40: enough to fill 150,000 Olympic pools.', hi: ['150,000'], space: true },
  { t: 32.0, m: 51, cap: 'Minute 51: more coffee than Lake Erie.', hi: ['Lake', 'Erie.'], space: true },
  { t: 34.4, m: 72, cap: 'Minute 72: more than ALL of Earth’s oceans.', hi: ['ALL'], red: ['oceans.'], big: true, space: true },
  { t: 36.8, m: 82, cap: 'Minute 82: the coffee is bigger than EARTH.', red: ['EARTH.'], big: true, space: true },
  { t: 39.2, m: 92, cap: 'Minute 92: bigger than JUPITER.', red: ['JUPITER.'], big: true, space: true },
  { t: 41.6, m: 92, cap: 'All from ONE cup of coffee. ☕', hi: ['ONE', 'cup'] },
  { t: 44.0, m: 92, cap: 'What should double next? 👇', hi: ['double', 'next?'] },
].map(b => ({ ...b, v: L(b.m) }));

function hideProps() { [dome, tPuddle, stream, gPuddle, mound, lake, ...floaters].forEach(o => o.visible = false); spot.visible = false; brownEarth.material.opacity = 0; ball.visible = false; jupiter.visible = false; }
function jer(x, z, ry, pose) { J.visible = true; J.position.set(x, .18, z); J.rotation.set(0, ry, 0); J.pose(pose); }
const t2 = V(TABLE.x, TABLE.y, TABLE.z);

run({
  total: 46.5, ctaAt: 41.6, sub: 'of Jeremy’s coffee',
  reel: ['(x)', 'GRAVITY DOUBLED', 'YOUR CAR NEVER STOPPED', 'EARTH STOPPED', 'YOU DOUBLED 1¢', 'THE MOON VANISHED', 'YOUR COFFEE DOUBLED EVERY MINUTE?'],
  beats: B,
  label: (b) => b.t >= 41.6 ? 'MINUTE 92' : 'MINUTE ' + b.m,
  fmt: v => fmtBig(v, 'L'),
  introShot(t) { mode('street'); hideProps(); jer(20.5, 5.6, -Math.PI / 2, { expr: 'happy', bob: Math.abs(Math.sin(t * 6)) * .03, armL: .2, armR: .2 }); J.position.x = 16 + t * .9;
    dolly(V(10, 9, -4), V(13, 6, -1), V(20, 1.5, 6), V(20, 1.2, 6), t / 3.2); },
  shot(t, b, lt, i) {
    hideProps(); flood.normalMap.offset.set(t * .02, t * .013); coffee.normalMap.offset.set(t * .05, t * .03);
    const k = clamp(lt / .7), m = b.m;
    if (b.space) mode('space'); else mode('street');
    if (i === 0) { // POV walking up to Café π, cup in hand
      pov(true); const x = 13 + lt * 1.5, bob = Math.sin(t * 9) * .03; cam(V(x, 1.62 + bob, 5.3), V(x + 6, 1.2, 6.6)); K.hands.right.rotation.z = Math.sin(t * 9) * .03;
    } else if (i === 1) { // close-up: dome rises over the rim
      dome.visible = true; dome.scale.set(1, lerp(.05, .55, eOut(k)), 1);
      dolly(V(TABLE.x + .28, TABLE.y + .2, TABLE.z - .32), V(TABLE.x + .22, TABLE.y + .16, TABLE.z - .26), V(TABLE.x, TABLE.y + .08, TABLE.z), V(TABLE.x, TABLE.y + .09, TABLE.z), lt / 2.4);
    } else if (i === 2) { // spilling across the table and off the edge
      dome.visible = true; dome.scale.set(1, .6, 1); tPuddle.visible = true; tPuddle.scale.setScalar(lerp(.1, .44, eOut(k)));
      stream.visible = lt > .4; const sl = TABLE.y - .18; stream.position.set(TABLE.x + .3, .18 + sl / 2, TABLE.z - .3); stream.scale.set(1, sl * clamp((lt - .4) / .3), 1); stream.position.y = TABLE.y - sl * clamp((lt - .4) / .3) / 2;
      gPuddle.visible = lt > .7; gPuddle.scale.setScalar(lerp(.05, .5, clamp((lt - .7) / 1.2)));
      dolly(V(TABLE.x + .75, 1.0, TABLE.z - .95), V(TABLE.x + .65, .85, TABLE.z - .85), V(TABLE.x, .62, TABLE.z), V(TABLE.x, .5, TABLE.z), lt / 2.4);
    } else if (i === 3) { // Jeremy, shocked, standing in it
      tPuddle.visible = true; tPuddle.scale.setScalar(.45); stream.visible = true; gPuddle.visible = true; gPuddle.scale.setScalar(lerp(.6, 1.6, eOut(k)));
      jer(21.6, 5.9, Math.PI + .25, { expr: 'shocked', armL: 2.3, armR: 2.3, look: .3, sweatK: lt * .8, bob: lt < .3 ? Math.sin(lt * 30) * .04 : 0 });
      dolly(V(23.4, 1.7, 2.4), V(23.2, 1.6, 2.8), V(21.6, 1.0, 6), V(21.6, 1.0, 6), lt / 2.4);
      bubble(t, b.bubble, b.t + .2, headPos());
    } else if (i === 4) { // bathtub
      tPuddle.visible = true; tPuddle.scale.setScalar(.45); stream.visible = true; gPuddle.visible = true; gPuddle.scale.setScalar(lerp(1.6, 2.9, eOut(k)));
      jer(lerp(21, 19.5, eOut(k)), 5.4, -Math.PI / 2 - .5, { expr: 'worried', armL: .8, armR: .8, bob: Math.abs(Math.sin(t * 9)) * .04 });
      dolly(V(15.5, 3.4, 1.0), V(16, 3.1, 1.4), V(21.5, .4, 6.4), V(21.5, .4, 6.4), lt / 2.4);
    } else if (i === 5 || i === 6) { // the coffee mound
      gPuddle.visible = true; gPuddle.scale.setScalar(i === 5 ? 3.4 : 5.5); mound.visible = true;
      const R = lerp(moundR(B[i - 1].v), moundR(b.v), eOut(k)); const w = 1 + Math.sin(t * 7) * .015; mound.scale.set(R * w, R * .55 / w, R * w); mound.position.y = .18;
      if (i === 5) { jer(19.6, 5.0, -Math.PI / 2 - 1.0, { expr: 'shocked', armL: 2.2, armR: 2.2, look: .5, sweatK: lt }); dolly(V(16.5, 2.4, 1.2), V(16.2, 2.6, .9), V(21.5, 1.0, 6.2), V(21.5, 1.2, 6.2), lt / 2.4); }
      else { const run_ = lt * 3.2; jer(17.5 - run_, 5.2, -Math.PI / 2, { expr: 'panic', armL: 2.5 + Math.sin(t * 16) * .4, armR: 2.5 - Math.sin(t * 16) * .4, bob: Math.abs(Math.sin(t * 14)) * .1, look: .8, sweatK: lt * 2 });
        cam(V(13.5 - run_ * .6, 2.6, 1.2), V(18 - run_ * .4, 1.6, 6)); bubble(t, b.bubble, b.t + .3, headPos()); }
    } else if (i >= 7 && i <= 9) { // flood rising
      lake.visible = true; const lv = [[.05, .35], [.35, 1.0], [1.0, 7]][i - 7]; const y = lerp(lv[0], lv[1], eOut(clamp(lt / 1.6))); lake.position.set(20, y + Math.sin(t * 2) * .02, 0);
      if (i === 7) dolly(V(6, 4.5, -2.5), V(7, 4, -2), V(20, .3, 6), V(20, .3, 6), lt / 2.4);
      if (i === 8) { jer(15.2, 5.4, -Math.PI / 2 - .6, { expr: 'worried', armL: 1.6, armR: 1.6, bob: Math.sin(t * 3) * .02 }); dolly(V(10.5, 1.8, 1.5), V(10.2, 2.0, 1.2), V(16, .8, 5), V(16, .8, 5), lt / 2.4); }
      if (i === 9) { floaters.forEach((c, j) => { c.visible = true; c.position.y = y - .5 + Math.sin(t * 1.6 + j) * .08; c.rotation.z = Math.sin(t * 1.3 + j) * .05; c.position.x = 16 + j * 6 + lt * .4; });
        const car = floaters[0]; jer(car.position.x - .2, car.position.z, Math.PI + .4, { expr: 'panic', armL: 2.6 + Math.sin(t * 12) * .3, armR: 2.6 - Math.sin(t * 12) * .3, sweatK: lt * 2 }); J.position.y = car.position.y + 1.66;
        dolly(V(14, y + 3.5, -5), V(14.5, y + 3, -4.5), V(17, y + 1.2, 1.5), V(17, y + 1.2, 1.5), lt / 2.4); bubble(t, b.bubble, b.t + .3, headPos()); }
    } else if (i === 10) { // city lake from above
      lake.visible = true; lake.position.set(20, lerp(7, 27, eOut(clamp(lt / 2))), 0); lake.scale.set(1, 1, 1);
      dolly(V(-20, 60, -70), V(-30, 110, -90), V(25, 5, 10), V(25, 0, 10), lt / 2.4);
    } else if (i >= 11 && i <= 13) { // Earth: a brown stain spreads, then the oceans go brown
      const rot = t * .08; K.earth.rotation.y = rot; brownEarth.rotation.y = rot; K.clouds.rotation.y = rot * 1.2;
      spot.visible = i < 13; spot.rotation.set(1.15, 0, .5 + 0); spot.scale.setScalar(1);
      const cap = i === 11 ? lerp(.02, .06, eOut(k)) : i === 12 ? lerp(.06, .16, eOut(k)) : .16;
      spot.geometry = capGeo(cap); spot.rotation.y = rot;
      brownEarth.material.opacity = i === 13 ? eOut(clamp(lt / 1.2)) : 0;
      const d = i === 11 ? 15 : i === 12 ? 14 : 15.5; dolly(V(d * .35, 2.2, d), V(d * .3, 1.8, d * .96), V(0, 0, 0), V(0, 0, 0), lt / 2.4, 0, 45);
    } else if (i === 14) { // coffee ball bigger than Earth
      brownEarth.material.opacity = 0; ball.visible = true; const R = lerp(.5, 3 * Math.cbrt(b.v / 1.083e24), eOut(k)); ball.scale.setScalar(R); ball.position.set(7.4, 0, -1); ball.rotation.y = t * .1; K.earth.rotation.y = t * .08;
      ball.rotation.set(Math.PI / 2 - .5, 0, t * .1); dolly(V(3.7, 2.5, 26), V(3.7, 2.2, 28), V(3.7, 0, 0), V(3.7, 0, 0), lt / 2.4, 0, 45);
      tag('EARTH', V(0, -4, 0), '#7fd0ff'); tag('COFFEE', V(7.4, -R - 1, -1), '#ffb36b');
    } else if (i === 15) { // ...bigger than Jupiter
      ball.visible = true; jupiter.visible = true; const RJ = 33.6, RB = 3 * Math.cbrt(b.v / 1.083e24);
      jupiter.scale.setScalar(RJ); jupiter.position.set(-40, 0, -60); jupiter.rotation.y = t * .05;
      ball.scale.setScalar(lerp(3.5, RB, eOut(k))); ball.position.set(40, 0, -60); ball.rotation.set(Math.PI / 2 - .5, 0, t * .06);
      dolly(V(0, 20, 190), V(0, 26, 215), V(0, 0, -60), V(0, 0, -60), lt / 2.4, 0, 50);
      tag('JUPITER', V(-40, -40, -60), '#ffd8a0'); tag('COFFEE', V(40, -40, -60), '#ffb36b');
    } else { // back on the street: sip (POV), then CTA
      if (i === 16) { pov(true); const lift = Math.sin(clamp((lt - .6) / 1.2) * Math.PI); cam(V(21, 1.62, 5.3), V(26, 1.0 + lift * .4, 6.8)); K.hands.right.position.y = -.15 + lift * .07; K.hands.right.rotation.x = .2 + lift * .5; }
      else { K.hands.right.position.y = -.15; K.hands.right.rotation.x = .2; jer(21.5, 5.8, Math.PI + .1, { expr: 'happy', armL: .2 + Math.abs(Math.sin(t * 5)) * 2.6, armR: .3, bob: Math.abs(Math.sin(t * 5)) * .03, look: .1 });
        dolly(V(21.4, 1.5, 3.4), V(21.4, 1.45, 3.7), V(21.5, 1.35, 6), V(21.5, 1.35, 6), lt / 2.4); }
    }
    if (b.big && lt < .35) shake(.06 * (1 - lt / .35) * (b.space ? 2 : 1), t);
  },
});
const caps = new Map();
function capGeo(th) { const key = th.toFixed(3); if (!caps.has(key)) caps.set(key, new THREE.SphereGeometry(3.012, 96, 24, 0, 6.283, 0, th)); return caps.get(key); }
