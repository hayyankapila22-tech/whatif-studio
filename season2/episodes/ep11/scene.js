// Episode 11 — What if everyone could read minds?  TIMELINE: counter = time since everyone started hearing thoughts.
// Facts (checked 2026-11-10):
//  - ~6,200 thoughts per day: Tseng & Poppenk 2020, Nature Communications ("thought worms"), Queen's University Gazette
//    https://www.queensu.ca/gazette/stories/discovery-thought-worms-opens-window-mind
//  - Americans average 1.65 lies per day (most told by a few prolific liars): Serota, Levine & Boster 2010, Human Communication Research
//    https://oakland.edu/Assets/upload/docs/News/2014/Serota-et-al-Prevalence-of-Lying-2010.pdf
//  - global advertising revenue ~$1.14 trillion in 2025: WPP Media "This Year Next Year", Dec 2025
//    https://www.wppmedia.com/news/campaigns-report-this-year-next-year-december-2025
//  - foil helmets can AMPLIFY some radio frequencies: Rahimi et al., MIT 2005 "On the Effectiveness of Aluminium Foil Helmets"
//    https://www.mentalfloss.com/article/12632/can-foil-hat-keep-people-or-aliens-reading-your-thoughts
//  - 2023: UT Austin semantic decoder (Tang, LeBel, Jain & Huth, Nature Neuroscience) turned fMRI brain scans into the gist of
//    what a person heard/imagined — needs a cooperative volunteer and hours in the scanner.
//  Everything else (poker, dates, politics, year 10 / year 100) is clearly labelled speculation on screen.
import { THREE, RoundedBoxGeometry, scene, camera, canvasTex, rand, clamp, prog, lerp, eOut, eInOut, V, K, boot, mode, dolly, shake, bubble, headPos, run, focus, noFocus, RIM, GRADE, INK, rimLight } from './kit.js';
import { buildWorld, W, setAge, setSky, poof } from './world.js';
import { makeJeremy2 } from './jeremy2.js';

await boot('WHAT IF WE COULD READ MINDS?', 'EP. 11');
const J = K.J;
buildWorld(K);

// ---------- clear the set: no lamp post / tree / parked car between camera and the action ----------
const S = K.street.group;
const near = (o, x, z) => Math.abs(o.position.x - x) < .1 && Math.abs(o.position.z - z) < .1;
S.children.forEach(o => { if ([[21, 4.8], [30, 4.8], [35, -4.8], [26, -4.8], [33, -7.2]].some(([x, z]) => near(o, x, z))) o.visible = false; });
W.cars.forEach(c => { if (near(c, 26, 3.2) || near(c, 40, -3.2)) c.visible = false; });

// ---------- cast ----------
const std = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .6, ...o });
const darker = (c) => new THREE.Color(c).multiplyScalar(.78).getHex();
function person({ top, hair = 0x3a2417, skin = 0xf1b58e, legs = 0x2b3a5e, shoes = 0xf6f6f6, long = false, apron = 0, tie = 0, tex = null, s = .75 }) {
  const p = makeJeremy2();
  const map = new Map([[0x2f6dff, top], [0x2457cc, darker(top)], [0x3a2417, hair], [0xf1b58e, skin], [0x2b3a5e, legs], [0xff3d6e, shoes]]);
  const seen = new Set();
  p.traverse(o => { if (!o.isMesh || seen.has(o.material)) return; seen.add(o.material); const m = o.material; const h = m.color?.getHex();
    if (map.has(h)) { m.color.setHex(map.get(h)); if (m.sheenColor) m.sheenColor.setHex(map.get(h)); if (tex && h === 0x2f6dff) { m.map = tex; m.color.setHex(0xffffff); m.needsUpdate = true; } } });
  const hairM = std(hair, { roughness: .45 });
  if (long) { // long hair falling behind the head + side locks
    const back = new THREE.Mesh(new THREE.SphereGeometry(.56, 40, 24, Math.PI, Math.PI, 0, Math.PI * .72), hairM); back.scale.set(1.02, 1.35, 1); back.position.set(0, -.18, -.04); p.headG.add(back);
    for (const sx of [-1, 1]) { const lock = new THREE.Mesh(new THREE.CapsuleGeometry(.11, .5, 8, 16), hairM); lock.position.set(sx * .47, -.3, -.02); lock.rotation.z = sx * .08; p.headG.add(lock); }
  }
  if (apron) { const a = new THREE.Mesh(new RoundedBoxGeometry(.66, .78, .05, 3, .02), std(apron, { roughness: .85 })); a.position.set(0, 1.0, .39); a.rotation.x = -.06; p.bodyG.add(a);
    const strap = new THREE.Mesh(new THREE.TorusGeometry(.2, .02, 6, 20, Math.PI), std(apron)); strap.position.set(0, 1.42, .3); strap.rotation.x = -.5; p.bodyG.add(strap); }
  if (tie) { const col = new THREE.Mesh(new THREE.ConeGeometry(.16, .22, 3), std(0xffffff)); col.rotation.x = Math.PI; col.position.set(0, 1.56, .33); col.scale.z = .3; p.bodyG.add(col);
    const tk = new THREE.Mesh(new THREE.BoxGeometry(.1, .46, .03), std(tie, { roughness: .4 })); tk.position.set(0, 1.27, .39); tk.rotation.x = -.12; p.bodyG.add(tk); }
  // tinfoil hat (toggled per shot)
  const foil = new THREE.Mesh(new THREE.ConeGeometry(.46, .7, 9, 3), new THREE.MeshStandardMaterial({ color: 0xdfe4ea, metalness: 1, roughness: .32, flatShading: true }));
  { const a = foil.geometry.attributes.position, r = rand(9); for (let i = 0; i < a.count; i++) { a.setX(i, a.getX(i) * (1 + (r() - .5) * .12)); a.setZ(i, a.getZ(i) * (1 + (r() - .5) * .12)); } foil.geometry.computeVertexNormals(); }
  foil.position.set(0, .62, -.02); foil.rotation.z = .08; foil.castShadow = true; foil.visible = false; p.headG.add(foil); p.foil = foil;
  p.scale.setScalar(s); p.s0 = s; scene.add(p); rimLight(p); p.visible = false; return p;
}
const sweaterTex = canvasTex(256, 256, (ctx, w, h) => { ctx.fillStyle = '#c8203a'; ctx.fillRect(0, 0, w, h);
  for (let y = 0; y < h; y += 64) { ctx.fillStyle = '#2f9a48'; ctx.fillRect(0, y + 24, w, 16); ctx.fillStyle = '#ffffff'; for (let x = 0; x < w; x += 32) { ctx.beginPath(); ctx.moveTo(x, y + 24); ctx.lineTo(x + 16, y + 8); ctx.lineTo(x + 32, y + 24); ctx.fill(); }
    ctx.fillStyle = '#ffd23d'; for (let x = 8; x < w; x += 32) { ctx.beginPath(); ctx.arc(x, y + 52, 6, 0, 7); ctx.fill(); } } }).tex;
