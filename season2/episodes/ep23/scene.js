// Episode 23 — What if Earth had two suns?  (v5.1 premium studio look + AI voiceover; one continuous gallery glide, structure from ep13/ep21)
// Everything is timed to the narration (vo.json written by tools/narrate.py from vo_lines.json).
// Facts (checked 2026-11-16):
//  - Raghavan et al. 2010, ApJS 190, 1 "A Survey of Stellar Families: Multiplicity of Solar-type Stars": 54-56% of solar-type stars are single,
//    i.e. ~44-46% have at least one stellar/brown-dwarf companion (33% double, 8% triple, 3% higher) -> "almost half", HUD "≈46%".
//  - Alpha Centauri A and B orbit their common centre of mass every ~79.9 years, 11.2-35.6 AU apart, 4.37 light-years away (EarthSky "Alpha Centauri").
//  - Kepler-16b: first confirmed planet orbiting two stars (announced Sept 2011, Science); Saturn-sized, orbits both stars every 229 days;
//    stars of 69% and 20% of the Sun's mass; ~200 light-years away (NASA JPL news "NASA's Kepler discovery confirms first planet orbiting two stars").
//  - a second identical Sun at the same distance doubles the sunlight (2 x ~1,361 W/m²). "Dozens of degrees hotter, oceans start to boil away" is OUR GUESS
//    (simple radiative estimate: temperature scales with flux^1/4 -> 2^0.25 ≈ 1.19 x 288 K ≈ +50 °C, ignoring feedbacks) -> labelled SPECULATION.
//  - the Sun brightens ~10% every billion years (Britannica "Sun – Evolution"); in roughly a billion years that is expected to be enough to boil away
//    Earth's oceans (McDonald Observatory StarDate "Brighter Sun"). It is about 25% brighter than when it formed (StarDate).
import { THREE, RoundedBoxGeometry, scene, camera, clamp, lerp, eOut, eInOut, K, rimLight } from './kit.js';
import { key, hemi, DOF, draw, renderer, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd } from './studio.js';
import { makeJeremy2 } from './jeremy2.js';

await bootStudio('WHAT IF EARTH HAD TWO SUNS?', 'EP. 23');
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
const glass = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .05, metalness: 0, transparent: true, opacity: .16, clearcoat: 1, depthWrite: false, side: THREE.DoubleSide });
const shadowAll = g => { g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };
function plinth(w, d, h) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, .03), marble); m.position.y = h / 2; m.castShadow = m.receiveShadow = true; return m; }
const X = { A: 0, B: 8, C: 16, D: 24, E: 32 };
const TL = new THREE.TextureLoader();
const earthImg = await TL.loadAsync('./assets/planets/earth_atmos_2048.jpg'); earthImg.colorSpace = THREE.SRGBColorSpace; earthImg.anisotropy = 8;
const earthN = await TL.loadAsync('./assets/planets/earth_normal_2048.jpg');
// Earth material whose oceans can boil away (from ep21): ocean pixels (blue-dominant) fade to a dry sea floor as uDrain goes 0 -> 1
function drainEarthMat() {
  const m = new THREE.MeshStandardMaterial({ map: earthImg, normalMap: earthN, roughness: .6 }); const U = { uDrain: { value: 0 } }; m.userData.U = U;
  m.onBeforeCompile = sh => { sh.uniforms.uDrain = U.uDrain;
    sh.fragmentShader = 'uniform float uDrain;\n' + sh.fragmentShader.replace('#include <map_fragment>', `#include <map_fragment>
      { vec3 c = diffuseColor.rgb; float ocean = smoothstep(.015, .06, c.b - max(c.r, c.g) * .9) * (1. - smoothstep(.35, .6, max(c.r, c.g)));
        vec2 q = vMapUv * vec2(90., 45.); float n = .5 + .25 * sin(q.x * 1.3 + sin(q.y * 1.7)) * cos(q.y * 1.1 + sin(q.x * .7)) + .25 * sin(q.x * 3.1 - q.y * 2.3) * .5;
        float depthTone = clamp(c.b * 3.2, 0., 1.);
        vec3 floorC = mix(vec3(.24, .18, .14), vec3(.66, .52, .38), clamp(n * .6 + (1. - depthTone) * .5, 0., 1.));
        diffuseColor.rgb = mix(c, floorC, ocean * uDrain); }`)
      .replace('#include <emissivemap_fragment>', '#include <emissivemap_fragment>\n totalEmissiveRadiance += diffuseColor.rgb * .5;'); };
  return m; }
