// Episode 18 — What if the Moon disappeared?  (v5.1 premium studio look + AI voiceover; one continuous gallery shot, structure copied from ep13)
// Everything is timed to the narration (vo.json written by tools/narrate.py from vo_lines.json).
// Facts (checked 2026-11-14):
//  - the Sun's tide-raising effect is ~44-46% of the Moon's (HyperPhysics "Tides": "44% of that of the Moon") -> without the Moon only the solar
//    tide is left: 0.44 / 1.44 ≈ 0.31 of today's spring-tide range ("about a third")  https://www.hyperphysics.gsu.edu/hbase/tide.html
//  - full Moon on a clear night ≈ 0.25 lux; clear moonless night incl. airglow ≈ 0.002 lux -> >100x (Wikipedia "Orders of magnitude (illuminance)")
//  - many reef corals time their mass spawning to the lunar cycle / moonlight (Great Barrier Reef spawns a few nights after the November full moon)
//  - Earth's tilt today varies ~22.1°-24.5° over a 41,000-year cycle; the Moon helps keep it stable. Without the Moon: early models (Laskar 1993)
//    0-85°; Lissauer et al. (AGU / Icarus 2012) simulations stayed between ~10° and ~40° over 100 million years (Space.com 24517) -> SPECULATION/model
//  - the Moon recedes ~3.8 cm per year, measured by laser ranging to Apollo retroreflectors; NASA: "roughly the rate at which fingernails grow" (Live Science)
import { THREE, RoundedBoxGeometry, scene, camera, clamp, lerp, eOut, eInOut, K, rimLight } from './kit.js';
import { key, hemi, DOF, draw, renderer, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd } from './studio.js';
import { makeJeremy2 } from './jeremy2.js';

await bootStudio('WHAT IF THE MOON DISAPPEARED?', 'EP. 18');
const VO = await (await fetch('./vo.json')).json(), LN = VO.lines, total = VO.total;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const $ = id => document.getElementById(id);
floorScale(2);

// ---------------------------------------------------------------- materials
const marbleTex = canvasTex(512, 512, (ctx, w, h) => { const r = rand(8); ctx.fillStyle = '#e9e6e0'; ctx.fillRect(0, 0, w, h);
  for (let i = 0; i < 26; i++) { ctx.strokeStyle = `rgba(120,116,112,${.05 + r() * .12})`; ctx.lineWidth = .6 + r() * 2.2; ctx.beginPath(); let x = r() * w, y = r() * h; ctx.moveTo(x, y); for (let k = 0; k < 9; k++) { x += (r() - .5) * 120; y += (r() - .3) * 90; ctx.lineTo(x, y); } ctx.stroke(); } }).tex;
const marble = new THREE.MeshPhysicalMaterial({ map: marbleTex, roughness: .28, clearcoat: .5, clearcoatRoughness: .3 });
const brass = new THREE.MeshStandardMaterial({ color: 0xb8894a, metalness: 1, roughness: .3 });
const darkIron = new THREE.MeshStandardMaterial({ color: 0x2a2b30, metalness: .85, roughness: .38 });
const glass = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .05, metalness: 0, transparent: true, opacity: .14, clearcoat: 1, depthWrite: false, side: THREE.DoubleSide });
const accentM = new THREE.MeshBasicMaterial({ color: ACCENT, toneMapped: false });
const shadowAll = g => { g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };
function plinth(w, d, h) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, .03), marble); m.position.y = h / 2; m.castShadow = m.receiveShadow = true; return m; }
const X = { orr: 0, tide: 7, reef: 14, tilt: 21, laser: 28 };
const TL = new THREE.TextureLoader();
const earthImg = await TL.loadAsync('./assets/planets/earth_atmos_2048.jpg'); earthImg.colorSpace = THREE.SRGBColorSpace; earthImg.anisotropy = 8;
const earthN = await TL.loadAsync('./assets/planets/earth_normal_2048.jpg');
const moonImg = await TL.loadAsync('./assets/planets/moon_1024.jpg'); moonImg.colorSpace = THREE.SRGBColorSpace; moonImg.anisotropy = 8;
const earthMat = new THREE.MeshStandardMaterial({ map: earthImg, normalMap: earthN, roughness: .55, emissive: 0xffffff, emissiveMap: earthImg, emissiveIntensity: .5 });
const moonMat = () => new THREE.MeshStandardMaterial({ map: moonImg, bumpMap: moonImg, bumpScale: 1.5, roughness: 1, transparent: true });
const earth = r => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), earthMat); m.castShadow = true; return m; };