sweaterTex.wrapS = sweaterTex.wrapT = THREE.RepeatWrapping; sweaterTex.repeat.set(2, 2);
const P = {
  barista: person({ top: 0xf4f1ea, hair: 0x1d1410, skin: 0xc68a62, apron: 0x1d6b52, shoes: 0x2a2a2e }),
  mia: person({ top: 0xff7aa8, hair: 0x6a3a1c, skin: 0xf3c8a8, long: true, legs: 0x38405e, shoes: 0xffffff, s: .72 }),
  sam: person({ top: 0xff8a2a, hair: 0x241812, skin: 0x8d5a3b, legs: 0x3b3b44, shoes: 0x2fb57d }),
  zoe: person({ top: 0xffffff, tex: sweaterTex, hair: 0xe0b060, skin: 0xf1c3a0, long: true, legs: 0x2b3a5e, shoes: 0xe8364e, s: .72 }),
  ken: person({ top: 0x6b4fd6, hair: 0x101010, skin: 0xe9b88e, legs: 0x2a2d35, shoes: 0xffc93a }),
  ava: person({ top: 0x29b48a, hair: 0x2a1a12, skin: 0xa86a48, long: true, legs: 0x2b3a5e, shoes: 0xffffff, s: .72 }),
  pol: person({ top: 0x262a3a, hair: 0x8a8a8a, skin: 0xf0b896, legs: 0x262a3a, shoes: 0x111111, tie: 0xe8364e, s: .78 }),
};
const CAST = Object.values(P);
const head = (p) => p.localToWorld(V(0, 2.75, 0));
function put(p, x, z, ry, pose = {}) { p.visible = true; p.position.set(x, .18, z); p.rotation.set(0, ry, 0); p.pose(pose); }
const face = (x0, z0, x1, z1) => Math.atan2(x1 - x0, z1 - z0); // ry that turns a character at (x0,z0) to look at (x1,z1)

