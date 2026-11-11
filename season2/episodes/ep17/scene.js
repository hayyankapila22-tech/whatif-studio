// Episode 17 — What if a nuclear bomb went off near your city?  (original street look + AI voiceover; beats timed to vo.json)
// Educational / preparedness framing: what happens in the first seconds, minutes and days, and what official guidance says to do. No casualties shown.
// Facts (checked 2026-11-12):
//  - bright flash can cause temporary blindness; blast wave; fallout; "you will have 10 minutes or more to find an adequate shelter before
//    fallout arrives"; shelter in brick or concrete, basement or the middle of the building; stay inside 24 hours unless told otherwise;
//    "GET INSIDE, STAY INSIDE, STAY TUNED" — FEMA / Ready.gov "Nuclear Explosion" (https://www.ready.gov/nuclear-explosion)
//  - fireball temperatures reach tens of millions of degrees at first (hotter than the Sun's ~5,500 °C surface) — atomicarchive.com "Effects of Nuclear Weapons"
//  - the shock front initially travels faster than sound (same source; Glasstone & Dolan, "The Effects of Nuclear Weapons")
//  - 7-10 rule of thumb: for every 7-fold increase in time after detonation, fallout dose rate falls 10-fold -> ~10% at 7 h, ~1% at 49 h (2 days)
//    of the 1-hour level (FEMA "Planning Guidance for Response to a Nuclear Detonation")
import { THREE, RoundedBoxGeometry, scene, camera, canvasTex, rand, clamp, prog, lerp, eOut, eInOut, V, K, boot, mode, dolly, shake, headPos, run, tag, focus, noFocus, RIM, GRADE, INK, rimLight } from './kit.js';
import { buildWorld, W, setAge, setSky } from './world.js';

await boot('WHAT IF A NUKE WENT OFF TODAY?', 'EP. 17');
const VO = await (await fetch('./vo.json')).json(), LN = VO.lines;
const J = K.J;
buildWorld(K);
const $ = id => document.getElementById(id);

// ---------- clear the set ----------
const S = K.street.group;
const near = (o, x, z) => Math.abs(o.position.x - x) < .1 && Math.abs(o.position.z - z) < .1;
S.children.forEach(o => { if ([[21, 4.8], [30, 4.8], [35, -4.8], [26, -4.8], [33, -7.2]].some(([x, z]) => near(o, x, z))) o.visible = false; });
const parked = W.cars.find(c => near(c, 26, 3.2)); W.cars.forEach(c => { if (near(c, 40, -3.2)) c.visible = false; });
const std = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .6, ...o });
const shadows = g => { g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };
const hash = (n) => { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); };

