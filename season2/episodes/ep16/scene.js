// Episode 16 — What if robots took every job?  (original street look + AI voiceover; beats are timed to vo.json)
// Facts (checked 2026-11-12):
//  - about 3.5 billion people are employed worldwide (ILO, World Employment and Social Outlook / ILOSTAT)
//  - about 5 million industrial robots operate in factories worldwide (International Federation of Robotics,
//    "Five million robots now operate in factories globally", https://ifr.org/news/five-million-robots-now-operate-in-factories-globally/)
//  - about 60% of US employment in 2018 was in job titles that did not exist in 1940 (Autor, Chin, Salomons & Seegmiller, "New Frontiers";
//    MIT News 2024, https://news.mit.edu/2024/does-technology-help-or-hurt-employment-0401)
//  - everything from "imagine robots take every job" on is labelled SPECULATION on screen (note line) and in the voiceover ("imagine", "maybe").
import { THREE, RoundedBoxGeometry, scene, camera, canvasTex, rand, clamp, prog, lerp, eOut, eInOut, V, K, boot, mode, dolly, shake, bubble, headPos, run, focus, noFocus, RIM, GRADE, INK, rimLight } from './kit.js';
import { buildWorld, W, setAge, setSky } from './world.js';
import { makeJeremy2 } from './jeremy2.js';

await boot('WHAT IF ROBOTS TOOK EVERY JOB?', 'EP. 16');
const VO = await (await fetch('./vo.json')).json(), LN = VO.lines;
const J = K.J;
buildWorld(K);

// ---------- clear the set: nothing between the camera and the action ----------
const S = K.street.group;
const near = (o, x, z) => Math.abs(o.position.x - x) < .1 && Math.abs(o.position.z - z) < .1;
S.children.forEach(o => { if ([[21, 4.8], [30, 4.8], [35, -4.8], [26, -4.8], [33, -7.2]].some(([x, z]) => near(o, x, z))) o.visible = false; });
const parked = W.cars.find(c => near(c, 26, 3.2)); W.cars.forEach(c => { if (near(c, 40, -3.2)) c.visible = false; });

// ---------- cast ----------
const std = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .6, ...o });
const darker = (c) => new THREE.Color(c).multiplyScalar(.78).getHex();
const shadows = g => { g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };
function fedora(col = 0x4a3b2e) { const g = new THREE.Group(), m = std(col, { roughness: .8 });
  const brim = new THREE.Mesh(new THREE.CylinderGeometry(.74, .74, .035, 40), m); const crown = new THREE.Mesh(new THREE.CylinderGeometry(.42, .5, .34, 40), m); crown.position.y = .18;
  const band = new THREE.Mesh(new THREE.CylinderGeometry(.505, .505, .07, 40), std(0x1c1714)); band.position.y = .06; g.add(brim, crown, band); g.position.set(0, .5, 0); g.rotation.x = -.08; g.visible = false; shadows(g); return g; }
function person({ top, hair = 0x3a2417, skin = 0xf1b58e, legs = 0x2b3a5e, shoes = 0xf6f6f6, long = false, tie = 0, s = .75 }) {
  const p = makeJeremy2();
  const map = new Map([[0x2f6dff, top], [0x2457cc, darker(top)], [0x3a2417, hair], [0xf1b58e, skin], [0x2b3a5e, legs], [0xff3d6e, shoes]]);
  const seen = new Set();
  p.traverse(o => { if (!o.isMesh || seen.has(o.material)) return; seen.add(o.material); const m = o.material; const h = m.color?.getHex();
    if (map.has(h)) { m.color.setHex(map.get(h)); if (m.sheenColor) m.sheenColor.setHex(map.get(h)); } });
  const hairM = std(hair, { roughness: .45 });
  if (long) { const back = new THREE.Mesh(new THREE.SphereGeometry(.56, 40, 24, Math.PI, Math.PI, 0, Math.PI * .72), hairM); back.scale.set(1.02, 1.35, 1); back.position.set(0, -.18, -.04); p.headG.add(back);
    for (const sx of [-1, 1]) { const lock = new THREE.Mesh(new THREE.CapsuleGeometry(.11, .5, 8, 16), hairM); lock.position.set(sx * .47, -.3, -.02); lock.rotation.z = sx * .08; p.headG.add(lock); } }
  if (tie) { const col = new THREE.Mesh(new THREE.ConeGeometry(.16, .22, 3), std(0xffffff)); col.rotation.x = Math.PI; col.position.set(0, 1.56, .33); col.scale.z = .3; p.bodyG.add(col);
    const tk = new THREE.Mesh(new THREE.BoxGeometry(.1, .46, .03), std(tie, { roughness: .4 })); tk.position.set(0, 1.27, .39); tk.rotation.x = -.12; p.bodyG.add(tk); }
  p.hat = fedora(); p.headG.add(p.hat);
  p.scale.setScalar(s); scene.add(p); rimLight(p); p.visible = false; return p;
}
const P = {
  mia: person({ top: 0xff7aa8, hair: 0x6a3a1c, skin: 0xf3c8a8, long: true, legs: 0x38405e, shoes: 0xffffff, s: .72 }),
  sam: person({ top: 0xff8a2a, hair: 0x241812, skin: 0x8d5a3b, legs: 0x3b3b44, shoes: 0x2fb57d }),
  ken: person({ top: 0x6b4fd6, hair: 0x101010, skin: 0xe9b88e, legs: 0x2a2d35, shoes: 0xffc93a }),
  ava: person({ top: 0x29b48a, hair: 0x2a1a12, skin: 0xa86a48, long: true, legs: 0x2b3a5e, shoes: 0xffffff, s: .72 }),
  pol: person({ top: 0x262a3a, hair: 0x8a8a8a, skin: 0xf0b896, legs: 0x262a3a, shoes: 0x111111, tie: 0xe8364e, s: .78 }),
};
const CAST = Object.values(P);
J.hat = fedora(0x3a3f55); J.headG.add(J.hat);
function put(p, x, z, ry, pose = {}) { p.visible = true; p.position.set(x, .18, z); p.rotation.set(0, ry, 0); p.pose(pose); }
const face = (x0, z0, x1, z1) => Math.atan2(x1 - x0, z1 - z0);