// ---------------------------------------------------------------- A. brass orrery: Earth + Moon (the Moon vanishes in line 0)
const orr = new THREE.Group(), orrMoon = new THREE.Group(); let moonA;
{ const base = plinth(2.4, 2.4, .55); const disc = new THREE.Mesh(new THREE.CylinderGeometry(.5, .58, .08, 64), brass); disc.position.y = .59;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.03, .045, .9, 24), brass); post.position.y = 1.08;
  const E = earth(.5); E.position.y = 2.03; E.rotation.z = .41; E.name = 'earthA';
  const ringM = new THREE.Mesh(new THREE.TorusGeometry(1.25, .008, 8, 160), brass); ringM.rotation.x = Math.PI / 2; ringM.position.y = 1.55;
  const arm = new THREE.Mesh(new THREE.CylinderGeometry(.014, .014, 1.25, 12), brass); arm.rotation.z = Math.PI / 2; arm.position.set(.625, 1.55, 0);
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, .08, 24), brass); hub.position.y = 1.55;
  const stalk = new THREE.Mesh(new THREE.CylinderGeometry(.01, .01, .25, 12), brass); stalk.position.set(1.25, 1.67, 0);
  moonA = new THREE.Mesh(new THREE.SphereGeometry(.15, 64, 48), moonMat()); moonA.position.set(1.25, 1.88, 0); moonA.castShadow = true;
  orrMoon.add(arm, stalk, moonA); orrMoon.position.y = 0; orr.add(base, disc, post, E, ringM, hub, orrMoon);
  orr.position.x = X.orr; scene.add(shadowAll(orr)); }
// soft glow sprite for the vanish
const glowTex = canvasTex(128, 128, (ctx, w, h) => { const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); g.addColorStop(0, 'rgba(255,240,220,.9)'); g.addColorStop(.4, 'rgba(255,220,190,.3)'); g.addColorStop(1, 'rgba(255,220,190,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex;
const vanishGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, transparent: true, depthWrite: false, opacity: 0, toneMapped: false })); scene.add(vanishGlow);

