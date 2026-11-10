// v5 "premium studio" kit: clean infinite tiled floor, soft studio light, photoreal objects, editorial HUD,
// 3D callout tags and one continuous camera. Inspired by minimal scale-comparison shorts (our own design + content).
import { THREE, RoundedBoxGeometry, scene, camera, canvasTex, rand, clamp, lerp, eOut, eInOut, K, boot } from './kit.js';
import { key, hemi, sky, LOOK, GRADE, DOF, INK, setEnv, draw, renderer } from './engine.js';

export const ACCENT = '#f0743c';
const $ = id => document.getElementById(id);
const V = (x, y, z) => new THREE.Vector3(x, y, z);
export const S = {};

// ------------------------------------------------------------------ boot
export async function bootStudio(title, ep) {
  await boot(title, ep, { street: false });
  for (const f of ['80px IDB', '80px IDBo', '40px IM', 'italic 40px LoraI', '600 40px ISB']) await document.fonts.load(f);
  // hide the old Season 2 HUD
  ['bar', 'track', 'counter', 'intro', 'caps', 'pov', 'small', 'flash', 'black'].forEach(id => { const e = $(id); if (e) e.style.display = 'none'; });
  hud();
  // studio look
  setEnv('studio'); scene.environmentIntensity = .32; if (K.hands) K.hands.visible = false;
  LOOK.zenith.set('#5d5a57'); LOOK.horizon.set('#bdb8b1'); LOOK.ground.set('#a9a49c'); LOOK.sunGlow.set('#000000');
  scene.fog = new THREE.Fog(0xb7b2ab, 40, 420);
  key.intensity = 1.7; key.color.set('#fff3e6'); hemi.intensity = .4; hemi.color.set('#f2efe9'); hemi.groundColor.set('#6d655c');
  renderer.toneMappingExposure = .4; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  GRADE.sat = .95; GRADE.contrast = .16; GRADE.split = .03; GRADE.vignette = .3; GRADE.gain = 1.0;
  INK.strength = 0; INK.ao = .5;
  K.J.visible = false;
  S.floor = floor(); scene.add(S.floor);
  return S;
}

// ------------------------------------------------------------------ infinite tiled floor (1 m tiles, polished concrete)
function floor() {
  const T = canvasTex(1024, 1024, (ctx, w, h) => {
    const r = rand(5); ctx.fillStyle = '#9b968f'; ctx.fillRect(0, 0, w, h);
    for (let ty = 0; ty < 4; ty++) for (let tx = 0; tx < 4; tx++) {
      const v = (r() - .5) * 14; ctx.fillStyle = `rgb(${155 + v},${150 + v},${143 + v})`; ctx.fillRect(tx * 256 + 2, ty * 256 + 2, 252, 252);
      for (let i = 0; i < 900; i++) { const g = 120 + r() * 70; ctx.fillStyle = `rgba(${g},${g - 3},${g - 8},${.06 + r() * .1})`; const s = 1 + r() * 5; ctx.fillRect(tx * 256 + r() * 256, ty * 256 + r() * 256, s, s); }
      const gr = ctx.createLinearGradient(tx * 256, ty * 256, tx * 256 + 256, ty * 256 + 256); gr.addColorStop(0, 'rgba(255,255,255,.05)'); gr.addColorStop(1, 'rgba(0,0,0,.05)'); ctx.fillStyle = gr; ctx.fillRect(tx * 256, ty * 256, 256, 256);
    }
  }).tex;
  T.wrapS = T.wrapT = THREE.RepeatWrapping; T.repeat.set(5000, 5000); T.anisotropy = 16;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(20000, 20000), new THREE.MeshStandardMaterial({ map: T, roughness: .62, metalness: 0, envMapIntensity: .6 }));
  // analytic grid lines: filtered with screen-space derivatives so they never alias or shimmer; they fade out when thinner than a pixel
  GRID.tile = { value: 1 };
  m.material.onBeforeCompile = sh => { sh.uniforms.uTile = GRID.tile;
    sh.vertexShader = 'varying vec3 vWp;\n' + sh.vertexShader.replace('#include <project_vertex>', '#include <project_vertex>\n vWp = (modelMatrix * vec4(transformed, 1.)).xyz;');
    sh.fragmentShader = 'varying vec3 vWp; uniform float uTile;\n' + sh.fragmentShader.replace('#include <map_fragment>', `#include <map_fragment>
      { vec2 g = vWp.xz / uTile; vec2 fw = max(fwidth(g), vec2(1e-6)); vec2 d = abs(fract(g - .5) - .5);
        float lw = .011; vec2 dw = max(vec2(lw), fw * .75);
        vec2 a = 1. - smoothstep(dw - fw * .75, dw + fw * .75, d);
        a *= clamp(lw / dw, vec2(0.), vec2(1.));
        float fade = 1. - smoothstep(.25, .6, max(fw.x, fw.y));
        float line = max(a.x, a.y) * fade;
        diffuseColor.rgb = mix(diffuseColor.rgb, vec3(.86, .845, .815), line * .9); }`); };
  m.rotation.x = -Math.PI / 2; m.receiveShadow = true; m.scale.setScalar(1); return m;
}
const GRID = {};
/** keep floor tiles readable at any scale: tile size in metres (1, 10, 100 …) */
export function floorScale(tile, sc = 1) { GRID.tile.value = tile; S.floor.scale.setScalar(sc); S.floor.material.map.repeat.set(20000 * sc / 4 / tile, 20000 * sc / 4 / tile); }