// ---------- humanoid robot: glossy white shell, dark joints, glowing visor eyes ----------
function robot(accent = 0x35d6ff) {
  const g = new THREE.Group(), white = new THREE.MeshPhysicalMaterial({ color: 0xf1f3f6, roughness: .22, clearcoat: .9, clearcoatRoughness: .15 }), dark = std(0x2a2e37, { metalness: .65, roughness: .38 });
  const glow = new THREE.MeshBasicMaterial({ color: accent, toneMapped: false }), visorM = new THREE.MeshPhysicalMaterial({ color: 0x07090d, roughness: .08, clearcoat: 1 });
  const add = (geo, mat, x, y, z, parent = g) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); parent.add(m); return m; };
  add(new RoundedBoxGeometry(.66, .74, .44, 6, .16), white, 0, 1.3, 0); add(new THREE.CylinderGeometry(.2, .24, .16, 24), dark, 0, .88, 0); add(new RoundedBoxGeometry(.5, .2, .36, 5, .09), white, 0, .76, 0);
  const chest = add(new THREE.CircleGeometry(.07, 24), glow, 0, 1.42, .223); add(new THREE.CylinderGeometry(.09, .09, .12, 16), dark, 0, 1.72, 0);
  const head = new THREE.Group(); head.position.set(0, 2.02, 0); g.add(head); g.head = head;
  add(new RoundedBoxGeometry(.6, .5, .5, 7, .2), white, 0, 0, 0, head); add(new RoundedBoxGeometry(.48, .24, .1, 5, .05), visorM, 0, .0, .215, head);
  g.eyes = [-1, 1].map(s => { const e = add(new THREE.CapsuleGeometry(.035, .06, 6, 12), glow, s * .11, .0, .268, head); return e; });
  add(new THREE.CylinderGeometry(.012, .012, .2, 8), dark, .2, .34, 0, head); add(new THREE.SphereGeometry(.035, 12, 10), glow, .2, .45, 0, head);
  for (const s of [-1, 1]) { add(new THREE.CylinderGeometry(.05, .05, .06, 16), dark, s * .31, 0, 0, head).rotation.z = Math.PI / 2; }
  g.legs = [-1, 1].map(s => { const l = new THREE.Group(); l.position.set(s * .17, .68, 0); g.add(l); add(new THREE.CapsuleGeometry(.1, .34, 8, 16), white, 0, -.26, 0, l); add(new THREE.SphereGeometry(.085, 16, 12), dark, 0, -.02, 0, l);
    add(new RoundedBoxGeometry(.2, .12, .34, 4, .05), dark, 0, -.56, .05, l); return l; });
  g.arms = [-1, 1].map(s => { const a = new THREE.Group(); a.position.set(s * .43, 1.56, 0); g.add(a); add(new THREE.SphereGeometry(.11, 16, 12), dark, 0, 0, 0, a); add(new THREE.CapsuleGeometry(.08, .44, 8, 16), white, 0, -.36, 0, a);
    add(new THREE.SphereGeometry(.095, 16, 12), dark, 0, -.7, 0, a); a.rotation.z = s * .1; return a; });
  g.pose = ({ walk = 0, ph = 0, armL = 0, armR = 0, look = 0, bob = 0, nod = 0 } = {}) => { g.legs[0].rotation.x = Math.sin(ph) * .5 * walk; g.legs[1].rotation.x = -Math.sin(ph) * .5 * walk;
    g.arms[0].rotation.x = armL || -Math.sin(ph) * .4 * walk; g.arms[1].rotation.x = armR || Math.sin(ph) * .4 * walk; head.rotation.y = look; head.rotation.x = nod; g.position.y = .18 + bob + Math.abs(Math.sin(ph)) * .02 * walk; };
  glow.userData.rim = true; g.scale.setScalar(.88); shadows(g); scene.add(g); rimLight(g); g.visible = false; return g; // (rim shader needs lit materials: skip the unlit glow)
}
const R = [robot(), robot(0x7dff9a), robot(0xffb648), robot()];
function rput(r, x, z, ry, pose = {}) { r.visible = true; r.position.set(x, .18, z); r.rotation.set(0, ry, 0); r.pose(pose); }