// ---------- props ----------
function bistro() { // small café table for two with coffee + a rose
  const g = new THREE.Group(); const wood = std(0x9a6a3e, { roughness: .5 }), metal = std(0x30343c, { metalness: .8, roughness: .35 });
  const top = new THREE.Mesh(new THREE.CylinderGeometry(.42, .42, .05, 40), wood); top.position.y = .78; const leg = new THREE.Mesh(new THREE.CylinderGeometry(.035, .035, .76, 12), metal); leg.position.y = .39;
  const base = new THREE.Mesh(new THREE.CylinderGeometry(.24, .26, .03, 32), metal); base.position.y = .015; g.add(top, leg, base);
  for (const s of [-1, 1]) { const cup = new THREE.Mesh(new THREE.CylinderGeometry(.05, .04, .1, 24), std(0xfafafa, { roughness: .2 })); cup.position.set(s * .22, .86, s * .05); const cof = new THREE.Mesh(new THREE.CircleGeometry(.045, 24), std(0x5a2a10, { roughness: .15 })); cof.rotation.x = -Math.PI / 2; cof.position.set(s * .22, .905, s * .05); g.add(cup, cof); }
  const vase = new THREE.Mesh(new THREE.CylinderGeometry(.035, .05, .16, 20), new THREE.MeshPhysicalMaterial({ color: 0xbfe6ff, roughness: .05, transmission: .4, transparent: true, opacity: .7 })); vase.position.set(0, .89, -.05);
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(.008, .008, .32, 6), std(0x2f8a3c)); stem.position.set(0, 1.0, -.05);
  const rose = new THREE.Mesh(new THREE.IcosahedronGeometry(.06, 1), std(0xe8203a, { roughness: .45, flatShading: true })); rose.scale.set(1, 1.15, 1); rose.position.set(0, 1.17, -.05);
  const leaf = new THREE.Mesh(new THREE.CircleGeometry(.04, 6), std(0x3f9a3a, { side: THREE.DoubleSide })); leaf.position.set(.03, 1.04, -.05); leaf.rotation.set(0, .6, .7); leaf.scale.y = .5;
  g.add(vase, stem, rose, leaf); g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); scene.add(g); g.visible = false; return g;
}
const cardTex = (suit, red) => canvasTex(128, 180, (ctx, w, h) => { ctx.fillStyle = '#fbfbf6'; ctx.fillRect(0, 0, w, h); ctx.strokeStyle = '#c8c8c0'; ctx.lineWidth = 6; ctx.strokeRect(3, 3, w - 6, h - 6);
  ctx.fillStyle = red ? '#d21f3c' : '#15161a'; ctx.font = 'bold 120px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(suit, w / 2, h / 2 + 6); }).tex;
function pokerTable() {
  const g = new THREE.Group();
  const felt = canvasTex(512, 512, (ctx, w, h) => { const gr = ctx.createRadialGradient(w / 2, h / 2, 20, w / 2, h / 2, w / 2); gr.addColorStop(0, '#2fa05a'); gr.addColorStop(1, '#13643a'); ctx.fillStyle = gr; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = 'rgba(255,240,180,.55)'; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(w / 2, h / 2, w * .3, 0, 7); ctx.stroke(); }).tex;
  const top = new THREE.Mesh(new THREE.CylinderGeometry(.9, .9, .06, 64), [std(0x13643a), new THREE.MeshStandardMaterial({ map: felt, roughness: .95 }), std(0x13643a)]); top.position.y = .9;
  const rim = new THREE.Mesh(new THREE.TorusGeometry(.92, .06, 12, 64), std(0x5a3418, { roughness: .35 })); rim.rotation.x = Math.PI / 2; rim.position.y = .92;
  const leg = new THREE.Mesh(new THREE.CylinderGeometry(.08, .1, .88, 16), std(0x2a2a2e, { metalness: .7, roughness: .3 })); leg.position.y = .44;
  const base = new THREE.Mesh(new THREE.CylinderGeometry(.4, .45, .05, 32), std(0x2a2a2e, { metalness: .7, roughness: .3 })); base.position.y = .025; g.add(top, rim, leg, base);
  [['♠', 0], ['♥', 1], ['♦', 1], ['♣', 0], ['♥', 1]].forEach(([s, r], i) => { const c = new THREE.Mesh(new THREE.BoxGeometry(.13, .004, .18), [std(0xfbfbf6), std(0xfbfbf6), new THREE.MeshStandardMaterial({ map: cardTex(s, r), roughness: .5 }), std(0x2a4aa0), std(0xfbfbf6), std(0xfbfbf6)]);
    c.position.set(-.34 + i * .17, .935, .05); c.rotation.y = (i - 2) * .03; g.add(c); });
  const r = rand(4); const chipCols = [0xe8364e, 0x2f6dff, 0xfafafa, 0x111111, 0xffc93a];
  [[.45, -.35], [-.45, -.4], [0, .5], [.55, .3], [-.5, .32], [.12, -.18]].forEach(([x, z], k) => { const n = 4 + Math.floor(r() * 8); for (let i = 0; i < n; i++) { const ch = new THREE.Mesh(new THREE.CylinderGeometry(.045, .045, .014, 20), std(chipCols[(k + i) % 5], { roughness: .4 })); ch.position.set(x + (r() - .5) * .01, .94 + i * .015, z); g.add(ch); } });
  g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); scene.add(g); g.visible = false; return g;
}
function giftBox() {
  const g = new THREE.Group(); const b = new THREE.Mesh(new RoundedBoxGeometry(.42, .34, .42, 3, .02), std(0x6b4fd6, { roughness: .45 })); g.add(b);
  const rib = std(0xffd23d, { roughness: .3, metalness: .2 });
  for (const [sx, sz] of [[.44, .07], [.07, .44]]) { const rb = new THREE.Mesh(new THREE.BoxGeometry(sx, .35, sz), rib); g.add(rb); }
  for (const s of [-1, 1]) { const bow = new THREE.Mesh(new THREE.TorusGeometry(.07, .025, 8, 20), rib); bow.position.set(s * .07, .22, 0); bow.rotation.set(0, 0, s * .5); g.add(bow); }
  g.traverse(o => { if (o.isMesh) o.castShadow = true; }); scene.add(g); g.visible = false; return g;
}
function billboard() {
  const g = new THREE.Group();
  const tex = canvasTex(1400, 560, (ctx, w, h) => { const gr = ctx.createLinearGradient(0, 0, w, h); gr.addColorStop(0, '#ff3d6e'); gr.addColorStop(1, '#ff9a3a'); ctx.fillStyle = gr; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = 'rgba(255,255,255,.18)'; for (let i = 0; i < 14; i++) { ctx.beginPath(); ctx.moveTo(w * .78, h * .5); ctx.arc(w * .78, h * .5, 900, i * .45, i * .45 + .2); ctx.fill(); }
    ctx.fillStyle = '#ffffff'; ctx.strokeStyle = '#1b1626'; ctx.lineWidth = 16; ctx.font = '900 150px IDB'; ctx.textAlign = 'left'; ctx.strokeText('FIZZO', 70, 210); ctx.fillText('FIZZO', 70, 210);
    ctx.font = '900 92px IDB'; ctx.fillStyle = '#ffe14a'; ctx.strokeText('TASTE THE FIZZ!', 70, 340); ctx.fillText('TASTE THE FIZZ!', 70, 340);
    ctx.fillStyle = '#1b1626'; ctx.beginPath(); ctx.roundRect(70, 400, 420, 110, 55); ctx.fill(); ctx.fillStyle = '#ffffff'; ctx.font = '900 64px IDB'; ctx.fillText('BUY NOW', 120, 478);
    // the can
    const cx = w * .78, cy = h * .52; ctx.fillStyle = '#e8203a'; ctx.beginPath(); ctx.roundRect(cx - 95, cy - 200, 190, 400, 40); ctx.fill(); ctx.lineWidth = 12; ctx.stroke();
    ctx.fillStyle = '#ffffff'; ctx.save(); ctx.translate(cx + 20, cy + 10); ctx.rotate(-Math.PI / 2); ctx.font = '900 64px IDB'; ctx.textAlign = 'center'; ctx.fillText('FIZZO', 0, 0); ctx.restore();
    ctx.fillStyle = '#c9ced8'; ctx.fillRect(cx - 80, cy - 195, 160, 22); }).tex;
  const board = new THREE.Mesh(new THREE.PlaneGeometry(7, 2.8), new THREE.MeshStandardMaterial({ map: tex, roughness: .55, emissive: 0xffffff, emissiveMap: tex, emissiveIntensity: .25 })); board.position.set(0, 4.0, .08);
  const frame = new THREE.Mesh(new RoundedBoxGeometry(7.3, 3.1, .18, 3, .05), std(0x2a2d35, { metalness: .5, roughness: .4 })); frame.position.set(0, 4.0, -.02);
  g.add(board, frame);
  for (const s of [-1, 1]) { const pole = new THREE.Mesh(new THREE.CylinderGeometry(.12, .15, 2.6, 16), std(0x3a3d45, { metalness: .6, roughness: .4 })); pole.position.set(s * 2.4, 1.3, -.1); g.add(pole); }
  const catwalk = new THREE.Mesh(new THREE.BoxGeometry(7.2, .06, .5), std(0x3a3d45, { metalness: .6 })); catwalk.position.set(0, 2.55, .25); g.add(catwalk);
  for (let i = 0; i < 3; i++) { const lamp = new THREE.Mesh(new THREE.BoxGeometry(.25, .12, .3), std(0x2a2d35)); lamp.position.set(-2.4 + i * 2.4, 5.65, .35); g.add(lamp); }
  g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); scene.add(g); g.visible = false; return g;
}
function podium() {
  const g = new THREE.Group();
  const banner = canvasTex(512, 512, (ctx, w, h) => { ctx.fillStyle = '#1f3f9a'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#ffffff'; for (let i = 0; i < 5; i++) { const x = 70 + i * 93; ctx.beginPath(); for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + k * Math.PI / 5, r = k % 2 ? 14 : 34; ctx.lineTo(x + Math.cos(a) * r, 90 + Math.sin(a) * r); } ctx.fill(); }
    ctx.fillStyle = '#e8364e'; ctx.fillRect(0, 160, w, 70); ctx.fillStyle = '#ffffff'; ctx.font = '900 120px IDB'; ctx.textAlign = 'center'; ctx.fillText('VOTE', w / 2, 360); ctx.fillText('ME!', w / 2, 470); }).tex;
  const body = new THREE.Mesh(new THREE.BoxGeometry(.9, 1.15, .55), [std(0x6a4528), std(0x6a4528), std(0x6a4528), std(0x6a4528), new THREE.MeshStandardMaterial({ map: banner, roughness: .6 }), std(0x6a4528)]); body.position.y = .575;
  const lip = new THREE.Mesh(new THREE.BoxGeometry(1.0, .06, .65), std(0x4a2f1a)); lip.position.y = 1.18; lip.rotation.x = -.12;
  const mic = new THREE.Mesh(new THREE.CylinderGeometry(.008, .008, .4, 6), std(0x111111, { metalness: .8 })); mic.position.set(0, 1.27, .12); mic.rotation.x = .5;
  const micH = new THREE.Mesh(new THREE.SphereGeometry(.04, 16, 12), std(0x222222, { metalness: .6, roughness: .5 })); micH.position.set(0, 1.4, .2);
  g.add(body, lip, mic, micH); g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); scene.add(g); g.visible = false; return g;
}
const date = bistro(), poker = pokerTable(), gift = giftBox(), board = billboard(), pod = podium();
board.position.set(34, 0, -7.4);
const PROPS = [date, poker, gift, board, pod];