// ---------------------------------------------------------------- B. tide tank: a beach cross-section in glass, water level rises and falls
const TW = 2.6, TD = 1.0, TH = 1.0, TB = .5; let water, waterSide;
{ const g = new THREE.Group(); g.add(plinth(2.9, 1.3, TB));
  const sandTex = canvasTex(512, 512, (ctx, w, h) => { const r = rand(12); ctx.fillStyle = '#d8c39b'; ctx.fillRect(0, 0, w, h); for (let i = 0; i < 6000; i++) { const v = r() * 40 - 20; ctx.fillStyle = `rgba(${170 + v},${150 + v},${110 + v},.35)`; ctx.fillRect(r() * w, r() * h, 2, 2); } }).tex;
  // sand: a wedge (beach) from the left (deep) to the right (dry), with gentle ripples
  const sg = new THREE.PlaneGeometry(TW - .04, TD - .04, 120, 40), sp = sg.attributes.position;
  for (let i = 0; i < sp.count; i++) { const x = sp.getX(i), y = sp.getY(i); const u = (x + TW / 2) / TW; sp.setZ(i, .1 + .62 * Math.pow(u, 1.4) + .012 * Math.sin(x * 22 + y * 3)); }
  sg.computeVertexNormals(); const sand = new THREE.Mesh(sg, new THREE.MeshStandardMaterial({ map: sandTex, roughness: 1 })); sand.rotation.x = -Math.PI / 2; sand.position.y = TB; g.add(sand);
  // sand body (front cut face, so the wedge reads as solid)
  const shp = new THREE.Shape(); shp.moveTo(-TW / 2 + .02, 0); for (let k = 0; k <= 40; k++) { const u = k / 40, x = -TW / 2 + .02 + u * (TW - .04); shp.lineTo(x, .1 + .62 * Math.pow((x + TW / 2) / TW, 1.4)); } shp.lineTo(TW / 2 - .02, 0); shp.closePath();
  const body = new THREE.Mesh(new THREE.ExtrudeGeometry(shp, { depth: TD - .04, bevelEnabled: false }), new THREE.MeshStandardMaterial({ map: sandTex, roughness: 1, color: 0xc9b38a })); body.position.set(0, TB, -(TD - .04) / 2); g.add(body);
  // pebbles
  const r = rand(4); for (let i = 0; i < 16; i++) { const u = .35 + r() * .6, x = -TW / 2 + u * TW, z = (r() - .5) * .8; const p = new THREE.Mesh(new THREE.SphereGeometry(.03 + r() * .03, 16, 12), new THREE.MeshStandardMaterial({ color: new THREE.Color().setHSL(.08, .1, .35 + r() * .3), roughness: .7 })); p.scale.y = .55; p.position.set(x, TB + .1 + .62 * Math.pow(u, 1.4) + .01, z); g.add(p); }
  // water: a box whose height we animate (top face shiny)
  water = new THREE.Mesh(new THREE.BoxGeometry(TW - .05, 1, TD - .05), new THREE.MeshPhysicalMaterial({ color: 0x2c8fb3, roughness: .06, metalness: 0, clearcoat: 1, transparent: true, opacity: .62, depthWrite: false }));
  water.position.set(0, TB, 0); g.add(water);
  // glass walls + brass frame
  const gl = new THREE.Mesh(new THREE.BoxGeometry(TW, TH, TD), glass); gl.position.y = TB + TH / 2; g.add(gl);
  for (const [x, z] of [[-1, -1], [-1, 1], [1, -1], [1, 1]]) { const c = new THREE.Mesh(new THREE.BoxGeometry(.03, TH, .03), brass); c.position.set(x * TW / 2, TB + TH / 2, z * TD / 2); g.add(c); }
  for (const y of [TB, TB + TH]) for (const z of [-1, 1]) { const b = new THREE.Mesh(new THREE.BoxGeometry(TW, .03, .03), brass); b.position.set(0, y, z * TD / 2); g.add(b); }
  for (const y of [TB, TB + TH]) for (const x of [-1, 1]) { const b = new THREE.Mesh(new THREE.BoxGeometry(.03, .03, TD), brass); b.position.set(x * TW / 2, y, 0); g.add(b); }
  // tide staff (gauge) with marks on the back wall
  const st = canvasTex(64, 512, (ctx, w, h) => { ctx.fillStyle = '#f4f1ea'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#1e1e22'; for (let i = 0; i < 20; i++) ctx.fillRect(0, i * 25.6, i % 2 ? 22 : 44, 4); ctx.fillStyle = ACCENT; ctx.fillRect(w - 10, 0, 10, h); }).tex;
  const staff = new THREE.Mesh(new THREE.BoxGeometry(.08, .9, .02), new THREE.MeshStandardMaterial({ map: st, roughness: .5 })); staff.position.set(-.55, TB + .48, -TD / 2 + .06); g.add(staff);
  g.position.x = X.tide; scene.add(shadowAll(g)); water.castShadow = false; gl.castShadow = false; }
const tideLevel = (k) => TB + .1 + .38 + k * .2; // k in [-1, 1]

// ---------------------------------------------------------------- C. night reef tank with a moon lamp
let lamp, lampLight, reefWater; const eggs = [];
{ const g = new THREE.Group(); g.add(plinth(2.2, 1.3, .55));
  const tank = new THREE.Mesh(new THREE.BoxGeometry(1.9, .85, 1.0), glass); tank.position.y = .55 + .425; g.add(tank);
  reefWater = new THREE.Mesh(new THREE.BoxGeometry(1.86, .74, .96), new THREE.MeshPhysicalMaterial({ color: 0x14506e, roughness: .1, transparent: true, opacity: .45, depthWrite: false })); reefWater.position.y = .55 + .37; g.add(reefWater);
  const bed = new THREE.Mesh(new RoundedBoxGeometry(1.86, .08, .96, 2, .02), new THREE.MeshStandardMaterial({ color: 0xcdbb98, roughness: 1 })); bed.position.y = .59; g.add(bed);
  // branching corals (smooth tubes) + brain corals
  const r = rand(21), cols = [0xe07a5f, 0xf2a65a, 0xd96c9b, 0xf4d06f, 0x9c89b8];
  const branch = (p, dir, len, rad, depth, mat) => { const end = p.clone().addScaledVector(dir, len); const c = new THREE.Mesh(new THREE.TubeGeometry(new THREE.LineCurve3(p, end), 1, rad, 10), mat); g.add(c);
    const tip = new THREE.Mesh(new THREE.SphereGeometry(rad, 12, 10), mat); tip.position.copy(end); g.add(tip);
    if (depth > 0) for (let k = 0; k < 2; k++) { const d2 = dir.clone().add(V((r() - .5) * .9, .35, (r() - .5) * .9)).normalize(); branch(end, d2, len * .72, rad * .78, depth - 1, mat); } };
  for (let n = 0; n < 13; n++) { const mat = new THREE.MeshStandardMaterial({ color: cols[n % 5], roughness: .6 }); branch(V(-.78 + n * .13, .63, (r() - .5) * .6), V((r() - .5) * .3, 1, (r() - .5) * .3).normalize(), .16, .024, 3, mat); }
  for (let n = 0; n < 4; n++) { const b = new THREE.Mesh(new THREE.SphereGeometry(.09 + r() * .05, 32, 20, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xb5835a, roughness: .8 })); b.position.set(-.7 + r() * 1.4, .62, -.3 + r() * .6); g.add(b); }
  // moon lamp on a brass arm
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(.018, .022, 1.35, 16), brass); pole.position.set(.95, .55 + .675, -.4);
  const armL = new THREE.Mesh(new THREE.CylinderGeometry(.014, .014, .9, 12), brass); armL.rotation.z = Math.PI / 2; armL.position.set(.5, 1.9, -.4);
  lamp = new THREE.Mesh(new THREE.SphereGeometry(.16, 64, 48), new THREE.MeshStandardMaterial({ map: moonImg, emissive: 0xffffff, emissiveMap: moonImg, emissiveIntensity: 1.2, roughness: 1 })); lamp.position.set(.05, 1.9, -.4);
  lampLight = new THREE.PointLight(0xdfe8ff, 2.5, 4, 1.6); lampLight.position.copy(lamp.position).add(V(0, -.2, .1)); g.add(pole, armL, lamp, lampLight);
  // spawning egg bundles (small pink beads)
  for (let i = 0; i < 46; i++) { const e = new THREE.Mesh(new THREE.SphereGeometry(.011, 10, 8), new THREE.MeshStandardMaterial({ color: 0xff9eb5, emissive: 0xff7f9f, emissiveIntensity: .35, roughness: .4, transparent: true })); e.userData = { x: -.8 + r() * 1.6, z: -.35 + r() * .7, s: r(), v: .5 + r() * .5 }; g.add(e); eggs.push(e); }
  g.position.x = X.reef; scene.add(shadowAll(g)); tank.castShadow = reefWater.castShadow = false; lamp.castShadow = false; eggs.forEach(e => e.castShadow = false); }

