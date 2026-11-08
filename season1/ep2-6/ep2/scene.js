// Episode 2 — What if you doubled 1¢ every day?
import {
  THREE, RoundedBoxGeometry, scene, camera, draw, flash as flashLight, M, canvasTex, rr, loadFont, text3d,
  makeJeremy, renderCaptions, clamp, prog, eOut, eInOut, eBack, lerp, rand, popS, floor
} from './engine.js';
import { setTitle, intro, counter, stageAt, keyframes, flash } from './hud.js';

await document.fonts.load('80px IDB'); await document.fonts.load('80px IDBo'); await document.fonts.load('40px IM');
await loadFont();

const TOTAL = 50;
setTitle('WHAT IF YOU DOUBLED 1¢?', 'EP. 2');
const REEL = ['(x)', 'THE MOON VANISHED', 'GRAVITY DOUBLED', '0 DISAPPEARED', 'EARTH STOPPED', 'THE SUN WENT OUT', 'YOU DOUBLED 1¢?'];
window.REEL = REEL;

const V = (x, y, z) => new THREE.Vector3(x, y, z);
const look = new THREE.Vector3();
function setCam(p, l, roll = 0) { camera.position.copy(p); look.copy(l); camera.lookAt(look); camera.rotateZ(roll); }
function rbox(w, h, d, r, mat) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, r), mat); m.castShadow = m.receiveShadow = true; return m; }
function group(...k) { const g = new THREE.Group(); k.forEach(x => g.add(x)); scene.add(g); return g; }
const J = makeJeremy(); scene.add(J);
const sceneBg = scene.background.clone(); const sceneFog = scene.fog;

// ---------- money textures ----------
function drawBill(ctx, x, y, w, h) {
  const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, '#d5ead0'); g.addColorStop(1, '#9fc596');
  ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = '#4f7a4a'; ctx.lineWidth = h * 0.05; ctx.strokeRect(x + h * .08, y + h * .08, w - h * .16, h - h * .16);
  ctx.fillStyle = '#86ae7f'; ctx.beginPath(); ctx.ellipse(x + w / 2, y + h / 2, h * .26, h * .34, 0, 0, 7); ctx.fill();
  ctx.fillStyle = '#2f5a33'; ctx.font = `${h * .32}px IDB`; ctx.fillText('100', x + h * .14, y + h * .42); ctx.textAlign = 'right'; ctx.fillText('100', x + w - h * .14, y + h * .9); ctx.textAlign = 'left';
}
const billTex = canvasTex(512, 220, (ctx, w, h) => { drawBill(ctx, 0, 0, w, h); ctx.fillStyle = '#f2e7c4'; ctx.fillRect(w * .44, 0, w * .12, h); ctx.fillStyle = '#b89a4a'; ctx.font = '30px IDB'; ctx.save(); ctx.translate(w / 2 + 10, h / 2); ctx.rotate(-Math.PI / 2); ctx.textAlign = 'center'; ctx.fillText('$10,000', 0, 0); ctx.restore(); }).tex;
const edgeTex = canvasTex(256, 64, (ctx, w, h) => { ctx.fillStyle = '#cfe3c8'; ctx.fillRect(0, 0, w, h); for (let i = 0; i < h; i += 3) { ctx.fillStyle = i % 6 ? '#b7d1ae' : '#e6f1e1'; ctx.fillRect(0, i, w, 1.5); } ctx.fillStyle = '#f2e7c4'; ctx.fillRect(w * .44, 0, w * .12, h); }).tex;
const wallTex = canvasTex(1024, 1024, (ctx, w, h) => { // face of a cube made of cash bundles
  ctx.fillStyle = '#7da874'; ctx.fillRect(0, 0, w, h);
  const bw = 128, bh = 32;
  for (let y = 0; y < h; y += bh) for (let x = (y / bh % 2) * -bw / 2; x < w; x += bw) {
    ctx.fillStyle = (x + y) % 3 ? '#c9e0c2' : '#b6d2ad'; ctx.fillRect(x + 2, y + 2, bw - 4, bh - 4);
    for (let k = 4; k < bh - 4; k += 3) { ctx.fillStyle = 'rgba(80,120,80,.25)'; ctx.fillRect(x + 2, y + k, bw - 4, 1); }
    ctx.fillStyle = '#efe2b8'; ctx.fillRect(x + bw / 2 - 8, y + 2, 16, bh - 4);
  }
});
wallTex.tex.wrapS = wallTex.tex.wrapT = THREE.RepeatWrapping;
const moneyMat = (rep = 1) => { const t = wallTex.tex.clone(); t.needsUpdate = true; t.repeat.set(rep, rep); t.wrapS = t.wrapT = THREE.RepeatWrapping; return new THREE.MeshStandardMaterial({ map: t, roughness: .7 }); };

