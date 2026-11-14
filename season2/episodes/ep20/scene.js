// Episode 20 — What if Earth stopped spinning for 5 seconds?  (v5.1 premium studio look + AI voiceover; one continuous gallery glide, structure from ep13/ep18)
// Everything is timed to the narration (vo.json written by tools/narrate.py from vo_lines.json).
// Facts (checked 2026-11-15):
//  - Earth's equatorial circumference 40,075 km / sidereal day 23.93 h ≈ 1,670 km/h (465 m/s) (NASA / Space.com 33527 "How fast is Earth moving?");
//    ground speed = 1,670·cos(latitude): 45° ≈ 1,180 km/h, 75° ≈ 430 km/h, pole ≈ 0.
//  - speed of sound in air at 20 °C ≈ 343 m/s ≈ 1,235 km/h -> 1,670 km/h ≈ Mach 1.35.
//  - strongest tornado wind ever measured: 1999 Bridge Creek–Moore tornado, Doppler on Wheels, ~301 mph ≈ 484 km/h (Guinness; Wikipedia) -> 1,670/484 ≈ 3.4x.
//  - the atmosphere and oceans keep moving by inertia if the solid Earth stops (standard physics thought experiment, e.g. NASA/Live Science explainers);
//    what exactly the oceans and a restart would do is labelled SPECULATION ("our guess") in voice and HUD.
//  - Earth's spin is slowing (tidal braking). Winter et al. 2020 (Paleoceanography & Paleoclimatology), daily growth layers in a 70-million-year-old
//    rudist clam (Torreites sanchezi): 372 days a year, a day of ~23.5 h (sci.news "70 Million Years Ago Day Lasted 23.5 Hours").
import { THREE, RoundedBoxGeometry, scene, camera, clamp, lerp, eOut, eInOut, K, rimLight } from './kit.js';
import { key, hemi, DOF, draw, renderer, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd } from './studio.js';
import { makeJeremy2 } from './jeremy2.js';

await bootStudio('WHAT IF EARTH STOPPED SPINNING?', 'EP. 20');
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
const steel = new THREE.MeshStandardMaterial({ color: 0xc9ccd3, metalness: 1, roughness: .18 });
const glass = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .05, metalness: 0, transparent: true, opacity: .14, clearcoat: 1, depthWrite: false, side: THREE.DoubleSide });
const accentM = new THREE.MeshBasicMaterial({ color: ACCENT, toneMapped: false });
const accentS = new THREE.MeshStandardMaterial({ color: ACCENT, roughness: .4, metalness: .2 });
const greyS = new THREE.MeshStandardMaterial({ color: 0x8d8f96, roughness: .45, metalness: .3 });
const shadowAll = g => { g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };
function plinth(w, d, h) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, .03), marble); m.position.y = h / 2; m.castShadow = m.receiveShadow = true; return m; }
const X = { globe: 0, fly: 8, bars: 16, pole: 23, tank: 30, clock: 37 };
const TL = new THREE.TextureLoader();
const earthImg = await TL.loadAsync('./assets/planets/earth_atmos_2048.jpg'); earthImg.colorSpace = THREE.SRGBColorSpace; earthImg.anisotropy = 8;
const earthN = await TL.loadAsync('./assets/planets/earth_normal_2048.jpg');
const earthMat = new THREE.MeshStandardMaterial({ map: earthImg, normalMap: earthN, roughness: .55, emissive: 0xffffff, emissiveMap: earthImg, emissiveIntensity: .5 });
const earth = r => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 128, 96), earthMat); m.castShadow = true; return m; };
function arrow(len, rad, mat) { const g = new THREE.Group(); const s = new THREE.Mesh(new THREE.CylinderGeometry(rad, rad, len, 20), mat); s.position.y = len / 2;
  const h = new THREE.Mesh(new THREE.ConeGeometry(rad * 2.6, rad * 6, 24), mat); h.position.y = len + rad * 3; g.add(s, h); return g; }

