// Episode 22 — What if Earth had two moons?  (v5.1 premium studio look + AI voiceover; one continuous gallery glide, structure from ep13/ep21)
// Everything is timed to the narration (vo.json written by tools/narrate.py from vo_lines.json).
// Facts (checked 2026-11-16):
//  - Moon: mean diameter 3,474 km; mean distance 384,400 km (NASA Moon fact sheet). Earth 12,742 km.
//  - tide-generating force varies inversely as the CUBE of distance (NOAA Ocean Service, Tides & Water Levels tutorial "What causes tides?").
//    An identical moon at half the distance -> 2^3 = 8 x the tidal pull. Apparent diameter x2 -> apparent area / reflected light x4 (geometry).
//  - "far bigger tides, flooding coasts every day" is our guess: labelled SPECULATION on screen and in the voice.
//  - two-moon hypothesis: Jutzi & Asphaug, Nature, 4 Aug 2011 — a ~1,200 km companion moon (about 1/3 of the Moon's width, ~4% of its mass)
//    collided slowly (~7,200-10,800 km/h) with the Moon and spread into the far-side highlands. Computer simulations, not confirmed -> "one theory" / HUD "THEORY"
//    (Space.com / LiveScience 2011 "Earth had two moons that crashed to form one, study suggests").
//  - 2024 PT5: ~10 m asteroid, a temporary "mini-moon" travelling with Earth from 29 Sep to 25 Nov 2024 (about two months); it never completed a full orbit
//    (AAS Nova 2024-12-17; de la Fuente Marcos & de la Fuente Marcos 2024, RNAAS). Voice says "tagged along with Earth", not "orbited".
import { THREE, RoundedBoxGeometry, scene, camera, clamp, lerp, eOut, eInOut, K, rimLight } from './kit.js';
import { key, hemi, DOF, draw, renderer, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd } from './studio.js';
import { makeJeremy2 } from './jeremy2.js';

await bootStudio('WHAT IF EARTH HAD TWO MOONS?', 'EP. 22');
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
const X = { A: 0, B: 8, C: 16, D: 24 };
const TL = new THREE.TextureLoader();
const earthImg = await TL.loadAsync('./assets/planets/earth_atmos_2048.jpg'); earthImg.colorSpace = THREE.SRGBColorSpace; earthImg.anisotropy = 8;
const earthN = await TL.loadAsync('./assets/planets/earth_normal_2048.jpg');
const moonImg = await TL.loadAsync('./assets/planets/moon_1024.jpg'); moonImg.colorSpace = THREE.SRGBColorSpace; moonImg.anisotropy = 8;
const earthMat = () => { const m = new THREE.MeshStandardMaterial({ map: earthImg, normalMap: earthN, roughness: .6 });
  m.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\n totalEmissiveRadiance += diffuseColor.rgb * .5;'); }; return m; };
const moonMat = (glow = .3) => new THREE.MeshStandardMaterial({ map: moonImg, bumpMap: moonImg, bumpScale: 1.2, roughness: 1, emissive: 0xffffff, emissiveMap: moonImg, emissiveIntensity: glow });
function globeOnStand(x, z, GY, GR, tilt = .41) { const g = new THREE.Group(); g.add(plinth(1.5, 1.5, .55));
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(.36, .44, .07, 64), darkIron); disc.position.y = .585;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, GY - GR - .62, 20), brass); post.position.y = .62 + (GY - GR - .62) / 2;
  const holder = new THREE.Group(); holder.position.y = GY; holder.rotation.z = tilt; const E = new THREE.Mesh(new THREE.SphereGeometry(GR, 128, 96), earthMat()); holder.add(E);
  const axis = new THREE.Mesh(new THREE.CylinderGeometry(.01, .01, GR * 2 + .3, 12), brass); holder.add(axis);
  g.add(disc, post, holder); g.position.set(x, 0, z); scene.add(shadowAll(g)); return { g, E }; }