// ---------- industrial robot arm (factory orange) ----------
function arm() {
  const g = new THREE.Group(), or = new THREE.MeshPhysicalMaterial({ color: 0xf26a1b, roughness: .3, clearcoat: .7 }), dk = std(0x23262d, { metalness: .7, roughness: .35 });
  const m = (geo, mat, p) => { const x = new THREE.Mesh(geo, mat); p.add(x); return x; };
  m(new THREE.CylinderGeometry(.42, .48, .22, 40), dk, g).position.y = .11;
  const yaw = new THREE.Group(); yaw.position.y = .22; g.add(yaw); m(new THREE.CylinderGeometry(.3, .34, .4, 32), or, yaw).position.y = .2;
  const sh = new THREE.Group(); sh.position.y = .5; yaw.add(sh); const j1 = m(new THREE.CylinderGeometry(.2, .2, .5, 24), dk, sh); j1.rotation.x = Math.PI / 2;
  const l1 = m(new THREE.CapsuleGeometry(.14, 1.15, 8, 20), or, sh); l1.position.y = .7;
  const el = new THREE.Group(); el.position.y = 1.4; sh.add(el); const j2 = m(new THREE.CylinderGeometry(.16, .16, .42, 24), dk, el); j2.rotation.x = Math.PI / 2;
  const l2 = m(new THREE.CapsuleGeometry(.105, .95, 8, 20), or, el); l2.position.y = .58;
  const wr = new THREE.Group(); wr.position.y = 1.16; el.add(wr); m(new THREE.CylinderGeometry(.09, .09, .16, 16), dk, wr).position.y = .06; const tool = m(new THREE.ConeGeometry(.05, .26, 12), std(0xcfd3da, { metalness: 1, roughness: .25 }), wr); tool.position.y = .26;
  const tip = new THREE.Object3D(); tip.position.y = .4; wr.add(tip); g.tip = tip;
  g.set = (y, a, b, c = 0) => { yaw.rotation.y = y; sh.rotation.x = a; el.rotation.x = b; wr.rotation.x = c; };
  shadows(g); scene.add(g); g.visible = false; return g;
}
const ARMS = [arm(), arm()];
const sparkTex = canvasTex(64, 64, (ctx, w, h) => { const gr = ctx.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.3, 'rgba(255,220,120,.9)'); gr.addColorStop(1, 'rgba(255,140,20,0)'); ctx.fillStyle = gr; ctx.fillRect(0, 0, w, h); }).tex;
const SPARKS = ARMS.map(() => { const n = 26, geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(n * 3), 3));
  const p = new THREE.Points(geo, new THREE.PointsMaterial({ map: sparkTex, size: .16, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, color: 0xffffff })); p.frustumCulled = false; scene.add(p); INK.skip.push(p); p.visible = false;
  const core = new THREE.Sprite(new THREE.SpriteMaterial({ map: sparkTex, blending: THREE.AdditiveBlending, depthWrite: false })); scene.add(core); INK.skip.push(core); core.visible = false; p.core = core; return p; });
const hash = (n) => { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); };
function sparks(i, t, on) { const p = SPARKS[i]; p.visible = p.core.visible = on; if (!on) return; const c = ARMS[i].tip.getWorldPosition(new THREE.Vector3()), a = p.geometry.attributes.position;
  for (let k = 0; k < a.count; k++) { const life = ((t * 2.6 + hash(k + i * 50)) % 1), th = hash(k * 3 + 1 + Math.floor(t * 2.6 + hash(k + i * 50))) * 6.283, sp = .5 + hash(k * 7 + 2) * .9;
    a.setXYZ(k, c.x + Math.cos(th) * sp * life * .7, c.y + sp * life * .6 - life * life * 1.1, c.z + Math.sin(th) * sp * life * .7); }
  a.needsUpdate = true; const f = .7 + .3 * Math.sin(t * 47) * Math.sin(t * 31); p.core.position.copy(c); p.core.scale.setScalar(.55 * f); p.material.opacity = .9; }