// ---------------------------------------------------------------- A. spinning globe on a brass stand, orange equator ring + "east" arrow
const GY = 1.75, GR = .72; const globeSpin = new THREE.Group(); let eqArrow;
{ const g = new THREE.Group(); g.add(plinth(2.0, 2.0, .55));
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(.42, .5, .07, 64), darkIron); disc.position.y = .585;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, GY - GR - .62, 20), brass); post.position.y = .62 + (GY - GR - .62) / 2;
  const E = earth(GR); globeSpin.add(E);
  const axis = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, GR * 2 + .4, 12), brass); globeSpin.add(axis);
  globeSpin.position.y = GY;
  const eq = new THREE.Mesh(new THREE.TorusGeometry(GR + .012, .008, 10, 200), accentM); eq.rotation.x = Math.PI / 2; eq.position.y = GY;
  const mer = new THREE.Mesh(new THREE.TorusGeometry(GR + .09, .014, 12, 160, Math.PI), brass); mer.position.y = GY; mer.rotation.z = Math.PI / 2; mer.rotation.y = Math.PI / 2;
  eqArrow = new THREE.Group(); const a = arrow(.36, .016, accentM); a.rotation.z = -Math.PI / 2; eqArrow.add(a); eqArrow.position.set(-.18, GY, GR + .06);
  g.add(disc, post, globeSpin, eq, mer, eqArrow); g.position.x = X.globe; scene.add(shadowAll(g)); eq.castShadow = false; }

// ---------------------------------------------------------------- B. fly-off set: Jeremy, a chair, beach balls; an orange bolted bollard stays put
const ball = (r, col) => { const tx = canvasTex(256, 128, (ctx, w, h) => { for (let i = 0; i < 6; i++) { ctx.fillStyle = col[i % col.length]; ctx.fillRect(i * w / 6, 0, w / 6 + 1, h); } }).tex;
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 32), new THREE.MeshPhysicalMaterial({ map: tx, roughness: .35, clearcoat: .6 })); m.castShadow = true; return m; };
const flyBalls = [ball(.3, ['#f2f2f2', '#e8493b', '#f5c242', '#3a8de0']), ball(.22, ['#ffffff', '#2fb36b'])]; const FBP = [V(X.fly - 1.1, .3, .7), V(X.fly + .1, .22, 1.1)];
flyBalls.forEach((b, n) => { b.position.copy(FBP[n]); scene.add(b); });
const chair = new THREE.Group();
{ const wood = new THREE.MeshStandardMaterial({ color: 0x9b6b43, roughness: .6 });
  const seat = new THREE.Mesh(new RoundedBoxGeometry(.46, .05, .44, 3, .015), wood); seat.position.y = .46;
  const back = new THREE.Mesh(new RoundedBoxGeometry(.46, .42, .04, 3, .015), wood); back.position.set(0, .72, -.2);
  chair.add(seat, back); for (const x of [-.2, .2]) for (const z of [-.19, .19]) { const l = new THREE.Mesh(new THREE.CylinderGeometry(.018, .015, .46, 12), wood); l.position.set(x, .23, z); chair.add(l); }
  chair.position.set(X.fly - .45, 0, -1.1); chair.rotation.y = .5; scene.add(shadowAll(chair)); }
const bollard = new THREE.Group();
{ const p = new THREE.Mesh(new THREE.CylinderGeometry(.09, .1, 1.0, 32), accentS); p.position.y = .5; const cap = new THREE.Mesh(new THREE.SphereGeometry(.09, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), accentS); cap.position.y = 1.0;
  const pl = new THREE.Mesh(new THREE.CylinderGeometry(.22, .22, .035, 40), steel); pl.position.y = .018; bollard.add(p, cap, pl);
  for (let k = 0; k < 4; k++) { const b = new THREE.Mesh(new THREE.CylinderGeometry(.022, .022, .04, 12), steel); b.position.set(Math.cos(k * 1.57 + .78) * .16, .045, Math.sin(k * 1.57 + .78) * .16); bollard.add(b); }
  bollard.position.set(X.fly - 1.55, 0, -1.0); scene.add(shadowAll(bollard)); }
// speed streaks (screen-readable motion lines, slow-motion feel)
const streakM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthWrite: false, toneMapped: false });
const streaks = []; { const r = rand(31); for (let i = 0; i < 26; i++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(.006, .006, 1, 6), streakM); s.rotation.z = Math.PI / 2; s.userData = { y: .2 + r() * 2.3, z: -1.6 + r() * 2.6, ph: r(), len: .5 + r() * 1.1, sp: .8 + r() * .6 }; scene.add(s); streaks.push(s); } }

