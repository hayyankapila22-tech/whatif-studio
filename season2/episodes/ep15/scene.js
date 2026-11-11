// Episode 15 — What if a drop of water doubled every minute?  (v5.1 studio look + AI voiceover; doubling format)
// The whole video is timed to the narration (vo.json written by tools/narrate.py from vo_lines.json).
// Facts (checked 2026-11-11):
//  - metric drop = 0.05 mL, 20 drops per mL (Wikipedia "Drop (unit)"). Volume after m minutes = 0.05 mL x 2^m; shown as a ball, width = cbrt(6V/pi).
//  - m22: 210 litres (a bathtub holds ~150-300 L).  m26: 3.36 m³, ball 1.86 m wide (> Jeremy 1.75 m).
//  - m36: 3,436 m³ (> Olympic pool, 50 x 25 x 2 m = 2,500 m³).  m53: ball 951 m wide (> Burj Khalifa 828 m).  m63: ball 9.6 km wide (> Everest 8,849 m).
//  - m85: 1.93 billion km³ (> all water on, in and above Earth, 1.386 billion km³; USGS "How Much Water is There on Earth?": that water as a
//    sphere would be about 1,385 km wide). Our ball at m85 is 1,546 km wide; the Moon is 3,474 km wide -> less than half as wide.
//  - m95: 1.98 trillion km³ (> Earth's volume 1.083 trillion km³), ball 15,580 km wide (> Earth 12,742 km). NASA planetary fact sheets.
import { THREE, scene, camera, clamp, lerp, eOut, eInOut, K } from './kit.js';
import { key, hemi, LOOK, DOF, INK, draw, sky, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd, jeremy, bathtub, pool, planets } from './studio.js';

await bootStudio('WHAT IF A WATER DROP DOUBLED?', 'EP. 15');
const VO = await (await fetch('./vo.json')).json(), LN = VO.lines, total = VO.total;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const $ = id => document.getElementById(id);
// floor is one 20 km quad (depth only good to ~1 cm): draw sky, then floor without depth write, then everything else on top (see ep14)
S.floor.material.depthWrite = false; S.floor.renderOrder = -10; sky.renderOrder = -20;
const V0 = 5e-8, RE = 6.371e6, RM = 1.7374e6;
const vol = m => V0 * Math.pow(2, m), diam = m => Math.cbrt(6 * vol(m) / Math.PI);