// ---------- distant fireball + mushroom cloud (far down the street, towards +x) ----------
const CX = 330, CZ = -20;
const fireball = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 32), new THREE.MeshBasicMaterial({ color: 0xfff1c9, toneMapped: false, fog: false, transparent: true })); scene.add(fireball); fireball.visible = false;
const glowTex = canvasTex(256, 256, (ctx, w, h) => { const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); g.addColorStop(0, 'rgba(255,245,215,1)'); g.addColorStop(.3, 'rgba(255,190,90,.6)'); g.addColorStop(1, 'rgba(255,120,30,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex;
const fireGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, fog: false })); scene.add(fireGlow); fireGlow.visible = false; INK.skip.push(fireGlow);
const cloud = (() => { const g = new THREE.Group(), r = rand(21);
  const mat = new THREE.MeshStandardMaterial({ color: 0x8f867e, roughness: 1, fog: false, emissive: 0xff5a1a, emissiveIntensity: .0 }); g.userData.mat = mat;
  const dark = new THREE.MeshStandardMaterial({ color: 0x6f6862, roughness: 1, fog: false, emissive: 0xff5a1a, emissiveIntensity: .0 }); g.userData.dark = dark;
  const hot = new THREE.MeshStandardMaterial({ color: 0xcf9a6a, roughness: 1, fog: false, emissive: 0xff6a1a, emissiveIntensity: .9 }); g.userData.hot = hot;
  const add = (x, y, z, s, m = mat, sy = 1) => { const b = new THREE.Mesh(new THREE.SphereGeometry(1, 18, 12), m); b.position.set(x, y, z); b.scale.set(s, s * sy, s); g.add(b); };
  for (let i = 0; i < 44; i++) { const y = 4 + i * 2.6, a = r() * 6.283, d = 2 + r() * 5; add(Math.cos(a) * d, y, Math.sin(a) * d, 6.5 + r() * 4 + (y < 20 ? (20 - y) * .5 : 0), r() < .35 ? dark : mat); }   // lumpy stem
  for (let i = 0; i < 26; i++) { const a = i / 26 * 6.283 + r() * .2, d = 24 + r() * 14; add(Math.cos(a) * d, 3 + r() * 5, Math.sin(a) * d, 7 + r() * 6, r() < .5 ? dark : mat, .7); }                 // base surge
  for (let i = 0; i < 70; i++) { const a = r() * 6.283, d = Math.sqrt(r()) * 46; add(Math.cos(a) * d, 132 + (r() - .35) * 16 - d * .2, Math.sin(a) * d, 11 + r() * 9, r() < .3 ? dark : mat, .85); }  // cap
  for (let i = 0; i < 24; i++) { const a = i / 24 * 6.283 + r() * .2; add(Math.cos(a) * (50 + r() * 4), 116 + r() * 7, Math.sin(a) * (50 + r() * 4), 9 + r() * 5, r() < .4 ? dark : mat, .9); }      // rolling rim
  for (let i = 0; i < 12; i++) { const a = i / 12 * 6.283; add(Math.cos(a) * 20, 113 + r() * 5, Math.sin(a) * 20, 11, hot); }                                                                       // glowing underside
  g.position.set(CX, 0, CZ); scene.add(g); g.visible = false; return g; })();
function nuke(kFire, kCloud, glow = 0) { // kFire 0..1 fireball brightness/size, kCloud 0..1 cloud growth
  fireball.visible = fireGlow.visible = kFire > 0; if (kFire > 0) { const s = 18 + 24 * kFire; fireball.position.set(CX, 36 + 46 * kCloud, CZ); fireball.scale.setScalar(s * (1 - kCloud * .55)); fireball.material.opacity = clamp(kFire * 1.5);
    fireGlow.position.copy(fireball.position); fireGlow.scale.setScalar(s * 7 * kFire); fireGlow.material.opacity = kFire; }
  cloud.visible = kCloud > 0; cloud.scale.set(.7 * (.55 + .45 * kCloud), .7 * Math.max(.02, kCloud), .7 * (.55 + .45 * kCloud)); cloud.userData.mat.emissiveIntensity = glow * .22; cloud.userData.dark.emissiveIntensity = glow * .12; cloud.userData.hot.emissiveIntensity = .25 + glow; }