// ---------------------------------------------------------------- C. 3D bar chart: tornado record vs speed of sound vs the wind if Earth stopped
const BARS = [{ v: 484, mat: greyS, dx: -.95 }, { v: 1235, mat: greyS, dx: 0 }, { v: 1670, mat: accentS, dx: .95 }]; const BH = 2.0 / 1670; const barMesh = [];
{ const g = new THREE.Group(); const base = new THREE.Mesh(new RoundedBoxGeometry(3.3, .3, 1.1, 4, .03), marble); base.position.y = .15; g.add(base);
  for (const b of BARS) { const m = new THREE.Mesh(new RoundedBoxGeometry(.56, 1, .56, 4, .05), b.mat); m.position.set(b.dx, .3, 0); g.add(m); barMesh.push(m); }
  g.position.x = X.bars; scene.add(shadowAll(g)); }
const windStreaks = []; { const r = rand(44); for (let i = 0; i < 30; i++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(.005, .005, 1, 6), streakM.clone()); s.rotation.z = Math.PI / 2; s.userData = { y: .4 + r() * 2.6, z: -1.5 + r() * 2.8, ph: r(), len: .6 + r() * 1.2, sp: 1 + r() * .7 }; scene.add(s); windStreaks.push(s); } }

// ---------------------------------------------------------------- D. latitude globe (still) with speed arrows: equator / 45° / 75°
const poleG = new THREE.Group(), poleEarth = new THREE.Group(); const PY = 1.75, PR = .72; const latArrows = [];
{ poleG.add(plinth(2.0, 2.0, .55)); const disc = new THREE.Mesh(new THREE.CylinderGeometry(.42, .5, .07, 64), darkIron); disc.position.y = .585;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, PY - PR - .62, 20), brass); post.position.y = .62 + (PY - PR - .62) / 2;
  const E = earth(PR); poleEarth.add(E); poleEarth.position.y = PY;
  const axis = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, PR * 2 + .4, 12), brass); axis.position.y = PY;
  for (const [lat, sp] of [[0, 1670], [45, 1181], [75, 432]]) { const la = THREE.MathUtils.degToRad(lat); const len = .55 * sp / 1670 + .02; const a = arrow(len, .014, accentM); a.rotation.z = -Math.PI / 2;
    const h = new THREE.Group(); h.add(a); h.position.set(-len / 2, PY + Math.sin(la) * (PR + .03), Math.cos(la) * (PR + .03)); h.userData = { lat, sp, len }; poleG.add(h); latArrows.push(h);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(Math.cos(la) * (PR + .006), .004, 8, 160), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .55, toneMapped: false })); ring.rotation.x = Math.PI / 2; ring.position.y = PY + Math.sin(la) * (PR + .006); poleG.add(ring); }
  const capDot = new THREE.Mesh(new THREE.SphereGeometry(.03, 20, 14), accentM); capDot.position.y = PY + PR + .01;
  poleG.add(disc, post, poleEarth, axis, capDot); poleG.position.x = X.pole; scene.add(shadowAll(poleG)); }

