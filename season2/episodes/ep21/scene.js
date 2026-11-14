// Episode 21 — What if all the oceans disappeared?  (v5.1 premium studio look + AI voiceover; one continuous gallery glide, structure from ep13/ep18)
// Everything is timed to the narration (vo.json written by tools/narrate.py from vo_lines.json).
// Facts (checked 2026-11-15):
//  - the ocean covers ~71% of Earth's surface and holds ~96.5-97% of Earth's water (USGS Water Science School "How much water is there on Earth?";
//    NOAA Ocean Service).
//  - average ocean depth ≈ 3,682 m (NOAA Ocean Service "How deep is the ocean?") -> "3.7 km".
//  - Challenger Deep, Mariana Trench ≈ 10,935 m (NOAA Ocean Exploration "How deep is the ocean?"); Everest 8,849 m (2020 China–Nepal survey)
//    -> 10,935 − 8,849 = 2,086 m to spare ("2 km").
//  - Mauna Kea ≈ 10,210 m from its base on the sea floor to the summit (4,207 m above sea level) (USGS / NOAA) -> "over 10 km".
//  - marine phytoplankton produce roughly half (estimates 50-80%) of Earth's oxygen (NOAA Ocean Service "How much oxygen comes from the ocean?").
//  - most evaporation that feeds rain comes from the ocean (~86%, NASA water cycle); "rain would nearly stop" is labelled SPECULATION / "our guess".
//  - all of Earth's water (oceans, ice, groundwater, lakes, rivers, atmosphere) ≈ 1,386,000 km³ -> a sphere ≈ 1,385 km in diameter
//    (USGS "How much water is there on Earth?"); Moon diameter 3,474 km, Earth 12,742 km (NASA).
import { THREE, RoundedBoxGeometry, scene, camera, clamp, lerp, eOut, eInOut, K, rimLight } from './kit.js';
import { key, hemi, DOF, draw, renderer, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd } from './studio.js';
import { makeJeremy2 } from './jeremy2.js';

await bootStudio('WHAT IF THE OCEANS DISAPPEARED?', 'EP. 21');
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
const X = { globe: 0, prof: 8, tank: 16, ball: 24 };
const TL = new THREE.TextureLoader();
const earthImg = await TL.loadAsync('./assets/planets/earth_atmos_2048.jpg'); earthImg.colorSpace = THREE.SRGBColorSpace; earthImg.anisotropy = 8;
const earthN = await TL.loadAsync('./assets/planets/earth_normal_2048.jpg');
const moonImg = await TL.loadAsync('./assets/planets/moon_1024.jpg'); moonImg.colorSpace = THREE.SRGBColorSpace;
// Earth material whose oceans can be drained: ocean pixels (blue-dominant) fade to a sculpted sea-floor colour as uDrain goes 0 -> 1
function drainEarthMat() {
  const m = new THREE.MeshStandardMaterial({ map: earthImg, normalMap: earthN, roughness: .6 }); const U = { uDrain: { value: 0 } }; m.userData.U = U;
  m.onBeforeCompile = sh => { sh.uniforms.uDrain = U.uDrain;
    sh.fragmentShader = 'uniform float uDrain;\n' + sh.fragmentShader.replace('#include <map_fragment>', `#include <map_fragment>
      { vec3 c = diffuseColor.rgb; float ocean = smoothstep(.015, .06, c.b - max(c.r, c.g) * .9) * (1. - smoothstep(.35, .6, max(c.r, c.g)));
        vec2 q = vMapUv * vec2(90., 45.); float n = .5 + .25 * sin(q.x * 1.3 + sin(q.y * 1.7)) * cos(q.y * 1.1 + sin(q.x * .7)) + .25 * sin(q.x * 3.1 - q.y * 2.3) * .5;
        float depthTone = clamp(c.b * 3.2, 0., 1.); // the texture is darker over deep water: reuse it as a depth hint
        vec3 floorC = mix(vec3(.20, .17, .15), vec3(.62, .53, .42), clamp(n * .6 + (1. - depthTone) * .5, 0., 1.));
        diffuseColor.rgb = mix(c, floorC, ocean * uDrain); }`)
      .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\n totalEmissiveRadiance += diffuseColor.rgb * .5;'); };
  return m; }
const earthMatA = drainEarthMat(), earthMatD = drainEarthMat();

// ---------------------------------------------------------------- A. globe on a brass stand (oceans drain in lines 1-2)
const GY = 1.75, GR = .72; const globeA = new THREE.Group();
{ const g = new THREE.Group(); g.add(plinth(2.0, 2.0, .55));
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(.42, .5, .07, 64), darkIron); disc.position.y = .585;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, GY - GR - .62, 20), brass); post.position.y = .62 + (GY - GR - .62) / 2;
  const E = new THREE.Mesh(new THREE.SphereGeometry(GR, 128, 96), earthMatA); globeA.add(E); globeA.position.y = GY; globeA.rotation.z = .41;
  const axis = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, GR * 2 + .4, 12), brass); globeA.add(axis);
  const mer = new THREE.Mesh(new THREE.TorusGeometry(GR + .09, .014, 12, 160, Math.PI), brass); mer.position.y = GY; mer.rotation.z = Math.PI / 2 + .41; mer.rotation.y = Math.PI / 2;
  g.add(disc, post, globeA, mer); g.position.x = X.globe; scene.add(shadowAll(g)); }