// ---------- blast wave dust + flying debris ----------
const dustTex = canvasTex(256, 256, (ctx, w, h) => { const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); g.addColorStop(0, 'rgba(214,196,172,.95)'); g.addColorStop(.6, 'rgba(206,188,166,.5)'); g.addColorStop(1, 'rgba(200,184,160,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex;
const DUST = [...Array(46)].map((_, i) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: dustTex, transparent: true, depthWrite: false })); scene.add(s); INK.skip.push(s); s.visible = false; return s; });
const BITS = (() => { const m = new THREE.InstancedMesh(new THREE.BoxGeometry(.16, .01, .22), std(0xe9e4d8, { side: THREE.DoubleSide }), 40); m.frustumCulled = false; scene.add(m); m.visible = false; return m; })();
const dm = new THREE.Object3D();
function blast(k, t, cx) { // k: 0..1.4  wave front sweeps from +x to -x past cx
  const on = k > 0 && k < 1.5; DUST.forEach(s => s.visible = on); BITS.visible = on; if (!on) return;
  const front = cx + 16 - k * 30;
  DUST.forEach((s, i) => { const lag = hash(i) * 12; s.position.set(front + lag, .6 + hash(i * 3 + 1) * 3.4, -3 + hash(i * 5 + 2) * 11); s.scale.setScalar(3.2 + hash(i * 7) * 3.5); s.material.opacity = .5 * clamp(k * 5) * clamp((1.5 - k) * 2); });
  for (let i = 0; i < BITS.count; i++) { const x = front + 4 + hash(i * 11) * 14 - (t * 3 % 1); dm.position.set(x, .4 + hash(i * 13 + 3) * 3 + Math.sin(t * 6 + i) * .2, -1 + hash(i * 17 + 4) * 9); dm.rotation.set(t * 9 + i, t * 7 + i * 2, i); dm.updateMatrix(); BITS.setMatrixAt(i, dm.matrix); } BITS.instanceMatrix.needsUpdate = true;
}