// ---------------------------------------------------------------- E. ocean tank: water sloshes east (right) onto a model coast with little houses
const TW = 2.6, TD = 1.0, TB = .5; let waterGeo, waterY0;
{ const g = new THREE.Group(); g.add(plinth(2.9, 1.3, TB));
  const sandTex = canvasTex(512, 512, (ctx, w, h) => { const r = rand(12); ctx.fillStyle = '#d8c39b'; ctx.fillRect(0, 0, w, h); for (let i = 0; i < 6000; i++) { const v = r() * 40 - 20; ctx.fillStyle = `rgba(${170 + v},${150 + v},${110 + v},.35)`; ctx.fillRect(r() * w, r() * h, 2, 2); } }).tex;
  const coast = u => .08 + .5 * Math.pow(clamp((u - .45) / .55), 1.3); // seabed on the left (west), coast rising on the right (east)
  const sg = new THREE.PlaneGeometry(TW - .04, TD - .04, 120, 30), sp = sg.attributes.position;
  for (let i = 0; i < sp.count; i++) { const x = sp.getX(i), y = sp.getY(i); sp.setZ(i, coast((x + TW / 2) / TW) + .008 * Math.sin(x * 20 + y * 4)); }
  sg.computeVertexNormals(); const sand = new THREE.Mesh(sg, new THREE.MeshStandardMaterial({ map: sandTex, roughness: 1 })); sand.rotation.x = -Math.PI / 2; sand.position.y = TB; g.add(sand);
  const shp = new THREE.Shape(); shp.moveTo(-TW / 2 + .02, 0); for (let k = 0; k <= 50; k++) { const x = -TW / 2 + .02 + k / 50 * (TW - .04); shp.lineTo(x, coast((x + TW / 2) / TW)); } shp.lineTo(TW / 2 - .02, 0); shp.closePath();
  const body = new THREE.Mesh(new THREE.ExtrudeGeometry(shp, { depth: TD - .04, bevelEnabled: false }), new THREE.MeshStandardMaterial({ map: sandTex, roughness: 1, color: 0xc9b38a })); body.position.set(0, TB, -(TD - .04) / 2); g.add(body);
  // little houses on the coast
  const r = rand(9), wall = new THREE.MeshStandardMaterial({ color: 0xf1ede6, roughness: .7 }), roof = new THREE.MeshStandardMaterial({ color: 0xa4513a, roughness: .6 });
  for (let i = 0; i < 6; i++) { const u = .78 + (i % 3) * .07, x = -TW / 2 + u * TW, z = -.28 + Math.floor(i / 3) * .4 + (r() - .5) * .06; const y = TB + coast(u);
    const hb = new THREE.Mesh(new RoundedBoxGeometry(.1, .07, .08, 2, .008), wall); hb.position.set(x, y + .035, z);
    const rf = new THREE.Mesh(new THREE.ConeGeometry(.08, .05, 4), roof); rf.rotation.y = Math.PI / 4; rf.position.set(x, y + .095, z); rf.scale.set(1, 1, .8); g.add(hb, rf); }
  // water: a box whose top vertices we move every frame
  waterGeo = new THREE.BoxGeometry(TW - .05, 1, TD - .05, 60, 1, 4); waterGeo.translate(0, .5, 0); waterY0 = Float32Array.from(waterGeo.attributes.position.array);
  const water = new THREE.Mesh(waterGeo, new THREE.MeshPhysicalMaterial({ color: 0x1f7fa6, roughness: .06, metalness: 0, clearcoat: 1, transparent: true, opacity: .78, depthWrite: false })); water.position.set(0, TB, 0); g.add(water);
  const gl = new THREE.Mesh(new THREE.BoxGeometry(TW, 1, TD), glass); gl.position.y = TB + .5; g.add(gl);
  for (const [x, z] of [[-1, -1], [-1, 1], [1, -1], [1, 1]]) { const c = new THREE.Mesh(new THREE.BoxGeometry(.03, 1, .03), brass); c.position.set(x * TW / 2, TB + .5, z * TD / 2); g.add(c); }
  for (const y of [TB, TB + 1]) for (const z of [-1, 1]) { const b = new THREE.Mesh(new THREE.BoxGeometry(TW, .03, .03), brass); b.position.set(0, y, z * TD / 2); g.add(b); }
  for (const y of [TB, TB + 1]) for (const x of [-1, 1]) { const b = new THREE.Mesh(new THREE.BoxGeometry(.03, .03, TD), brass); b.position.set(x * TW / 2, y, 0); g.add(b); }
  g.position.x = X.tank; scene.add(shadowAll(g)); water.castShadow = false; gl.castShadow = false; }
function setWater(t, k) { // k: 0 = calm, 1 = full surge to the east
  const p = waterGeo.attributes.position; for (let i = 0; i < p.count; i++) { if (waterY0[i * 3 + 1] < .5) continue; const x = waterY0[i * 3], u = (x + TW / 2) / TW;
    const calm = .36 + .006 * Math.sin(x * 9 + t * 2.2); const surge = .22 + .55 * Math.pow(u, 2.2) + .05 * Math.sin(u * 10 - t * 4) * u; p.setY(i, lerp(calm, surge, k)); }
  p.needsUpdate = true; waterGeo.computeVertexNormals(); }