// ---------------------------------------------------------------- D. tilt globe: Earth on a gimbal, axis rod + orange tilt arc
const tiltG = new THREE.Group(), tiltEarth = new THREE.Group(); const TGY = 1.75, TR = .7; let arc;
{ const base = plinth(2.0, 2.0, .55); const disc = new THREE.Mesh(new THREE.CylinderGeometry(.42, .5, .07, 64), darkIron); disc.position.y = .585;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, TGY - TR - .62, 20), brass); post.position.y = .62 + (TGY - TR - .62) / 2;
  const E = earth(TR); const axis = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, TR * 2 + .5, 12), brass);
  const caps = [-1, 1].map(s => { const c = new THREE.Mesh(new THREE.SphereGeometry(.025, 16, 12), brass); c.position.y = s * (TR + .25); return c; });
  tiltEarth.add(E, axis, ...caps); tiltEarth.position.y = TGY;
  const ring = new THREE.Mesh(new THREE.TorusGeometry(TR + .1, .018, 12, 128), brass); ring.position.y = TGY; ring.rotation.y = Math.PI / 2; // meridian ring in the YZ plane... we tilt in the XY plane, so ring faces camera side
  ring.rotation.set(0, 0, 0);
  const vert = new THREE.Mesh(new THREE.CylinderGeometry(.006, .006, TR * 2 + .7, 8), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: .4, transparent: true, opacity: .7 })); vert.position.y = TGY;
  tiltG.add(base, disc, post, tiltEarth, ring, vert); tiltG.position.x = X.tilt; scene.add(shadowAll(tiltG)); vert.castShadow = false; }