// ---------- phase A: coins ----------
const copper = new THREE.MeshStandardMaterial({ color: 0xd8875a, metalness: 1, roughness: .28 });
const coinGeo = new THREE.CylinderGeometry(0.16, 0.16, 0.035, 40);
const hero = new THREE.Group(); { const c = new THREE.Mesh(coinGeo, copper); c.rotation.x = Math.PI / 2; c.castShadow = true; hero.add(c);
  const lab = text3d('1', 0.13, copper, 0.02); lab.position.z = 0.02; hero.add(lab); const lab2 = lab.clone(); lab2.position.z = -0.02; lab2.rotation.y = Math.PI; hero.add(lab2); }
hero.scale.setScalar(3.2); scene.add(hero);
const COINS = 512; const coins = new THREE.InstancedMesh(coinGeo, copper, COINS); coins.castShadow = true; coins.receiveShadow = true; scene.add(coins);
const coinPos = []; { const r = rand(3); let i = 0;
  for (let i = 0; i < 16; i++) coinPos.push([0.55, 0.02 + i * 0.037, 0.4, 0, (r() - .5) * .3]); // a neat stack of 16 first
  while (coinPos.length < COINS) { const a = r() * 6.283, d = Math.sqrt(r()) * 1.25, hgt = Math.max(0, (1.25 - d) * 0.55) * r();
    coinPos.push([0.6 + Math.cos(a) * d, 0.02 + hgt, 0.3 + Math.sin(a) * d, (r() - .5) * .8, r() * 6]); } }
const dm = new THREE.Object3D();

// ---------- phase B: cash bundles ----------
const brickGeo = new THREE.BoxGeometry(0.42, 0.1, 0.2);
const brickMats = [new THREE.MeshStandardMaterial({ map: edgeTex, roughness: .8 }), new THREE.MeshStandardMaterial({ map: edgeTex, roughness: .8 }),
  new THREE.MeshStandardMaterial({ map: billTex, roughness: .6 }), new THREE.MeshStandardMaterial({ map: billTex, roughness: .6 }),
  new THREE.MeshStandardMaterial({ map: edgeTex, roughness: .8 }), new THREE.MeshStandardMaterial({ map: edgeTex, roughness: .8 })];
const BR = 410; const bricks = new THREE.InstancedMesh(brickGeo, brickMats, BR); bricks.castShadow = bricks.receiveShadow = true; scene.add(bricks);
const brickPos = []; { const r = rand(8); for (let L = 0; L < 8; L++) { const nx = 8 - L, nz = 16 - 2 * L;
  for (let ix = 0; ix < nx; ix++) for (let iz = 0; iz < nz; iz++) brickPos.push([0.6 + (ix - (nx - 1) / 2) * 0.44, 0.05 + L * 0.1, 0.1 + (iz - (nz - 1) / 2) * 0.22, (r() - .5) * .12]); } }
// pallets
const palletGeo = new THREE.BoxGeometry(1, 1, 1); const palletMat = moneyMat(1);
const PL = 48; const pallets = new THREE.InstancedMesh(palletGeo, palletMat, PL); pallets.castShadow = pallets.receiveShadow = true; scene.add(pallets);
const palPos = []; for (let L = 0; L < 4; L++) for (let iz = 0; iz < 3; iz++) for (let ix = 0; ix < 4; ix++) palPos.push([0.6 + (ix - 1.5) * 1.06, 0.5 + L * 1.04, -0.6 + (iz - 1) * 1.06]);

// ---------- props (what the money buys) floating above Jeremy ----------
function makeCoffee() { const g = new THREE.Group(); const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.25, 0.75, 32), M.white); const sleeve = new THREE.Mesh(new THREE.CylinderGeometry(0.33, 0.29, 0.3, 32), new THREE.MeshStandardMaterial({ color: 0x8a5a36, roughness: .8 })); sleeve.position.y = -.05;
  const lid = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.08, 32), new THREE.MeshStandardMaterial({ color: 0x222, roughness: .4 })); lid.position.y = .41; g.add(cup, sleeve, lid); return g; }