// ---------------------------------------------------------------- A. Earth + Moon orrery (sizes to scale, distance shortened), the twin moon appears at half the distance; tidal-pull bars
const AY = 1.55, AR = .5, MRA = AR * 3474 / 12742; const LA1 = 1.2, LA2 = .6; // arm lengths (distance not to scale)
const A = globeOnStand(X.A, 0, AY, AR);
const moonA = new THREE.Mesh(new THREE.SphereGeometry(MRA, 96, 64), moonMat(.3)); scene.add(moonA); moonA.castShadow = true;
const twinMat = moonMat(.3); const twinA = new THREE.Mesh(new THREE.SphereGeometry(MRA, 96, 64), twinMat); scene.add(twinA); twinA.castShadow = true;
function arm(len) { const g = new THREE.Group(); const r = new THREE.Mesh(new THREE.CylinderGeometry(.011, .011, len, 12), brass); r.rotation.z = Math.PI / 2; r.position.x = len / 2; g.add(r);
  const st = new THREE.Mesh(new THREE.CylinderGeometry(.009, .009, AR + .1 - MRA * .6, 10), brass); st.position.set(len, (AR + .1 - MRA * .6) / 2, 0); g.add(st);
  const col = new THREE.Mesh(new THREE.CylinderGeometry(.04, .04, .05, 24), brass); g.add(col); g.position.set(X.A, AY - AR - .1, 0); scene.add(shadowAll(g)); return g; }
const armA1 = arm(LA1), armA2 = arm(LA2);
const moonAt = (len, ang) => V(X.A + Math.cos(ang) * len, AY, -Math.sin(ang) * len);
// tidal-pull bars on a small plinth to the right
const BARX = X.A + 1.6; const bars = [];
{ const g = new THREE.Group(); g.add(plinth(.8, .6, .45)); g.position.set(BARX, 0, .2); scene.add(shadowAll(g));
  for (const [dx, col] of [[-.17, 0xd9d4cc], [.17, ACCENT]]) { const m = new THREE.Mesh(new RoundedBoxGeometry(.22, 1, .22, 3, .02), col === ACCENT ? new THREE.MeshStandardMaterial({ color: ACCENT, roughness: .45, emissive: ACCENT, emissiveIntensity: .25 }) : new THREE.MeshStandardMaterial({ color: col, roughness: .4 }));
    m.position.set(BARX + dx, .45, .2); m.castShadow = true; scene.add(m); bars.push(m); } }
const BAR1 = .14; // 1x height (8x = 1.12 m)