// one global mind: glowing links between cities (space finale)
const net = new THREE.Group(); K.space.add(net); net.visible = false;
{ const r = rand(61), pts = [];
  for (let i = 0; i < 70; i++) { const th = r() * 6.283, ph = Math.acos(lerp(-.75, .85, r())); pts.push(V(Math.sin(ph) * Math.cos(th), Math.cos(ph), Math.sin(ph) * Math.sin(th)).multiplyScalar(3.02)); }
  const dotM = new THREE.MeshBasicMaterial({ color: 0xfff1b0, toneMapped: false }); pts.forEach(p => { const d = new THREE.Mesh(new THREE.SphereGeometry(.035, 10, 8), dotM); d.position.copy(p); net.add(d); });
  const lineM = new THREE.MeshBasicMaterial({ color: 0xb08cff, toneMapped: false, transparent: true, opacity: .9, blending: THREE.AdditiveBlending, depthWrite: false });
  net.userData.arcs = [];
  for (let i = 0; i < 110; i++) { const a = pts[Math.floor(r() * pts.length)], b = pts[Math.floor(r() * pts.length)]; if (a.distanceTo(b) < .8) continue;
    const mid = a.clone().add(b).multiplyScalar(.5); mid.setLength(3 + a.distanceTo(b) * .35);
    const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(a, mid, b), 32, .012, 5), lineM); tube.userData.n = tube.geometry.index.count; tube.userData.d = r(); net.add(tube); net.userData.arcs.push(tube); } }
function netShow(k) { net.visible = true; for (const a of net.userData.arcs) { const f = clamp((k - a.userData.d * .6) / .4); a.geometry.setDrawRange(0, Math.floor(a.userData.n * f / 3) * 3); a.visible = f > 0; } }

// ---------- thought clouds (HTML, crisp; clamped inside the safe zone, above heads, below the counter) ----------
const ui = document.getElementById('ui'), capsEl = document.getElementById('caps');
const css = document.createElement('style');
css.textContent = `.th{position:absolute;left:0;top:0;padding:12px 30px 16px;border-radius:999px;background:#f3ecff;color:#1a1030;font-family:IDB;font-size:44px;letter-spacing:.5px;
border:6px solid #0a0b18;box-shadow:0 8px 0 #0a0b18,0 0 34px rgba(170,130,255,.65);white-space:nowrap;opacity:0;transform-origin:50% 100%}
.th.red{background:#ffe1e6;box-shadow:0 8px 0 #0a0b18,0 0 34px rgba(255,84,104,.6)}.th i{font-style:normal;color:#7a4dff}.th.red i{color:#e8203a}
.thd{position:absolute;left:0;top:0;border-radius:50%;background:#f3ecff;border:5px solid #0a0b18;opacity:0;transform:translate(-50%,-50%)}`;
document.head.appendChild(css);
const TH = [], TD = [];
for (let i = 0; i < 6; i++) { const e = document.createElement('div'); e.className = 'th'; ui.insertBefore(e, capsEl); TH.push(e);
  for (let k = 0; k < 2; k++) { const d = document.createElement('div'); d.className = 'thd'; ui.insertBefore(d, e); TD.push(d); } }
