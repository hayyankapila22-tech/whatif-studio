// Episode 14 — What if a black hole doubled every minute?  (v5.1 studio look + AI voiceover; doubling format; idea from a viewer comment)
// The whole video is timed to the narration (vo.json written by tools/narrate.py from vo_lines.json).
// Facts (checked 2026-11-11):
//  - Schwarzschild radius r_s = 2GM/c² (Wikipedia "Schwarzschild radius"): Earth mass (5.972e24 kg) -> r_s = 8.87 mm, i.e. a 1.77 cm wide
//    event horizon (marble-sized); Sun -> 2.95 km. r_s is proportional to mass, so doubling the mass doubles the width.
//  - Start: 1 Earth mass, 1.774 cm wide. After m minutes: mass = 2^m Earths, width = 1.774 cm x 2^m.
//  - m4: 28 cm (basketball 24 cm), 16 Earths.  m7: 2.27 m (> Jeremy 1.75 m), 128 Earths (> Saturn, 95.2 Earths; NASA fact sheet).
//  - m16: 1.16 km (> Burj Khalifa 828 m).  m19: 9.3 km (> Everest 8,849 m), 524,288 Earths (> Sun = 332,946 Earths).
//  - m30: 19,050 km (> Earth 12,742 km).  m37: 2.44 million km (> Sun 1.39 million km).
//  - m49: 9.99 billion km (> Neptune's orbit, 2 x 4.495 billion km = 8.99 billion km wide).
//  - m60: 2^60 Earths = 3.5 trillion Suns (> Milky Way total mass ~1-1.5 trillion Suns, Wikipedia "Milky Way"); width 2.05e16 m = 2.2 light-years.
//  - Sizes are the event horizon of a non-rotating black hole. Purely hypothetical: a real Earth-mass black hole on the floor would not sit still.
import { THREE, scene, camera, clamp, lerp, eOut, eInOut, K } from './kit.js';
import { key, hemi, LOOK, DOF, INK, draw, sky, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd, jeremy, planets } from './studio.js';

await bootStudio('WHAT IF A BLACK HOLE DOUBLED?', 'EP. 14');
const VO = await (await fetch('./vo.json')).json(), LN = VO.lines, total = VO.total;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const $ = id => document.getElementById(id);
// the floor is one 20 km quad: its interpolated depth is only accurate to ~1 cm, which swallowed the 1.8 cm marble.
// Draw sky, then floor (no depth write), then everything else on top: nothing in this episode goes below the floor.
S.floor.material.depthWrite = false; S.floor.renderOrder = -10; sky.renderOrder = -20;
const D0 = .01774, RE = 6.371e6, RM = 1.7374e6, RS = 6.957e8, SUN_E = 332946, LY = 9.4607e15;
const diam = m => D0 * Math.pow(2, m);