const arcMesh = new THREE.Mesh(new THREE.BufferGeometry(), accentM); arcMesh.position.set(X.tilt, TGY, .02); scene.add(arcMesh);
function setArc(deg) { const a = THREE.MathUtils.degToRad(deg), R = TR + .32, pts = []; for (let k = 0; k <= 24; k++) { const u = k / 24 * a; pts.push(V(Math.sin(u) * R, Math.cos(u) * R, 0)); }
  arcMesh.geometry.dispose(); arcMesh.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 48, .022, 8); }

// ---------------------------------------------------------------- E. Earth -> Moon laser ranging with a measuring tape (the twist: it is already leaving)
const lasG = new THREE.Group(); let lasMoon, beam, tape; const LMY = 1.35;
{ const base = plinth(3.6, 1.2, .55); lasG.add(base);
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.025, .035, .45, 16), brass); post.position.set(-1.25, .78, 0);
  const E = earth(.38); E.position.set(-1.25, LMY, 0); E.rotation.z = .41; E.name = 'earthE';
  const rail = new THREE.Mesh(new THREE.CylinderGeometry(.01, .01, 2.6, 12), brass); rail.rotation.z = Math.PI / 2; rail.position.set(.15, .9, 0);
  for (const x of [-1.0, 1.4]) { const s = new THREE.Mesh(new THREE.CylinderGeometry(.012, .016, .35, 12), brass); s.position.set(x, .72, 0); lasG.add(s); }
  lasMoon = new THREE.Group(); const m = new THREE.Mesh(new THREE.SphereGeometry(.15, 64, 48), moonMat()); m.position.y = LMY; m.castShadow = true;
  const ms = new THREE.Mesh(new THREE.CylinderGeometry(.008, .008, LMY - .9, 10), brass); ms.position.y = .9 + (LMY - .9) / 2; lasMoon.add(m, ms); lasMoon.position.x = .9;
  // tape measure: yellow ribbon with ticks along the top of the plinth
  const tt = canvasTex(1024, 64, (ctx, w, h) => { ctx.fillStyle = '#f2c94c'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#222'; for (let i = 0; i <= 100; i++) ctx.fillRect(i * 10.2, 0, 2, i % 10 ? 18 : 34); ctx.font = '700 22px Arial'; for (let i = 0; i <= 10; i++) ctx.fillText(String(i * 10), i * 102 + 4, 58); }).tex;
  tape = new THREE.Mesh(new THREE.PlaneGeometry(2.4, .12), new THREE.MeshStandardMaterial({ map: tt, roughness: .5 })); tape.rotation.x = -Math.PI / 2; tape.position.set(.15, .556, .38);
  lasG.add(post, E, rail, lasMoon, tape); lasG.position.x = X.laser; scene.add(shadowAll(lasG)); tape.castShadow = false; }
beam = new THREE.Mesh(new THREE.CylinderGeometry(.006, .006, 1, 8), new THREE.MeshBasicMaterial({ color: 0xff3b2f, toneMapped: false, transparent: true })); beam.rotation.z = Math.PI / 2; scene.add(beam);

// ---------------------------------------------------------------- Jeremys (scale .75 ≈ 1.75 m label)
const J1 = K.J, J2 = makeJeremy2(), J3 = makeJeremy2(), J4 = makeJeremy2(); [J2, J3, J4].forEach(j => { scene.add(j); rimLight(j); });
const putJ = (J, x, z, ry, pose) => { J.visible = true; J.position.set(x, 0, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose); };

// ---------------------------------------------------------------- timeline (from the voiceover)
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), endAt = T0[10] + 1.2;
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const CAM = [ // one per narration line: [target x, y, dist, yaw, pitch]
  [X.orr + .3, 1.25, 10.8, -.5, .2], [X.tide + .2, .95, 11.2, -.4, .2], [X.tide + .2, .95, 10.4, -.34, .2], [X.reef, 1.05, 9.6, -.45, .18], [X.reef, 1.0, 8.8, -.4, .16],
  [X.tilt + .3, 1.5, 10.6, -.4, .12], [X.tilt + .3, 1.5, 10.0, -.34, .12], [X.tilt + .3, 1.5, 10.8, -.42, .14], [X.laser + .2, 1.0, 12.6, -.36, .16], [X.laser + .3, 1.0, 11.8, -.3, .16], [X.laser + .2, 1.0, 13.4, -.38, .18]];