// ---------- basement shelter set (built high above the street, closed box, lit by one warm bulb) ----------
const BY = 200, BXc = 24;
const fillLight = new THREE.PointLight(0xffe6c4, 0, 16, 1.4); fillLight.position.set(BXc + .6, BY + 1.9, -3.4); scene.add(fillLight);
const bulbLight = new THREE.PointLight(0xffd9a0, 0, 14, 1.6); bulbLight.position.set(BXc + 2.2, BY + 2.5, -.5); bulbLight.castShadow = true; bulbLight.shadow.mapSize.set(1024, 1024); bulbLight.shadow.bias = -.002; scene.add(bulbLight);
const room = (() => { const g = new THREE.Group();
  const conc = canvasTex(512, 512, (ctx, w, h) => { const r = rand(4); ctx.fillStyle = '#8f8c88'; ctx.fillRect(0, 0, w, h); for (let i = 0; i < 2400; i++) { const v = 120 + r() * 50; ctx.fillStyle = `rgba(${v},${v},${v - 4},.18)`; ctx.fillRect(r() * w, r() * h, 2 + r() * 10, 2 + r() * 6); }
    ctx.strokeStyle = 'rgba(60,58,55,.5)'; ctx.lineWidth = 3; for (let y = 0; y < h; y += 128) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); for (let x = (y / 128 % 2) * 128; x < w; x += 256) { ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y + 128); ctx.stroke(); } } }).tex;
  conc.wrapS = conc.wrapT = THREE.RepeatWrapping; conc.repeat.set(2, 1.2); const wall = new THREE.MeshStandardMaterial({ map: conc, roughness: .95 }), floorM = std(0x5d5a57, { roughness: .9 });
  const box = (w, h, d, x, y, z, m) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); b.position.set(x, y, z); g.add(b); return b; };
  box(7, .2, 6, 0, -.1, 0, floorM); box(7, .2, 6, 0, 3.3, 0, std(0x6a6763)); box(7, 3.4, .2, 0, 1.6, 2.4, wall); box(.2, 3.4, 6, -3.4, 1.6, 0, wall); box(.2, 3.4, 6, 3.4, 1.6, 0, wall);
  // shelf with cans and water
  const wood = std(0x8a6a44, { roughness: .7 }); for (const y of [1.0, 1.75]) box(2.3, .06, .5, -1.7, y, 2.0, wood); for (const x of [-2.8, -.6]) box(.07, 1.9, .5, x, .95, 2.0, wood);
  const cols = [0xd8402f, 0x2f8fd0, 0xe8b23a, 0x3fa05a, 0xd8402f, 0xe8e2d2];
  for (let i = 0; i < 6; i++) { const c = new THREE.Mesh(new THREE.CylinderGeometry(.09, .09, .24, 20), std(cols[i], { roughness: .35, metalness: .3 })); c.position.set(-2.55 + i * .24, 1.9, 2.0); g.add(c); const band = new THREE.Mesh(new THREE.CylinderGeometry(.092, .092, .1, 20), std(0xf4f0e6)); band.position.copy(c.position); g.add(band); }
  for (let i = 0; i < 3; i++) { const j = new THREE.Mesh(new THREE.CylinderGeometry(.17, .17, .42, 20), new THREE.MeshPhysicalMaterial({ color: 0x8fd0f2, roughness: .08, transparent: true, opacity: .75 })); j.position.set(-2.4 + i * .5, 1.27, 2.0); g.add(j); const cap = new THREE.Mesh(new THREE.CylinderGeometry(.07, .07, .07, 12), std(0x2f6dff)); cap.position.set(-2.4 + i * .5, 1.51, 2.0); g.add(cap); }
  // table + radio
  box(1.1, .06, .7, 1.75, .78, 1.2, wood); for (const [x, z] of [[1.28, .92], [2.22, .92], [1.28, 1.48], [2.22, 1.48]]) box(.06, .78, .06, x, .39, z, wood);
  const radio = new THREE.Group(); const body = new THREE.Mesh(new RoundedBoxGeometry(.56, .34, .2, 4, .04), std(0xc8402f, { roughness: .35 })); radio.add(body);
  const grille = new THREE.Mesh(new THREE.CircleGeometry(.11, 28), std(0x25272c, { roughness: .8 })); grille.position.set(-.12, 0, -.101); grille.rotation.y = Math.PI; radio.add(grille);
  const dial = new THREE.Mesh(new THREE.CylinderGeometry(.05, .05, .03, 20), std(0xe9e4d8)); dial.rotation.x = Math.PI / 2; dial.position.set(.15, .04, -.11); radio.add(dial);
  const led = new THREE.Mesh(new THREE.SphereGeometry(.018, 10, 8), new THREE.MeshBasicMaterial({ color: 0x5dff8a, toneMapped: false })); led.position.set(.15, -.08, -.105); radio.add(led); g.userData.led = led;
  const ant = new THREE.Mesh(new THREE.CylinderGeometry(.008, .008, .6, 6), std(0xcfd3da, { metalness: 1, roughness: .3 })); ant.position.set(.22, .44, 0); ant.rotation.z = -.25; radio.add(ant);
  radio.position.set(1.75, .98, 1.2); radio.rotation.y = .25; g.add(radio);
  // hanging bulb
  box(.015, .6, .015, 2.2, 2.95, -.5, std(0x222222)); const bulb = new THREE.Mesh(new THREE.SphereGeometry(.09, 16, 12), new THREE.MeshBasicMaterial({ color: 0xfff0c8, toneMapped: false })); bulb.position.set(2.2, 2.62, -.5); g.add(bulb);
  g.traverse(o => { if (o.isMesh && o !== bulb && o !== led) { o.castShadow = true; o.receiveShadow = true; } }); g.position.set(BXc, BY, 0); scene.add(g); g.visible = false; return g; })();

// ---------- HUD extras: white flash + "radiation outside" meter ----------
$('ui').insertAdjacentHTML('beforeend', `<div id="nflash" style="position:absolute;inset:0;background:#fffdf2;opacity:0;pointer-events:none"></div>
 <div id="rad" style="position:absolute;left:90px;top:560px;width:810px;opacity:0;font-family:IDB;color:#fff;text-shadow:0 3px 10px rgba(0,0,0,.6)">
  <div style="font-size:40px;letter-spacing:4px;display:flex;justify-content:space-between"><span>RADIATION OUTSIDE</span><span id="radp">100%</span></div>
  <div style="height:48px;margin-top:12px;border-radius:24px;background:rgba(10,11,24,.7);border:3px solid rgba(255,255,255,.85);overflow:hidden"><div id="radf" style="height:100%;width:100%;border-radius:20px"></div></div></div>
 <div id="adv" style="position:absolute;left:60px;right:150px;top:690px;text-align:center;font-family:IDB;font-size:62px;line-height:1.25;-webkit-text-stroke:7px #0a0b18;paint-order:stroke fill"><div style="color:#3dffb0">1. GET INSIDE</div><div style="color:#ffe53d">2. STAY INSIDE</div><div style="color:#fff">3. STAY TUNED</div></div>`);