// ---------------------------------------------------------------- B. ocean cross-section: land with Everest, abyssal plain, Mauna Kea, the Mariana Trench (true vertical scale, 8 cm per km)
const KM = .08, PB = .62, SL = PB + 11.3 * KM; // sea level height in the model (plinth top at .55)
const prof = [[-1.6, 1.2], [-1.35, 2.2], [-1.1, 8.849], [-.95, 5.0], [-.8, 2.0], [-.62, .4], [-.5, -.15], [-.4, -2.6], [-.3, -4.6], [-.1, -5.6], [.0, -5.7], [.1, -4.0], [.28, 4.207], [.46, -4.0], [.58, -5.7],
  [.8, -5.9], [.95, -7.5], [1.1, -10.935], [1.25, -8.2], [1.4, -6.4], [1.6, -6.2]]; // [x in m, height in km]
const hAt = x => { for (let k = 1; k < prof.length; k++) if (x <= prof[k][0]) { const [x0, h0] = prof[k - 1], [x1, h1] = prof[k]; return lerp(h0, h1, (x - x0) / (x1 - x0)); } return prof[prof.length - 1][1]; };
const smoothH = x => { let s = 0, w = 0; for (let k = -3; k <= 3; k++) { const ww = 1 / (1 + k * k); s += hAt(clamp(x + k * .012, -1.6, 1.6)) * ww; w += ww; } return s / w; };
const PD = .55; let waterB, ghost;
{ const g = new THREE.Group(); g.add(plinth(3.5, .9, .55));
  const rockTex = canvasTex(1024, 512, (ctx, w, h) => { const r = rand(3); ctx.fillStyle = '#7d6e5f'; ctx.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 2) { const v = Math.sin(y * .07) * 10 + (r() - .5) * 14; ctx.fillStyle = `rgba(${120 + v},${104 + v},${88 + v},.5)`; ctx.fillRect(0, y, w, 2); }
    for (let i = 0; i < 3000; i++) { const v = r() * 50 - 25; ctx.fillStyle = `rgba(${90 + v},${80 + v},${70 + v},.35)`; ctx.fillRect(r() * w, r() * h, 3, 2); } }).tex;
  const shp = new THREE.Shape(); shp.moveTo(-1.6, 0); for (let k = 0; k <= 320; k++) { const x = -1.6 + k / 320 * 3.2; shp.lineTo(x, SL - PB + smoothH(x) * KM); } shp.lineTo(1.6, 0); shp.closePath();
  const slab = new THREE.Mesh(new THREE.ExtrudeGeometry(shp, { depth: PD, bevelEnabled: true, bevelSize: .008, bevelThickness: .008, bevelSegments: 2, curveSegments: 4 }),
    new THREE.MeshStandardMaterial({ map: rockTex, roughness: .9 }));
  slab.geometry.computeBoundingBox(); slab.position.set(0, PB, -PD / 2); g.add(slab);
  // snow caps: a thin lighter extrusion over the top of Everest and Mauna Kea
  const cap = (x0, x1, minH) => { const s = new THREE.Shape(); let first = true; const pts = []; for (let k = 0; k <= 60; k++) { const x = x0 + k / 60 * (x1 - x0); const hh = smoothH(x); if (hh >= minH) pts.push([x, hh]); }
    if (pts.length < 3) return; s.moveTo(pts[0][0], SL - PB + pts[0][1] * KM - .004); pts.forEach(([x, hh]) => s.lineTo(x, SL - PB + hh * KM + .006)); for (let k = pts.length - 1; k >= 0; k--) s.lineTo(pts[k][0], SL - PB + Math.max(minH, pts[k][1] - 1.1) * KM);
    const m = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: PD + .02, bevelEnabled: false }), new THREE.MeshStandardMaterial({ color: 0xf3f4f6, roughness: .6 })); m.position.set(0, PB, -PD / 2 - .01); g.add(m); };
  cap(-1.35, -.9, 6.0); cap(.18, .38, 3.2);
  // sea-level line (brass) across the back
  const sl = new THREE.Mesh(new THREE.BoxGeometry(3.25, .008, .008), brass); sl.position.set(0, SL, -PD / 2 - .02); g.add(sl);
  // water: box from the sea floor up to the (animated) level, over the ocean part only
  waterB = new THREE.Mesh(new THREE.BoxGeometry(2.12, 1, PD + .04), new THREE.MeshPhysicalMaterial({ color: 0x1f6f9c, roughness: .06, clearcoat: 1, transparent: true, opacity: .72, depthWrite: false }));
  waterB.position.set(.54, 0, 0); g.add(waterB);
  // ghost Everest (orange, translucent) that drops into the trench
  const gs = new THREE.Shape(); gs.moveTo(-.16, 0); gs.lineTo(-.06, .5 * 8.849 * KM); gs.lineTo(0, 8.849 * KM); gs.lineTo(.05, .62 * 8.849 * KM); gs.lineTo(.16, 0); gs.closePath();
  ghost = new THREE.Mesh(new THREE.ExtrudeGeometry(gs, { depth: .02, bevelEnabled: false }), new THREE.MeshBasicMaterial({ color: ACCENT, transparent: true, opacity: 0, toneMapped: false, depthWrite: false })); ghost.position.z = PD / 2 + .03; g.add(ghost);
  g.position.x = X.prof; scene.add(shadowAll(g)); waterB.castShadow = false; ghost.castShadow = false; }