let thN = 0; const tmp = new THREE.Vector3();
const eBack = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
function clearThoughts() { thN = 0; TH.forEach(e => e.style.opacity = 0); TD.forEach(e => e.style.opacity = 0); }
// text: '*word*' = coloured word. o: {dx, up, red, size, until, minY}
function thought(text, wp, t0, t, o = {}) {
  if (t < t0 || (o.until && t > o.until + .2)) return;
  const el = TH[thN], d1 = TD[thN * 2], d2 = TD[thN * 2 + 1]; thN++;
  camera.updateMatrixWorld(); tmp.copy(wp).project(camera); if (tmp.z > 1) return;
  const hx = (tmp.x * .5 + .5) * 1080, hy = (-tmp.y * .5 + .5) * 1920;
  el.className = 'th' + (o.red ? ' red' : ''); el.style.fontSize = (o.size ?? 44) + 'px';
  el.innerHTML = text.replace(/\*(.+?)\*/g, '<i>$1</i>');
  el.style.transform = 'none'; const w = el.offsetWidth, h = el.offsetHeight;
  const bx = clamp(hx + (o.dx ?? 0), 66 + w / 2, 924 - w / 2), by = clamp(o.y ?? (hy - (o.up ?? 110)), (o.minY ?? 620) + h, 1110);
  const k = t - t0, s = k < .25 ? Math.max(.01, eBack(k / .25)) : 1, a = clamp(k / .08) * (o.until ? 1 - clamp((t - o.until) / .2) : 1);
  el.style.left = bx + 'px'; el.style.top = by + 'px'; el.style.opacity = a;
  el.style.transform = `translate(-50%,-100%) scale(${s}) rotate(${Math.sin(t * 2.2 + thN * 1.7) * 1.2}deg)`;
  // two little "thinking" dots from the head to the cloud
  const ex = bx, ey = by + 8, dist = Math.hypot(ex - hx, ey - hy);
  [[d1, .62, 30], [d2, .3, 18]].forEach(([d, f, sz]) => { d.style.width = d.style.height = sz + 'px'; d.style.background = o.red ? '#ffe1e6' : '#f3ecff';
    d.style.left = lerp(hx, ex, f) + 'px'; d.style.top = lerp(hy - 30, ey, f) + 'px'; d.style.opacity = dist > 70 ? a * clamp((k - .05 * (f > .5 ? 1 : 2)) / .1) : 0; });
}

// ---------- timeline (v = days since everyone could read minds) ----------
const D = 1, H = 1 / 24, Y = 365.25, SEC = 1 / 86400;
const B = [
  { t: 3.2, v: 1 * SEC, cap: 'Everyone on Earth can suddenly hear thoughts.', hi: ['hear', 'thoughts'], size: 62 },
  { t: 5.6, v: 10 * SEC, cap: 'Second 10: Jeremy hears the barista.', hi: ['barista'] },
  { t: 8.0, v: 60 * SEC, cap: 'We each think ~6,200 thoughts a day. ALL public.', hi: ['6,200'], red: ['ALL', 'public'], size: 60 },
  { t: 10.4, v: 1 * H, cap: 'Hour 1: surprise parties are dead. Forever.', red: ['dead'], size: 64 },
  { t: 12.8, v: 6 * H, cap: 'Hour 6: poker is over. Every bluff is heard.', hi: ['bluff'], size: 64 },
  { t: 15.2, v: 1 * D, cap: 'Day 1: no more lies. We tell ~1.65 a day.', hi: ['1.65'], red: ['lies'], note: 'Real study: we average 1.65 lies a day' },
  { t: 17.6, v: 3 * D, cap: 'Day 3: first dates get VERY honest.', hi: ['VERY', 'honest'] },
  { t: 20.0, v: 7 * D, cap: 'Week 1: ads stop working. Everyone thinks "meh."', hi: ['"meh."'], size: 60, note: 'Real: ~$1.14 trillion spent on ads in 2025' },
  { t: 22.4, v: 30.44 * D, cap: "Month 1: politicians can't hide a thing.", hi: ['hide'], note: 'Speculation: our guess, not science' },
  { t: 24.8, v: 1 * Y, cap: 'Year 1: tinfoil hats sell out. Useless.', hi: ['tinfoil'], red: ['Useless'], note: 'Real MIT test: foil hats can AMPLIFY signals' },
  { t: 27.2, v: 10 * Y, cap: 'Year 10: nobody talks out loud anymore.', hi: ['nobody'], note: 'Speculation: our guess, not science' },
  { t: 29.6, v: 100 * Y, cap: 'Year 100: billions of minds become ONE?', hi: ['ONE?'], big: true, space: true, note: 'Speculation: our guess, not science' },
  { t: 32.0, v: 100 * Y, cap: 'Real life: AI can already decode the gist.', hi: ['AI'], size: 62, note: 'UT Austin 2023: brain scan + AI = rough gist' },
  { t: 34.4, v: 100 * Y, cap: 'Would YOU want to read minds? 👇', hi: ['YOU', 'minds?'] },
];
B.forEach(b => b.capY ??= 1225);
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;
function fmt(v) {
  const s = v * 86400;
  if (s < 59.5) return plural(Math.max(1, Math.round(s)), 'second');
  if (s < 3600) return plural(Math.round(s / 60), 'minute');
  if (v < 1) return plural(Math.max(1, Math.round(v * 24)), 'hour');
  if (v >= 6.5 && v < 7.5) return '1 week';
  if (v < 28) return plural(Math.round(v), 'day');
  if (v < 360) return plural(Math.round(v / 30.44), 'month');
  return plural(Math.round(v / Y), 'year');
}

// ---------- helpers ----------
const JX = 23.4, JZ = 6.0;
function jer(x, z, ry, pose, cup = false) {
  J.visible = true; J.position.set(x, .18, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose);
  if (cup) { J.arms[1].rotation.x = -1.15; J.arms[1].add(W.cup); W.cup.position.set(-.02, -.74, .05); W.cup.rotation.set(1.15, 0, 0); W.cup.visible = true; }
}
function hideAll() {
  J.visible = false; J.arms[1].rotation.x = 0; J.arms[0].rotation.x = 0; if (W.cup.parent !== scene) scene.add(W.cup); W.cup.visible = false; W.splash.visible = false; W.sparkle.visible = false;
  CAST.forEach(p => { p.visible = false; p.foil.visible = false; p.arms[0].rotation.x = 0; p.arms[1].rotation.x = 0; }); J.foil && (J.foil.visible = false);
  PROPS.forEach(p => p.visible = false); net.visible = false;
  noFocus(); RIM.k = .55; INK.on = true; GRADE.split = .08; clearThoughts();
}
// Jeremy gets a foil hat too
{ const f = P.ken.foil.clone(); f.visible = false; J.headG.add(f); J.foil = f; }
const bob = (t, ph = 0, a = .012) => Math.sin(t * 7 + ph) * a;