// glowing star: granulated surface (unlit, bright enough to bloom) + soft additive halo sprite
const granTex = canvasTex(512, 256, (ctx, w, h) => { const r = rand(11); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, w, h);
  for (let i = 0; i < 9000; i++) { const g = 215 + r() * 40; ctx.fillStyle = `rgba(${g},${g * .93},${g * .84},.14)`; const s = 1 + r() * 2.5; ctx.beginPath(); ctx.arc(r() * w, r() * h, s, 0, 7); ctx.fill(); }
  for (let i = 0; i < 6; i++) { ctx.fillStyle = 'rgba(170,110,50,.10)'; ctx.beginPath(); ctx.arc(r() * w, h * (.3 + r() * .4), 4 + r() * 8, 0, 7); ctx.fill(); } }).tex;
const haloTex = canvasTex(256, 256, (ctx, w, h) => { const g = ctx.createRadialGradient(128, 128, 0, 128, 128, 128); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.25, 'rgba(255,255,255,.55)'); g.addColorStop(.55, 'rgba(255,255,255,.12)'); g.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex;
function star(r, col, glow = 2.2) { const g = new THREE.Group(); const c = new THREE.Color(col);
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 96, 64), new THREE.MeshBasicMaterial({ map: granTex, color: c.clone().multiplyScalar(glow), toneMapped: false })); g.add(m);
  const h = new THREE.Sprite(new THREE.SpriteMaterial({ map: haloTex, color: c, transparent: true, opacity: .7, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); h.scale.setScalar(r * 4.2); g.add(h);
  g.userData = { core: m, halo: h, r, glow, col: c }; return g; }
const setGlow = (s, k) => { s.userData.core.material.color.copy(s.userData.col).multiplyScalar(s.userData.glow * k); s.userData.halo.material.opacity = .7 * Math.min(1.5, k); };
function postAt(x, z, y0, y1) { const p = new THREE.Mesh(new THREE.CylinderGeometry(.012, .016, y1 - y0, 12), brass); p.position.set(x, (y0 + y1) / 2, z); p.castShadow = true; scene.add(p); return p; }
function ring(r, y, x, z, tube = .005, op = .75) { const m = new THREE.Mesh(new THREE.TorusGeometry(r, tube, 8, 220), new THREE.MeshBasicMaterial({ color: ACCENT, toneMapped: false, transparent: true, opacity: op })); m.rotation.x = Math.PI / 2; m.position.set(x, y, z); scene.add(m); return m; }

// ---------------------------------------------------------------- A. star census: 13 Sun-like stars on brass pins; 6 of them (≈46%) gain a companion
const census = []; const PAIRED = [0, 2, 5, 7, 9, 11];
{ const g = new THREE.Group(); g.add(plinth(2.5, 1.2, .55)); g.position.x = X.A; scene.add(shadowAll(g)); const r = rand(21);
  for (let k = 0; k < 13; k++) { const row = k < 7 ? 0 : 1, col = row ? k - 7 : k; const x = X.A - 1.02 + col * .34 + (row ? .17 : 0), z = row ? -.28 : .2, y = .95 + r() * .25 + (row ? .12 : 0);
    postAt(x, z, .55, y - .07); const s = star(.07, 0xffd27a, 2.2); s.position.set(x, y, z); scene.add(s);
    let comp = null; if (PAIRED.includes(k)) { comp = star(.042, k % 4 === 1 ? 0xff9a5a : 0xffb46b, 2.0); scene.add(comp); }
    census.push({ s, comp, x, y, z, ph: r() * 6 }); } }

// ---------------------------------------------------------------- B. Alpha Centauri A + B on a brass orrery arm around their centre of mass
const BY = 1.55; let acA, acB, acArm;
{ const g = new THREE.Group(); g.add(plinth(1.6, 1.6, .55)); const disc = new THREE.Mesh(new THREE.CylinderGeometry(.34, .42, .07, 64), darkIron); disc.position.y = .585; g.add(disc); g.position.x = X.B; scene.add(shadowAll(g));
  postAt(X.B, 0, .62, BY); acArm = new THREE.Group(); acArm.position.set(X.B, BY, 0); scene.add(acArm);
  const bar = new THREE.Mesh(new THREE.CylinderGeometry(.009, .009, 1.24, 10), brass); bar.rotation.z = Math.PI / 2; acArm.add(bar);
  const hub = new THREE.Mesh(new THREE.SphereGeometry(.03, 24, 16), brass); acArm.add(hub);
  acA = star(.2, 0xffe08a, 2.2); acA.position.x = -.62 * .9 / 2.0; acArm.add(acA); // mass ratio 1.1 : 0.9 -> A sits closer to the centre
  acB = star(.17, 0xffa95e, 2.1); acB.position.x = .62 * 1.1 / 2.0 + .3; acArm.add(acB);
  acA.position.x = -.56; acB.position.x = .69; ring(.56, BY, X.B, 0, .004, .45); ring(.69, BY, X.B, 0, .004, .45); }

// ---------------------------------------------------------------- C. Kepler-16: a K dwarf + red dwarf in a tight pair, a Saturn-sized planet circling BOTH
const CY = 1.45; let k16pair, k16planet; const KR = 1.0;
{ const g = new THREE.Group(); g.add(plinth(2.6, 2.0, .5)); g.position.x = X.C; scene.add(shadowAll(g));
  postAt(X.C, 0, .5, CY); k16pair = new THREE.Group(); k16pair.position.set(X.C, CY, 0); scene.add(k16pair);
  const a = star(.12, 0xffa55a, 2.1); a.position.x = -.05; const b = star(.065, 0xff6a45, 2.0); b.position.x = .2; k16pair.add(a, b);
  const bar = new THREE.Mesh(new THREE.CylinderGeometry(.006, .006, .25, 8), brass); bar.rotation.z = Math.PI / 2; bar.position.x = .075; k16pair.add(bar);
  ring(KR, CY, X.C, 0, .005, .8);
  const bandTex = canvasTex(512, 256, (ctx, w, h) => { const r = rand(16); for (let y = 0; y < h; y++) { const v = Math.sin(y * .09) * 18 + Math.sin(y * .31) * 8 + (r() - .5) * 6; ctx.fillStyle = `rgb(${178 + v},${156 + v},${120 + v})`; ctx.fillRect(0, y, w, 1); } }).tex;
  k16planet = new THREE.Mesh(new THREE.SphereGeometry(.13, 96, 64), new THREE.MeshStandardMaterial({ map: bandTex, roughness: .7, emissive: 0xffffff, emissiveMap: bandTex, emissiveIntensity: .15 })); k16planet.castShadow = true; scene.add(k16planet);
  const pl = new THREE.PointLight(0xffb070, 1.2, 3, 2); pl.position.set(X.C, CY, 0); scene.add(pl); }

// ---------------------------------------------------------------- D. Earth with one Sun ... then two (sizes/distances not to scale); thermometer; steam
const DY = 1.5, DR = .48; let earthD, sun1, sun2, sun2arm, thermo, steam = [];
const earthMatD = drainEarthMat();
{ const g = new THREE.Group(); g.add(plinth(1.5, 1.5, .55)); const disc = new THREE.Mesh(new THREE.CylinderGeometry(.34, .42, .07, 64), darkIron); disc.position.y = .585; g.add(disc); g.position.x = X.D; scene.add(shadowAll(g));
  postAt(X.D, 0, .62, DY - DR); const holder = new THREE.Group(); holder.position.set(X.D, DY, 0); holder.rotation.z = .41; earthD = new THREE.Mesh(new THREE.SphereGeometry(DR, 128, 96), earthMatD); earthD.castShadow = true; holder.add(earthD); scene.add(holder);
  sun1 = star(.24, 0xffe29a, 2.2); sun1.position.set(X.D - 1.0, 2.3, -1.3); scene.add(sun1); postAt(X.D - 1.0, -1.3, 0, 2.3 - .24);
  sun2 = star(.24, 0xffe29a, 2.2); sun2.position.set(X.D + 1.0, 2.3, -1.3); scene.add(sun2); sun2arm = postAt(X.D + 1.0, -1.3, 0, 2.3 - .24);
  // thermometer: glass tube with an orange column on a small plinth
  const tg = new THREE.Group(); tg.add(plinth(.45, .45, .4)); const tube = new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, 1.3, 32, 1, true), glass); tube.position.y = .4 + .7; tg.add(tube);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(.09, 32, 24), new THREE.MeshStandardMaterial({ color: ACCENT, emissive: ACCENT, emissiveIntensity: .35, roughness: .3 })); bulb.position.y = .5; tg.add(bulb);
  thermo = new THREE.Mesh(new THREE.CylinderGeometry(.035, .035, 1, 24), bulb.material); tg.add(thermo);
  for (let k = 0; k < 6; k++) { const tk = new THREE.Mesh(new THREE.BoxGeometry(.05, .006, .006), brass); tk.position.set(.075, .6 + k * .2, 0); tg.add(tk); }
  tg.position.set(X.D + 1.15, 0, .55); scene.add(shadowAll(tg)); tube.castShadow = false;
  const sm = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 1, transparent: true, opacity: .0, depthWrite: false }); const r = rand(31);
  for (let k = 0; k < 22; k++) { const p = new THREE.Sprite(new THREE.SpriteMaterial({ map: haloTex, color: 0xffffff, transparent: true, opacity: 0, depthWrite: false })); p.scale.setScalar(.25 + r() * .2); p.userData.s0 = p.scale.x; const a = r() * Math.PI * 2; p.userData = { a, ph: r(), lat: (r() - .3) * .9 }; scene.add(p); steam.push(p); } }