const kaLine = new THREE.Mesh(new THREE.CylinderGeometry(.006, .006, 1, 8), accentM); scene.add(kaLine);

// ---------------------------------------------------------------- C. plankton tank (green water, oxygen bubbles) + a little island with trees under a rain cloud
const CW = 2.4; let tankWater; const bubbles = [], plankton = [], drops = [], crowns = []; let cloud;
{ const g = new THREE.Group(); g.add(plinth(2.7, 1.2, .55));
  const tank = new THREE.Mesh(new THREE.BoxGeometry(1.3, .8, .9), glass); tank.position.set(-.55, .55 + .4, 0); g.add(tank);
  for (const [x, z] of [[-1.2, -.45], [-1.2, .45], [.1, -.45], [.1, .45]]) { const c = new THREE.Mesh(new THREE.BoxGeometry(.025, .8, .025), brass); c.position.set(x, .95, z); g.add(c); }
  tankWater = new THREE.Mesh(new THREE.BoxGeometry(1.26, 1, .86), new THREE.MeshPhysicalMaterial({ color: 0x3f8f72, roughness: .08, clearcoat: 1, transparent: true, opacity: .55, depthWrite: false })); tankWater.position.x = -.55; g.add(tankWater);
  const r = rand(5);
  for (let i = 0; i < 70; i++) { const p = new THREE.Mesh(new THREE.SphereGeometry(.006 + r() * .006, 8, 6), new THREE.MeshStandardMaterial({ color: 0x9fdc6a, emissive: 0x5fae3a, emissiveIntensity: .5 })); p.userData = { x: -1.15 + r() * 1.2, y: r(), z: -.4 + r() * .8, s: r() * 6 }; g.add(p); plankton.push(p); }
  for (let i = 0; i < 26; i++) { const b = new THREE.Mesh(new THREE.SphereGeometry(.012 + r() * .01, 16, 12), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .05, transparent: true, opacity: .7, clearcoat: 1 })); b.userData = { x: -1.1 + r() * 1.1, z: -.35 + r() * .7, ph: r(), v: .5 + r() * .5 }; g.add(b); bubbles.push(b); }
  // island (right half of the plinth): soil mound + three smooth trees
  const mound = new THREE.Mesh(new THREE.SphereGeometry(.55, 64, 24, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0x6d5a43, roughness: 1 })); mound.scale.set(1, .22, .8); mound.position.set(.75, .55, 0); g.add(mound);
  const trunkM = new THREE.MeshStandardMaterial({ color: 0x5a4330, roughness: .9 });
  for (const [x, z, s] of [[.6, -.15, 1], [.92, .12, .8], [.78, .3, .65]]) { const tr = new THREE.Mesh(new THREE.CylinderGeometry(.02 * s, .03 * s, .3 * s, 12), trunkM); tr.position.set(x, .62 + .15 * s, z); g.add(tr);
    const cm = new THREE.MeshStandardMaterial({ color: 0x4f8a3a, roughness: .8 }); for (let k = 0; k < 4; k++) { const c = new THREE.Mesh(new THREE.SphereGeometry(.1 * s, 32, 20), cm); c.position.set(x + Math.cos(k * 2.1) * .06 * s, .62 + .36 * s + (k === 3 ? .07 * s : 0), z + Math.sin(k * 2.1) * .06 * s); g.add(c); } crowns.push(cm); }
  // rain cloud on a thin brass arm
  cloud = new THREE.Group(); const cmat = new THREE.MeshStandardMaterial({ color: 0xf2f3f5, roughness: .95, transparent: true });
  for (const [x, y, s] of [[-.2, 0, .16], [0, .06, .2], [.2, 0, .15], [.08, -.04, .14], [-.1, -.04, .13]]) { const c = new THREE.Mesh(new THREE.SphereGeometry(s, 32, 20), cmat); c.position.set(x, y, 0); cloud.add(c); }
  cloud.position.set(.75, 1.95, 0); g.add(cloud);
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(.012, .016, 1.45, 12), brass); pole.position.set(1.25, .55 + .72, -.4); const arm = new THREE.Mesh(new THREE.CylinderGeometry(.01, .01, .5, 10), brass); arm.rotation.z = Math.PI / 2; arm.position.set(1.0, 2.0, -.4); g.add(pole, arm);
  const dm = new THREE.MeshBasicMaterial({ color: 0xbfd9ff, transparent: true, opacity: .8, toneMapped: false });
  for (let i = 0; i < 40; i++) { const d = new THREE.Mesh(new THREE.CylinderGeometry(.003, .003, .06, 6), dm); d.userData = { x: .5 + r() * .5, z: -.2 + r() * .4, ph: r() }; g.add(d); drops.push(d); }
  g.position.x = X.tank; scene.add(shadowAll(g)); tank.castShadow = tankWater.castShadow = false; drops.forEach(d => d.castShadow = false); bubbles.forEach(b => b.castShadow = false); cloud.traverse(o => o.castShadow = false); }