// ------------------------------------------------------------------ soft shadows that follow the subject size
export function shadowFit(center, size) {
  const c = key.shadow.camera, s = Math.max(4, size * 1.6);
  c.left = -s; c.right = s; c.top = s; c.bottom = -s; c.near = .5; c.far = s * 6 + 50; c.updateProjectionMatrix();
  const dir = V(.45, 1, .35).normalize();
  key.target.position.copy(center); key.position.copy(center).addScaledVector(dir, s * 3 + 20); key.target.updateMatrixWorld();
  key.shadow.bias = -.0004; key.shadow.normalBias = .02 * s / 4;
}

// ------------------------------------------------------------------ continuous camera: orbit/pull-back around a target
export function orbit(target, dist, { yaw = -.55, pitch = .32, fov = 38, lookUp = .0 } = {}) {
  const p = V(Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), Math.cos(yaw) * Math.cos(pitch)).multiplyScalar(dist).add(target);
  camera.position.copy(p); camera.lookAt(target.x, target.y + dist * lookUp, target.z);
  if (camera.fov !== fov) { camera.fov = fov; camera.updateProjectionMatrix(); }
  camera.near = Math.max(.02, dist / 400); camera.far = Math.max(6000, dist * 50); camera.updateProjectionMatrix();
  scene.fog.near = dist * 1.6; scene.fog.far = dist * 9 + 40;
  sky.position.copy(camera.position); sky.scale.setScalar(camera.far * .9);
}