// ---------------------------------------------------------------- E. our one Sun, slowly brightening; a small Earth beside it loses its oceans in ~1 billion years; brightness gauge
const EY = 1.6; let sunE, earthE, gaugeFill; const earthMatE = drainEarthMat();
{ const g = new THREE.Group(); g.add(plinth(1.5, 1.5, .55)); g.position.x = X.E; scene.add(shadowAll(g)); postAt(X.E, 0, .55, EY - .5);
  sunE = star(.5, 0xffe08a, 2.1); sunE.position.set(X.E, EY, 0); scene.add(sunE);
  const g2 = new THREE.Group(); g2.add(plinth(.7, .7, .7)); g2.position.set(X.E + 1.35, 0, .2); scene.add(shadowAll(g2)); postAt(X.E + 1.35, .2, .7, 1.2);
  earthE = new THREE.Mesh(new THREE.SphereGeometry(.2, 96, 64), earthMatE); earthE.position.set(X.E + 1.35, 1.4, .2); earthE.rotation.z = .41; earthE.castShadow = true; scene.add(earthE);
  // gauge: a brass rail on the front of the big plinth with an orange fill
  const rail = new THREE.Mesh(new RoundedBoxGeometry(1.2, .07, .03, 2, .01), darkIron); rail.position.set(X.E, .3, .77); scene.add(rail);
  gaugeFill = new THREE.Mesh(new RoundedBoxGeometry(1, .05, .035, 2, .01), new THREE.MeshBasicMaterial({ color: ACCENT, toneMapped: false })); scene.add(gaugeFill); }