// ---------------------------------------------------------------- D. the twist: Earth vs one ball of all its water vs the Moon (true relative sizes)
const DY = 1.6, DR = .62; const globeD = new THREE.Group(); let waterBall, moonBall; const WR = DR * 1385 / 12742, MR = DR * 3474 / 12742;
const WPOS = V(X.ball + 1.05, 1.15, .45), MPOS = V(X.ball + 1.5, 1.15, -.15);
{ const g = new THREE.Group(); g.add(plinth(1.8, 1.8, .55));
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(.4, .48, .07, 64), darkIron); disc.position.y = .585;
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, DY - DR - .62, 20), brass); post.position.y = .62 + (DY - DR - .62) / 2;
  const E = new THREE.Mesh(new THREE.SphereGeometry(DR, 128, 96), earthMatD); globeD.add(E); globeD.position.y = DY; globeD.rotation.z = .41;
  g.add(disc, post, globeD); g.position.x = X.ball - .3; scene.add(shadowAll(g));
  const side = new THREE.Group(); side.add(plinth(1.0, 1.1, .7)); side.position.set(X.ball + 1.3, 0, .15); scene.add(shadowAll(side));
  for (const p of [WPOS, MPOS]) { const s = new THREE.Mesh(new THREE.CylinderGeometry(.01, .014, p.y - .7, 12), brass); s.position.set(p.x, .7 + (p.y - .7) / 2, p.z); s.castShadow = true; scene.add(s); }
  waterBall = new THREE.Mesh(new THREE.SphereGeometry(WR, 64, 48), new THREE.MeshPhysicalMaterial({ color: 0x2a8fd0, roughness: .05, clearcoat: 1, emissive: 0x0d4f80, emissiveIntensity: .6 })); waterBall.castShadow = true; scene.add(waterBall);
  moonBall = new THREE.Mesh(new THREE.SphereGeometry(MR, 64, 48), new THREE.MeshStandardMaterial({ map: moonImg, roughness: 1, emissive: 0xffffff, emissiveMap: moonImg, emissiveIntensity: .25 })); moonBall.position.copy(MPOS); moonBall.castShadow = true; scene.add(moonBall); }