// ---------------------------------------------------------------- F. 24-hour clock + 70-million-year-old fossil clam (the twist)
const CY = 1.55, CR = .62; let hand, wedge;
{ const g = new THREE.Group(); g.add(plinth(1.6, 1.0, .55));
  const face = canvasTex(1024, 1024, (ctx, w, h) => { ctx.fillStyle = '#f4f1ea'; ctx.beginPath(); ctx.arc(w / 2, h / 2, w / 2, 0, Math.PI * 2); ctx.fill();
    ctx.translate(w / 2, h / 2); for (let i = 0; i < 96; i++) { const a = i / 96 * Math.PI * 2; const big = i % 4 === 0, major = i % 24 === 0; ctx.save(); ctx.rotate(a); ctx.fillStyle = '#1e1e22'; ctx.fillRect(-(major ? 5 : big ? 3 : 1.5), -470, major ? 10 : big ? 6 : 3, major ? 60 : big ? 38 : 18); ctx.restore(); }
    ctx.fillStyle = '#1e1e22'; ctx.font = '700 78px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    [['24', 0], ['6', 6], ['12', 12], ['18', 18]].forEach(([s, hh]) => { const a = hh / 24 * Math.PI * 2; ctx.fillText(s, Math.sin(a) * 340, -Math.cos(a) * 340); });
    ctx.font = '600 40px Arial'; ctx.fillStyle = '#6a655e'; ctx.fillText('HOURS', 0, 150); }).tex;
  const rim = new THREE.Mesh(new THREE.CylinderGeometry(CR + .05, CR + .05, .12, 96), brass); rim.rotation.x = Math.PI / 2; rim.position.set(0, CY, 0);
  const dial = new THREE.Mesh(new THREE.CircleGeometry(CR, 96), new THREE.MeshStandardMaterial({ map: face, roughness: .5 })); dial.position.set(0, CY, .061);
  wedge = new THREE.Mesh(new THREE.CircleGeometry(CR * .93, 48, Math.PI / 2, (.5 / 24) * Math.PI * 2), new THREE.MeshBasicMaterial({ color: ACCENT, transparent: true, opacity: 0, toneMapped: false, depthWrite: false })); wedge.position.set(0, CY, .064);
  hand = new THREE.Group(); const hm = new THREE.Mesh(new RoundedBoxGeometry(.03, CR * .82, .012, 2, .005), darkIron); hm.position.y = CR * .36; hand.add(hm); hand.position.set(0, CY, .07);
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(.035, .035, .03, 32), brass); hub.rotation.x = Math.PI / 2; hub.position.set(0, CY, .08);
  const leg = new THREE.Mesh(new THREE.CylinderGeometry(.035, .05, CY - CR - .55, 20), brass); leg.position.set(0, .55 + (CY - CR - .55) / 2, 0);
  g.add(rim, dial, wedge, hand, hub, leg); g.position.set(X.clock - .9, 0, 0); scene.add(shadowAll(g)); wedge.castShadow = false; }
const clam = new THREE.Group();
{ clam.add(plinth(.7, .7, .9));
  const ringTex = canvasTex(256, 512, (ctx, w, h) => { const r = rand(17); ctx.fillStyle = '#b9a58a'; ctx.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 3 + r() * 4) { const v = r() * 40 - 20; ctx.fillStyle = `rgba(${110 + v},${92 + v},${70 + v},.55)`; ctx.fillRect(0, y, w, 1 + r() * 1.5); } }).tex;
  const pts = []; for (let k = 0; k <= 30; k++) { const u = k / 30; pts.push(new THREE.Vector2(.02 + .15 * Math.pow(u, .85), u * .42)); } pts.push(new THREE.Vector2(.0, .42));
  const shell = new THREE.Mesh(new THREE.LatheGeometry(pts, 64), new THREE.MeshStandardMaterial({ map: ringTex, roughness: .85 })); shell.position.y = .9; shell.rotation.z = .12;
  const lid = new THREE.Mesh(new THREE.SphereGeometry(.17, 48, 16, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xa8957a, roughness: .9 })); lid.scale.y = .25; lid.position.set(-.05, 1.32, 0); lid.rotation.z = .12;
  clam.add(shell, lid); clam.position.set(X.clock + .95, 0, .1); scene.add(shadowAll(clam)); }

// ---------------------------------------------------------------- Jeremys (scale .75 ≈ 1.75 m label)
const J1 = K.J, J2 = makeJeremy2(), J3 = makeJeremy2(), J4 = makeJeremy2(), J5 = makeJeremy2(); [J2, J3, J4, J5].forEach(j => { scene.add(j); rimLight(j); });
const putJ = (J, x, z, ry, pose, y = 0) => { J.visible = true; J.position.set(x, y, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose); };