// ------------------------------------------------------------------ HUD (editorial)
function hud() {
  const ui = $('ui');
  const css = document.createElement('style');
  css.textContent = `
  @font-face{font-family:LoraI;font-style:italic;src:url(assets/Lora-Italic.ttf)}
  @font-face{font-family:ISB;font-weight:600;src:url(assets/Inter-SemiBold.otf)}
  #v5brand{position:absolute;top:270px;left:0;right:90px;text-align:center;font-family:ISB;font-size:22px;letter-spacing:7px;color:rgba(255,255,255,.72)}
  #v5q{position:absolute;left:72px;top:318px;width:760px;font-family:IDBo;font-size:52px;line-height:1.08;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.28)}
  #v5q b{color:${ACCENT};font-weight:inherit;text-shadow:0 1px 2px rgba(0,0,0,.35)}
  #v5data{position:absolute;left:72px;top:470px;font-family:IDBo;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.28)}
  .v5row{display:flex;gap:64px;align-items:flex-end}
  .v5lab{font-family:ISB;font-size:21px;letter-spacing:3px;color:${ACCENT};margin-bottom:2px;text-shadow:0 1px 2px rgba(0,0,0,.35)}
  .v5num{font-size:62px;line-height:1}
  .v5num.s{font-size:40px;line-height:1.3}
  #v5val{font-size:84px;line-height:1.05;color:${ACCENT};font-family:IDB;white-space:nowrap;text-shadow:0 1px 2px rgba(0,0,0,.35)}
  #v5line{font-family:LoraI;font-style:italic;font-size:40px;color:rgba(255,255,255,.92);margin-top:6px;text-shadow:0 2px 14px rgba(0,0,0,.45)}
  #v5end{position:absolute;left:0;right:90px;top:330px;text-align:center;font-family:IDBo;font-size:72px;line-height:1.15;color:#fff;text-shadow:0 4px 24px rgba(0,0,0,.45)}
  #v5end b{color:${ACCENT};font-weight:inherit}
  .v5tag{position:absolute;transform:translate(-50%,-100%);padding:10px 16px 12px;border-radius:10px;background:rgba(32,28,26,.80);box-shadow:0 6px 24px rgba(0,0,0,.25);white-space:nowrap}
  .v5tag .t{font-family:IDBo;font-size:28px;letter-spacing:1px;color:${ACCENT}}
  .v5tag .d{font-family:LoraI;font-style:italic;font-size:26px;color:#efe9e1}
  .v5tag:after{content:'';position:absolute;left:50%;bottom:-12px;margin-left:-9px;border:9px solid transparent;border-top:10px solid rgba(32,28,26,.80);border-bottom:0}`;
  document.head.appendChild(css);
  ui.insertAdjacentHTML('beforeend', `<div id="v5brand">WHAT IF (X)?</div><div id="v5q"></div>
    <div id="v5data"><div class="v5row"><div><div class="v5lab" id="v5l1"></div><div class="v5num" id="v5n1"></div></div><div><div class="v5lab" id="v5l2"></div><div class="v5num s" id="v5n2"></div></div></div>
    <div class="v5lab" id="v5l3" style="margin-top:14px"></div><div id="v5val"></div><div id="v5line"></div></div><div id="v5end"></div>` +
    [0, 1, 2, 3].map(i => `<div class="v5tag" id="v5tag${i}"><div class="t"></div><div class="d"></div></div>`).join(''));
}
export function setHUD({ q = '', l1 = '', n1 = '', l2 = '', n2 = '', l3 = '', val = '', line = '', lineA = 1, end = '', endA = 0, dataA = 1, qA = 1 }) {
  $('v5q').innerHTML = q; $('v5q').style.opacity = qA;
  $('v5l1').textContent = l1; $('v5n1').textContent = n1; $('v5l2').textContent = l2; $('v5n2').textContent = n2; $('v5l3').textContent = l3;
  $('v5val').textContent = val; $('v5line').textContent = line; $('v5line').style.opacity = lineA; $('v5data').style.opacity = dataA;
  $('v5end').innerHTML = end; $('v5end').style.opacity = endA;
  const n = (val || '').length; $('v5val').style.fontSize = Math.min(84, Math.floor(1500 / Math.max(1, n))) + 'px';
}
const tmp = new THREE.Vector3();
let tagsUsed = 0;
export function tagsReset() { tagsUsed = 0; }
export function tagsEnd() { for (let i = tagsUsed; i < 4; i++) $('v5tag' + i).style.opacity = 0; }
/** a callout tag anchored at a 3D point (bottom tip at the point) */
export function tag3(title, detail, pos, alpha = 1) {
  if (tagsUsed > 3) return; const el = $('v5tag' + tagsUsed++);
  camera.updateMatrixWorld(); tmp.copy(pos).project(camera);
  const x = clamp((tmp.x * .5 + .5) * 1080, 200, 860), y = clamp((-tmp.y * .5 + .5) * 1920, 880, 1430);
  el.querySelector('.t').textContent = title; el.querySelector('.d').textContent = detail;
  el.style.left = x + 'px'; el.style.top = y + 'px'; el.style.opacity = tmp.z < 1 ? alpha : 0;
}

// ------------------------------------------------------------------ scale references
export function jeremy(pos, ry = .5, pose = {}) { const J = K.J; J.visible = true; J.position.copy(pos); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose({ expr: 'happy', ...pose }); return J; }
export const JEREMY_H = 2.62 * .75; // model height in metres at scale .75 (~1.97 m incl. hair) -> labelled 1.75 m