// ---------------------------------------------------------------- Jeremys (scale .75 ≈ 1.75 m label)
const J1 = K.J, J2 = makeJeremy2(), J3 = makeJeremy2(), J4 = makeJeremy2(); [J2, J3, J4].forEach(j => { scene.add(j); rimLight(j); });
const putJ = (J, x, z, ry, pose) => { J.visible = true; J.position.set(x, 0, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose); };

// ---------------------------------------------------------------- timeline (from the voiceover)
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), endAt = T0[9] + 1.2;
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const CAM = [ // [target x, y, dist, yaw, pitch]
  [X.globe + .3, 1.25, 10.8, -.45, .18], [X.globe + .2, 1.3, 9.8, -.38, .16], [X.globe + .2, 1.3, 9.4, -.32, .16], [X.prof + .2, 1.15, 12.0, -.22, .12], [X.prof + .2, 1.15, 11.6, -.18, .12],
  [X.tank + .1, 1.05, 10.6, -.4, .16], [X.tank + .2, 1.05, 10.0, -.34, .16], [X.ball + .3, 1.05, 11.0, -.42, .16], [X.ball + .4, 1.0, 10.2, -.34, .14], [X.ball + .3, 1.05, 11.8, -.4, .18]];
function camAt(t) { let c = CAM[0].slice(); for (let i = 1; i < CAM.length; i++) { const k = eInOut(clamp((t - (T0[i] - .8)) / 1.3)); if (k <= 0) break; c = c.map((v, j) => lerp(v, CAM[i][j], k)); } return c; }
const HUDS = [ // [l1, n1, THIS PART IS, l3, value]
  ['THE OCEANS', 'Full', 'FACT', 'SURFACE COVERED', '71%'], ['THE OCEANS', 'Full', 'FACT', 'SURFACE COVERED', '71%'], ['THE OCEANS', 'Draining', 'FACT', 'AVERAGE DEPTH', '3.7 km'],
  ['THE OCEANS', 'Gone', 'FACT', 'DEEPEST POINT', '10,935 m'], ['THE OCEANS', 'Gone', 'FACT', 'MAUNA KEA, BASE TO PEAK', '10,210 m'], ['THE OCEANS', 'Gone', 'FACT', 'OXYGEN FROM OCEAN PLANKTON', 'About 50%'],
  ['THE OCEANS', 'Gone', 'SPECULATION', 'RAIN', 'Nearly stops'], ['REAL LIFE', 'Today', 'FACT', "EARTH'S WIDTH", '12,742 km'], ['REAL LIFE', 'Today', 'FACT', 'ALL ITS WATER, AS ONE BALL', '1,385 km'], ['REAL LIFE', 'Today', 'FACT', 'ALL ITS WATER, AS ONE BALL', '1,385 km']];