// ---------- the water ball: clear blue, glossy, slightly see-through ----------
const BALL = new THREE.Group(); scene.add(BALL);
const water = new THREE.Mesh(new THREE.SphereGeometry(1, 128, 96), new THREE.MeshPhysicalMaterial({ color: 0x1f8fc9, roughness: .04, metalness: 0, clearcoat: 1, clearcoatRoughness: .03, transparent: true, opacity: .88, envMapIntensity: 1.6, emissive: 0x0a3a66, emissiveIntensity: .35 }));
water.castShadow = true; BALL.add(water);
const rim = new THREE.Mesh(new THREE.SphereGeometry(1.012, 96, 64), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  vertexShader: `varying vec3 vN; varying vec3 vV; void main(){ vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position,1.); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
  fragmentShader: `varying vec3 vN; varying vec3 vV; void main(){ float f = pow(1. - abs(dot(normalize(vN), normalize(vV))), 3.2); gl_FragColor = vec4(vec3(.55, .85, 1.) * f * .9, 1.); }` }));
BALL.add(rim); INK.skip.push(rim);

// ---------- scale references (ground) ----------
const tub = bathtub(), olympic = pool();
const burj = (() => { const g = new THREE.Group(), glass = new THREE.MeshPhysicalMaterial({ color: 0x9fb4c8, metalness: .6, roughness: .15, clearcoat: 1 });
  [[0, 300, 32], [300, 520, 22], [520, 650, 14], [650, 700, 8], [700, 828, 2]].forEach(([a, b, r]) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r * .8, r, b - a, 24), glass); m.position.y = (a + b) / 2; m.castShadow = true; g.add(m); });
  return g; })();
const everest = (() => { const H = 8849, B = 6000, g = new THREE.ConeGeometry(B, H, 256, 110, true); g.translate(0, H / 2, 0); const p = g.attributes.position, col = new Float32Array(p.count * 3), r = rand(7);
  const ph = [...Array(16)].map(() => r() * 6.28);
  for (let i = 0; i < p.count; i++) { let x = p.getX(i), y = p.getY(i), z = p.getZ(i); const u = clamp(y / H), a = Math.atan2(z, x);
    let n = 0, hf = 0; for (let k = 0; k < 6; k++) n += Math.sin(a * (2 + k) + ph[k]) / (1.4 + k);
    for (let k = 6; k < 16; k++) hf += Math.sin(a * (7 + k * 3) + ph[k]) * Math.sin(u * (9 + k * 5) + ph[15 - k + 6]) / (k - 3);
    const amp = Math.pow(Math.sin(Math.PI * Math.min(1, u * 1.15 + .12)), .8);
    const prof = Math.pow(1 - u, 1.3) * (1 + (n * .26 + hf * .1) * amp) + .012 * (1 - u);
    x *= prof / Math.max(1 - u, 1e-4); z *= prof / Math.max(1 - u, 1e-4); y += (hf * 90 + n * 120) * (1 - u) * u * 4;
    p.setXYZ(i, x, Math.max(0, y), z); const snow = clamp((u - .34 + n * .1 + hf * .08) / .06);
    const rk = .15 + hf * .03 + n * .02; col[i * 3] = lerp(rk * 1.12, 1, snow); col[i * 3 + 1] = lerp(rk, 1, snow); col[i * 3 + 2] = lerp(rk * .9, 1.02, snow); }
  g.setAttribute('color', new THREE.BufferAttribute(col, 3)); g.computeVertexNormals();
  const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .95, flatShading: true })); m.castShadow = m.receiveShadow = true; return m; })();
[tub, olympic, burj, everest].forEach(o => scene.add(o));

// ---------- space references (to scale; positions in metres above the ball's top) ----------
const SPACE = planets(); scene.add(SPACE); const E = SPACE.userData.earth, Mo = SPACE.userData.moon;
const stars = (() => { const a = [], r = rand(5); for (let i = 0; i < 2600; i++) { const th = r() * 6.283, ph = Math.acos(2 * r() - 1), d = 5000; a.push(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d, Math.sin(ph) * Math.sin(th) * d); }
  return new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(a, 3)), new THREE.PointsMaterial({ color: 0xffffff, size: 1.4, sizeAttenuation: false, fog: false })); })();
scene.add(stars); const SPACE_BG = new THREE.Color(0x0a0a0c);

// ---------- timeline: the minute is a continuous function of time, driven by the narration ----------
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), tSpace = T0[7] - .35, endAt = T0[10] + 1.6;
const KEYS = [[0, 0], [T0[2] - .4, 0], [T0[2] + 1.2, 22], [T0[3] - .3, 22], [T0[3] + 1.0, 26], [T0[4] - .4, 26], [T0[4] + 1.0, 36], [T0[5] - .4, 36], [T0[5] + 1.2, 53], [T0[6] - .4, 53], [T0[6] + 1.0, 63], [tSpace - .9, 63], [tSpace, 82],
  [T0[7] + 1.0, 85], [T0[9] - .3, 85], [T0[9] + 1.6, 95], [total + 1, 95]];
function minuteAt(t) { for (let i = 1; i < KEYS.length; i++) { const [t0, m0] = KEYS[i - 1], [t1, m1] = KEYS[i]; if (t <= t1) return lerp(m0, m1, eInOut(clamp((t - t0) / (t1 - t0)))); } return 95; }
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const logKeys = K2 => m => { for (let i = 1; i < K2.length; i++) { const [m0, r0] = K2[i - 1], [m1, r1] = K2[i]; if (m <= m1) return Math.exp(lerp(Math.log(r0), Math.log(r1), eInOut(clamp((m - m0) / (m1 - m0))))); } return K2[K2.length - 1][1]; };
const refAt = logKeys([[0, .014], [6, .04], [16, .5], [21, 3.2], [22.5, 3.2], [25, 4.4], [27, 4.6], [33, 30], [36, 64], [39, 80], [50, 800], [53, 1700], [60, 9000], [63, 20000], [68, 1.5e5], [82, 6e6]]);
const comma = n => Math.round(n).toLocaleString('en-US');
const WORDS = [[1e27, 'octillion'], [1e24, 'septillion'], [1e21, 'sextillion'], [1e18, 'quintillion'], [1e15, 'quadrillion'], [1e12, 'trillion'], [1e9, 'billion'], [1e6, 'million']];
const big = n => { for (const [d, w] of WORDS) if (n >= d) return (n / d).toFixed(n / d >= 100 ? 0 : 1).replace(/\.0$/, '') + ' ' + w; return comma(n); };
function fmtVol(v) { if (v < 1e-6) return (v * 1e6).toFixed(2) + ' mL'; if (v < 1e-3) return (v * 1e6).toFixed(v < 1e-5 ? 1 : 0) + ' mL'; if (v < 1) return (v * 1000).toFixed(v < .01 ? 1 : 0) + ' litres';
  if (v < 1e7) return comma(v) + ' m³'; if (v < 1e9) return big(v) + ' m³'; return big(v / 1e9) + ' km³'; }
function fmtW(d) { if (d < .01) return (d * 1000).toFixed(1) + ' mm'; if (d < 1) return (d * 100).toFixed(d < .1 ? 1 : 0) + ' cm'; if (d < 1000) return d.toFixed(d < 10 ? 1 : 0) + ' m'; const km = d / 1000; return km < 100 ? km.toFixed(1) + ' km' : comma(km) + ' km'; }

window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: tSpace + .2, name: 'room', gain: .12 }, { t0: tSpace - .2, t1: total, name: 'space', gain: .22 }],
  sfx: [...[2, 3, 4, 5, 6, 9].map(i => ({ t: T0[i] - .2, name: 'swell', gain: .28 })), { t: tSpace - .9, name: 'wind_gust', gain: .16 }, { t: T0[7], name: 'rumble_low', gain: .4 }, { t: T0[8], name: 'chime', gain: .25 }, { t: endAt, name: 'chime', gain: .3 }] };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';
$('ui').insertAdjacentHTML('afterbegin', '<div id="v5fade" style="position:absolute;inset:0;background:#0a0a0c;opacity:0"></div>');

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), m = minuteAt(t), mi = Math.floor(m + .03), n = Math.pow(2, m), d = diam(m), R = d / 2, space = t > tSpace;
  const endK = clamp((t - endAt) / .4);
  S.floor.visible = !space; stars.visible = space; SPACE.visible = space;
  [tub, olympic, burj, everest].forEach(o => o.visible = false);
  water.rotation.y = t * .1;
  if (!space) {
    sky.visible = true; scene.background = null; LOOK.zenith.set('#5d5a57'); LOOK.horizon.set('#bdb8b1'); key.intensity = 1.7; hemi.intensity = .4;
    BALL.position.set(0, R, 0); BALL.scale.setScalar(R);
    const size = Math.max(d * 1.7, refAt(m)), dist = size * 2.9 + Math.min(.3, size), tgt = V(0, R * .95 + size * .3, 0);
    orbit(tgt, dist, { yaw: -.55 + t * .008, pitch: lerp(.38, .3, clamp(m / 40)), fov: 36 });
    camera.near = Math.max(.02, dist * .05); camera.far = dist * 14 + 80; camera.updateProjectionMatrix(); sky.scale.setScalar(camera.far * .9);
    // references stand in front of the ball (towards the camera, a little to one side)
    const place = (o, mRef, w, ang) => { const dd = diam(mRef) / 2 * 1.1 + w * .5, k = eOut(clamp((dist / (dd * 1.6 + w) - 1) * 3)); // grows in only once the camera has pulled back well past it (never inside the camera)
      o.scale.setScalar(Math.max(k, 1e-3)); o.userData.k = k; o.position.set(Math.cos(ang) * dd, o.userData.lift ? o.userData.lift * k : 0, Math.sin(ang) * dd); o.visible = k > 0 && R < dd - w * .1; return o.position; };
    if (m > 16 && m < 25) { const p = place(tub, 22, 1.5, 1.35); tub.rotation.y = -.55; if (tub.visible && tub.userData.k > .7 && m > 20) tag3('BATHTUB', '~200 litres', p.clone().add(V(0, .8, 0)), clamp((m - 20) * 2)); }
    if (m > 29 && m < 42) { const p = place(olympic, 36, 30, 2.12); olympic.rotation.y = -.55; if (olympic.visible && olympic.userData.k > .7 && m > 33) tag3('OLYMPIC POOL', '2,500 m³', p.clone().add(V(0, 2, 0)), clamp((m - 33) * 2)); }
    if (m > 46 && m < 58) { const p = place(burj, 53, 60, 1.48); if (burj.visible && burj.userData.k > .7 && m > 50) tag3('BURJ KHALIFA', '828 m', p.clone().add(V(0, 850, 0)), clamp((m - 50) * 2)); }
    if (m > 58) { const p = place(everest, 63, 6000, 1.76); if (everest.visible && everest.userData.k > .7 && m > 61) tag3('MOUNT EVEREST', '8,849 m tall', p.clone().add(V(0, 9000, 0)), clamp((m - 61) * 2) * clamp(66 - m)); }
    const jd = R + .75; if (m > 23.5 && m < 31) jeremy(V(Math.cos(3.39) * jd, 0, Math.sin(3.39) * jd), -.1, { expr: m > 25.3 ? 'shocked' : 'happy', look: .5, armL: m > 25.3 ? 2.3 : .2, armR: m > 25.3 ? 2.3 : .2, blink: (t % 3.1) < .1 }); else K.J.visible = false;
    if (m > 24.2 && m < 30) tag3('JEREMY', '1.75 m', K.J.position.clone().add(V(0, 2.25, 0)), clamp((m - 24.2) * 2) * clamp((30 - m) / 1.5));
    tag3(m < .5 ? 'ONE DROP' : 'WATER', m < .5 ? '0.05 mL' : fmtW(d) + ' wide', V(0, d * 1.05, 0), clamp((t - T0[1] - .3) / .4));
    floorScale(1, Math.max(1, dist / 400)); shadowFit(V(0, 0, 0), size * 1.4);
    DOF.on = m < 18; DOF.focus = camera.position.distanceTo(V(0, R, 0)); DOF.aperture = .9; DOF.maxR = 10;
  } else {
    // ---- space: to scale, drawn in "frame units" (the framed height is always 10 units)
    K.J.visible = false; DOF.on = false;
    const top = 2.5e7, pad = 1.3e7 * (1 - clamp((m - 86) / 6)), hgt = top + d + pad, u = 10 / hgt, mid = (top - d - pad) / 2 * u; // small ball: keep it above the bottom safe line
    BALL.position.set(0, -R * u, 0); BALL.scale.setScalar(R * u);
    E.scale.setScalar(RE * u); E.position.set(0, RE * 1.3 * u, 0); Mo.scale.setScalar(RM * u); Mo.position.set(0, (RE * 2.8 + RM) * u, 0);
    E.rotation.y = t * .04; SPACE.userData.clouds.rotation.y = t * .01; Mo.rotation.y = t * .02;
    sky.visible = false; scene.background = SPACE_BG; scene.fog.near = 1e6; scene.fog.far = 2e6;
    key.position.set(40, 12, 30); key.target.position.set(0, 0, 0); key.target.updateMatrixWorld(); key.intensity = 3.2; hemi.intensity = .06;
    const dist = 10 / (2 * Math.tan(18 * Math.PI / 180)) * 1.75;
    camera.position.set(dist * .18, mid + 3, dist); camera.lookAt(0, mid + 3, 0); camera.fov = 36; camera.near = .1; camera.far = 1e4; camera.updateProjectionMatrix();
    stars.position.copy(camera.position);
    const a0 = clamp((t - tSpace - .5) / .4) * (1 - endK);
    tag3('MOON', '3,474 km wide', Mo.position.clone().add(V(RM * u + .5, RM * u * .5, 0)), a0); tag3('EARTH', '12,742 km wide', E.position.clone().add(V(RE * u * .9, RE * u * .6, 0)), a0);
    tag3(m < 86 ? 'ALL THAT WATER' : 'WATER', comma(d / 1000) + ' km wide', V(R * u * .72 + (m < 86 ? .9 : .15), -R * u + R * u * .72 + .1, 0), a0);
  }
  tagsEnd();
  // ---- HUD
  const lt = t - T0[i], H = i === 0 ? '' : LN[i].show;
  setHUD({ q: 'What if a drop of water <b>doubled every minute</b>?', qA: clamp((t - .2) / .4) * (1 - endK),
    l1: 'MINUTE', n1: String(mi), l2: 'DROPS', n2: n < 1e6 ? comma(n) : big(n), l3: 'VOLUME', val: fmtVol(vol(m)), line: H, lineA: clamp(lt / .25) * clamp((T1[i] + .3 - t) / .2 + (i >= 9 ? 9 : 0)),
    dataA: 1 - endK, end: 'All from <b>ONE</b> drop of water.<br>What should double next? 👇', endA: clamp((t - endAt - .35) / .5) });
  $('v5fade').style.opacity = clamp(1 - Math.abs(t - tSpace) / .28);
  draw();
};
window.READY = true;