// ---------------------------------------------------------------- B. tide tank: a coast with little houses; water rises and falls; speculation flood
const TB = { w: 2.4, d: .8, h: .85 }; let tideW; const houses = [];
const landH = x => x < -.25 ? .07 : x < .55 ? lerp(.07, .46, eInOut((x + .25) / .8)) : .46; // height above tank floor
{ const g = new THREE.Group(); g.add(plinth(2.8, 1.15, .55));
  const tank = new THREE.Mesh(new THREE.BoxGeometry(TB.w, TB.h, TB.d), glass); tank.position.y = .55 + TB.h / 2; g.add(tank);
  for (const [x, z] of [[-1.2, -.4], [-1.2, .4], [1.2, -.4], [1.2, .4]]) { const c = new THREE.Mesh(new THREE.BoxGeometry(.025, TB.h, .025), brass); c.position.set(x, .55 + TB.h / 2, z); g.add(c); }
  const sandTex = canvasTex(512, 256, (ctx, w, h) => { const r = rand(4); ctx.fillStyle = '#c9b48c'; ctx.fillRect(0, 0, w, h); for (let i = 0; i < 4000; i++) { const v = r() * 40 - 20; ctx.fillStyle = `rgba(${190 + v},${168 + v},${128 + v},.5)`; ctx.fillRect(r() * w, r() * h, 2, 2); } }).tex;
  const shp = new THREE.Shape(); shp.moveTo(-1.18, 0); for (let k = 0; k <= 120; k++) { const x = -1.18 + k / 120 * 2.36; shp.lineTo(x, landH(x)); } shp.lineTo(1.18, 0); shp.closePath();
  const land = new THREE.Mesh(new THREE.ExtrudeGeometry(shp, { depth: TB.d - .04, bevelEnabled: false, curveSegments: 4 }), new THREE.MeshStandardMaterial({ map: sandTex, roughness: .95 }));
  land.position.set(0, .56, -(TB.d - .04) / 2); g.add(land);
  // grass strip on the land top
  const grass = new THREE.Mesh(new RoundedBoxGeometry(.62, .02, TB.d - .06, 2, .008), new THREE.MeshStandardMaterial({ color: 0x6f8f4a, roughness: .9 })); grass.position.set(.86, .56 + .46 + .01, 0); g.add(grass);
  const wallM = new THREE.MeshStandardMaterial({ color: 0xf1ece4, roughness: .7 }), roofM = new THREE.MeshStandardMaterial({ color: 0x9a5a44, roughness: .7 });
  for (const [x, z, s] of [[.72, -.18, 1], [.98, .14, .9], [.7, .22, .8], [1.05, -.22, .85]]) { const h = new THREE.Group();
    const b = new THREE.Mesh(new RoundedBoxGeometry(.13 * s, .1 * s, .11 * s, 2, .008), wallM); b.position.y = .05 * s; h.add(b);
    const roof = new THREE.Mesh(new THREE.CylinderGeometry(.0001, .1 * s, .08 * s, 4, 1), roofM); roof.rotation.y = Math.PI / 4; roof.position.y = .1 * s + .04 * s; h.add(roof);
    h.position.set(x, .56 + .47, z); g.add(h); houses.push(h); }
  tideW = new THREE.Mesh(new THREE.BoxGeometry(TB.w - .04, 1, TB.d - .04), new THREE.MeshPhysicalMaterial({ color: 0x1f6f9c, roughness: .06, clearcoat: 1, transparent: true, opacity: .78, depthWrite: false })); g.add(tideW);
  // brass "today's high tide" mark on the back glass
  const mk = new THREE.Mesh(new THREE.BoxGeometry(TB.w - .02, .008, .008), brass); mk.position.set(0, .56 + .36, -TB.d / 2 - .005); g.add(mk);
  g.position.x = X.B; scene.add(shadowAll(g)); tideW.castShadow = false; tank.castShadow = false; }
const HI = .36; // today's high tide (above tank floor)

// ---------------------------------------------------------------- C. the twist: a small companion moon (1,200 km) slowly hits our Moon (3,474 km) and spreads into a crust
const CY = 1.5, CR = .55, SR = CR * 1200 / 3474; let moonC, smallC, crust; const IMP = V(-.5, .3, .8).normalize(); // impact direction (towards camera side so it is visible)
{ const g = new THREE.Group(); g.add(plinth(1.6, 1.6, .55));
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(.34, .42, .07, 64), darkIron); disc.position.y = .585;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, CY - CR - .62, 20), brass); post.position.y = .62 + (CY - CR - .62) / 2; g.add(disc, post);
  g.position.x = X.C; scene.add(shadowAll(g));
  moonC = new THREE.Mesh(new THREE.SphereGeometry(CR, 128, 96), moonMat(.28)); moonC.position.set(X.C, CY, 0); moonC.castShadow = true; scene.add(moonC);
  smallC = new THREE.Mesh(new THREE.SphereGeometry(SR, 96, 64), new THREE.MeshStandardMaterial({ map: moonImg, bumpMap: moonImg, bumpScale: 1.2, color: 0xd8cfc2, roughness: 1, emissive: 0xffffff, emissiveMap: moonImg, emissiveIntensity: .22 }));
  smallC.castShadow = true; scene.add(smallC);
  crust = new THREE.Mesh(new THREE.SphereGeometry(CR * 1.012, 96, 48, 0, Math.PI * 2, 0, .01), new THREE.MeshStandardMaterial({ map: moonImg, bumpMap: moonImg, bumpScale: 2, color: 0xe9e1d3, roughness: 1, emissive: 0xffffff, emissiveMap: moonImg, emissiveIntensity: .3 }));
  crust.position.copy(moonC.position); crust.quaternion.setFromUnitVectors(V(0, 1, 0), IMP); scene.add(crust); }