const tDrainA0 = T0[2] + .2, tDrainA1 = T0[2] + 4.2;            // globe drains while "Drain them..."
const tDrainB0 = T0[3] - .5, tDrainB1 = T0[3] + 2.4;          // cross-section drains on arrival
const tGhost0 = T0[3] + 3.6, tGhost1 = T0[3] + 5.4;           // Everest drops into the trench ("would fit inside")
const tBall0 = T0[8] + 2.6, tBall1 = T0[8] + 5.2;             // the water leaves the globe and gathers into a ball
window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: total, name: 'room', gain: .1 }, { t0: tDrainA0 - .3, t1: tDrainA1 + .3, name: 'drip', gain: .14 }, { t0: T0[6] - .5, t1: T0[6] + 2.5, name: 'drip', gain: .14 }],
  sfx: [{ t: 1.0, name: 'swell', gain: .3 }, ...[3, 5, 7].map(i => ({ t: T0[i] - .85, name: 'glide', gain: .26 })), { t: tDrainA0, name: 'hiss', gain: .18 }, { t: tDrainA0 + .2, name: 'swell', gain: .24 },
    { t: tDrainB0 + .4, name: 'hiss', gain: .14 }, { t: tGhost1 - .1, name: 'ding', gain: .22 }, { t: T0[4] + 1.6, name: 'chime', gain: .2 }, { t: T0[5] + .8, name: 'pops', gain: .14 },
    { t: T0[6] + 2.8, name: 'rumble_low', gain: .25 }, { t: T0[7] + .2, name: 'chime', gain: .28 }, { t: tBall0, name: 'swell', gain: .3 }, { t: tBall1, name: 'splash', gain: .18 }, { t: endAt, name: 'chime', gain: .3 }] };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';