// ---------------------------------------------------------------- Jeremys (scale .75 ≈ 1.75 m label)
const J1 = K.J, J2 = makeJeremy2(), J3 = makeJeremy2(), J4 = makeJeremy2(), J5 = makeJeremy2(); [J2, J3, J4, J5].forEach(j => { scene.add(j); rimLight(j); });
const putJ = (J, x, z, ry, pose) => { J.visible = true; J.position.set(x, 0, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose); };

// ---------------------------------------------------------------- timeline (from the voiceover)
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), endAt = T0[8] + 1.2;
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const CAM = [ // [target x, y, dist, yaw, pitch]
  [X.A + .3, 1.15, 11.6, -.34, .17], [X.A + .3, 1.1, 10.4, -.3, .16], [X.B + .5, 1.2, 10.6, -.3, .14], [X.C + .35, 1.15, 10.6, -.32, .2], [X.D - .45, 1.3, 12.4, -.28, .14],
  [X.D - .4, 1.25, 12.2, -.26, .14], [X.E + .15, 1.2, 11.4, -.3, .14], [X.E + .15, 1.15, 11.0, -.26, .14], [X.E + .15, 1.2, 12.0, -.3, .16]];
function camAt(t) { let c = CAM[0].slice(); for (let i = 1; i < CAM.length; i++) { const k = eInOut(clamp((t - (T0[i] - .8)) / 1.3)); if (k <= 0) break; c = c.map((v, j) => lerp(v, CAM[i][j], k)); } return c; }
const HUDS = [ // [l1, n1, THIS PART IS, l3, value]
  ['SUNS', '1', 'FACT', 'OUR SUN', 'Alone'], ['SUNS', '1', 'FACT', 'SUN-LIKE STARS WITH A PARTNER', '≈46%'], ['YEARS', '0', 'FACT', 'ALPHA CENTAURI A + B, ONE ORBIT', '79.9 years'],
  ['REAL LIFE', '2011', 'FACT', 'KEPLER-16b, ONE ORBIT OF BOTH STARS', '229 days'], ['SUNS', '2', 'FACT', 'SUNLIGHT', '2×'], ['SUNS', '2', 'SPECULATION', 'EARTH', 'Dozens of °C hotter'],
  ['REAL LIFE', 'Now', 'FACT', 'OUR SUN GETS BRIGHTER', '+10% / billion yrs'], ['REAL LIFE', '+1 billion yrs', 'FACT', 'OCEANS', 'Boiled away'], ['REAL LIFE', '+1 billion yrs', 'FACT', 'OCEANS', 'Boiled away']];