let crustTheta = -1;
function setCrust(th) { if (Math.abs(th - crustTheta) < 1e-4) return; crustTheta = th; crust.geometry.dispose(); crust.geometry = new THREE.SphereGeometry(CR * 1.012, 96, 48, 0, Math.PI * 2, 0, Math.max(.01, th)); crust.visible = th > .02; }

// ---------------------------------------------------------------- D. mini-moon 2024 PT5: a tiny rock traces a loop past Earth (path enlarged; rock enlarged)
const DY = 1.55, DR = .5; const D = globeOnStand(X.D - .2, 0, DY, DR);
const pathPts = [V(2.3, .55, -1.6), V(1.6, .45, -.9), V(1.15, .3, -.2), V(1.0, .15, .45), V(.45, .05, .95), V(-.3, .05, 1.0), V(-.85, .12, .5), V(-.8, .25, -.2), V(-.2, .35, -.75), V(.7, .45, -.85), V(1.6, .55, -.45), V(2.5, .65, .1)]
  .map(p => V(-p.x, p.y, p.z).add(V(X.D - .2, DY, 0))); // mirrored: enters and leaves at the back left, away from Jeremy
const curve = new THREE.CatmullRomCurve3(pathPts, false, 'centripetal', .5);
const pathMesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 400, .006, 8, false), new THREE.MeshBasicMaterial({ color: ACCENT, toneMapped: false, transparent: true, opacity: .85 })); scene.add(pathMesh);
const PATH_IDX = pathMesh.geometry.index.count; pathMesh.geometry.setDrawRange(0, 0);
const rockGeo = new THREE.IcosahedronGeometry(.045, 5); { const p = rockGeo.attributes.position, v = new THREE.Vector3(); for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const n = 1 + .18 * Math.sin(v.x * 70 + 1) * Math.cos(v.y * 60) + .1 * Math.sin(v.z * 90 + v.x * 40); v.multiplyScalar(n); p.setXYZ(i, v.x, v.y, v.z); } rockGeo.computeVertexNormals(); }
const rock = new THREE.Mesh(rockGeo, new THREE.MeshStandardMaterial({ color: 0x8a7e72, roughness: .95, emissive: 0x3a332c, emissiveIntensity: .4 })); rock.castShadow = true; scene.add(rock);

// ---------------------------------------------------------------- Jeremys (scale .75 ≈ 1.75 m label)
const J1 = K.J, J2 = makeJeremy2(), J3 = makeJeremy2(), J4 = makeJeremy2(); [J2, J3, J4].forEach(j => { scene.add(j); rimLight(j); });
const putJ = (J, x, z, ry, pose) => { J.visible = true; J.position.set(x, 0, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose); };

// ---------------------------------------------------------------- timeline (from the voiceover)
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), endAt = T0[8] + 1.2;
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const CAM = [ // [target x, y, z, dist, yaw, pitch]
  [X.A - .15, 1.2, 0, 13.2, -.3, .16], [X.A - .15, 1.25, 0, 13.0, -.26, .15], [X.A - .05, 1.15, 0, 13.0, -.22, .14], [X.A + .35, 1.3, 0, 8.6, -.2, .14], [X.B - .3, 1.0, 0, 12.2, -.3, .16],
  [X.C + .45, 1.2, 0, 10.4, -.32, .16], [X.C + .4, 1.25, 0, 9.8, -.28, .15], [X.D + .5, 1.2, 0, 11.8, -.3, .2], [X.D + .5, 1.2, 0, 12.8, -.34, .22]];