const advice = (lt) => [...$('adv').children].forEach((c, n) => c.style.opacity = lt < 0 ? 0 : clamp((lt - [1.7, 2.75, 3.7][n]) / .25));
function radBar(a, pct) { $('rad').style.opacity = a; if (a <= 0) return; const p = Math.max(pct, 1); $('radp').textContent = (pct >= 9.5 ? Math.round(pct) : pct.toFixed(pct < 1.5 ? 0 : 1)) + '%';
  $('radf').style.width = Math.max(1.5, p) + '%'; $('radf').style.background = pct > 50 ? '#ff3d55' : pct > 8 ? '#ffab1f' : '#3dffb0'; }

// ---------- timeline from the voiceover ----------
const T = LN.map(l => l.t0 - .12), total = VO.total, cap = i => LN[i].show;
const SEC = 1 / 86400, MIN = 1 / 1440, HR = 1 / 24;
const B = [
  { t: T[1], v: 1 * SEC, capY: 1225, cap: cap(1), red: ["Don't", 'look'], hi: ['brighter'], big: true },
  { t: T[2], v: 3 * SEC, capY: 1225, cap: cap(2), hi: ['hotter'], size: 62 },
  { t: T[3], v: 15 * SEC, capY: 1225, cap: cap(3), red: ['blast', 'wave'], big: true },
  { t: T[4], v: 1 * MIN, capY: 1225, cap: cap(4), hi: ['10', 'minutes'], note: 'Ready.gov: "10 minutes or more" to find shelter' },
  { t: T[5], v: 5 * MIN, capY: 1225, cap: cap(5), hi: ['Get', 'inside.'], size: 60 },
  { t: T[6], v: 1 * HR, capY: 1225, cap: cap(6), hi: ['fades', 'fast.'] },
  { t: T[7], v: 7 * HR, capY: 1225, cap: 'After 7 hours: 90% gone.', hi: ['90%'], note: 'The 7-10 rule of thumb (FEMA)' },
  { t: T[7] + (LN[7].t1 - LN[7].t0) * .55, v: 2, s: 6.5, capY: 1225, cap: 'After 2 days: 99% gone.', hi: ['99%'], note: 'The 7-10 rule of thumb (FEMA)' },
  { t: T[8], v: 2, capY: 610, size: 56, cap: cap(8), hi: ['simple:'], note: 'Source: FEMA / Ready.gov' },
  { t: T[9], v: 2, capY: 1225, cap: cap(9), hi: ['YOU'], size: 60 },
];
{ let n = 0; B.forEach(b => { if (b.s === undefined) b.s = n++; }); }
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;
function fmt(v) { const s = v * 86400; if (s < 59.5) return plural(Math.max(1, Math.round(s)), 'second'); if (s < 3570) return plural(Math.round(s / 60), 'minute'); if (v < .98) return plural(Math.max(1, Math.round(v * 24)), 'hour'); return plural(Math.round(v), 'day'); }