// ---------- props ----------
const awnTex = canvasTex(512, 128, (ctx, w, h) => { for (let i = 0; i < 8; i++) { ctx.fillStyle = i % 2 ? '#f6f1e7' : '#d8402f'; ctx.fillRect(i * 64, 0, 64, h); } }).tex;
const signTex = canvasTex(512, 160, (ctx, w, h) => { ctx.fillStyle = '#2b1d14'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#f6e7c8'; ctx.font = '900 104px IDB, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('COFFEE', w / 2, h / 2 + 6); }).tex;
const cart = (() => { const g = new THREE.Group(), wood = std(0x8a5a34, { roughness: .55 }), metal = std(0x30343c, { metalness: .8, roughness: .35 });
  const body = new THREE.Mesh(new RoundedBoxGeometry(1.7, .95, .7, 4, .04), wood); body.position.y = .5; const top = new THREE.Mesh(new RoundedBoxGeometry(1.84, .07, .84, 3, .03), std(0xe9e2d6, { roughness: .3 })); top.position.y = 1.0;
  const sign = new THREE.Mesh(new THREE.PlaneGeometry(1.1, .34), new THREE.MeshStandardMaterial({ map: signTex, roughness: .6 })); sign.position.set(0, .55, -.356); sign.rotation.y = Math.PI;
  for (const s of [-1, 1]) { const pole = new THREE.Mesh(new THREE.CylinderGeometry(.025, .025, 1.5, 10), metal); pole.position.set(s * .86, 1.75, .3); g.add(pole); const wh = new THREE.Mesh(new THREE.CylinderGeometry(.2, .2, .08, 24), std(0x1d1f24)); wh.rotation.z = Math.PI / 2; wh.position.set(s * .9, .2, .1); g.add(wh); }
  const awn = new THREE.Mesh(new THREE.BoxGeometry(2.0, .04, 1.25), new THREE.MeshStandardMaterial({ map: awnTex, roughness: .8 })); awn.position.set(0, 2.5, -.05); awn.rotation.x = .2;
  const mach = new THREE.Mesh(new RoundedBoxGeometry(.5, .42, .38, 4, .05), std(0xc9ced6, { metalness: .9, roughness: .25 })); mach.position.set(.5, 1.25, .1);
  for (let i = 0; i < 3; i++) { const c = new THREE.Mesh(new THREE.CylinderGeometry(.05, .04, .12, 20), std(0xfafafa, { roughness: .3 })); c.position.set(-.62 + i * .15, 1.1, .12); g.add(c); }
  g.add(body, top, sign, awn, mach); shadows(g); scene.add(g); g.visible = false; return g; })();
const boxes = [0, 1, 2].map(() => { const b = new THREE.Mesh(new RoundedBoxGeometry(.5, .4, .42, 3, .02), std(0xc49a62, { roughness: .85 })); const tape = new THREE.Mesh(new THREE.BoxGeometry(.51, .02, .09), std(0xe8dcc0)); tape.position.y = .2; b.add(tape); shadows(b); scene.add(b); b.visible = false; return b; });
const COINS = (() => { const n = 46, m = new THREE.InstancedMesh(new THREE.CylinderGeometry(.09, .09, .022, 28), new THREE.MeshStandardMaterial({ color: 0xffc83a, metalness: 1, roughness: .22, emissive: 0x6b4a00, emissiveIntensity: .5 }), n); m.castShadow = true; m.frustumCulled = false; scene.add(m); m.visible = false; return m; })();
const dm = new THREE.Object3D();
function coins(t, cx, cz, on) { COINS.visible = on; if (!on) return; for (let k = 0; k < COINS.count; k++) { const life = (t * .42 + hash(k)) % 1; dm.position.set(cx + (hash(k * 3 + 1) - .5) * 5.6, 4.2 - life * 4.1, cz + (hash(k * 5 + 2) - .5) * 1.8); dm.rotation.set(t * 3 + k, k, t * 2 + k * 2); dm.scale.setScalar(life > .96 ? 0 : 1); dm.updateMatrix(); COINS.setMatrixAt(k, dm.matrix); } COINS.instanceMatrix.needsUpdate = true; }
const paintTex = canvasTex(512, 640, (ctx, w, h) => { ctx.fillStyle = '#f7f2e6'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#bfe3f2'; ctx.fillRect(30, 30, w - 60, h - 60);
  ctx.fillStyle = '#eef0f3'; ctx.strokeStyle = '#2a2e37'; ctx.lineWidth = 10; const rr = (x, y, a, b, r) => { ctx.beginPath(); ctx.roundRect(x, y, a, b, r); ctx.fill(); ctx.stroke(); };
  rr(150, 150, 212, 170, 60); rr(170, 350, 172, 190, 50); ctx.fillStyle = '#0b0d12'; rr(175, 195, 162, 70, 24); ctx.fillStyle = '#35d6ff'; ctx.beginPath(); ctx.ellipse(222, 230, 14, 22, 0, 0, 7); ctx.ellipse(290, 230, 14, 22, 0, 0, 7); ctx.fill();
  ctx.fillStyle = '#ff7aa8'; ctx.beginPath(); ctx.arc(256, 440, 22, 0, 7); ctx.fill(); }).tex;
const easel = (() => { const g = new THREE.Group(), wood = std(0x9a6a3e, { roughness: .55 });
  for (const [x, z, rz, rx] of [[-.32, 0, .13, -.12], [.32, 0, -.13, -.12], [0, -.45, 0, .3]]) { const l = new THREE.Mesh(new THREE.CylinderGeometry(.025, .025, 2.0, 8), wood); l.position.set(x, 1.0, z); l.rotation.set(rx, 0, rz); g.add(l); }
  const shelf = new THREE.Mesh(new THREE.BoxGeometry(.8, .04, .08), wood); shelf.position.set(0, .86, .1); g.add(shelf);
  const cv = new THREE.Mesh(new THREE.BoxGeometry(.76, .95, .03), [std(0xf7f2e6), std(0xf7f2e6), std(0xf7f2e6), std(0xf7f2e6), new THREE.MeshStandardMaterial({ map: paintTex, roughness: .8 }), std(0xf7f2e6)]); cv.position.set(0, 1.36, .12); cv.rotation.x = -.1; g.add(cv);
  shadows(g); scene.add(g); g.visible = false; return g; })();
const brush = (() => { const g = new THREE.Group(); const h = new THREE.Mesh(new THREE.CylinderGeometry(.014, .018, .34, 8), std(0x7a4a22)); const tip = new THREE.Mesh(new THREE.ConeGeometry(.03, .09, 10), std(0xff7aa8)); tip.position.y = .2; g.add(h, tip); g.visible = false; J.arms[0].add(g); g.position.set(0, -.78, .1); g.rotation.x = -1.2; return g; })();
const PROPS = [cart, easel, ...boxes, ...ARMS];

// ---------- timeline from the voiceover: one beat per narration line (line 0 is spoken over the intro) ----------
const T = LN.map(l => l.t0 - .12), total = VO.total;
const cap = i => LN[i].show;
const B = [
  { t: T[1], v: 3.5e9, label: 'PEOPLE WITH A JOB', capY: 1225, cap: cap(1), hi: ['3.5', 'billion'] },
  { t: T[2], v: 5e6, label: 'ROBOTS IN FACTORIES', capY: 1225, cap: cap(2), hi: ['5', 'million'] },
  { t: T[3], v: 1.2e9, label: 'JOBS TAKEN BY ROBOTS', capY: 1225, cap: cap(3), red: ['EVERY'], note: 'From here on: speculation', big: true },
  { t: T[4], v: 3.5e9, label: 'JOBS TAKEN BY ROBOTS', capY: 1225, cap: cap(4), hi: ['never', 'close.'], note: 'Speculation' },
  { t: T[5], v: 3.5e9, label: 'JOBS TAKEN BY ROBOTS', capY: 1225, cap: cap(5), red: ['No', 'paycheck...'], note: 'Speculation' },
  { t: T[6], v: 3.5e9, label: 'JOBS TAKEN BY ROBOTS', capY: 1225, cap: cap(6), hi: ['share?'], red: ['few', 'owners'], size: 58, note: 'Speculation: economists disagree' },
  { t: T[7], v: 3.5e9, label: 'JOBS TAKEN BY ROBOTS', capY: 1225, cap: cap(7), hi: ['6', 'in', '10'], size: 60, note: 'Fact: MIT study of US jobs, 1940 to 2018', big: true },
  { t: T[8], v: 3.5e9, label: 'JOBS TAKEN BY ROBOTS', capY: 1225, cap: cap(8), hi: ['new', 'ones.'], size: 60 },
  { t: T[9], v: 3.5e9, label: '', capY: 1225, cap: cap(9), hi: ['YOU'], size: 60 },
];
const fmt = v => v >= 1e9 ? (v / 1e9).toFixed(1) + ' billion' : v >= 1e6 ? Math.round(v / 1e6) + ' million' : Math.round(v).toLocaleString('en-US');

// ---------- helpers ----------
const JX = 23.4, JZ = 6.0;
function jer(x, z, ry, pose, cup = false) {
  J.visible = true; J.position.set(x, .18, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose);
  if (cup) { J.arms[1].rotation.x = -1.15; J.arms[1].add(W.cup); W.cup.position.set(-.02, -.74, .05); W.cup.rotation.set(1.15, 0, 0); W.cup.visible = true; }
}
function hideAll() {
  J.visible = false; J.arms[1].rotation.x = 0; J.arms[0].rotation.x = 0; if (W.cup.parent !== scene) scene.add(W.cup); W.cup.visible = false; W.splash.visible = false; W.sparkle.visible = false; J.hat.visible = false; brush.visible = false;
  CAST.forEach(p => { p.visible = false; p.hat.visible = false; p.arms[0].rotation.x = 0; p.arms[1].rotation.x = 0; });
  R.forEach(r => { r.visible = false; r.arms.forEach(a => a.rotation.x = 0); }); PROPS.forEach(p => p.visible = false); sparks(0, 0, false); sparks(1, 0, false); coins(0, 0, 0, false);
  noFocus(); RIM.k = .55; INK.on = true; GRADE.split = .08; GRADE.sat = 1.05; GRADE.gain = 1.1; if (parked) parked.visible = false;
}
const bob = (t, ph = 0, a = .012) => Math.sin(t * 7 + ph) * a, step = (t, ph = 0) => Math.abs(Math.sin(t * 6 + ph)) * .03;
const carry = (r, b) => { b.visible = true; r.arms[0].rotation.x = -1.25; r.arms[1].rotation.x = -1.25; r.updateMatrixWorld(true); b.position.copy(r.localToWorld(V(0, 1.18, .62))); b.rotation.y = r.rotation.y; };
const cartSet = () => { cart.visible = true; cart.position.set(25.1, .18, 7.0); cart.rotation.y = 0; };

run({
  total, ctaAt: T[9], sub: '',
  reel: ['(x)', 'ALL HUMANS VANISHED', 'A BLACK HOLE DOUBLED', 'WE COULD READ MINDS', 'ROME NEVER FELL', 'POPCORN DOUBLED', 'ROBOTS TOOK EVERY JOB?'],
  beats: B, label: (b) => b.label, fmt,
  beds: [{ t0: 0, t1: T[2] + .1, name: 'city', gain: .26 }, { t0: T[2], t1: T[3] + .1, name: 'drone', gain: .18 }, { t0: T[3], t1: T[4] + .1, name: 'city', gain: .22 }, { t0: T[4], t1: T[5] + .1, name: 'crickets', gain: .16 },
    { t0: T[5], t1: T[7] + .1, name: 'city', gain: .2 }, { t0: T[7], t1: T[8] + .1, name: 'wind', gain: .14 }, { t0: T[8], t1: total, name: 'birds', gain: .2 }],
  sfx: [{ t: T[2] + .3, name: 'hiss', gain: .28 }, { t: T[2] + 1.4, name: 'hiss', gain: .22 }, { t: T[3] + .1, name: 'swell', gain: .3 }, { t: T[3] + 1.6, name: 'ding', gain: .3 }, { t: T[4] + .2, name: 'power_down', gain: 0 },
    { t: T[5] + 1.2, name: 'pop', gain: .35 }, { t: T[6] + .3, name: 'chips', gain: .45 }, { t: T[6] + 1.6, name: 'chips', gain: .35 }, { t: T[7] + .05, name: 'sparkle_rev', gain: .45 }, { t: T[8] + .2, name: 'chime', gain: .3 }, { t: T[9] + .1, name: 'ding', gain: .3 }].filter(e => e.gain > 0),
  introShot(t) {
    mode('street'); hideAll(); setSky('day'); setAge(0, t, { lamps: 0 });
    jer(lerp(19.6, JX, eOut(clamp(t / 3.2))), JZ, Math.PI / 2 + .3 * clamp(t / 3), { expr: 'happy', bob: step(t) * (1 - clamp((t - 2.8) / .5)), armL: .25 }, true);
    put(P.mia, lerp(27.8, 25.0, t / 3.4), 7.1, -Math.PI / 2, { expr: 'happy', bob: step(t, 1) });
    dolly(V(22.2, 1.6, -.6), V(23.2, 1.55, .2), V(21.0, 1.9, 6.2), V(23.3, 1.95, 6.0), t / 3.3, 0, 52);
    focus(V(J.position.x, 1.2, JZ), .8, 10);
  },
  shot(t, b, lt, i, next) {
    mode('street'); hideAll(); const dur = (next ? next.t : total) - b.t, k = clamp(lt / dur);
    if (i === 0) { // everyone on the way to work
      setSky('day'); setAge(0, t, { lamps: 0 });
      const ppl = [[P.mia, 25.0, 7.1, -1], [P.ken, 21.6, 6.9, 1], [P.ava, 27.6, 6.1, -1], [P.pol, 20.4, 5.9, 1], [P.sam, 28.8, 7.2, -1]];
      ppl.forEach(([p, x, z, d], j) => put(p, x + d * lt * .75, z, d * Math.PI / 2, { expr: 'happy', bob: step(t, j * 1.3) }));
      jer(JX + lt * .35, 5.5, Math.PI / 2 + .9, { expr: 'happy', bob: step(t, 4), armL: .25 }, true);
      dolly(V(24.4, 2.0, -3.4), V(24.9, 1.95, -2.7), V(24.6, 1.63, 6.4), V(24.8, 1.63, 6.4), k, 0, 52);
    } else if (i === 1) { // factory robots: two arms welding the parked car
      setSky('day'); setAge(0, t, { lamps: 0 }); GRADE.split = .1; if (parked) parked.visible = true;
      ARMS.forEach((a, j) => { a.visible = true; a.position.set(24.9 + j * 2.3, .18, 5.05); const w = Math.sin(t * 1.7 + j * 2) * .12; a.set(Math.PI + (j ? -.18 : .2) + w * .5, .62 + w, 1.25 - w * .6, .5); a.updateMatrixWorld(true); sparks(j, t + j * .37, Math.sin(t * 2.2 + j * 2.4) > -.5); });
      jer(23.1, 5.5, Math.PI / 2 + .9, { expr: 'shocked', look: .3, bob: bob(t), armL: .2 }, true);
      dolly(V(25.2, 3.3, -6.2), V(25.7, 3.1, -5.4), V(25.6, 1.25, 4.4), V(25.8, 1.25, 4.4), k, 0, 50);
      focus(V(26, 1.5, 4.2), .6, 8);
    } else if (i === 2) { // robots take over: first the coffee cart, then deliveries
      setSky('day'); setAge(0, t, { lamps: 0 });
      if (lt < dur * .52) { cartSet(); const give = eOut(clamp((lt - .5) / .6));
        rput(R[0], 24.75, 7.62, Math.PI, { armR: -1.25 * give, look: .25, bob: bob(t, 1, .006) });
        jer(23.55, 6.25, face(23.55, 6.25, 24.6, 7.2), { expr: lt > .9 ? 'shocked' : 'happy', look: 0, bob: bob(t, 2), armL: .2 }, lt > 1.5);
        if (lt <= 1.5) { W.cup.visible = true; R[0].updateMatrixWorld(true); W.cup.position.copy(R[0].arms[1].localToWorld(V(0, -.8, .06))); W.cup.rotation.set(0, 0, 0); }
        dolly(V(24.0, 1.55, .5), V(24.1, 1.55, 1.2), V(24.3, 1.58, 6.8), V(24.3, 1.58, 6.8), clamp(lt / (dur * .52)), 0, 52); focus(V(24.3, 1.5, 6.9), .7, 10);
      } else { const u = lt - dur * .52;
        [[R[1], 20.8, 6.1], [R[2], 22.6, 7.2], [R[3], 18.9, 6.8]].forEach(([r, x, z], j) => { rput(r, x + u * 1.35, z, Math.PI / 2, { walk: 1, ph: t * 7 + j * 2 }); carry(r, boxes[j]); });
        jer(26.6, 5.4, Math.PI - .5, { expr: 'shocked', look: Math.sin(t * 2) * .4, bob: bob(t), armL: .2 }, true);
        dolly(V(24.6, 1.7, -2.4), V(25.0, 1.7, -1.8), V(24.4, 1.53, 6.4), V(24.8, 1.53, 6.4), clamp(u / (dur * .48)), 0, 52);
      }
    } else if (i === 3) { // night shift: nothing ever closes
      setSky('dusk', 'night', .4); setAge(0, t, { lamps: 1, lights: 1 }); GRADE.split = .13; cartSet();
      rput(R[0], 24.75, 7.62, Math.PI, { armR: -.9 + Math.sin(t * 3) * .15, look: Math.sin(t * .9) * .3 });
      [[R[1], 20.2, 6.0], [R[2], 28.6, 6.6]].forEach(([r, x, z], j) => { const d = j ? -1 : 1; rput(r, x + d * lt * 1.2, z, d * Math.PI / 2, { walk: 1, ph: t * 7 + j * 2 }); carry(r, boxes[j]); });
      dolly(V(26.2, 2.1, -1.8), V(25.7, 2.0, -1.2), V(24.6, 1.63, 6.8), V(24.7, 1.63, 6.8), k, 0, 52);
    } else if (i === 4) { // no paycheck: empty pockets
      setSky('day'); setAge(0, t, { lamps: 0 }); cartSet();
      rput(R[0], 24.75, 7.62, Math.PI, { armR: -1.25, look: .3, nod: Math.sin(t * 2) * .04 }); R[0].updateMatrixWorld(true); W.cup.visible = true; W.cup.position.copy(R[0].arms[1].localToWorld(V(0, -.8, .06))); W.cup.rotation.set(0, 0, 0);
      const sh = eOut(clamp((lt - .6) / .5));
      jer(23.5, 6.15, Math.PI - .25, { expr: lt > .6 ? 'worried' : 'confused', look: lt > 1.6 ? .5 : -.1, armL: .2 + sh * .95, armR: .2 + sh * .95, tilt: sh * .08, bob: bob(t) });
      dolly(V(23.9, 1.5, 1.3), V(23.9, 1.52, 1.9), V(24.1, 1.58, 6.6), V(24.1, 1.58, 6.6), k, 0, 52); focus(V(23.8, 1.5, 6.4), .7, 10);
    } else if (i === 5) { // a share for everyone? (coins rain down)
      setSky('golden'); setAge(0, t, { lamps: 0 }); coins(t, 24.6, 6.4, true);
      [[P.mia, 22.3, 6.7], [P.sam, 26.7, 6.9], [P.ava, 27.9, 6.0], [P.ken, 21.1, 6.0]].forEach(([p, x, z], j) => put(p, x, z, Math.PI + (24.6 - x) * .08, { expr: 'happy', armL: 1.9 + Math.sin(t * 5 + j) * .25, armR: 1.9 + Math.cos(t * 5 + j) * .25, bob: step(t * .8, j) }));
      jer(24.5, 5.7, Math.PI, { expr: 'happy', armL: 2.1 + Math.sin(t * 6) * .2, armR: 2.1 + Math.cos(t * 6) * .2, bob: step(t * .8, 3) });
      dolly(V(24.6, 1.5, -1.6), V(24.6, 1.6, -.9), V(24.6, 1.83, 6.4), V(24.6, 1.88, 6.4), k, 0, 54);
    } else if (i === 6) { // 1940: a street of jobs that no longer exist (sepia)
      setSky('day'); setAge(0, t, { lamps: 0 }); GRADE.sat = .1; GRADE.split = .32; GRADE.gain = 1.5;
      [[P.pol, 21.4, 6.2, 1], [P.ken, 27.9, 7.0, -1], [P.sam, 19.8, 7.1, 1]].forEach(([p, x, z, d], j) => { put(p, x + d * lt * .6, z, d * Math.PI / 2, { expr: 'happy', bob: step(t * .9, j) }); p.hat.visible = true; });
      jer(24.2, 5.8, Math.PI - .1, { expr: lt > 1.4 ? 'confused' : 'happy', look: Math.sin(t * 1.2) * .5, bob: bob(t) }); J.hat.visible = true;
      dolly(V(24.3, 1.6, -.9), V(24.3, 1.6, -.2), V(24.3, 1.63, 6.2), V(24.3, 1.63, 6.2), k, 0, 52); focus(V(24.2, 1.5, 5.9), .6, 8);
    } else if (i === 7) { // new jobs: Jeremy the artist paints a robot's portrait
      setSky('day'); setAge(0, t, { lamps: 0 });
      easel.visible = true; easel.position.set(24.6, .18, 6.8); easel.rotation.y = Math.PI + .45;
      jer(23.75, 6.25, face(23.75, 6.25, 24.6, 6.8) + .2, { expr: 'happy', look: Math.sin(t * 1.5) > .3 ? .6 : 0, bob: bob(t), armR: .2 }); J.arms[0].rotation.x = -1.2 + Math.sin(t * 5) * .14; brush.visible = true;
      rput(R[0], 25.65, 6.35, Math.PI + .35, { armL: -2.6, look: -.25, bob: bob(t, 1, .005) });
      dolly(V(24.7, 1.55, .5), V(24.7, 1.55, 1.1), V(24.75, 1.53, 6.5), V(24.75, 1.53, 6.5), k, 0, 52); focus(V(24.6, 1.5, 6.5), .7, 10);
    } else { // CTA
      setSky('golden'); setAge(0, t, { lamps: 0 });
      jer(JX + .4, JZ, Math.PI - .1, { expr: 'happy', armL: .3 + Math.abs(Math.sin(t * 5)) * 2.3, bob: bob(t) });
      rput(R[0], JX + 1.75, JZ + .3, Math.PI + .12, { armR: 0, look: -.2, bob: bob(t, 1, .005) }); R[0].arms[0].rotation.z = -2.3 + Math.sin(t * 5 + 1) * .35;
      dolly(V(JX + 1.2, 1.5, JZ - 4.6), V(JX + 1.3, 1.6, JZ - 5.2), V(JX + 1.05, 1.38, JZ), V(JX + 1.05, 1.38, JZ), eInOut(k), 0, 50); focus(V(JX + 1, 1.4, JZ), .8, 10);
    }
    R.forEach(r => { if (i !== 8) { r.arms[0].rotation.z = -.1; r.arms[1].rotation.z = .1; } });
    const sm = document.getElementById('small'); sm.style.top = '1378px'; sm.style.fontSize = '36px'; sm.style.fontFamily = 'IDB'; sm.style.color = '#ffe08a'; sm.style.webkitTextStroke = '5px #0a0b18'; sm.style.paintOrder = 'stroke fill'; sm.style.left = '60px'; sm.style.right = '150px';
    sm.textContent = b.note || ''; sm.style.opacity = b.note ? clamp((lt - .3) / .3) : 0;
    if (b.big && lt < .35) shake(.05 * (1 - lt / .35), t);
  },
});