function camAt(t) { let c = CAM[0].slice(); for (let i = 1; i < CAM.length; i++) { const k = eInOut(clamp((t - (T0[i] - .8)) / 1.3)); if (k <= 0) break; c = c.map((v, j) => lerp(v, CAM[i][j], k)); } return c; }
const HUDS = [ // [l1, n1, THIS PART IS, l3, value]
  ['MOONS', '1', 'FACT', "MOON'S WIDTH", '3,474 km'], ['MOONS', '1', 'FACT', "MOON'S WIDTH", '3,474 km'], ['MOONS', '2', 'PHYSICS', 'TIDAL PULL OF THE TWIN', '8×'],
  ['MOONS', '2', 'PHYSICS', 'SIZE IN THE SKY', '4× bigger'], ['MOONS', '2', 'SPECULATION', 'TIDES', 'Far bigger'], ['REAL LIFE', 'Long ago', 'THEORY', 'MOONS, BILLIONS OF YEARS AGO', 'Maybe 2'],
  ['REAL LIFE', 'Long ago', 'THEORY', 'SECOND MOON', '≈1,200 km'], ['REAL LIFE', '2024', 'FACT', 'MINI-MOON 2024 PT5', '≈10 m'], ['REAL LIFE', '2024', 'FACT', 'MINI-MOON 2024 PT5', '≈10 m']];