function camAt(t) { let c = CAM[0].slice(); for (let i = 1; i < CAM.length; i++) { const k = eInOut(clamp((t - (T0[i] - .8)) / 1.3)); if (k <= 0) break; c = c.map((v, j) => lerp(v, CAM[i][j], k)); } return c; }
const HUDS = [ // [time label, FACT/SPECULATION, stat label, value]
  ['Tonight', 'FACT', 'THE MOON', ''], ['Day 1', 'FACT', "SUN'S TIDAL PULL", "44% of the Moon's"], ['Day 1', 'FACT', 'TIDE SIZE', ''], ['Night 1', 'FACT', 'NIGHT LIGHT', ''],
  ['Night 1', 'FACT', 'CORAL SPAWNING', 'No moon clock'], ['Today', 'FACT', "EARTH'S TILT", ''], ['Millions of years', 'SPECULATION', "EARTH'S TILT", ''], ['Millions of years', 'SPECULATION', 'SEASONS', 'Extreme'],
  ['Real life', 'FACT', 'THE MOON', 'Already leaving'], ['Real life', 'FACT', 'DRIFTING AWAY', '3.8 cm / year'], ['Real life', 'FACT', 'DRIFTING AWAY', '3.8 cm / year']];
window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: total, name: 'room', gain: .1 }, { t0: T0[1], t1: T1[2] + .3, name: 'drip', gain: .12 }, { t0: T0[3], t1: T1[4] + .3, name: 'crickets', gain: .12 }],
  sfx: [{ t: 1.25, name: 'swell', gain: .32 }, ...[1, 3, 5, 8].map(i => ({ t: T0[i] - .85, name: 'glide', gain: .28 })), { t: T0[2] + .3, name: 'swell', gain: .22 },
    { t: T0[3] + 1.0, name: 'swell', gain: .2 }, { t: T0[6], name: 'chime', gain: .26 }, { t: T0[7] + .3, name: 'rumble_low', gain: .4 }, { t: T0[8] + .2, name: 'chime', gain: .28 }, { t: endAt, name: 'chime', gain: .3 }] };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';