function makePhoneProp() { const g = new THREE.Group(); const b = rbox(0.6, 1.2, 0.08, 0.1, new THREE.MeshPhysicalMaterial({ color: 0x1a1d2a, metalness: .8, roughness: .2, clearcoat: 1 }));
  const s = new THREE.Mesh(new THREE.PlaneGeometry(0.54, 1.12), new THREE.MeshBasicMaterial({ map: canvasTex(256, 512, (ctx, w, h) => { const gg = ctx.createLinearGradient(0, 0, w, h); gg.addColorStop(0, '#5a7bff'); gg.addColorStop(1, '#ff5ad1'); ctx.fillStyle = gg; ctx.fillRect(0, 0, w, h); }).tex })); s.position.z = .042; g.add(b, s); return g; }
function makeCar() { const g = new THREE.Group(); const red = new THREE.MeshPhysicalMaterial({ color: 0xe8364e, metalness: .5, roughness: .25, clearcoat: 1 });
  const body = rbox(1.9, 0.45, 0.9, 0.16, red); body.position.y = 0.42; const cab = rbox(1.0, 0.42, 0.8, 0.16, new THREE.MeshPhysicalMaterial({ color: 0x223, metalness: .3, roughness: .05, clearcoat: 1 })); cab.position.set(-0.1, 0.8, 0);
  g.add(body, cab); for (const x of [-0.6, 0.6]) for (const z of [-0.45, 0.45]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.16, 24), new THREE.MeshStandardMaterial({ color: 0x111, roughness: .6 })); w.rotation.x = Math.PI / 2; w.position.set(x, 0.2, z); g.add(w); } return g; }
function makeHouse() { const g = new THREE.Group(); const walls = rbox(1.6, 1.1, 1.3, 0.04, M.white); walls.position.y = 0.55;
  const roof = new THREE.Mesh(new THREE.ConeGeometry(1.3, 0.8, 4), new THREE.MeshStandardMaterial({ color: 0xc8463a, roughness: .5 })); roof.position.y = 1.5; roof.rotation.y = Math.PI / 4; roof.scale.set(1, 1, 0.85);
  const door = rbox(0.32, 0.55, 0.05, 0.03, new THREE.MeshStandardMaterial({ color: 0x6b4426 })); door.position.set(0, 0.28, 0.66);
  const win = new THREE.MeshStandardMaterial({ color: 0xffe9a8, emissive: 0xffc860, emissiveIntensity: .8 }); for (const x of [-0.5, 0.5]) { const w = rbox(0.3, 0.3, 0.05, 0.03, win); w.position.set(x, 0.65, 0.66); g.add(w); }
  g.add(walls, roof, door); return g; }
const props = [makeCoffee(), makePhoneProp(), makeCar(), makeHouse()]; props.forEach(p => { p.traverse(o => { if (o.isMesh) o.castShadow = true; }); p.visible = false; scene.add(p); });
const ring = new THREE.Mesh(new THREE.TorusGeometry(0.75, 0.025, 8, 64), new THREE.MeshBasicMaterial({ color: 0xffc444 })); ring.rotation.x = Math.PI / 2; scene.add(ring);