const tTwin0 = T0[2] + .3, tTwin1 = T0[2] + 2.0;        // the twin moon grows in at half the distance
const tBar0 = T0[2] + 3.4, tBar1 = T0[2] + 6.4;         // 8x bar rises
const tHit0 = T0[6] + .6, tHit = T0[6] + 4.4, tHit1 = T0[6] + 7.0; // slow approach, contact, spread
const tPT0 = T0[7] + .3, tPT1 = T1[7] + 1.6;             // mini-moon passes
window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: total, name: 'room', gain: .1 }, { t0: T0[4] - .4, t1: T1[4] + .4, name: 'drip', gain: .12 }],
  sfx: [{ t: 1.0, name: 'swell', gain: .3 }, ...[4, 5, 7].map(i => ({ t: T0[i] - .85, name: 'glide', gain: .26 })), { t: tTwin0 + .1, name: 'chime', gain: .22 }, { t: tBar0, name: 'swell', gain: .22 }, { t: tBar1 - .2, name: 'ding', gain: .22 },
    { t: T0[3] + .6, name: 'chime', gain: .16 }, { t: T0[4] + 1.6, name: 'splash', gain: .16 }, { t: T0[4] + 3.4, name: 'rumble_low', gain: .22 }, { t: T0[5] + .2, name: 'chime', gain: .28 },
    { t: tHit0 + .4, name: 'swell', gain: .24 }, { t: tHit, name: 'rumble_low', gain: .3 }, { t: tPT0 + .2, name: 'hiss', gain: .12 }, { t: endAt, name: 'chime', gain: .3 }] };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), lt = t - T0[i], ld = T1[i] - T0[i];
  // ---- A. orrery: Moon to the left (slow), the twin to the right at half the distance (twice as fast)
  A.E.rotation.y = 2.2 + t * .08;
  const angM = Math.PI * .75 + Math.sin(t * .05) * .05, angT = -.75 + t * .012;
  armA1.rotation.y = angM; moonA.position.copy(moonAt(LA1, angM)); moonA.rotation.y = -angM + 1.5;
  const tw = eOut(clamp((t - tTwin0) / (tTwin1 - tTwin0))); armA2.rotation.y = angT; armA2.scale.set(tw, 1, 1); armA2.visible = tw > .01;
  twinA.position.copy(moonAt(LA2 * tw + .0001, angT)); twinA.scale.setScalar(Math.max(.001, tw)); twinA.visible = tw > .01; twinA.rotation.y = -angT + 1.5;
  const night = eInOut(clamp((t - (T0[3] + .4)) / 1.2)) * (1 - eInOut(clamp((t - (T1[3] + .2)) / .8)));
  twinMat.emissiveIntensity = .3 + 1.4 * night; twinA.scale.multiplyScalar(1 + .08 * night);
  const bk = eInOut(clamp((t - tBar0) / (tBar1 - tBar0)));
  bars[0].scale.y = BAR1; bars[0].position.y = .45 + BAR1 / 2; const h8 = BAR1 * lerp(1, 8, bk) * Math.max(.001, clamp((t - (tBar0 - .6)) / .4)); bars[1].scale.y = Math.max(.001, h8); bars[1].position.y = .45 + h8 / 2;
  // ---- B. tides: normal tide oscillates under the high-tide mark; speculation surge floods the houses, then ebbs
  const surge = eInOut(clamp((t - (T0[4] + 1.4)) / 2.2)) * (1 - eInOut(clamp((t - (T1[4] + .6)) / 1.6)));
  const lvl = lerp(.2 + .14 * (.5 + .5 * Math.sin(t * 1.1)), .74, surge); tideW.scale.y = lvl; tideW.position.y = .56 + lvl / 2;
  houses.forEach((h, k) => { h.rotation.z = Math.sin(t * 2 + k) * .03 * surge; });
  // ---- C. collision: slow approach, squash into the Moon, crust spreads over that side
  moonC.rotation.y = .4 + t * .03;
  const ap = eInOut(clamp((t - tHit0) / (tHit - tHit0))); const start = V(X.C, CY, 0).addScaledVector(V(-1.3, .25, .75).normalize(), 1.45), contact = V(X.C, CY, 0).addScaledVector(IMP, CR + SR * .9);
  const sp = clamp((t - tHit) / (tHit1 - tHit)), spE = eOut(sp);
  smallC.position.copy(start).lerp(contact, ap); smallC.visible = t > tHit0 - .6 && sp < .98; smallC.material.transparent = sp > 0; smallC.material.opacity = 1 - spE;
  if (sp > 0) { smallC.position.addScaledVector(IMP, -SR * .7 * spE); smallC.quaternion.setFromUnitVectors(V(0, 1, 0), IMP); smallC.scale.set(1 + spE * 1.2, Math.max(.05, 1 - spE * .95), 1 + spE * 1.2); } else { smallC.scale.setScalar(1); smallC.quaternion.identity(); }
  smallC.material.opacity *= clamp((t - (tHit0 - .6)) / .5);
  setCrust(sp > 0 ? Math.round(1.05 * spE * 200) / 200 : 0);
  // ---- D. mini-moon passes along the loop
  D.E.rotation.y = 3.6 + t * .06; const pk = clamp((t - tPT0) / (tPT1 - tPT0)); const pkE = pk; // steady speed
  pathMesh.geometry.setDrawRange(0, Math.floor(PATH_IDX * pkE / 3) * 3); pathMesh.visible = pk > 0;
  rock.visible = pk > 0 && pk < 1; rock.position.copy(curve.getPointAt(Math.min(.999, pkE))); rock.rotation.set(t * .7, t * .5, 0);
  // ---- Jeremys
  const bl = p => (t % p) < .1;
  putJ(J1, X.A - 1.6, -.25, .35, { expr: i === 2 && tw > .5 ? 'shocked' : 'happy', look: .4, armL: .25, armR: i === 1 ? 1.2 : .25, blink: bl(2.7) });
  putJ(J2, X.B - 1.6, -.85, .4, { expr: surge > .4 ? 'shocked' : 'happy', look: .5, armL: .25, armR: i === 4 && surge < .3 ? 1.1 : .25, blink: bl(2.9) });
  putJ(J3, X.C + 1.35, -.85, -.5, { expr: sp > 0 && sp < .7 ? 'shocked' : 'happy', look: -.5, armL: .25, armR: i === 5 ? 1.2 : .25, blink: bl(3.1) });
  putJ(J4, X.D + 1.6, -1.1, -.5, { expr: i >= 8 ? 'confused' : 'happy', look: -.5, armL: .25, armR: i === 8 ? 1.3 : .25, tilt: i >= 8 ? .1 : 0, blink: bl(2.3) });
  // ---- camera
  const c = camAt(t), drift = clamp(lt / Math.max(ld, 1));
  const tgt = V(c[0], c[1], c[2]), dist = c[3] * (1 - .035 * drift);
  orbit(tgt, dist, { yaw: c[4] + .04 * drift + t * .002, pitch: c[5], fov: 34, lookUp: .075 });
  shadowFit(tgt, 4.2); DOF.on = true; DOF.focus = dist; DOF.aperture = .55; DOF.maxR = 9;
  // ---- tags (orbit() first)
  const Al = (t0, t1) => clamp((t - t0) / .35) * clamp((t1 - t) / .3);
  if (i === 0) tag3('JEREMY', '1.75 m', V(X.A - 1.6, 2.3, -.25), Al(.6, T0[1] - .7));
  if (i === 1) { tag3('MOON', '3,474 km wide', moonA.position.clone().add(V(0, MRA + .08, 0)), Al(T0[1] + .8, T0[2] - .5)); tag3('EARTH', '12,742 km wide', V(X.A, AY + AR + .1, 0), Al(T0[1] + 2.4, T0[2] - .5)); }
  if (i === 2) { tag3('TWIN MOON', 'half the distance', twinA.position.clone().add(V(0, MRA + .08, 0)), Al(tTwin1 - .3, tBar0 + .4)); tag3('TIDAL PULL', '1× vs 8×', V(BARX + .2, .45 + h8 + .08, .2), Al(tBar0 + .8, T0[3] - .4)); }
  if (i === 3) tag3('LOOKS 4× BIGGER', '4× the moonlight', twinA.position.clone().add(V(0, MRA + .08, 0)), Al(T0[3] + .7, T0[4] - .7));
  if (i === 4) tag3('SPECULATION', 'coast under water', V(X.B + .85, 1.45, .2), Al(T0[4] + 2.6, T0[5] - .6));
  if (i === 5) tag3('OUR MOON', '3,474 km', V(X.C, CY + CR + .08, 0), Al(T0[5] + .8, T0[6] + .8));
  if (i === 6) { tag3('SECOND MOON', '≈1,200 km · theory', smallC.position.clone().add(V(0, SR + .08, 0)), Al(T0[6] + .7, tHit - .3)); tag3('FAR-SIDE HIGHLANDS', 'one explanation', V(X.C, CY, 0).addScaledVector(IMP, CR + .05).add(V(0, .25, 0)), Al(tHit1 - 1.4, T0[7] - .5)); }
  if (i >= 7) { tag3('2024 PT5', '≈10 m · enlarged', rock.visible ? rock.position.clone().add(V(0, .1, 0)) : curve.getPointAt(.999).add(V(0, .1, 0)), Al(T0[7] + 1.2, T1[7] - .2)); tag3('EARTH', 'it tagged along 2 months', V(X.D - .2, DY + DR + .1, 0), Al(T1[7] - .1, endAt - .1)); }
  tagsEnd();
  // ---- HUD
  const H = HUDS[i], endK = clamp((t - endAt) / .35), endIn = clamp((t - endAt - .35) / .45);
  let l3 = H[3], val = H[4];
  if (i === 1 && lt > 3.6) { l3 = 'DISTANCE'; val = '384,400 km'; }
  if (i === 2) { if (t < tBar0) { l3 = 'TWIN AT'; val = '192,200 km'; } else val = lerp(1, 8, bk).toFixed(bk < 1 ? 1 : 0).replace('.0', '') + '×'; }
  if (i === 7 && lt > 3.2) { l3 = 'TIME WITH EARTH'; val = '≈2 months'; }
  const fadeIn = clamp(lt / .25);
  setHUD({ q: 'What if Earth had <b>two moons</b>?', qA: clamp((t - .2) / .4) * (1 - endK), l1: H[0], n1: H[1], l2: 'THIS PART IS', n2: H[2], l3, val,
    line: i === 0 ? '' : LN[i].show, lineA: fadeIn * clamp((T1[i] + .25 - t) / .2 + (i === 8 ? 9 : 0)), dataA: (1 - endK),
    end: 'What would <b>you</b> name<br>the second moon? 👇', endA: endIn });
  $('v5n2').style.color = H[2] === 'SPECULATION' || H[2] === 'THEORY' ? ACCENT : '#fff';
  draw();
};
window.READY = true;