const wp = new THREE.Vector3();

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), lt = t - T0[i], ld = T1[i] - T0[i];
  // ---- A. globe turns slowly; oceans drain
  globeA.children[0].rotation.y = 3.3 + t * .06; earthMatA.userData.U.uDrain.value = eInOut(clamp((t - tDrainA0) / (tDrainA1 - tDrainA0)));
  // ---- B. cross-section: water level drops from sea level to nothing; ghost Everest drops into the trench; Mauna Kea measure line
  const bk = eInOut(clamp((t - tDrainB0) / (tDrainB1 - tDrainB0))); const lvl = lerp(SL, PB + .02, bk); const bot = PB;
  waterB.scale.y = Math.max(.001, lvl - bot); waterB.position.y = bot + (lvl - bot) / 2; waterB.visible = lvl - bot > .01;
  const gk = eInOut(clamp((t - tGhost0) / (tGhost1 - tGhost0))); const gVis = clamp((t - (tGhost0 - .5)) / .4) * (1 - clamp((t - (T0[4] + .6)) / .5));
  const g0 = V(-1.1, SL - PB + 0 * KM, 0), g1 = V(1.1, SL - PB - 10.935 * KM, 0); // ghost base: from Everest's sea-level base to the trench floor
  ghost.position.set(lerp(g0.x, g1.x, gk), PB + lerp(SL - PB, SL - PB - 10.935 * KM, gk), PD / 2 + .03); ghost.material.opacity = .8 * gVis; ghost.visible = gVis > .01;
  const kk = eOut(clamp((t - (T0[4] + 1.6)) / 1.2)) * (1 - clamp((t - (T0[5] - .6)) / .4)); const kaB = SL - 6.0 * KM, kaT = SL + 4.207 * KM;
  kaLine.visible = kk > .01; kaLine.scale.y = Math.max(.001, (kaT - kaB) * kk); kaLine.position.set(X.prof + .28, kaB + (kaT - kaB) * kk / 2, PD / 2 + .04);
  // ---- C. tank drains, bubbles stop; rain stops and the trees turn brown (speculation)
  const tk = eInOut(clamp((t - (T0[5] + 2.4)) / 2.4)); const tl = lerp(.72, .03, tk); tankWater.scale.y = tl; tankWater.position.y = .56 + tl / 2;
  plankton.forEach(p => { const u = p.userData; p.position.set(u.x + Math.sin(t * .6 + u.s) * .02, .58 + Math.min(u.y * .66, tl - .03) + Math.sin(t + u.s) * .01, u.z); });
  bubbles.forEach(b => { const u = b.userData, k = (t * .25 * u.v + u.ph) % 1; b.position.set(u.x, .58 + k * tl, u.z); b.visible = tl > .08 && k * tl < tl - .02; });
  const rain = 1 - clamp((t - (T0[6] + 2.6)) / 1.0); const ck = 1 - eInOut(clamp((t - (T0[6] + 2.6)) / 2.5));
  drops.forEach(d => { const u = d.userData, k = (t * 1.6 + u.ph) % 1; d.position.set(u.x, 1.8 - k * 1.1, u.z); d.visible = rain > .02 && k < .95; d.material.opacity = .8 * rain; });
  cloud.children.forEach(c => c.material.opacity = .25 + .75 * ck); cloud.scale.setScalar(.75 + .25 * ck);
  const brown = eInOut(clamp((t - (T0[6] + 3.6)) / 2.0)); crowns.forEach(m => m.color.set(0x4f8a3a).lerp(new THREE.Color(0x9c7a45), brown));
  // ---- D. globe D keeps its oceans until the twist, then the water leaves and gathers into one small ball
  globeD.children[0].rotation.y = 3.0 + t * .05; const wk = eInOut(clamp((t - tBall0) / (tBall1 - tBall0)));
  earthMatD.userData.U.uDrain.value = wk; const wStart = V(X.ball - .3, DY, 0).addScaledVector(V(.75, 0, .66).normalize(), DR * .9);
  waterBall.position.copy(wStart).lerp(WPOS, wk); waterBall.position.y += Math.sin(Math.PI * wk) * .25; waterBall.scale.setScalar(Math.max(.001, wk)); waterBall.visible = wk > .001;
  // ---- Jeremys
  const bl = p => (t % p) < .1;
  putJ(J1, X.globe + 1.15, -.5, -.7, { expr: i === 2 ? 'shocked' : 'happy', look: -.4, armL: .25, armR: i === 1 ? 1.2 : .25, blink: bl(2.7) });
  putJ(J2, X.prof + 1.55, -.55, -.6, { expr: i === 4 ? 'shocked' : 'happy', look: -.6, armL: .25, armR: i === 3 ? 1.2 : .25, blink: bl(2.9) });
  putJ(J3, X.tank - .15, -1.05, -.45, { expr: i === 6 ? 'worried' : 'happy', look: -.5, armL: .25, armR: i === 5 ? 1.1 : .25, blink: bl(3.1) });
  putJ(J4, X.ball + .55, -.9, -.4, { expr: i >= 9 ? 'confused' : i === 8 && wk > .5 ? 'shocked' : 'happy', look: -.4, armL: .25, armR: i === 9 ? 1.3 : .25, tilt: i >= 9 ? .1 : 0, blink: bl(2.3) });
  // ---- camera
  const c = camAt(t), drift = clamp(lt / Math.max(ld, 1));
  const tgt = V(c[0], c[1], 0), dist = c[2] * (1 - .035 * drift);
  orbit(tgt, dist, { yaw: c[3] + .04 * drift + t * .002, pitch: c[4], fov: 34, lookUp: .075 });
  shadowFit(tgt, 4.2); DOF.on = true; DOF.focus = dist; DOF.aperture = .55; DOF.maxR = 9;
  // ---- tags (orbit() first)
  const A = (t0, t1) => clamp((t - t0) / .35) * clamp((t1 - t) / .3);
  if (i === 0) tag3('JEREMY', '1.75 m', V(X.globe + 1.15, 2.3, -.5), A(.6, T0[1] - .7));
  if (i === 2) tag3('SEA FLOOR', 'avg. 3.7 km down', V(X.globe - .25, GY + .1, GR * .8), A(tDrainA1 - .6, T0[3] - .7));
  if (i === 3) { tag3('EVEREST', '8,849 m', V(X.prof - 1.1, SL + 8.849 * KM + .05, 0), A(T0[3] + 1.0, T0[4] - .7)); tag3('CHALLENGER DEEP', '10,935 m deep', V(X.prof + 1.1, SL - 10.935 * KM + .05, PD / 2), A(T0[3] + 2.2, T0[4] - .7)); }
  if (i === 4) { tag3('MAUNA KEA', '10,210 m base to peak', V(X.prof + .28, SL + 4.207 * KM + .06, 0), A(T0[4] + 1.6, T0[5] - .7)); tag3('EVEREST', '8,849 m', V(X.prof - 1.1, SL + 8.849 * KM + .05, 0), A(T0[4] + .3, T0[5] - .7)); }
  if (i === 5) tag3('PLANKTON', '≈ half our oxygen', V(X.tank - .75, 1.0, .3), A(T0[5] + 1.0, T0[6] - .5));
  if (i === 6) tag3('SPECULATION', 'little rain left', V(X.tank + .75, 1.2, .3), A(T0[6] + 1.0, T0[7] - .6));
  if (i === 7) tag3('EARTH', '12,742 km wide', V(X.ball - .3, DY + DR + .05, 0), A(T0[7] + .9, T0[8] + 1.8));
  if (i >= 8) { tag3('ALL ITS WATER', '1,385 km', WPOS.clone().add(V(0, WR + .03, 0)), A(tBall1 - .2, endAt - .1)); tag3('MOON', '3,474 km', MPOS.clone().add(V(0, MR + .38, 0)), A(tBall1 + .8, endAt - .1)); }
  tagsEnd();
  // ---- HUD
  const H = HUDS[i], endK = clamp((t - endAt) / .35), endIn = clamp((t - endAt - .35) / .45);
  let l3 = H[3], val = H[4];
  if (i === 1 && lt > 3.0) { l3 = 'SHARE OF ALL WATER'; val = '97%'; }
  if (i === 2) { const d = eInOut(clamp((t - tDrainA0) / (tDrainA1 - tDrainA0))); if (d < .99) { l3 = 'OCEANS LEFT'; val = Math.round(100 * (1 - d)) + '%'; } }
  if (i === 3 && t > tGhost0) { l3 = 'ROOM TO SPARE'; val = '2,086 m'; }
  const fadeIn = clamp(lt / .25);
  setHUD({ q: 'What if the oceans <b>disappeared</b>?', qA: clamp((t - .2) / .4) * (1 - endK), l1: H[0], n1: H[1], l2: 'THIS PART IS', n2: H[2], l3, val,
    line: i === 0 ? '' : LN[i].show, lineA: fadeIn * clamp((T1[i] + .25 - t) / .2 + (i === 9 ? 9 : 0)), dataA: (1 - endK),
    end: 'Where would <b>you</b><br>walk first? 👇', endA: endIn });
  $('v5n2').style.color = H[2] === 'FACT' ? '#fff' : ACCENT;
  draw();
};
window.READY = true;