// ---------- phase C ----------
const giant = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), moneyMat(6)); giant.castShadow = giant.receiveShadow = true; scene.add(giant);
const city = new THREE.Group(); scene.add(city);
{ const r = rand(17); const winTex = canvasTex(128, 256, (ctx, w, h) => { ctx.fillStyle = '#1a2040'; ctx.fillRect(0, 0, w, h); for (let y = 6; y < h; y += 16) for (let x = 6; x < w; x += 16) { ctx.fillStyle = r() > .45 ? '#ffd98a' : '#2a3366'; ctx.fillRect(x, y, 8, 9); } }).tex;
  const bm = new THREE.MeshStandardMaterial({ color: 0x8890b0, map: winTex, emissive: 0xffffff, emissiveMap: winTex, emissiveIntensity: .5, roughness: .4, metalness: .3 });
  for (let i = 0; i < 70; i++) { const a = r() * 6.283, d = 14 + r() * 26; const h = 2 + r() * r() * 14, w = 1.5 + r() * 2.5;
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, w), bm); b.position.set(Math.cos(a) * d, h / 2, Math.sin(a) * d - 6); b.castShadow = b.receiveShadow = true; city.add(b); } }
const earthTex = canvasTex(2048, 1024, (ctx, w, h) => {
  const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#1d4f9a'); g.addColorStop(.5, '#1565c0'); g.addColorStop(1, '#1d4f9a'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  const r = rand(23); const blob = (cx, cy, s, col) => { for (let i = 0; i < 70; i++) { ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(cx + (r() - .5) * s * 1.6, cy + (r() - .5) * s, s * (.15 + r() * .3), s * (.12 + r() * .25), r() * 3, 0, 7); ctx.fill(); } };
  [[330, 330, 260], [520, 640, 200], [1060, 330, 230], [1120, 600, 220], [1500, 380, 320], [1700, 700, 140], [1000, 900, 300]].forEach(([x, y, s], i) => { blob(x, y, s, '#3f8a3c'); blob(x + 20, y + 10, s * .6, '#7a8b45'); });
  ctx.fillStyle = '#f2f6ff'; ctx.fillRect(0, 0, w, 50); ctx.fillRect(0, h - 70, w, 70);
});
const earth = new THREE.Mesh(new THREE.SphereGeometry(6, 96, 64), new THREE.MeshStandardMaterial({ map: earthTex.tex, roughness: .7 }));
const atmo = new THREE.Mesh(new THREE.SphereGeometry(6.25, 64, 48), new THREE.MeshBasicMaterial({ color: 0x5ab0ff, transparent: true, opacity: .18, side: THREE.BackSide, blending: THREE.AdditiveBlending }));
const moneyBall = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), moneyMat(10));
const space = group(earth, atmo, moneyBall);
const stars = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute((() => { const r = rand(5), a = []; for (let i = 0; i < 2500; i++) { const th = r() * 6.283, ph = Math.acos(2 * r() - 1), d = 300; a.push(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d, Math.sin(ph) * Math.sin(th) * d); } return a; })(), 3)), new THREE.PointsMaterial({ color: 0xffffff, size: 1.2, sizeAttenuation: false }));
space.add(stars);

// ---------- CTA ----------
function card(l1, l2, col) { const g = new THREE.Group(); g.add(rbox(2.25, 1.5, 0.16, 0.22, new THREE.MeshPhysicalMaterial({ color: 0x18245a, roughness: .1, clearcoat: 1, transparent: true, opacity: .85 })));
  const lab = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 1.45), new THREE.MeshBasicMaterial({ transparent: true, toneMapped: false, map: canvasTex(660, 435, (ctx, w, h) => { ctx.textAlign = 'center'; ctx.fillStyle = col; ctx.font = '120px IDB'; ctx.fillText(l1, w / 2, 200); ctx.fillStyle = '#fff'; ctx.font = '58px IDBo'; ctx.fillText(l2, w / 2, 320); }).tex }));
  lab.position.z = 0.09; g.add(lab); return g; }
const cA = card('$1M', 'today', '#5dff9e'), cB = card('1¢', 'doubled ×30', '#ffc444'); const vs = text3d('VS', 0.5, M.goldGlow);
const cta = group(cA, cB, vs);