const wp = new THREE.Vector3();

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), lt = t - T0[i], ld = T1[i] - T0[i];
  // ---- A. orrery: the Moon circles, then fades away with a soft glow (line 0)
  orr.getObjectByName('earthA').rotation.y = 1.7 + t * .05;
  orrMoon.rotation.y = -1.45 + t * .3; const vk = clamp((t - 1.0) / .55); moonA.material.opacity = 1 - eInOut(vk); moonA.scale.setScalar(1 - .6 * eInOut(vk)); moonA.visible = vk < 1;
  orrMoon.children.forEach(o => { if (o !== moonA) o.visible = true; });
  moonA.getWorldPosition(wp); vanishGlow.position.copy(wp); vanishGlow.scale.setScalar(.25 + .6 * vk); vanishGlow.material.opacity = Math.sin(Math.PI * vk) * .8;
  // ---- B. tide: oscillating level, amplitude shrinks to 0.31 in line 2
  const amp = i < 2 ? 1 : i === 2 ? lerp(1, .31, eInOut(clamp((lt - .2) / 1.8))) : .31;
  const lvl = tideLevel(amp * Math.sin((t - T0[1]) * 1.9 + Math.PI / 2)); water.scale.y = lvl - TB; water.position.y = TB + (lvl - TB) / 2;
  // ---- C. night: moon lamp dims (line 3), egg bundles rise while the lamp is on, then drift aimlessly
  const lampK = 1 - eInOut(clamp((t - (T0[3] + 1.2)) / 2.2)); lamp.material.emissiveIntensity = .05 + 1.15 * lampK; lamp.material.color.setScalar(.35 + .65 * lampK); lampLight.intensity = 2.5 * lampK;
  eggs.forEach((e, n) => { const u = e.userData, k = ((t * .08 * u.v + u.s) % 1); e.position.set(u.x + Math.sin(t * .7 + n) * .03, .66 + k * .62, u.z); const show = clamp((t - (T0[3] - 2)) / 1) * (i <= 4 ? 1 : 0);
    e.material.opacity = show * Math.sin(Math.PI * k) * (i === 4 ? lerp(1, .15, clamp(lt / ld)) : 1); e.visible = e.material.opacity > .01; });
  // ---- D. tilt: 23.4° wobbling 22.1-24.5 (exaggerated speed), then the speculative 10-40° swing
  let tilt; if (i < 6) tilt = 23.3 + 1.2 * Math.sin((t - T0[5]) * 1.6); else { const w = eInOut(clamp((t - T0[6] - .3) / 2.5)); tilt = lerp(23.3 + 1.2 * Math.sin((t - T0[5]) * 1.6), 25 + 15 * Math.sin((t - T0[6]) * 1.1 - .3), w); }
  tilt = clamp(tilt, 10, 40); tiltEarth.rotation.set(0, 0, -THREE.MathUtils.degToRad(tilt)); tiltEarth.children[0].rotation.y = 2.9 + t * .05; setArc(tilt);
  // ---- E. laser + Moon slowly sliding away along the rail
  const mx = .9 + (i >= 8 ? eInOut(clamp((t - T0[8] - .4) / 6)) * .4 : 0); lasMoon.position.x = mx; lasG.getObjectByName('earthE').rotation.y = -.3 + t * .05;
  const bx0 = X.laser - 1.25 + .38, bx1 = X.laser + mx - .15, bOn = i >= 8 ? clamp((t - T0[8] - .8) / .3) : 0; beam.position.set((bx0 + bx1) / 2, LMY, 0); beam.scale.set(1, Math.max(.001, (bx1 - bx0) * bOn), 1); beam.position.x = bx0 + (bx1 - bx0) * bOn / 2; beam.visible = bOn > 0; beam.material.opacity = .65 + .35 * Math.sin(t * 20) ** 2;
  // ---- Jeremys
  const bl = p => (t % p) < .1;
  putJ(J1, X.orr + 2.0, -1.0, -.75, { expr: t > 1.4 ? 'shocked' : 'happy', look: -.3, armL: t > 1.4 ? 2.1 : .25, armR: t > 1.4 ? 2.1 : .25, blink: bl(2.7) });
  putJ(J2, X.tide + .95, -1.35, -.45, { expr: i === 2 ? 'worried' : 'happy', look: -.5, armL: .25, armR: i === 1 ? 1.1 : .25, blink: bl(3.1) });
  putJ(J3, X.tilt + 1.3, -1.25, -.6, { expr: i >= 7 ? 'worried' : i === 6 ? 'shocked' : 'happy', look: -.55, armL: .25, armR: i === 5 ? 1.2 : .25, blink: bl(2.5) });
  putJ(J4, X.laser - .3, -1.3, -.35, { expr: i >= 10 ? 'confused' : 'happy', look: -.55, armL: .25, armR: i === 9 ? 2.0 + Math.sin(t * 3) * .1 : i >= 10 ? 1.3 : .25, tilt: i >= 10 ? .1 : 0, blink: bl(2.3) });
  // ---- light mood: dimmer, cooler "night" while at the reef (lines 3-4)
  const mk = eInOut(clamp((t - (T0[3] - .6)) / 1)) * (1 - eInOut(clamp((t - (T0[5] - .7)) / 1)));
  const nightK = mk * (1 - .55 * lampK * 0) * lerp(.55, 1, 1 - lampK);
  renderer.toneMappingExposure = lerp(.4, .36, mk); key.intensity = lerp(1.7, 1.0, nightK); key.color.set(mk > .01 ? new THREE.Color('#fff3e6').lerp(new THREE.Color('#c9d6ff'), nightK) : new THREE.Color('#fff3e6'));
  hemi.intensity = lerp(.4, .16, nightK); scene.environmentIntensity = lerp(.32, .12, nightK);
  // ---- camera: one continuous glide along the gallery
  const c = camAt(t), drift = clamp(lt / Math.max(ld, 1));
  const tgt = V(c[0], c[1], 0), dist = c[2] * (1 - .035 * drift);
  orbit(tgt, dist, { yaw: c[3] + .04 * drift + t * .002, pitch: c[4], fov: 34, lookUp: .075 });
  shadowFit(tgt, 4.2); DOF.on = true; DOF.focus = dist; DOF.aperture = .55; DOF.maxR = 9;
  // ---- callout tags (orbit() first)
  const A = (t0, t1) => clamp((t - t0) / .35) * clamp((t1 - t) / .3);
  if (i === 0) tag3('JEREMY', '1.75 m', V(X.orr + 2.0, 2.3, -1.0), A(.5, T0[1] - .7));
  if (i === 1) { tag3('HIGH TIDE', 'pulled up by the Moon', V(X.tide - .5, 1.3, .5), A(T0[1] + .8, T0[2] + .2)); }
  if (i === 2) tag3('SUN ONLY', 'about 1/3 of today\'s tides', V(X.tide - .5, 1.3, .5), A(T0[2] + 1.0, T0[3] - .5));
  if (i === 3) tag3(lampK > .5 ? 'FULL MOON' : 'NO MOON', lampK > .5 ? '0.25 lux' : '0.002 lux', V(X.reef - .75, 1.5, .4), A(T0[3] + .4, T0[4] - .4));
  if (i === 4) tag3('CORAL SPAWNING', 'timed by moonlight', V(X.reef - .3, 1.45, 0), A(T0[4] + .4, T0[5] - .7));
  if (i === 5) tag3('TODAY', '22.1° – 24.5°', V(X.tilt - .9, 2.5, 0), A(T0[5] + 1.2, T0[6] + .2));
  if (i === 6 || i === 7) tag3('SPECULATION', i === 6 ? 'models: about 10° – 40°' : 'harsher summers and winters', V(X.tilt - .9, 2.5, 0), A(T0[6] + .9, T0[8] - .7));
  if (i === 8 || i === 9) tag3('LASER RANGING', 'Apollo mirrors on the Moon', V(X.laser + mx, LMY + .2, 0), A(T0[8] + 1.0, T0[10] - .2));
  if (i === 9) tag3('3.8 cm / YEAR', 'like a growing fingernail', V(X.laser + .85, .6, .38), A(T0[9] + 1.8, T0[10] - .2));
  tagsEnd();
  // ---- HUD
  const H = HUDS[i], endK = clamp((t - endAt) / .35), endIn = clamp((t - endAt - .35) / .45);
  let val = H[3]; if (i === 0) val = t < 1.45 ? 'Still here' : 'Gone';
  if (i === 2) val = Math.round(lerp(100, 31, eInOut(clamp((lt - .2) / 1.8)))) + '% of today';
  if (i === 3) val = lampK > .02 ? (lerp(.002, .25, lampK)).toFixed(lampK > .05 ? 2 : 3) + ' lux' : '0.002 lux';
  if (i >= 5 && i <= 6) val = tilt.toFixed(1) + '°';
  const fadeIn = clamp(lt / .25);
  setHUD({ q: 'What if the Moon <b>disappeared</b>?', qA: clamp((t - .2) / .4) * (1 - endK), l1: 'TIME AFTER', n1: H[0], l2: 'THIS PART IS', n2: H[1], l3: H[2], val,
    line: i === 0 ? '' : LN[i].show, lineA: fadeIn * clamp((T1[i] + .25 - t) / .2 + (i === 10 ? 9 : 0)), dataA: (1 - endK),
    end: 'Would <b>you</b> miss<br>the Moon? 👇', endA: endIn });
  if (i >= 8) $('v5l1').textContent = 'MEANWHILE';
  $('v5n2').style.color = H[1] === 'FACT' ? '#fff' : ACCENT;
  draw();
};
window.READY = true;