run({
  total: 38.6, ctaAt: 34.4, sub: '',
  reel: ['(x)', 'ALL HUMANS VANISHED', 'PIGEONS DOUBLED', 'YOUR COFFEE DOUBLED', 'JEREMY KEPT GROWING', 'GRAVITY DOUBLED', 'WE COULD READ MINDS?'],
  beats: B, label: () => 'EVERYONE READS MINDS', fmt,
  beds: [{ t0: 0, t1: 12.9, name: 'city', gain: .28 }, { t0: 3.4, t1: 10.5, name: 'murmur', gain: .55 }, { t0: 12.8, t1: 15.3, name: 'crickets', gain: .2 },
    { t0: 15.2, t1: 24.9, name: 'city', gain: .24 }, { t0: 20.0, t1: 24.9, name: 'murmur', gain: .5 }, { t0: 24.8, t1: 27.3, name: 'winter', gain: .3 },
    { t0: 27.2, t1: 29.7, name: 'birds', gain: .22 }, { t0: 29.6, t1: 32.1, name: 'drone', gain: .35 }, { t0: 32.0, t1: 38.6, name: 'city', gain: .2 }],
  sfx: [{ t: 3.3, name: 'sparkle_rev', gain: .55 }, { t: 4.45, name: 'clatter', gain: .5 }, { t: 4.5, name: 'splash', gain: .3 },
    { t: 13.5, name: 'chips', gain: .55 }, { t: 14.6, name: 'chips', gain: .4 }, { t: 25.0, name: 'wind_gust', gain: .3 }, { t: 25.3, name: 'rustle', gain: .3 },
    { t: 29.7, name: 'poof', gain: .5 }, { t: 32.1, name: 'ding', gain: .35 },
    // thought-cloud pops (match the thought() start times below)
    ...[3.55, 3.95, 5.95, 8.15, 8.45, 8.75, 9.05, 9.35, 10.75, 11.55, 13.95, 16.7, 18.0, 18.8, 20.6, 21.0, 21.4, 23.3, 25.9, 27.6, 28.3, 32.5, 35.0].map(t => ({ t, name: 'pop', gain: .4 }))],
  introShot(t) {
    mode('street'); hideAll(); setSky('day'); setAge(0, t, { lamps: 0 });
    jer(lerp(19.4, JX, eOut(clamp(t / 3.0))), JZ, Math.PI / 2 + .3 * clamp(t / 3), { expr: 'happy', bob: Math.abs(Math.sin(t * 6)) * .03 * (1 - clamp((t - 2.6) / .5)), armL: .25 }, true);
    put(P.mia, lerp(27.5, 24.6, t / 3.2), 7.1, -Math.PI / 2, { expr: 'happy', bob: Math.abs(Math.sin(t * 6 + 1)) * .03 });
    dolly(V(22.2, 1.6, -.6), V(23.2, 1.55, .2), V(21.0, 1.9, 6.2), V(23.3, 1.95, 6.0), t / 3.2, 0, 52);
    focus(V(J.position.x, 1.2, JZ), .8, 10);
  },
  shot(t, b, lt, i) {
    mode('street'); hideAll(); const k = clamp(lt / 2.4), T0 = b.t;
    if (i === 0) { // it starts: everyone hears everyone
      setSky('day'); setAge(0, t, { lamps: 0 });
      const drop = lt > 1.15, f = clamp((lt - 1.15) / .3);
      jer(JX, JZ, Math.PI - .15, { expr: lt > .55 ? 'shocked' : 'happy', look: lt > .55 ? Math.sin(t * 3) * .5 : 0, armL: .2, bob: bob(t) }, !drop);
      if (drop) { W.cup.visible = true; W.cup.position.set(JX - .3, lerp(1.1, .27, f * f), JZ + .35); W.cup.rotation.set(0, .4, f * Math.PI / 2);
        if (f >= 1) { W.splash.visible = true; W.splash.position.set(JX - .45, .19, JZ + .15); W.splash.scale.setScalar(.2 + eOut(clamp((lt - 1.45) / .4)) * 1.3); } }
      put(P.mia, 24.75, 7.1, Math.PI + .5, { expr: 'happy', bob: bob(t, 1) });
      put(P.sam, 22.05, 7.2, Math.PI - .45, { expr: 'worried', bob: bob(t, 2) });
      dolly(V(23.4, 1.6, -.8), V(23.4, 1.58, 0), V(23.4, 2.0, 6.4), V(23.4, 2.0, 6.4), k, 0, 52);
      focus(V(JX, 1.3, JZ), .7, 10);
      thought('Is he *staring* at me?', head(P.mia), T0 + .35, t, { dx: 60, y: 900 });
      thought('Did I lock my *car?*', head(P.sam), T0 + .75, t, { dx: -60, y: 770 });
    } else if (i === 1) { // the barista's real opinion
      setSky('day'); setAge(0, t, { lamps: 0 });
      W.cup.visible = true; W.cup.position.set(JX - .45, .27, JZ + .35); W.cup.rotation.set(0, .4, Math.PI / 2); W.splash.visible = true; W.splash.position.set(JX - .6, .19, JZ + .15); W.splash.scale.setScalar(1.5);
      put(P.barista, 21.7, 7.05, face(21.7, 7.05, JX, JZ), { expr: 'happy', armR: .9, bob: bob(t) });
      P.barista.arms[1].rotation.x = -1.0;
      jer(JX, JZ, face(JX, JZ, 21.7, 7.05), { expr: lt > .7 ? 'shocked' : 'confused', look: 0, bob: bob(t, 2) });
      dolly(V(22.4, 1.55, .9), V(22.5, 1.55, 1.5), V(22.5, 1.98, 6.6), V(22.55, 1.98, 6.6), k, 0, 52);
      focus(V(22.5, 1.6, 6.5), .8, 10);
      thought('Ugh. *HIM* again.', head(P.barista), T0 + .35, t, { red: true, size: 50, dx: -20, y: 880 });
    } else if (i === 2) { // a street full of thoughts
      setSky('day'); setAge(0, t, { lamps: 0 });
      const ppl = [[P.mia, 22.6, 6.2, 2.4], [P.ken, 23.7, 7.3, 3.0], [P.ava, 26.1, 7.2, -2.9], [P.sam, 27.2, 6.0, -2.3]];
      ppl.forEach(([p, x, z, ry], j) => put(p, x + Math.sin(t * .8 + j) * .06, z, ry, { expr: j % 2 ? 'worried' : 'happy', bob: bob(t, j), look: Math.sin(t + j) * .4 }));
      jer(24.9, 5.6, Math.PI - .1, { expr: 'shocked', look: Math.sin(t * 4) * .7, bob: bob(t, 5) });
      dolly(V(24.6, 2.0, -3.2), V(25.0, 1.95, -2.5), V(24.8, 2.05, 6.4), V(24.9, 2.05, 6.4), k, 0, 52);
      const txt = ['Rent is *due*...', 'Did I leave the *oven* on?', 'Nice *shoes*', '*Pizza.* Pizza. Pizza.'];
      ppl.forEach(([p], j) => thought(txt[j], head(p), T0 + .15 + j * .3, t, { size: 38, y: [930, 750, 750, 930][j], dx: [-40, -20, 20, 40][j] }));
    } else if (i === 3) { // no more surprise parties
      setSky('day'); setAge(0, t, { lamps: 0 });
      put(P.ava, 24.9, 6.1, -Math.PI / 2 - .5, { expr: 'happy', armL: .05, armR: .05, bob: bob(t) });
      P.ava.arms[0].rotation.x = .5; P.ava.arms[1].rotation.x = .5;
      gift.visible = true; gift.position.set(25.25, .95, 6.55); gift.rotation.y = .4;
      jer(23.1, 6.0, Math.PI / 2 + .45, { expr: lt > 1.2 ? 'confused' : 'happy', look: .3, bob: bob(t, 3) });
      dolly(V(24.0, 1.55, .4), V(24.0, 1.55, 1.0), V(24.0, 2.0, 6.2), V(24.0, 2.0, 6.2), k, 0, 52);
      focus(V(24, 1.4, 6.1), .7, 10);
      thought('Surprise party at *8!*', head(P.ava), T0 + .35, t, { dx: 60, y: 900 });
      thought('...I can *hear* you.', headPos(), T0 + 1.15, t, { dx: -60, y: 770 });
    } else if (i === 4) { // poker night
      setSky('dusk', 'night', .35); setAge(0, t, { lamps: 1, lights: .7 }); GRADE.split = .12;
      poker.visible = true; poker.position.set(25.6, .18, 6.4);
      jer(25.6, 7.45, Math.PI, { expr: lt > 1.3 ? 'happy' : 'confused', armL: .5, armR: .5, bob: bob(t) });
      J.arms[0].rotation.x = -.6; J.arms[1].rotation.x = -.6;
      put(P.ken, 24.45, 6.55, Math.PI / 2, { expr: 'worried', sweatK: (t * .8) % 1, armL: .4, armR: .4 }); P.ken.arms[0].rotation.x = -.7; P.ken.arms[1].rotation.x = -.7;
      put(P.sam, 26.75, 6.6, -Math.PI / 2, { expr: 'happy', look: -.4, armL: .4, armR: .4 }); P.sam.arms[0].rotation.x = -.6; P.sam.arms[1].rotation.x = -.6;
      dolly(V(25.6, 2.55, .4), V(25.6, 2.45, 1.1), V(25.6, 1.75, 6.8), V(25.6, 1.75, 6.8), k, 0, 52);
      focus(V(25.6, 1.2, 6.6), .8, 10);
      thought('I have *NOTHING.*', head(P.ken), T0 + 1.15, t, { red: true, dx: -40, y: 800 });
    } else if (i === 5) { // honest compliments
      setSky('day'); setAge(0, t, { lamps: 0 });
      put(P.zoe, 22.4, 6.1, Math.PI / 2 + .55, { expr: lt > 1.65 ? 'shocked' : 'happy', armL: lt < 1.65 ? .9 + Math.sin(t * 4) * .1 : .2, armR: lt < 1.65 ? .9 : .2, bob: bob(t) });
      jer(24.0, 5.9, -Math.PI / 2 - .5, { expr: 'happy', armL: .2, bob: bob(t, 2) });
      dolly(V(23.3, 1.55, -.4), V(23.25, 1.55, .3), V(23.2, 2.0, 6.0), V(23.2, 2.0, 6.0), k, 0, 52);
      focus(V(23.2, 1.3, 6.0), .7, 10);
      bubble(t, 'LOVE IT!', T0 + .05, headPos());
      thought("It's *hideous*", headPos(), T0 + 1.5, t, { red: true, dx: 160, y: 740 });
    } else if (i === 6) { // first date
      setSky('golden'); setAge(0, t, { lamps: 0 });
      date.visible = true; date.position.set(24.2, .18, 6.3); date.rotation.y = 0;
      put(P.mia, 23.45, 6.35, Math.PI / 2 - .1, { expr: lt > 1.4 ? 'worried' : 'happy', bob: bob(t), look: .2 });
      put(P.sam, 24.95, 6.3, -Math.PI / 2 + .1, { expr: 'happy', bob: bob(t, 1), look: -.2 });
      dolly(V(24.3, 1.55, -.2), V(24.2, 1.55, .5), V(24.2, 1.95, 6.3), V(24.2, 1.95, 6.3), k, 0, 52);
      focus(V(24.2, 1.2, 6.3), .8, 10);
      thought("She's *SO* cute", head(P.sam), T0 + .4, t, { dx: 90, y: 900 });
      thought('Spinach in his *teeth?*', head(P.mia), T0 + 1.2, t, { dx: -60, y: 760, red: true });
    } else if (i === 7) { // advertising dies
      setSky('overcast'); setAge(0, t, { lamps: 0 });
      board.visible = true;
      const crowd = [[P.ken, 32.6, 3.5], [P.ava, 33.8, 2.9], [P.barista, 35.3, 3.6]];
      crowd.forEach(([p, x, z], j) => put(p, x, z, Math.PI + (x - 34) * -.05, { expr: 'confused', bob: bob(t, j) }));
      jer(34.4, 4.4, Math.PI + .1, { expr: 'confused', bob: bob(t, 4) });
      dolly(V(34.3, 1.65, 9.6), V(34.2, 1.75, 9.0), V(34.0, 2.55, -7.4), V(34.0, 2.7, -7.4), k, 0, 52);
      focus(V(34, 3.2, -7.4), .6, 8);
      thought('*meh.*', head(P.ken), T0 + .6, t, { y: 1100, dx: -60 });
      thought('*nope.*', head(P.ava), T0 + 1.0, t, { y: 1010, dx: 0 });
      thought('who *cares*', head(P.barista), T0 + 1.4, t, { y: 1100, dx: 60 });
    } else if (i === 8) { // politics
      setSky('day'); setAge(0, t, { lamps: 0 });
      pod.visible = true; pod.position.set(25, .18, 6.7);
      put(P.pol, 25, 7.25, Math.PI, { expr: lt > 1.2 ? 'worried' : 'happy', armL: lt < 1.2 ? .9 + Math.sin(t * 5) * .3 : .2, armR: .3, bob: bob(t) });
      put(P.mia, 23.4, 4.0, -.3, { expr: 'confused' }); put(P.ken, 26.4, 3.8, .35, { expr: 'confused' });
      dolly(V(25.0, 1.25, 2.0), V(25.0, 1.3, 2.6), V(25.0, 1.95, 7), V(25.0, 1.9, 7), k, 0, 50);
      focus(head(P.pol), .7, 10);
      bubble(t, 'TRUST ME!', T0 + .2, head(P.pol));
      thought("I have *no plan*", head(P.pol), T0 + 1.1, t, { red: true, dx: 180, up: 170 });
    } else if (i === 9) { // tinfoil hats
      setSky('winter'); setAge(0, t, { snow: 1, cx: 24, cz: 4, lamps: 0 }); GRADE.split = .04;
      [[P.ken, 22.0, 6.2, .35], [P.zoe, 25.3, 6.0, -.4]].forEach(([p, x, z, ry], j) => { put(p, x, z, Math.PI + ry, { expr: 'worried', look: Math.sin(t * 2 + j) * .5, bob: bob(t, j) }); p.foil.visible = true; });
      jer(JX + .2, 5.5, Math.PI, { expr: lt > 1.3 ? 'worried' : 'happy', bob: bob(t, 3), look: lt > 1.3 ? Math.sin(t * 3) * .6 : 0 }); J.foil.visible = true;
      dolly(V(23.7, 1.6, -1.0), V(23.65, 1.6, -.3), V(23.6, 2.05, 6), V(23.6, 2.05, 6), k, 0, 52);
      focus(V(23.6, 1.6, 5.6), .7, 10);
      thought('They *still* hear me', headPos(), T0 + 1.1, t, { y: 720, dx: 120 });
    } else if (i === 10) { // a silent street
      setSky('golden'); setAge(0, t, { lamps: 0 });
      put(P.ava, 22.4, 6.2, Math.PI / 2 + .5, { expr: 'happy', bob: Math.abs(Math.sin(t * 9)) * .03 });
      jer(23.6, 6.0, -Math.PI / 2 - .5, { expr: 'happy', bob: Math.abs(Math.sin(t * 9 + 1)) * .03 });
      put(P.sam, 26.4, 6.6, -Math.PI / 2 - .4, { expr: 'happy', look: .3 }); put(P.zoe, 27.5, 6.3, Math.PI / 2 + 1.0, { expr: 'happy' });
      dolly(V(22.7, 1.6, -.4), V(23.1, 1.6, .2), V(22.9, 2.0, 6.2), V(23.2, 2.0, 6.2), k, 0, 52);
      focus(V(23, 1.4, 6.1), .7, 10);
      thought('Ha! *Good one.*', head(P.ava), T0 + .4, t, { dx: -40, y: 900 });
      thought('*Lunch?* 🍕', headPos(), T0 + 1.1, t, { dx: 90, y: 760 });
    } else if (i === 11) { // one global mind
      mode('space'); hideAll(); INK.on = false; const kk = eInOut(k);
      K.earth.rotation.y = t * .12; K.clouds.rotation.y = t * .14; net.rotation.y = K.earth.rotation.y; netShow(clamp(lt / 1.8));
      K.moon.visible = true;
      dolly(V(0, 1.2, 13), V(0, 1.6, 10.5), V(0, -.3, 0), V(0, -.2, 0), kk, 0, 50);
    } else { // back to Jeremy: it's already starting / CTA
      setSky('day'); setAge(0, t, { lamps: 0 });
      const cta = i === 13;
      jer(JX, JZ, Math.PI - .1, { expr: cta ? 'happy' : (lt < 1.2 ? 'shocked' : 'confused'), look: cta ? 0 : Math.sin(t * 2) * .5, armL: cta ? .3 + Math.abs(Math.sin(t * 5)) * 2.3 : .2, bob: bob(t) });
      if (i === 12) dolly(V(JX + .6, 1.5, JZ - 4.3), V(JX + .35, 1.5, JZ - 3.6), V(JX, 1.72, JZ), V(JX, 1.72, JZ), k, 0, 50);
      else dolly(V(JX + .35, 1.5, JZ - 3.6), V(JX + .9, 1.7, JZ - 4.8), V(JX, 1.72, JZ), V(JX, 1.75, JZ), eInOut(k), 0, 50);
      focus(V(JX, 1.4, JZ), .9, 10);
      if (i === 12) thought('Wait... *really?!*', headPos(), T0 + .5, t, { up: 240, dx: 120 });
      else thought('What are *YOU* thinking?', headPos(), T0 + .6, t, { up: 250, dx: 0 });
    }
    const sm = document.getElementById('small'); sm.style.top = '1378px'; sm.style.fontSize = '36px'; sm.style.fontFamily = 'IDB'; sm.style.color = '#ffe08a'; sm.style.webkitTextStroke = '5px #0a0b18'; sm.style.paintOrder = 'stroke fill'; sm.style.left = '60px'; sm.style.right = '150px';
    sm.textContent = b.note || ''; sm.style.opacity = b.note ? clamp((lt - .3) / .3) : 0;
    if (b.big && lt < .35) shake(.06 * (1 - lt / .35), t);
  },
});