// =================== TIMELINE ===================
const st = [
  { t: 3.0, d: 1, cap: 'Day 1: one cent.', hi: ['cent'], j: 'confused' },
  { t: 5.6, d: 5, cap: 'Day 5: 16¢. Can’t even buy gum.', hi: ['16¢'], j: 'confused' },
  { t: 8.2, d: 10, cap: 'Day 10: $5.12. One coffee.', hi: ['$5.12'], j: 'worried', prop: 0 },
  { t: 10.8, d: 14, cap: 'Day 14: $81.92. Dinner for two.', hi: ['$81.92'], j: 'happy' },
  { t: 13.4, d: 17, cap: 'Day 17: $655. A new phone.', hi: ['$655'], j: 'happy', prop: 1 },
  { t: 16.0, d: 20, cap: 'Day 20: $5,242. Wait… what?', hi: ['$5242'], j: 'shocked' },
  { t: 18.6, d: 23, cap: 'Day 23: a brand-new car.', hi: ['car'], j: 'panic', prop: 2 },
  { t: 21.2, d: 26, cap: 'Day 26: Jeremy quits his job.', hi: ['quits'], j: 'happy', dance: true },
  { t: 23.8, d: 28, cap: 'Day 28: a house. Cash.', hi: ['house'], j: 'shocked', prop: 3 },
  { t: 26.4, d: 30, cap: 'Day 30: $5.3 MILLION.', hi: ['MILLION'], j: 'panic', dance: true },
  { t: 29.4, d: 30, cap: 'Day 30 alone beats days 1–29 combined.', hi: ['alone'], j: 'confused', fact: true },
  { t: 32.4, d: 30, cap: 'But what if he kept going?', hi: ['kept', 'going'], j: 'shocked' },
  { t: 34.6, d: 40, cap: 'Day 40: $5.5 BILLION.', hi: ['BILLION'], phase: 'giant' },
  { t: 37.2, d: 50, cap: 'Day 50: bigger than Japan’s whole economy.', hi: ['Japan’s'], phase: 'city' },
  { t: 40.0, d: 55, cap: 'Day 55: more than ALL the money on Earth.', hi: ['ALL'], phase: 'earth' },
  { t: 43.0, d: 64, cap: 'Day 64: $92 QUADRILLION.', hi: ['QUADRILLION'], phase: 'boom' },
  { t: 46.2, d: 64, cap: 'Would you take $1M now… or the 1¢?', hi: ['$1M', '1¢'], phase: 'cta' },
];
window.STAGES = st;
const dayKF = [[0, 1]]; st.forEach((s, i) => { if (i > 0) { dayKF.push([s.t - (i === 12 ? 2.0 : 0.9), st[i - 1].d]); } dayKF.push([s.t, s.d]); });
const dayAt = t => Math.floor(keyframes(dayKF, t) + 1e-6);
const money = d => 0.01 * Math.pow(2, d - 1);
function fmtMoney(v) {
  if (v < 1e6) return '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  if (v < 1e9) return '$' + Math.floor(v).toLocaleString('en-US');
  const u = [[1e15, 'QUADRILLION'], [1e12, 'TRILLION'], [1e9, 'BILLION']].find(([k]) => v >= k);
  return '$' + (v / u[0]).toFixed(1) + ' ' + u[1];
}
const sevAt = d => d < 10 ? 0 : d < 17 ? 1 : d < 23 ? 2 : d < 30 ? 3 : d < 50 ? 4 : 5;

// camera keyframes for phase A/B (on stage)
const camKF = [ // t, pos, look
  [3.0, V(0.6, 2.0, 4.6), V(0.6, 2.0, 1.2)], [5.4, V(0.4, 2.1, 5.2), V(0.5, 1.6, 0.6)], [5.9, V(0.2, 2.6, 7.6), V(0.3, 1.4, 0.3)],
  [8.4, V(0, 2.9, 9.2), V(0.2, 1.5, 0.3)], [11, V(-0.2, 3.3, 10.5), V(0.2, 1.7, 0.2)], [16, V(0.2, 3.6, 11.2), V(0.2, 1.8, 0)],
  [21, V(-0.2, 4.6, 13.5), V(0.3, 2.2, -0.3)], [26.4, V(0.2, 5.2, 15.5), V(0.3, 2.5, -0.5)], [29.4, V(1.4, 4.4, 14.5), V(0.3, 2.5, -0.5)], [34.6, V(0.4, 4.8, 16), V(0.3, 2.5, -0.5)]];
function camAt(t) { let k = 0; while (k < camKF.length - 1 && t > camKF[k + 1][0]) k++; const a = camKF[k], b = camKF[Math.min(k + 1, camKF.length - 1)];
  const p = b === a ? 1 : eInOut(clamp((t - a[0]) / (b[0] - a[0]))); return [a[1].clone().lerp(b[1], p), a[2].clone().lerp(b[2], p)]; }