// ---------- helpers ----------
const JX = 23.4, JZ = 6.0;
function jer(x, z, ry, pose, cup = false) {
  J.visible = true; J.position.set(x, .18, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose);
  if (cup) { J.arms[1].rotation.x = -1.15; J.arms[1].add(W.cup); W.cup.position.set(-.02, -.74, .05); W.cup.rotation.set(1.15, 0, 0); W.cup.visible = true; }
}
function hideAll() {
  J.visible = false; J.arms[1].rotation.x = 0; J.arms[0].rotation.x = 0; if (W.cup.parent !== scene) scene.add(W.cup); W.cup.visible = false; W.splash.visible = false; W.sparkle.visible = false;
  nuke(0, 0); blast(0, 0, 0); room.visible = false; bulbLight.intensity = 0; fillLight.intensity = 0; radBar(0, 100); advice(-1); $('nflash').style.opacity = 0;
  noFocus(); RIM.k = .55; INK.on = true; GRADE.split = .08; GRADE.gain = 1.1; GRADE.sat = 1.05; if (parked) parked.visible = false;
}
const bob = (t, ph = 0, a = .012) => Math.sin(t * 7 + ph) * a, step = (t, ph = 0) => Math.abs(Math.sin(t * 6 + ph)) * .03;
function basement(t, jx, pose, ry = Math.PI) { setSky('night'); setAge(0, t, { lamps: 0 }); room.visible = true; bulbLight.intensity = 15 + Math.sin(t * 13) * .4; fillLight.intensity = 6; GRADE.split = .12; GRADE.gain = 1.08; RIM.k = .2;
  jer(jx, .6, ry, pose); J.position.y = BY; room.userData.led.visible = Math.floor(t * 2) % 2 === 0; }
const camB = (k, x0 = 0, x1 = 0, d0 = 5.6, d1 = 5.2) => dolly(V(BXc + x0, BY + 1.6, -d0), V(BXc + x1, BY + 1.6, -d1), V(BXc + x0 * .5, BY + 1.3, 1.2), V(BXc + x1 * .5, BY + 1.3, 1.2), k, 0, 50);