export function bathtub() {
  const g = new THREE.Group(); const white = new THREE.MeshPhysicalMaterial({ color: 0xf4f2ee, roughness: .18, clearcoat: .8 });
  const outer = new THREE.Mesh(new RoundedBoxGeometry(1.7, .58, .78, 6, .2), white); outer.position.y = .33; g.add(outer);
  const inner = new THREE.Mesh(new RoundedBoxGeometry(1.5, .1, .6, 6, .05), new THREE.MeshStandardMaterial({ color: 0xc9d6dc, roughness: .15 })); inner.position.y = .58; g.add(inner);
  const tap = new THREE.Mesh(new THREE.CylinderGeometry(.025, .025, .25, 16), new THREE.MeshStandardMaterial({ color: 0xd9d9de, metalness: 1, roughness: .2 })); tap.position.set(-.75, .72, 0); g.add(tap);
  for (const [x, z] of [[-.55, -.22], [-.55, .22], [.55, -.22], [.55, .22]]) { const f = new THREE.Mesh(new THREE.SphereGeometry(.06, 16, 12), new THREE.MeshStandardMaterial({ color: 0xc9a24a, metalness: .9, roughness: .3 })); f.position.set(x, .04, z); g.add(f); }
  g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g;
}
export function pool() { // Olympic pool 50 x 25 x 2 m = 2,500 m3
  const g = new THREE.Group();
  const deck = new THREE.Mesh(new THREE.BoxGeometry(54, .4, 29), new THREE.MeshStandardMaterial({ color: 0xe9e5de, roughness: .7 })); deck.position.y = .2; g.add(deck);
  const water = new THREE.Mesh(new THREE.BoxGeometry(50, .02, 25), new THREE.MeshPhysicalMaterial({ color: 0x2f9fc4, roughness: .05, metalness: .1, clearcoat: 1, transmission: 0 })); water.position.y = .405; g.add(water);
  for (let i = 1; i < 10; i++) { const l = new THREE.Mesh(new THREE.BoxGeometry(50, .03, .12), new THREE.MeshStandardMaterial({ color: i % 2 ? 0xf2d14a : 0xd93a3a, roughness: .5 })); l.position.set(0, .42, -12.5 + i * 2.5); g.add(l); }
  g.traverse(o => { if (o.isMesh) { o.receiveShadow = true; o.castShadow = true; } }); return g;
}
export function pyramid() { // Great Pyramid: base 230.3 m, original height 146.6 m
  const tex = canvasTex(1024, 1024, (ctx, w, h) => { const r = rand(4); ctx.fillStyle = '#cfb183'; ctx.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 8) { ctx.fillStyle = 'rgba(90,70,40,.35)'; ctx.fillRect(0, y, w, 2); for (let x = (y / 8 % 2) * 12; x < w; x += 24) { const v = r() * 30 - 15; ctx.fillStyle = `rgba(${200 + v},${170 + v},${120 + v},.6)`; ctx.fillRect(x, y + 2, 22, 6); } } }).tex;
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(1, 1);
  const geo = new THREE.ConeGeometry(230.3 / Math.SQRT2, 146.6, 4, 1); geo.rotateY(Math.PI / 4); geo.translate(0, 146.6 / 2, 0);
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, roughness: .95, flatShading: true })); m.castShadow = m.receiveShadow = true; return m;
}
export function planets() {
  const L = new THREE.TextureLoader(); const g = new THREE.Group();
  const em = L.load('./assets/planets/earth_atmos_2048.jpg'); em.colorSpace = THREE.SRGBColorSpace;
  const earth = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), new THREE.MeshStandardMaterial({ map: em, normalMap: L.load('./assets/planets/earth_normal_2048.jpg'), roughness: .8 }));
  const cm = L.load('./assets/planets/earth_clouds_1024.png'); const clouds = new THREE.Mesh(new THREE.SphereGeometry(1.01, 96, 64), new THREE.MeshStandardMaterial({ map: cm, transparent: true, opacity: .8, depthWrite: false }));
  const atmo = new THREE.Mesh(new THREE.SphereGeometry(1.035, 64, 48), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, side: THREE.BackSide, blending: THREE.AdditiveBlending,
    vertexShader: `varying vec3 vN; varying vec3 vV; void main(){ vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position,1.); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying vec3 vN; varying vec3 vV; void main(){ float f = pow(1. - abs(dot(vN, vV)), 3.); gl_FragColor = vec4(vec3(.35,.6,1.) * f * 1.4, f); }` }));
  earth.add(clouds); earth.add(atmo);
  const mm = L.load('./assets/planets/moon_1024.jpg'); mm.colorSpace = THREE.SRGBColorSpace;
  const moon = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshStandardMaterial({ map: mm, roughness: 1 }));
  g.add(earth, moon); g.userData = { earth, moon, clouds }; return g;
}