window.renderAt = (T) => {
  flashLight.intensity = 0; flash(0); document.getElementById('black').style.opacity = 0; document.getElementById('small').textContent = '';
  const inIntro = intro(T, REEL, 3.0);
  const { i, lt, s } = stageAt(st, T);
  const phase = T < 3 ? 'intro' : s.phase || 'stage';
  const day = dayAt(T);
  // visibility
  const onStage = phase === 'stage' || phase === 'intro' || phase === 'cta';
  floor.visible = phase !== 'earth' && phase !== 'boom';
  scene.background = floor.visible ? sceneBg : new THREE.Color(0x01020a); scene.fog = (phase === 'stage' || phase === 'intro' || phase === 'cta') ? sceneFog : null;
  [hero, coins, bricks, pallets, ring, ...props].forEach(o => o.visible = false);
  giant.visible = phase === 'giant' || phase === 'city'; city.visible = phase === 'city'; space.visible = phase === 'earth' || phase === 'boom'; cta.visible = phase === 'cta';
  J.visible = phase === 'stage' || phase === 'giant' || phase === 'cta';

  if (phase === 'intro') {
    // slowly turning coin behind the reel
    hero.visible = false;
    setCam(V(0, 3.0, 9), V(0, 3.0, 0));
  }
  if (phase === 'stage') {
    const m = money(day);
    // coins / bricks / pallets by amount
    if (day === 1 && T < 5.4) { hero.visible = true; hero.scale.setScalar(3.2 * popS(T, 3.0, .5)); hero.position.set(0.6, 2.0 + Math.sin(T * 2) * .05, 1.2); hero.rotation.set(0.1, T * 2.2, 0); }
    else if (day <= 12) { const n = Math.min(COINS, Math.round(m * 100)); coins.visible = true; coins.count = n;
      for (let k = 0; k < n; k++) { const p = coinPos[k]; dm.position.set(p[0], p[1], p[2]); dm.rotation.set(p[3], p[4], 0); dm.scale.setScalar(1); dm.updateMatrix(); coins.setMatrixAt(k, dm.matrix); } coins.instanceMatrix.needsUpdate = true; }
    if (day >= 13 && day <= 25) { const n = Math.min(brickPos.length, Math.round(4 * Math.pow(2, (day - 14) * 0.78))); bricks.visible = true; bricks.count = n;
      for (let k = 0; k < n; k++) { const p = brickPos[k]; dm.position.set(p[0], p[1], p[2]); dm.rotation.set(0, p[3], 0); dm.scale.setScalar(1); dm.updateMatrix(); bricks.setMatrixAt(k, dm.matrix); } bricks.instanceMatrix.needsUpdate = true; }
    if (day >= 26) { const n = Math.min(PL, [0, 4, 8, 14, 22, 48][Math.min(5, day - 25)]); pallets.visible = true; pallets.count = n;
      for (let k = 0; k < n; k++) { const p = palPos[k]; const born = popS(T, 0, 1); dm.position.set(p[0], p[1], p[2]); dm.rotation.set(0, 0, 0); dm.scale.setScalar(1); dm.updateMatrix(); pallets.setMatrixAt(k, dm.matrix); } pallets.instanceMatrix.needsUpdate = true; }
    // prop of the current stage (stays for its stage)
    if (s.prop !== undefined) { const p = props[s.prop]; p.visible = true; const sc = popS(lt, 0.1, .45); p.scale.setScalar(sc * (s.prop >= 2 ? 0.75 : 1)); p.position.set(-1.35, 3.45 + Math.sin(T * 2) * .06, 1.3); p.rotation.set(0.15, T * 1.2, 0);
      ring.visible = true; ring.position.set(-1.35, 3.0, 1.3); ring.scale.setScalar(sc); }
    // Jeremy
    J.scale.setScalar(0.9); J.position.set(-1.45, 0, 1.6); J.rotation.y = 0.45;
    const exc = s.j === 'panic' || s.dance;
    J.pose({ expr: s.j === 'panic' ? 'shocked' : s.j, look: 0.6, tilt: s.j === 'confused' ? 0.15 : 0,
      armL: exc ? 2.5 + Math.sin(T * 12) * .3 : s.j === 'worried' ? 0.9 : 0.2, armR: exc ? 2.5 + Math.cos(T * 12) * .3 : s.j === 'worried' ? 0.9 : 0.2,
      bob: exc ? Math.abs(Math.sin(T * 9)) * .15 : 0, sweatK: s.j === 'shocked' ? lt : 0, blink: (T % 3.1) < .1 });
    if (s.dance) J.rotation.y = 0.45 + Math.sin(T * 6) * .4;
    const [cp, cl] = camAt(T); setCam(cp, cl, 0);
    if (s.fact) { flashLight.intensity = 6; flashLight.position.set(0.6, 4.5, 3); }
  }
  if (phase === 'giant') { // $5.5B: a cube of cash ~ 12 units tall
    const g = eOut(prog(lt, 0, 1.0)); giant.scale.set(9, 12 * g, 9); giant.position.set(1.5, 6 * g, -6);
    J.scale.setScalar(0.9); J.position.set(-2.2, 0, 1.0); J.rotation.y = 0.5; J.pose({ expr: 'shocked', look: 0.8, armL: 2.4, armR: 2.4, sweatK: lt });
    const k = eInOut(prog(lt, 0, 2.6)); setCam(V(lerp(-1, 0.5, k), lerp(2.0, 3.0, k), lerp(17, 24, k)), V(0.3, lerp(4, 6.5, k), -5));
  }
  if (phase === 'city') { const g = eOut(prog(lt, 0, 1.2)); giant.scale.set(16, 40 * g, 16); giant.position.set(0, 20 * g, -6);
    const k = eInOut(prog(lt, 0, 2.8)); setCam(V(lerp(10, 20, k), lerp(14, 26, k), lerp(55, 62, k)), V(0, lerp(10, 14, k), -6)); }
  if (phase === 'earth' || phase === 'boom') {
    earth.rotation.y = T * 0.15; stars.rotation.y = T * 0.01;
    if (phase === 'earth') { const g = eInOut(prog(lt, 0.3, 2.4)); moneyBall.scale.setScalar(Math.max(0.001, 6.35 * g)); moneyBall.position.set(0, 0, 0); moneyBall.rotation.y = -T * 0.1;
      setCam(V(0, 2, lerp(26, 22, eInOut(prog(lt, 0, 3)))), V(0, 0, 0)); }
    else { const g = eInOut(prog(lt, 0.2, 2.4)); moneyBall.scale.setScalar(6.35 + 60 * g); moneyBall.position.set(-40 * g, 10 * g, -70 * g);
      earth.position.set(0, 0, 0); const sh = lt > 0.2 && lt < 1.6 ? (Math.random() - .5) * .6 : 0;
      setCam(V(lerp(0, 18, g) + sh, 2 + sh, lerp(22, 60, g)), V(-12 * g, 4 * g, -20 * g)); if (lt < .35) flash(.6 * (1 - lt / .35)); }
  }
  if (phase === 'cta') {
    cA.position.set(-1.3, 3.4, 0); cB.position.set(1.3, 3.4, 0); vs.position.set(0, 3.4, 0.4);
    cA.scale.setScalar(popS(lt, 0, .4)); cB.scale.setScalar(popS(lt, .2, .4)); vs.scale.setScalar(popS(lt, .45, .4));
    cA.rotation.y = 0.15 + Math.sin(T * 1.5) * .05; cB.rotation.y = -0.15 - Math.sin(T * 1.5) * .05;
    J.scale.setScalar(0.85); J.position.set(0, 0, 1.6); J.rotation.y = 0; J.pose({ expr: 'confused', look: Math.sin(T * 2.4), tilt: Math.sin(T * 1.2) * .15, armL: .3, armR: 1.4 });
    setCam(V(lerp(-0.4, 0.4, eInOut(prog(lt, 0, 3.8))), 2.6, 9.6), V(0, 2.5, 0));
    document.getElementById('small').style.top = '1525px'; document.getElementById('small').style.opacity = clamp((lt - 1.4) / .4); document.getElementById('small').textContent = 'Purely hypothetical · for entertainment';
  }
  // counter
  counter(T, { on: T >= 3.0, valueAt: t => money(dayAt(Math.max(3, t))), fmt: fmtMoney, label: `DAY ${day}`, sub: '1¢ doubled every day', sev: sevAt(day), shake: phase === 'boom' && lt < 1.6 ? 1 : 0 });
  // captions
  const caps = [];
  if (T >= 3.0) { const end = i + 1 < st.length ? st[i + 1].t - 0.15 : TOTAL; caps.push({ t0: s.t + 0.05, t1: end, text: s.cap, y: phase === 'cta' ? 1270 : 1330, size: s.cap.length > 30 ? 68 : 82, g: s.hi.map(w => w.replace(/[,.?!…:]/g, '')) }); }
  if (phase === 'cta') caps.push({ t0: s.t + 1.2, t1: TOTAL, text: 'Comment below ↓', y: 1440, size: 66, g: ['below', '↓'] });
  renderCaptions(caps, T);
  document.getElementById('fill').style.width = (clamp(T / TOTAL) * 100) + '%';
  draw();
};
window.TOTAL = TOTAL;
window.READY = true;