run({
  total, ctaAt: T[9], sub: '',
  reel: ['(x)', 'ROBOTS TOOK EVERY JOB', 'ALL HUMANS VANISHED', 'A BLACK HOLE DOUBLED', 'WE COULD READ MINDS', 'ROME NEVER FELL', 'A NUKE WENT OFF TODAY?'],
  beats: B, label: () => 'TIME SINCE THE FLASH', fmt,
  beds: [{ t0: 0, t1: T[1] + .1, name: 'city', gain: .28 }, { t0: T[1], t1: T[3] + .1, name: 'drone', gain: .3 }, { t0: T[3], t1: T[5] + 2.6, name: 'wind', gain: .26 }, { t0: T[5] + 2.4, t1: T[9] + .1, name: 'drone', gain: .12 }, { t0: T[9], t1: total, name: 'birds', gain: .2 }],
  sfx: [{ t: T[1] + .05, name: 'swell', gain: .5 }, { t: T[2] + .1, name: 'rumble_low', gain: .5 }, { t: T[3] + .9, name: 'wind_gust', gain: .6 }, { t: T[3] + 1.0, name: 'rumble_low', gain: .8 }, { t: T[3] + 1.5, name: 'crack', gain: .45, pan: -.3 }, { t: T[3] + 1.9, name: 'crack', gain: .35, pan: .3 },
    { t: T[4] + .2, name: 'siren', gain: .22, pan: .3 }, { t: T[6] + .3, name: 'hiss', gain: .16 }, { t: T[7] + .2, name: 'chime', gain: .28 }, { t: T[7] + 3.0, name: 'chime', gain: .28 }, { t: T[8] + 2.0, name: 'ding', gain: .28 }, { t: T[9] + .1, name: 'sparkle_rev', gain: .35 }],
  introShot(t) {
    mode('street'); hideAll(); setSky('day'); setAge(0, t, { lamps: 0 });
    jer(lerp(19.6, JX, eOut(clamp(t / 3.2))), JZ, Math.PI / 2 + .3 * clamp(t / 3), { expr: 'happy', bob: step(t) * (1 - clamp((t - 2.8) / .5)), armL: .25 }, true);
    dolly(V(22.2, 1.6, -.6), V(23.2, 1.55, .2), V(21.0, 1.5, 6.2), V(23.3, 1.55, 6.0), t / 3.3, 0, 52);
    focus(V(J.position.x, 1.2, JZ), .8, 10);
  },
  shot(t, b, lt, i0, next) {
    const i = b.s; mode('street'); hideAll(); const dur = (next ? next.t : total) - b.t, k = clamp(lt / dur);
    if (i === 0) { // the flash: everything goes white, Jeremy turns away and covers his eyes
      setSky('day', 'golden', clamp((lt - .2) / 2.5)); setAge(0, t, { lamps: 0 });
      const f = lt < .12 ? lt / .12 : Math.pow(clamp(1 - (lt - .12) / 2.2), 1.6); $('nflash').style.opacity = f * .96; GRADE.gain = 1.1 + 1.0 * f; RIM.k = .55 + 2.2 * f;
      const turn = eOut(clamp((lt - .25) / .5));
      jer(JX, JZ, Math.PI - .1 + turn * 1.15, { expr: lt > .15 ? 'panic' : 'happy', armL: .22, armR: .22, tilt: turn * .1, blink: lt > .2, bob: bob(t) });
      J.arms[0].rotation.x = -turn * 2.55; J.arms[1].rotation.x = -turn * 2.55; // forearms up in front of the face
      dolly(V(JX + .4, 1.55, .2), V(JX + .2, 1.55, .9), V(JX, 1.58, 6.2), V(JX, 1.58, 6.2), k, 0, 52); focus(V(JX, 1.4, JZ), .7, 10);
    } else if (i === 1) { // the fireball rises into a mushroom cloud, far down the street
      setSky('ominous'); setAge(0, t, { lamps: 0 }); GRADE.split = .15;
      const g = eOut(clamp(lt / (dur + .6))); nuke(1 - g * .75, clamp(.12 + g * .88), 1 - g * .5); GRADE.gain = 1.1 + .5 * (1 - g);
      dolly(V(50, 2.2, 1.0), V(52.5, 2.6, .8), V(330, 56, -20), V(330, 64, -20), k, 0, 44);
    } else if (i === 2) { // the blast wave hits the street: Jeremy ducks behind a parked car
      setSky('golden', 'ominous', .45); setAge(0, t, { lamps: 0 }); GRADE.split = .14; if (parked) parked.visible = true;
      const w = (lt - .9) / 2.6; blast(w, t, 26); nuke(.15, 1, .4);
      const duck = eOut(clamp((lt - .2) / .5));
      jer(26.2, 4.65, Math.PI + .2, { expr: 'panic', armL: .2 + duck * 2.3, armR: .2 + duck * 2.3, tilt: Math.sin(t * 20) * .02 * clamp(w * 4) * clamp((1.2 - w) * 3), blink: w > .1 && w < .9 }); J.position.y = .18 - duck * .12;
      J.arms[0].rotation.x = -duck * .5; J.arms[1].rotation.x = -duck * .5;
      if (w > 0 && w < 1.1) shake(.09 * clamp(w * 6) * clamp((1.1 - w) * 2), t);
      dolly(V(27.0, 2.9, -2.8), V(26.6, 2.8, -2.2), V(26.1, 1.0, 4.4), V(26.1, 1.0, 4.4), k, 0, 50); focus(V(26.2, 1.2, 4.2), .5, 8);
    } else if (i === 3) { // ten minutes: Jeremy looks at the cloud, then starts to move
      setSky('ominous'); setAge(0, t, { lamps: 0 }); GRADE.split = .14; nuke(.08, 1, .25);
      jer(52.9, .1, Math.PI / 2 - .12, { expr: 'worried', look: Math.sin(t * 1.3) * .2, bob: bob(t) }); J.position.y = .02;
      dolly(V(50.2, 2.1, 1.5), V(50.7, 2.15, 1.4), V(330, 36, -20), V(330, 40, -20), k, 0, 42); focus(V(330, 60, -20), .5, 8);
    } else if (i === 4) { // get inside: run for a building, then down to the basement
      if (lt < dur * .46) { setSky('ominous'); setAge(0, t, { lamps: 0 }); GRADE.split = .14;
        const u = clamp(lt / (dur * .46)), x = lerp(28.6, 23.6, u);
        jer(x, 6.2, -Math.PI / 2, { expr: 'worried', bob: Math.abs(Math.sin(t * 11)) * .06, armL: .5 + Math.sin(t * 11) * .3, armR: .5 - Math.sin(t * 11) * .3, tilt: .12 });
        dolly(V(26.2, 1.6, .4), V(24.4, 1.6, .7), V(27.4, 1.5, 6.2), V(23.9, 1.5, 6.2), u, 0, 52); focus(V(x, 1.3, 6.2), .6, 8);
      } else { const u = clamp((lt - dur * .46) / (dur * .54));
        basement(t, lerp(BXc + 2.6, BXc - .3, eOut(u)), { expr: u > .7 ? 'worried' : 'panic', bob: u < .8 ? Math.abs(Math.sin(t * 10)) * .04 : 0, look: u > .8 ? Math.sin(t * 2) * .5 : 0 }, u < .8 ? -Math.PI / 2 : Math.PI + .1);
        camB(u, .2, -.1, 5.9, 5.5); }
    } else if (i === 5) { // stay inside: listening to the radio
      basement(t, BXc - .2, { expr: lt > 2.6 ? 'confused' : 'worried', look: -.55, bob: bob(t, 0, .006), tilt: lt > 2.6 ? .08 : 0 }, Math.PI - .35);
      radBar(clamp((lt - .5) / .4), 100); camB(k, -.1, .25, 5.5, 5.0);
    } else if (i === 6 || i === 6.5) { // 7 hours: 90% gone ... 2 days: 99% gone
      const first = i === 6, p = first ? lerp(100, 10, eInOut(clamp((lt - .3) / 1.5))) : lerp(10, 1, eInOut(clamp((lt - .2) / 1.3)));
      basement(t, BXc - .2, { expr: first ? 'sleep' : 'happy', look: first ? 0 : -.4, bob: Math.sin(t * 2) * .01, tilt: first ? .14 : 0 }, Math.PI - .2);
      radBar(1, p); if (first) camB(k, .25, .1, 5.0, 4.85); else camB(k, .1, .0, 4.85, 4.7);
    } else if (i === 7) { // the official advice, in three steps
      basement(t, BXc + .55, { expr: 'happy', look: -.2, armL: .25, armR: lt > 3.9 ? 1.6 + Math.sin(t * 6) * .2 : .25, bob: bob(t, 0, .006) }, Math.PI - .15);
      dolly(V(BXc + .2, BY + 1.75, -5.9), V(BXc + .2, BY + 1.75, -5.6), V(BXc + .1, BY + 2.05, 1.2), V(BXc + .1, BY + 2.05, 1.2), k, 0, 50); advice(lt);
    } else { // two days later: back outside, CTA
      setSky('overcast', 'day', eInOut(k)); setAge(0, t, { lamps: 0 });
      jer(JX, JZ, Math.PI - .1, { expr: 'happy', armL: .3 + Math.abs(Math.sin(t * 5)) * 2.3, bob: bob(t) });
      dolly(V(JX + .35, 1.5, JZ - 3.8), V(JX + .9, 1.7, JZ - 5.0), V(JX, 1.45, JZ), V(JX, 1.5, JZ), eInOut(k), 0, 50); focus(V(JX, 1.4, JZ), .9, 10);
    }
    const sm = $('small'); sm.style.top = '1378px'; sm.style.fontSize = '34px'; sm.style.fontFamily = 'IDB'; sm.style.color = '#ffe08a'; sm.style.webkitTextStroke = '5px #0a0b18'; sm.style.paintOrder = 'stroke fill'; sm.style.left = '60px'; sm.style.right = '150px';
    sm.textContent = b.note || ''; sm.style.opacity = b.note ? clamp((lt - .3) / .3) : 0;
  },
});