// ---------- the black hole: pure black horizon + a thin hot ring of light hugging its edge ----------
const BH = new THREE.Group(); scene.add(BH);
const core = new THREE.Mesh(new THREE.SphereGeometry(1, 128, 96), new THREE.MeshBasicMaterial({ color: 0x000000, fog: false })); core.castShadow = true; BH.add(core);
const halo = new THREE.Mesh(new THREE.SphereGeometry(1.3, 128, 96), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { uK: { value: 1 } },
  vertexShader: `varying vec3 vN; varying vec3 vV; void main(){ vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position,1.); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
  fragmentShader: `varying vec3 vN; varying vec3 vV; uniform float uK;
    void main(){ float c = abs(dot(normalize(vN), normalize(vV))); float s = sqrt(max(0., 1. - c * c)) * 1.3; // distance from the centre in horizon radii
      float d = max(0., s - 1.); float ring = exp(-d * 34.) * 1.5 + exp(-d * 7.) * .35;
      vec3 col = mix(vec3(1., .46, .16), vec3(1., .93, .8), exp(-d * 60.));
      gl_FragColor = vec4(col * ring * uK * step(1., s), 1.); }` }));
BH.add(halo); INK.skip.push(halo);

// ---------- scale references (ground) ----------
const ballTex = canvasTex(512, 256, (ctx, w, h) => { ctx.fillStyle = '#c8642a'; ctx.fillRect(0, 0, w, h); const r = rand(3); for (let i = 0; i < 5000; i++) { ctx.fillStyle = `rgba(90,35,10,${.12 + r() * .15})`; ctx.fillRect(r() * w, r() * h, 2, 2); }
  ctx.strokeStyle = '#1c1512'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(0, h / 2); ctx.lineTo(w, h / 2); ctx.stroke(); for (const x of [w * .25, w * .75]) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
  for (const x of [0, w * .5, w]) { ctx.beginPath(); ctx.ellipse(x, h / 2, w * .09, h * .42, 0, 0, 7); ctx.stroke(); } }).tex;
const bball = new THREE.Mesh(new THREE.SphereGeometry(.12, 64, 48), new THREE.MeshStandardMaterial({ map: ballTex, roughness: .75 })); bball.castShadow = true;
const burj = (() => { const g = new THREE.Group(), glass = new THREE.MeshPhysicalMaterial({ color: 0x9fb4c8, metalness: .6, roughness: .15, clearcoat: 1 });
  [[0, 300, 32], [300, 520, 22], [520, 650, 14], [650, 700, 8], [700, 828, 2]].forEach(([a, b, r]) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r * .8, r, b - a, 24), glass); m.position.y = (a + b) / 2; m.castShadow = true; g.add(m); });
  return g; })();
const everest = (() => { const H = 8849, B = 6000, g = new THREE.ConeGeometry(B, H, 256, 110, true); g.translate(0, H / 2, 0); const p = g.attributes.position, col = new Float32Array(p.count * 3), r = rand(7);
  const ph = [...Array(16)].map(() => r() * 6.28);
  for (let i = 0; i < p.count; i++) { let x = p.getX(i), y = p.getY(i), z = p.getZ(i); const u = clamp(y / H), a = Math.atan2(z, x);
    let n = 0, hf = 0; for (let k = 0; k < 6; k++) n += Math.sin(a * (2 + k) + ph[k]) / (1.4 + k);                                // big ridges run straight down the slope
    for (let k = 6; k < 16; k++) hf += Math.sin(a * (7 + k * 3) + ph[k]) * Math.sin(u * (9 + k * 5) + ph[15 - k + 6]) / (k - 3);  // craggy detail
    const amp = Math.pow(Math.sin(Math.PI * Math.min(1, u * 1.15 + .12)), .8);
    const prof = Math.pow(1 - u, 1.3) * (1 + (n * .26 + hf * .1) * amp) + .012 * (1 - u); // concave flanks, sharp summit
    x *= prof / Math.max(1 - u, 1e-4); z *= prof / Math.max(1 - u, 1e-4); y += (hf * 90 + n * 120) * (1 - u) * u * 4;
    p.setXYZ(i, x, Math.max(0, y), z); const snow = clamp((u - .34 + n * .1 + hf * .08) / .06);
    const rk = .15 + hf * .03 + n * .02; col[i * 3] = lerp(rk * 1.12, 1, snow); col[i * 3 + 1] = lerp(rk, 1, snow); col[i * 3 + 2] = lerp(rk * .9, 1.02, snow); }
  g.setAttribute('color', new THREE.BufferAttribute(col, 3)); g.computeVertexNormals();
  const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .95, flatShading: true })); m.castShadow = m.receiveShadow = true; return m; })();
bball.userData.lift = .12; [bball, burj, everest].forEach(o => scene.add(o));

// ---------- space references (all to scale; positions in metres above the black hole's top) ----------
const SPACE = planets(); scene.add(SPACE); const E = SPACE.userData.earth, Mo = SPACE.userData.moon;
const sunTex = canvasTex(1024, 512, (ctx, w, h) => { const r = rand(11); ctx.fillStyle = '#ff9a1e'; ctx.fillRect(0, 0, w, h);
  for (let i = 0; i < 5000; i++) { const x = r() * w, y = r() * h, s = 4 + r() * 12; const g = ctx.createRadialGradient(x, y, 0, x, y, s); const hot = r() < .7; g.addColorStop(0, hot ? 'rgba(255,225,130,.5)' : 'rgba(220,90,10,.5)'); g.addColorStop(1, 'rgba(255,150,30,0)'); ctx.fillStyle = g; ctx.fillRect(x - s, y - s, s * 2, s * 2); } }).tex;
const sun = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), new THREE.MeshBasicMaterial({ map: sunTex, fog: false })); scene.add(sun);
const glowTex = canvasTex(256, 256, (ctx, w, h) => { const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); g.addColorStop(0, 'rgba(255,240,200,1)'); g.addColorStop(.25, 'rgba(255,170,60,.55)'); g.addColorStop(1, 'rgba(255,120,20,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex;
const sunGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, fog: false })); scene.add(sunGlow); INK.skip.push(sunGlow);
const ORB = [5.79e10, 1.082e11, 1.496e11, 2.279e11, 7.785e11, 1.4335e12, 2.8725e12, 4.4951e12]; // Mercury … Neptune, orbit radius in metres
const orbits = new THREE.Group(); scene.add(orbits); const TILT = 20 * Math.PI / 180;
ORB.forEach((r, i) => { const m = new THREE.Mesh(new THREE.TorusGeometry(1, i === 7 ? .0045 : .0035, 8, 256), new THREE.MeshBasicMaterial({ color: i === 7 ? 0xff8a3c : 0xd8d2c8, fog: false })); m.rotation.x = Math.PI / 2; m.userData.r = r; orbits.add(m); });
orbits.rotation.x = TILT; // near side dips towards the camera, so the growing horizon swallows the orbits from the inside out
const stars = (() => { const a = [], r = rand(5); for (let i = 0; i < 2600; i++) { const th = r() * 6.283, ph = Math.acos(2 * r() - 1), d = 5000; a.push(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d, Math.sin(ph) * Math.sin(th) * d); }
  return new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(a, 3)), new THREE.PointsMaterial({ color: 0xffffff, size: 1.4, sizeAttenuation: false, fog: false })); })();
scene.add(stars); const SPACE_BG = new THREE.Color(0x0a0a0c);

// ---------- timeline: the minute is a continuous function of time, driven by the narration ----------
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), tSpace = T0[6] - .35, endAt = T0[10] + 1.5;
const KEYS = [[0, 0], [T0[2] - .3, 0], [T0[2] + 1.0, 4], [T0[3] - .3, 4], [T0[3] + 1.0, 7], [T0[4] - .5, 7], [T0[4] + 1.1, 16], [T0[5] - .4, 16], [T0[5] + .9, 19], [tSpace - .9, 19], [tSpace, 27.5], [T0[6] + 1.0, 30],
  [T0[7] - .4, 30], [T0[7] + 1.1, 37], [T0[8] - .4, 37], [T0[8] + 1.4, 49], [T0[9] + .5, 49], [T0[9] + 3.4, 60], [total + 1, 60]];
function minuteAt(t) { for (let i = 1; i < KEYS.length; i++) { const [t0, m0] = KEYS[i - 1], [t1, m1] = KEYS[i]; if (t <= t1) return lerp(m0, m1, eInOut(clamp((t - t0) / (t1 - t0)))); } return 60; }
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const logKeys = K2 => m => { for (let i = 1; i < K2.length; i++) { const [m0, r0] = K2[i - 1], [m1, r1] = K2[i]; if (m <= m1) return Math.exp(lerp(Math.log(r0), Math.log(r1), eInOut(clamp((m - m0) / (m1 - m0))))); } return K2[K2.length - 1][1]; };
const refAt = logKeys([[0, .04], [2, .07], [4, .8], [6, 2.2], [7, 3.0], [9, 7], [12, 40], [15, 700], [16, 1200], [18, 9000], [19, 20000], [22, 1.2e5], [28, 6e6]]);  // ground framing size (m)
const topAt = logKeys([[27, 2.5e7], [31, 2.5e7], [35, 1.95e9], [38.5, 1.95e9], [45, 2.6e12], [50.5, 2.6e12], [60, 2.5e15]]);                                   // space: metres framed above the hole
const comma = n => Math.round(n).toLocaleString('en-US');
const WORDS = [[1e12, 'trillion'], [1e9, 'billion'], [1e6, 'million']];
const big = n => { for (const [d, w] of WORDS) if (n >= d) return (n / d).toFixed(n / d >= 100 ? 0 : 1).replace(/\.0$/, '') + ' ' + w; return comma(n); };
const fmtMass = n => n < SUN_E ? (n < 1.5 ? '1 Earth' : big(n) + ' Earths') : (s => s < 10 ? s.toFixed(1) + ' Suns' : big(s) + ' Suns')(n / SUN_E);
function fmtW(d) { if (d < 1) return (d * 100).toFixed(d < .1 ? 1 : 0) + ' cm'; if (d < 1000) return d.toFixed(d < 10 ? 1 : 0) + ' m'; const km = d / 1000; if (km < 100) return km.toFixed(1) + ' km';
  if (d < LY * .1) return big(km) + ' km'; return (d / LY).toFixed(1) + ' light-years'; }

window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: tSpace + .2, name: 'room', gain: .12 }, { t0: tSpace - .2, t1: total, name: 'space', gain: .22 }],
  sfx: [...[2, 3, 4, 5, 7, 8].map(i => ({ t: T0[i] - .2, name: 'swell', gain: .28 })), { t: tSpace - .9, name: 'wind_gust', gain: .16 }, { t: T0[6], name: 'rumble_low', gain: .4 }, { t: T0[8] + .2, name: 'rumble_low', gain: .4 },
    { t: T0[9] + .6, name: 'rumble_low', gain: .5 }, { t: T0[9], name: 'chime', gain: .25 }, { t: endAt, name: 'chime', gain: .3 }] };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';
$('ui').insertAdjacentHTML('afterbegin', '<div id="v5fade" style="position:absolute;inset:0;background:#0a0a0c;opacity:0"></div>');

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), m = minuteAt(t), mi = Math.floor(m + .03), n = Math.pow(2, m), d = diam(m), R = d / 2, space = t > tSpace;
  const endK = clamp((t - endAt) / .4);
  S.floor.visible = !space; stars.visible = space; SPACE.visible = space; sun.visible = sunGlow.visible = orbits.visible = false;
  [bball, burj, everest].forEach(o => o.visible = false);
  if (!space) {
    sky.visible = true; scene.background = null; LOOK.zenith.set('#5d5a57'); LOOK.horizon.set('#bdb8b1'); key.intensity = 1.7; hemi.intensity = .4;
    BH.position.set(0, R, 0); BH.scale.setScalar(R); halo.material.uniforms.uK.value = 1;
    const size = Math.max(d * 1.7, refAt(m)), dist = size * 2.9 + .3, tgt = V(0, R * .95 + size * .3, 0);
    orbit(tgt, dist, { yaw: -.55 + t * .012, pitch: lerp(.38, .3, clamp(m / 20)), fov: 36 });
    camera.near = Math.max(.02, dist * .05); camera.far = dist * 14 + 80; camera.updateProjectionMatrix(); sky.scale.setScalar(camera.far * .9); // tight depth range: a 2 cm sphere must not z-fight the floor
    // references stand in FRONT of the hole (towards the camera, a little to one side): lit objects against the black read instantly
    const place = (o, mRef, w, ang) => { const dd = diam(mRef) / 2 * 1.1 + w * .5, k = eOut(clamp((dist / (dd * 1.6 + w) - 1) * 3)); // grows in only once the camera has pulled back well past it (never inside the camera)
      o.scale.setScalar(Math.max(k, 1e-3)); o.userData.k = k; o.position.set(Math.cos(ang) * dd, o.userData.lift ? o.userData.lift * k : 0, Math.sin(ang) * dd); o.visible = k > 0 && R < dd - w * .1; return o.position; };
    if (m > 2.2 && m < 6.5) { const p = place(bball, 4, .3, 1.02); bball.rotation.y = 1; if (bball.visible && bball.userData.k > .7 && m > 3) tag3('BASKETBALL', '24 cm wide', p.clone().add(V(0, .15, 0)), clamp((m - 3) * 2)); }
    if (m > 12.5 && m < 18) { const p = place(burj, 16, 60, 1.48); if (burj.visible && burj.userData.k > .7 && m > 14.5) tag3('BURJ KHALIFA', '828 m', p.clone().add(V(0, 850, 0)), clamp((m - 14.5) * 2)); }
    if (m > 16.6) { const p = place(everest, 19, 6000, 1.76); if (everest.visible && everest.userData.k > .7 && m > 18) tag3('MOUNT EVEREST', '8,849 m tall', p.clone().add(V(0, 9000, 0)), clamp((m - 18) * 2) * clamp((21.5 - m))); }
    const jd = R + .6; if (m > 5 && m < 13) jeremy(V(Math.cos(2.42) * jd, 0, Math.sin(2.42) * jd), .15, { expr: m > 6.5 ? 'shocked' : 'happy', look: .5, armL: m > 6.5 ? 2.3 : .2, armR: m > 6.5 ? 2.3 : .2, blink: (t % 3.1) < .1 }); else K.J.visible = false;
    if (m > 5.6 && m < 11) tag3('JEREMY', '1.75 m', K.J.position.clone().add(V(0, 2.25, 0)), clamp((m - 5.6) * 2) * clamp((11 - m) / 1.5));
    tag3('BLACK HOLE', m < .5 ? 'the size of a marble' : fmtW(d) + ' wide', V(0, d * 1.04, 0), clamp((t - T0[1] - .3) / .4));
    floorScale(1, Math.max(1, dist / 400)); shadowFit(V(0, 0, 0), size * 1.4);
    DOF.on = m < 5; DOF.focus = camera.position.distanceTo(V(0, R, 0)); DOF.aperture = .9; DOF.maxR = 10;
  } else {
    // ---- space: everything to scale, drawn in "frame units" (the framed height is always 10 units) so nothing gets numerically huge
    K.J.visible = false; DOF.on = false;
    const top = topAt(m), hgt = top + d, u = 10 / hgt, mid = (top - d) / 2 * u;
    BH.position.set(0, -R * u, 0); BH.scale.setScalar(R * u);
    const show = (o, r, y) => { o.visible = r * u > .004 && y * u - r * u < 12; o.scale.setScalar(r * u); o.position.set(0, y * u, 0); return o.position; };
    show(E, RE, RE * 1.3); show(Mo, RM, RE * 2.8 + RM); E.rotation.y = t * .04; SPACE.userData.clouds.rotation.y = t * .01; Mo.rotation.y = t * .02;
    const sy = RS * 1.3; show(sun, RS, sy); sun.rotation.y = t * .02; sun.visible = sun.visible && m > 30.5;
    const gs = Math.max(RS * u * 3.2, .1); sunGlow.visible = m > 30.5 && sy * u < 12; sunGlow.position.set(0, sy * u, 0); sunGlow.scale.set(gs, gs, 1); sunGlow.material.opacity = clamp((m - 30.5) * 2);
    orbits.visible = m > 37.5; orbits.position.set(0, sy * u, 0); orbits.children.forEach(o => { const s = o.userData.r * u; o.scale.setScalar(s); o.visible = s > .03; });
    sky.visible = false; scene.background = SPACE_BG; scene.fog.near = 1e6; scene.fog.far = 2e6;
    key.position.set(40, 12, 30); key.target.position.set(0, 0, 0); key.target.updateMatrixWorld(); key.intensity = 3.2; hemi.intensity = .06;
    const dist = 10 / (2 * Math.tan(18 * Math.PI / 180)) * 1.75;
    camera.position.set(dist * .18, mid + 3, dist); camera.lookAt(0, mid + 3, 0); camera.fov = 36; camera.near = .1; camera.far = 1e4; camera.updateProjectionMatrix();
    stars.position.copy(camera.position);
    const A = (m0, m1) => clamp((m - m0) * 1.5) * clamp((m1 - m) * 1.5) * (1 - endK);
    if (m < 33) { tag3('MOON', '3,474 km wide', Mo.position.clone().add(V(RM * u + .5, RM * u * .5, 0)), A(27.6, 32.5)); tag3('EARTH', '12,742 km wide', E.position.clone().add(V(RE * u * .9, RE * u * .6, 0)), A(27.6, 32.5)); }
    if (m > 33 && m < 42) tag3('THE SUN', '1.39 million km wide', sun.position.clone().add(V(RS * u * .9, RS * u * .65, 0)), A(34, 41));
    if (m > 43 && m < 54) tag3("NEPTUNE'S ORBIT", '9 billion km wide', V(-ORB[7] * u * .8, sy * u + ORB[7] * u * Math.sin(TILT) * .1, 0), A(44, 53));
    if (m > 56) tag3('OUR SOLAR SYSTEM', 'a speck', V(0, sy * u + .1, 0), A(57, 99));
    tag3('BLACK HOLE', fmtW(d) + ' wide', V(R * u * .72, -R * u + R * u * .72, 0), clamp((t - tSpace - .5) / .4) * (1 - endK));
  }
  tagsEnd();
  // ---- HUD
  const lt = t - T0[i], H = i === 0 ? '' : LN[i].show;
  setHUD({ q: 'What if a black hole <b>doubled every minute</b>?', qA: clamp((t - .2) / .4) * (1 - endK),
    l1: 'MINUTE', n1: String(mi), l2: 'MASS', n2: fmtMass(n), l3: 'WIDTH', val: fmtW(d), line: H, lineA: clamp(lt / .25) * clamp((T1[i] + .3 - t) / .2 + (i >= 9 ? 9 : 0)),
    dataA: 1 - endK, end: 'All from <b>ONE</b> tiny marble.<br>What should double next? 👇', endA: clamp((t - endAt - .35) / .5) });
  $('v5fade').style.opacity = clamp(1 - Math.abs(t - tSpace) / .28);
  draw();
};
window.READY = true;