// ---------------------------------------------------------------- timeline (from the voiceover)
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), endAt = T0[9] + 1.2;
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const tStop = T0[3] + 1.35; // "Now the planet stops."
const CAM = [ // one per narration line: [target x, y, dist, yaw, pitch]
  [X.globe + .3, 1.25, 10.8, -.45, .18], [X.globe + .2, 1.3, 9.6, -.35, .16], [X.globe + .2, 1.3, 9.9, -.3, .16], [X.fly + .1, 1.0, 12.0, -.25, .16], [X.bars + .4, 1.0, 12.4, -.35, .16],
  [X.pole + .2, 1.35, 10.0, -.4, .16], [X.tank + .2, .95, 10.8, -.32, .2], [X.clock + .05, 1.05, 11.4, -.4, .16], [X.clock + .05, 1.05, 10.8, -.33, .16], [X.clock + .05, 1.05, 12.0, -.38, .18]];
function camAt(t) { let c = CAM[0].slice(); for (let i = 1; i < CAM.length; i++) { const k = eInOut(clamp((t - (T0[i] - .8)) / 1.3)); if (k <= 0) break; c = c.map((v, j) => lerp(v, CAM[i][j], k)); } return c; }
const HUDS = [ // [l1, n1, THIS PART IS, l3, value]
  ['EARTH', 'Spinning', 'FACT', 'SPIN AT THE EQUATOR', '1,670 km/h'], ['EARTH', 'Spinning', 'FACT', 'SPIN AT THE EQUATOR', '1,670 km/h'], ['SPEED OF SOUND', '1,235 km/h', 'FACT', 'FASTER THAN SOUND', 'Mach 1.35'],
  ['EARTH', 'Stopped', 'FACT', 'YOU KEEP MOVING AT', '1,670 km/h'], ['EARTH', 'Stopped', 'FACT', 'WIND AT THE EQUATOR', '1,670 km/h'], ['EARTH', 'Stopped', 'FACT', 'GROUND SPEED AT 75°', '432 km/h'],
  ['EARTH', 'Restarts', 'SPECULATION', 'THE OCEANS', 'Surge east'], ['REAL LIFE', 'Slowing down', 'FACT', 'A DAY TODAY', '24 hours'], ['REAL LIFE', 'Slowing down', 'FACT', 'A DAY, 70 MILLION YEARS AGO', '23.5 hours'], ['REAL LIFE', 'Slowing down', 'FACT', 'A DAY, 70 MILLION YEARS AGO', '23.5 hours']];