const tPair0 = T0[1] + 1.6, tPair1 = T0[1] + 4.2;          // companions appear
const tOrb0 = T0[2] + .4, tOrb1 = T1[2] - .2;               // Alpha Cen: one full orbit = 80 years
const tSun2a = T0[4] + .4, tSun2b = T0[4] + 2.0;            // second sun rises
const tHeat0 = T0[5] + .6, tHeat1 = T0[5] + 5.0;            // thermometer + steam
const tBri0 = T0[6] + 1.2, tBri1 = T0[7] + 1.0;             // the Sun brightens 10 %
const tBoil0 = T0[7] + .8, tBoil1 = T0[7] + 4.0;             // the little Earth's oceans boil away
window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: total, name: 'room', gain: .1 }, { t0: tHeat0, t1: T1[5] + .4, name: 'drip', gain: .1 }],
  sfx: [{ t: 1.0, name: 'swell', gain: .3 }, ...[2, 3, 4, 6].map(i => ({ t: T0[i] - .85, name: 'glide', gain: .26 })), ...PAIRED.map((k, j) => ({ t: tPair0 + j * .35, name: 'ding', gain: .1 })),
    { t: tOrb1 - .1, name: 'chime', gain: .2 }, { t: T0[3] + 1.2, name: 'chime', gain: .16 }, { t: tSun2a, name: 'swell', gain: .28 }, { t: tHeat0 + .3, name: 'hiss', gain: .16 }, { t: tHeat0 + 2.2, name: 'rumble_low', gain: .2 },
    { t: T0[6] + .2, name: 'chime', gain: .28 }, { t: tBri0, name: 'swell', gain: .22 }, { t: tBoil0 + .3, name: 'hiss', gain: .2 }, { t: endAt, name: 'chime', gain: .3 }] };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), lt = t - T0[i], ld = T1[i] - T0[i];
  // ---- A. census: companions grow in and circle their stars
  census.forEach((c, k) => { setGlow(c.s, 1 + .05 * Math.sin(t * 2 + c.ph)); if (!c.comp) return; const j = PAIRED.indexOf(k); const pk = eOut(clamp((t - (tPair0 + j * .35)) / .6));
    const a = c.ph + t * .9; c.comp.position.set(c.x + Math.cos(a) * .15, c.y + .01, c.z + Math.sin(a) * .15); c.comp.scale.setScalar(Math.max(.001, pk)); c.comp.visible = pk > .01; });
  // ---- B. Alpha Centauri: slow idle spin, then exactly one orbit during line 2 (80 years)
  const ok = eInOut(clamp((t - tOrb0) / (tOrb1 - tOrb0))); acArm.rotation.y = .5 + t * .03 + ok * Math.PI * 2;
  // ---- C. Kepler-16: the pair spins fast, the planet circles both
  k16pair.rotation.y = t * 2.2; const pa = 2.2 + t * .45; k16planet.position.set(X.C + Math.cos(pa) * KR, CY, -Math.sin(pa) * KR); k16planet.rotation.y = t * .8;
  // ---- D. second sun rises; heat; steam
  earthD.rotation.y = 2.4 + t * .07; const s2 = eOut(clamp((t - tSun2a) / (tSun2b - tSun2a)));
  sun2.scale.setScalar(Math.max(.001, s2)); sun2.visible = s2 > .01; sun2.position.y = lerp(1.2, 2.3, s2); sun2arm.scale.y = Math.max(.001, s2); sun2arm.position.y = (2.3 - .24) * s2 / 2; sun2arm.visible = s2 > .01;
  const hk = eInOut(clamp((t - tHeat0) / (tHeat1 - tHeat0))); const th = lerp(.35, 1.15, hk); thermo.scale.y = th; thermo.position.y = .55 + th / 2;
  earthMatD.userData.U.uDrain.value = .35 * hk;
  steam.forEach((p, k) => { const u = p.userData, f = (t * .35 + u.ph) % 1; const n = V(Math.cos(u.a), u.lat, Math.sin(u.a)).normalize();
    p.position.set(X.D, DY, 0).addScaledVector(n, DR + .03 + f * .45); p.position.y += f * .25; p.scale.setScalar(p.userData.s0 * (.6 + f * 1.6)); p.material.opacity = .5 * hk * Math.sin(Math.PI * f) * (1 - clamp((t - (T1[5] + .6)) / .8)); p.visible = p.material.opacity > .005; });
  // ---- E. brightening Sun, boiling oceans, gauge
  const bk = eInOut(clamp((t - tBri0) / (tBri1 - tBri0))); setGlow(sunE, 1 + .45 * bk); sunE.scale.setScalar(1 + .06 * bk); sunE.rotation.y = t * .1;
  earthE.rotation.y = 2.6 + t * .1; earthMatE.userData.U.uDrain.value = eInOut(clamp((t - tBoil0) / (tBoil1 - tBoil0)));
  const gw = lerp(.08, 1.12, bk); gaugeFill.scale.x = gw; gaugeFill.position.set(X.E - .56 + gw / 2, .3, .79);
  // ---- Jeremys
  const bl = p => (t % p) < .1;
  putJ(J1, X.A + 1.75, -1.6, -.5, { expr: i === 1 && t > tPair0 ? 'shocked' : 'happy', look: -.5, armL: .25, armR: i === 1 ? 1.2 : .25, blink: bl(2.7) });
  putJ(J2, X.B + 1.75, -1.3, -.5, { expr: 'happy', look: -.5, armL: .25, armR: i === 2 ? 1.2 : .25, blink: bl(2.9) });
  putJ(J3, X.C + 1.9, -1.9, -.5, { expr: i === 3 ? 'shocked' : 'happy', look: -.5, armL: .25, armR: .25, blink: bl(3.1) });
  putJ(J4, X.D - 1.7, -.45, .45, { expr: hk > .3 ? 'worried' : s2 > .5 ? 'shocked' : 'happy', look: .5, armL: .25, armR: i === 4 ? 1.2 : .25, sweatK: hk > .2 ? t * .8 : 0, blink: bl(2.5) });
  putJ(J5, X.E - .95, -1.7, .35, { expr: i >= 8 ? 'confused' : i === 7 ? 'worried' : 'happy', look: .5, armL: .25, armR: i === 8 ? 1.3 : .25, tilt: i >= 8 ? .1 : 0, blink: bl(2.3) });
  // ---- camera
  const c = camAt(t), drift = clamp(lt / Math.max(ld, 1));
  const tgt = V(c[0], c[1], 0), dist = c[2] * (1 - .035 * drift);
  orbit(tgt, dist, { yaw: c[3] + .04 * drift + t * .002, pitch: c[4], fov: 34, lookUp: .075 });
  shadowFit(tgt, 4.2); DOF.on = true; DOF.focus = dist; DOF.aperture = .55; DOF.maxR = 9;
  // ---- tags (orbit() first)
  const Al = (t0, t1) => clamp((t - t0) / .35) * clamp((t1 - t) / .3);
  if (i === 0) tag3('JEREMY', '1.75 m', V(X.A + 1.75, 2.3, -1.6), Al(.6, T0[1] - .7));
  if (i === 1) { tag3('SUN-LIKE STAR', 'like ours', census[3].s.position.clone().add(V(0, .12, 0)), Al(T0[1] + .3, tPair0 + .2)); tag3('6 OF 13', 'have a partner', census[5].s.position.clone().add(V(0, .16, 0)), Al(tPair1 - .4, T0[2] - .4)); }
  if (i === 2) tag3('ALPHA CENTAURI A + B', '4.37 light-years away', V(X.B, BY + .32, 0), Al(T0[2] + .5, T1[2] - .3));
  if (i === 3) { tag3('KEPLER-16b', 'Saturn-sized', k16planet.position.clone().add(V(0, .2, 0)), Al(T0[3] + 1.0, T0[4] - .5)); tag3('TWO STARS', '69% + 20% of the Sun', V(X.C, CY + .2, 0), Al(T0[3] + 2.6, T0[4] - .5)); }
  if (i === 4) { tag3('SUN', 'ours', sun1.position.clone().add(V(0, .32, 0)), Al(T0[4] + .3, T0[5] - .2)); tag3('SUN #2', 'just like ours', sun2.position.clone().add(V(0, .32, 0)), Al(tSun2b - .3, T0[5] - .2)); }
  if (i === 5) tag3('SPECULATION', 'oceans start to boil', V(X.D + .1, DY + DR + .02, 0), Al(tHeat0 + .8, T0[6] - .5));
  if (i === 6) tag3('THE SUN', '≈25% brighter than at birth', V(X.E, EY + .62, 0), Al(T0[6] + 1.0, T0[7] - .3));
  if (i === 7) tag3('EARTH', 'in ≈1 billion years', earthE.position.clone().add(V(0, .3, 0)), Al(tBoil0 - .2, endAt - .1));
  tagsEnd();
  // ---- HUD
  const H = HUDS[i], endK = clamp((t - endAt) / .35), endIn = clamp((t - endAt - .35) / .45);
  let n1 = H[1], l3 = H[3], val = H[4];
  if (i === 2) n1 = String(Math.round(79.9 * ok));
  if (i === 7) val = eInOut(clamp((t - tBoil0) / (tBoil1 - tBoil0))) < .5 ? 'Boiling' : 'Boiled away';
  const fadeIn = clamp(lt / .25);
  setHUD({ q: 'What if Earth had <b>two suns</b>?', qA: clamp((t - .2) / .4) * (1 - endK), l1: H[0], n1, l2: 'THIS PART IS', n2: H[2], l3, val,
    line: i === 0 ? '' : LN[i].show, lineA: fadeIn * clamp((T1[i] + .25 - t) / .2 + (i === 8 ? 9 : 0)), dataA: (1 - endK),
    end: 'Would <b>you</b> live<br>under two suns? 👇', endA: endIn });
  $('v5n2').style.color = H[2] === 'SPECULATION' ? ACCENT : '#fff';
  draw();
};
window.READY = true;