window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: total, name: 'room', gain: .1 }, { t0: T0[4] - .3, t1: T1[4] + .4, name: 'wind', gain: .26 }, { t0: T0[6], t1: T1[6] + .3, name: 'drip', gain: .1 }],
  sfx: [{ t: 1.0, name: 'swell', gain: .3 }, ...[1, 3, 4, 5, 6, 7].map(i => ({ t: T0[i] - .85, name: 'glide', gain: .26 })), { t: T0[2] + .6, name: 'chime', gain: .2 },
    { t: tStop - .05, name: 'rumble_low', gain: .42 }, { t: tStop + .1, name: 'wind_gust', gain: .3 }, { t: tStop + .7, name: 'clatter', gain: .18 }, { t: T0[4] + .3, name: 'wind_gust', gain: .26 },
    { t: T0[6] + 1.0, name: 'splash', gain: .22 }, { t: T0[7] + .2, name: 'chime', gain: .28 }, { t: T0[8] + 2.2, name: 'ding', gain: .22 }, { t: endAt, name: 'chime', gain: .3 }] };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), lt = t - T0[i], ld = T1[i] - T0[i];
  // ---- A. globe spins (exaggerated speed) until the stop, then halts in ~0.25 s
  const spinAng = s => 1.15 * s; const tS = tStop; const ang = t < tS ? spinAng(t) : spinAng(tS) + 1.15 * .12 * (1 - Math.pow(1 - clamp((t - tS) / .25), 2));
  globeSpin.rotation.y = -1.9 + ang; eqArrow.visible = t < tS + .2; eqArrow.children[0].scale.setScalar(.9 + .1 * Math.sin(t * 4));
  // ---- B. fly-off (slow motion): everything loose drifts east (right), tumbling a little; the bollard stays
  const fk = t < tS ? 0 : (t - tS); const fly = d => Math.min(d, fk * .55 * (1 - Math.exp(-fk * 2.2)) / 1); // smooth start, ~0.55 m/s on screen ("slow motion")
  const dx = fly(1.5), lift = Math.min(.45, fk * .12);
  flyBalls.forEach((b, n) => { b.position.set(FBP[n].x + dx * (1.1 + n * .25), FBP[n].y + lift * (1.2 - n * .4), FBP[n].z); b.rotation.set(fk * (1 + n), 0, -fk * 2.2); });
  chair.position.set(X.fly - .45 + dx * .95, lift * .8, -1.1); chair.rotation.set(0, .5, -Math.min(.6, fk * .3));
  const sk = clamp(fk / .5) * (1 - clamp((t - (T0[4] - .6)) / .5)); streakM.opacity = .45 * sk;
  streaks.forEach(s => { const u = s.userData, k = (t * u.sp + u.ph) % 1; s.visible = sk > .01; s.scale.y = u.len; s.position.set(X.fly - 2.6 + k * 5.2, u.y, u.z); });
  // ---- C. bars grow in, the wind blows across them
  const growB = (n, t0) => eInOut(clamp((t - t0) / 1.4)); const gk = [growB(0, T0[4] + 1.3), growB(1, T0[4] - .4), growB(2, T0[4] - .2)];
  barMesh.forEach((m, n) => { const h = Math.max(.001, BARS[n].v * BH * gk[n]); m.scale.y = h; m.position.y = .3 + h / 2; m.visible = gk[n] > .001; });
  const wk = clamp((t - (T0[4] + .2)) / .6) * (1 - clamp((t - (T1[4] + .2)) / .5));
  windStreaks.forEach(s => { const u = s.userData, k = (t * u.sp * 1.3 + u.ph) % 1; s.visible = wk > .01; s.material.opacity = .4 * wk * Math.sin(Math.PI * k); s.scale.y = u.len; s.position.set(X.bars - 2.8 + k * 5.6, u.y, u.z); });
  // ---- D. latitude arrows appear one by one; globe still
  poleEarth.rotation.y = -1.6 + .5;
  latArrows.forEach((a, n) => { const k = eOut(clamp((t - (T0[5] - .3 + n * .55)) / .5)); a.scale.setScalar(Math.max(.001, k)); a.visible = k > .001; });
  // ---- E. ocean surge (speculation)
  const sur = eInOut(clamp((t - (T0[6] + .6)) / 2.2)) * (1 - .45 * eInOut(clamp((t - (T0[6] + 4.5)) / 2.0)));
  setWater(t, sur);
  // ---- F. clock: hand sweeps; the missing half hour lights up in line 8
  hand.rotation.z = -(t * .55) % (Math.PI * 2); const wk2 = clamp((t - (T0[8] + 2.0)) / .5); wedge.material.opacity = .85 * wk2;
  // ---- Jeremys
  const bl = p => (t % p) < .1;
  putJ(J1, X.globe + 1.4, -.35, -.7, { expr: i === 2 ? 'shocked' : 'happy', look: -.4, armL: .25, armR: i === 1 ? 1.2 : .25, blink: bl(2.7) });
  const jf = fly(1.0); putJ(J2, X.fly - .6 + jf, -.35, -.25, { expr: fk > 0 ? 'shocked' : 'happy', look: -.2, armL: fk > 0 ? 2.5 : .25, armR: fk > 0 ? 2.5 : .25, blink: bl(2.9) }, lift * .9);
  J2.rotation.z = -Math.min(.75, fk * .45); J2.rotation.x = Math.sin(fk * 1.5) * .08;
  putJ(J3, X.bars + 1.6, .35, -.55, { expr: i === 4 ? 'worried' : 'happy', look: -.5, armL: .25, armR: .25, blink: bl(3.1) });
  putJ(J4, X.pole + 1.25, -.6, -.6, { expr: 'happy', look: -.55, armL: .25, armR: i === 5 ? 1.2 : .25, blink: bl(2.5) });
  putJ(J5, X.clock + .15, -.9, -.45, { expr: i >= 9 ? 'confused' : i === 8 ? 'shocked' : 'happy', look: -.55, armL: .25, armR: i === 9 ? 1.3 : .25, tilt: i >= 9 ? .1 : 0, blink: bl(2.3) });
  // ---- camera: one continuous glide along the gallery
  const c = camAt(t), drift = clamp(lt / Math.max(ld, 1));
  const tgt = V(c[0], c[1], 0), dist = c[2] * (1 - .035 * drift);
  orbit(tgt, dist, { yaw: c[3] + .04 * drift + t * .002, pitch: c[4], fov: 34, lookUp: .075 });
  shadowFit(tgt, 4.2); DOF.on = true; DOF.focus = dist; DOF.aperture = .55; DOF.maxR = 9;
  // ---- callout tags (orbit() first)
  const A = (t0, t1) => clamp((t - t0) / .35) * clamp((t1 - t) / .3);
  if (i === 0) tag3('JEREMY', '1.75 m', V(X.globe + 1.4, 2.3, -.35), A(.6, T0[1] - .7));
  if (i === 1 || i === 2) tag3('EQUATOR', '1,670 km/h', V(X.globe - .5, GY + .05, GR * .7), A(T0[1] + 2.2, T0[3] - .7));
  if (i === 2) tag3('SPEED OF SOUND', '1,235 km/h', V(X.globe + .55, 2.75, 0), A(T0[2] + .9, T0[3] - .7));
  if (i === 3) tag3('BOLTED DOWN', 'stays put', V(X.fly - 1.55, 1.2, -1.0), A(tStop + 1.6, T0[4] - .7));
  if (i === 3) tag3('NOT BOLTED DOWN', 'keeps going east', V(X.fly - .6 + jf, 2.25 + lift, -.35), A(tStop + .8, T0[4] - .7));
  if (i === 4) { tag3('STRONGEST TORNADO', '484 km/h', V(X.bars - .95, .3 + 484 * BH + .15, 0), A(T0[4] + 2.4, T0[5] - .7));
    tag3('THE WIND', '1,670 km/h', V(X.bars + .95, .3 + 1670 * BH + .15, 0), A(T0[4] + 1.2, T0[5] - .7)); }
  if (i === 5) { tag3('POLE', '≈ 0 km/h', V(X.pole, PY + PR + .05, 0), A(T0[5] + 1.6, T0[6] - .7)); tag3('EQUATOR', '1,670 km/h', V(X.pole - .35, PY - .02, PR), A(T0[5] + .6, T0[6] - .7)); }
  if (i === 6) tag3('SPECULATION', 'oceans surge east', V(X.tank - .6, 1.25, .45), A(T0[6] + 1.0, T0[7] - .6));
  if (i === 8 || i === 9) tag3('FOSSIL CLAM', '70 million years old', V(X.clock + .95, 1.45, .1), A(T0[8] + 3.2, endAt - .1));
  if (i === 8) tag3('−30 MIN', 'a shorter day', V(X.clock - 1.55, CY + .35, 0), A(T0[8] + 2.2, T0[9] - .3));
  tagsEnd();
  // ---- HUD
  const H = HUDS[i], endK = clamp((t - endAt) / .35), endIn = clamp((t - endAt - .35) / .45);
  let n1 = H[1], val = H[4];
  if (i === 3 && t < tStop) n1 = 'Spinning';
  if (i === 5) { const k = clamp((t - (T0[5] + .8)) / 2.4); val = Math.round(lerp(1670, 432, eInOut(k))).toLocaleString('en-US') + ' km/h'; $('v5l3').textContent = ''; }
  if (i === 8) val = lerp(24, 23.5, eInOut(clamp((t - (T0[8] + 1.8)) / 1.6))).toFixed(1) + ' hours';
  const fadeIn = clamp(lt / .25);
  setHUD({ q: 'What if Earth <b>stopped spinning</b> for 5 seconds?', qA: clamp((t - .2) / .4) * (1 - endK), l1: H[0], n1, l2: 'THIS PART IS', n2: H[2], l3: H[3], val,
    line: i === 0 ? '' : LN[i].show, lineA: fadeIn * clamp((T1[i] + .25 - t) / .2 + (i === 9 ? 9 : 0)), dataA: (1 - endK),
    end: 'Where would <b>you</b><br>want to stand? 👇', endA: endIn });
  if (i === 5) $('v5l3').textContent = t < T0[5] + 2.2 ? 'GROUND SPEED, EQUATOR → POLE' : 'GROUND SPEED AT 75°';
  $('v5n2').style.color = H[2] === 'FACT' ? '#fff' : ACCENT;
  draw();
};
window.READY = true;
