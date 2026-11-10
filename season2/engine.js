// Reusable "WHAT IF (x)?" 3D engine: renderer, set, materials, Jeremy, props helpers, captions.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
export { THREE, RoundedBoxGeometry };

export const W = 1080, H = 1920;

// ---------- math helpers ----------
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const prog = (t, a, b) => clamp((t - a) / (b - a));
export const eOut = x => 1 - Math.pow(1 - x, 3);
export const eIn = x => x * x * x;
export const eInOut = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
export const eBack = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
export const lerp = (a, b, k) => a + (b - a) * k;
export function rand(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
export const popS = (t, t0, d = .4) => { const p = prog(t, t0, t0 + d); return p <= 0 ? 0.0001 : eBack(p); };

// ---------- renderer ----------
export const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.52;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.prepend(renderer.domElement);

export const scene = new THREE.Scene();
import { Sky } from 'three/addons/objects/Sky.js';
// v3 look: the visible sky is a stylised gradient dome (saturated zenith -> bright horizon, warm sun glow);
// the physical Sky is only used to build the environment lighting.
const phys = new Sky(); phys.scale.setScalar(4500);
export const LOOK = { zenith: new THREE.Color('#2f6fd0'), horizon: new THREE.Color('#bcd6f2'), ground: new THREE.Color('#9fb6cf'), sunGlow: new THREE.Color('#fff1cf') };
export const sky = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 24), new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false, fog: false,
  uniforms: { uZen: { value: LOOK.zenith }, uHor: { value: LOOK.horizon }, uGnd: { value: LOOK.ground }, uSunCol: { value: LOOK.sunGlow }, uSun: { value: new THREE.Vector3(0, 1, 0) } },
  vertexShader: `varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position,1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; gl_Position.z = gl_Position.w; }`,
  fragmentShader: `uniform vec3 uZen,uHor,uGnd,uSunCol,uSun; varying vec3 vW;
    void main(){ vec3 d = normalize(vW - cameraPosition); float h = d.y;
      vec3 c = h > 0. ? mix(uHor, uZen, pow(clamp(h,0.,1.), .55)) : mix(uHor, uGnd, clamp(-h*6.,0.,1.));
      float sd = max(dot(d, normalize(uSun)), 0.); c += uSunCol * (pow(sd, 18.) * .35 + pow(sd, 400.) * 1.2);
      gl_FragColor = vec4(c, 1.); }`,
}));
sky.scale.setScalar(4500); sky.renderOrder = -10; sky.frustumCulled = false; scene.add(sky);
export const sunDir = new THREE.Vector3();
const pmrem = new THREE.PMREMGenerator(renderer);
let envRT = null;
// ---------- v4: real HDRI environment lighting (CC0 Poly Haven via @pmndrs/assets, 512px) ----------
import { EXRLoader } from 'three/addons/loaders/EXRLoader.js';
const ENVS = {}; let envName = null;
export async function loadEnvs(names = ['sky', 'city', 'park', 'sunset', 'sunrise', 'dawn', 'night', 'forest']) {
  const L = new EXRLoader();
  for (const n of names) { try { const tex = await L.loadAsync(`./assets/hdri/${n}.exr`); tex.mapping = THREE.EquirectangularReflectionMapping; ENVS[n] = pmrem.fromEquirectangular(tex).texture; tex.dispose(); } catch (e) { console.log('[ep] hdri missing', n); } }
}
export function setEnv(n) { if (!n || n === envName || !ENVS[n]) return; envName = n; scene.environment = ENVS[n]; }
export function setSun(elevDeg = 38, azimDeg = 200, turbidity = 4, rayleigh = 1.4) {
  const u = phys.material.uniforms; u.turbidity.value = turbidity; u.rayleigh.value = rayleigh; u.mieCoefficient.value = 0.004; u.mieDirectionalG.value = 0.85;
  sunDir.setFromSphericalCoords(1, THREE.MathUtils.degToRad(90 - elevDeg), THREE.MathUtils.degToRad(azimDeg)); u.sunPosition.value.copy(sunDir); sky.material.uniforms.uSun.value.copy(sunDir);
  const envScene = new THREE.Scene(); const sk = new Sky(); sk.scale.setScalar(4500); Object.keys(u).forEach(k => sk.material.uniforms[k].value = (u[k].value.clone ? u[k].value.clone() : u[k].value)); envScene.add(sk);
  if (envRT) envRT.dispose(); envRT = pmrem.fromScene(envScene, 0.02); if (!envName) scene.environment = envRT.texture;
}
scene.environmentIntensity = 0.6;
scene.fog = new THREE.Fog(LOOK.horizon.getHex(), 70, 300);

export const camera = new THREE.PerspectiveCamera(55, W / H, 0.05, 6000);
camera.position.set(0, 2, 12);

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));

// ---------- v3 look: ink outlines (depth + normal edges) ----------
import { Pass, FullScreenQuad } from 'three/addons/postprocessing/Pass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
export const INK = { on: true, color: new THREE.Color('#1b1626'), width: 2.0, strength: 0.0, far: 110, skip: [], ao: .55, aoR: .7 };  // v4: no outlines (realistic), screen-space AO on
class InkPass extends Pass {
  constructor() {
    super();
    this.rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType });
    this.rt.depthTexture = new THREE.DepthTexture(W, H); this.rt.depthTexture.type = THREE.UnsignedIntType;
    this.nm = new THREE.MeshNormalMaterial();
    this.q = new FullScreenQuad(new THREE.ShaderMaterial({
      uniforms: { tC: { value: null }, tN: { value: null }, tD: { value: null }, uRes: { value: new THREE.Vector2(W, H) }, uW: { value: 1.6 }, uK: { value: .9 }, uInk: { value: INK.color },
        uNear: { value: .05 }, uFar: { value: 6000 }, uFade: { value: 90 }, uAO: { value: .55 }, uAOR: { value: .7 }, uFocal: { value: 1 } },
      vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); }`,
      fragmentShader: `uniform sampler2D tC,tN,tD; uniform vec2 uRes; uniform float uW,uK,uNear,uFar,uFade,uAO,uAOR,uFocal; uniform vec3 uInk; varying vec2 vUv;
        float lin(float z){ return uNear * uFar / (uFar - z * (uFar - uNear)); }
        float D(vec2 o){ return lin(texture2D(tD, vUv + o / uRes).x); }
        vec3 N(vec2 o){ return texture2D(tN, vUv + o / uRes).xyz * 2. - 1.; }
        void main(){
          vec4 c = texture2D(tC, vUv);
          float d0 = D(vec2(0.)); vec3 n0 = N(vec2(0.));
          float w = uW;
          float de = 0., ne = 0.;
          vec2 off[4]; off[0]=vec2(w,0.); off[1]=vec2(-w,0.); off[2]=vec2(0.,w); off[3]=vec2(0.,-w);
          for (int i=0;i<4;i++){ float d = D(off[i]); de = max(de, (d0 - d) / max(d, .001)); ne = max(ne, 1. - dot(n0, N(off[i]))); }
          float edge = max(smoothstep(.06, .16, de), smoothstep(.22, .5, ne) * step(d0, uFar * .9));
          edge *= uK * (1. - smoothstep(uFade * .5, uFade, d0));
          // screen-space ambient occlusion: darken creases/contacts using the same depth buffer
          float ao = 0.;
          if (uAO > 0. && d0 < uFar * .5) {
            float rpx = clamp(uAOR * uFocal / d0, 2., 60.);
            for (int i = 0; i < 12; i++) { float fi = float(i) + .5; float a = fi * 2.39996; float rr = sqrt(fi / 12.) * rpx;
              float ds = D(vec2(cos(a), sin(a)) * rr); float dz = d0 - ds;
              ao += smoothstep(.02, .25, dz / uAOR) * (1. - smoothstep(uAOR, uAOR * 3., dz)); }
            ao = ao / 12.;
          }
          vec3 col = c.rgb * (1. - uAO * ao);
          gl_FragColor = vec4(mix(col, uInk * col * .25 + uInk * .5, edge), c.a);
        }`,
    }));
  }
  render(renderer, writeBuffer, readBuffer) {
    const u = this.q.material.uniforms;
    if (INK.on || DOF.on || INK.ao > 0) {
      const ov = scene.overrideMaterial, bg = scene.background, au = renderer.shadowMap.autoUpdate, sv = sky.visible;
      const hid = INK.skip.filter(o => o.visible); hid.forEach(o => o.visible = false);
      scene.overrideMaterial = this.nm; scene.background = null; renderer.shadowMap.autoUpdate = false; sky.visible = false;
      renderer.setRenderTarget(this.rt); renderer.setClearColor(0x8080ff, 1); renderer.clear(); renderer.render(scene, camera);
      scene.overrideMaterial = ov; scene.background = bg; renderer.shadowMap.autoUpdate = au; sky.visible = sv; renderer.setClearColor(0x000000, 0); hid.forEach(o => o.visible = true);
    }
    u.tC.value = readBuffer.texture; u.tN.value = this.rt.texture; u.tD.value = this.rt.depthTexture;
    u.uNear.value = camera.near; u.uFar.value = camera.far; u.uW.value = INK.width; u.uK.value = INK.on ? INK.strength : 0; u.uFade.value = INK.far; u.uAO.value = INK.ao; u.uAOR.value = INK.aoR; u.uFocal.value = H / (2 * Math.tan(camera.fov * Math.PI / 360));
    renderer.setRenderTarget(this.renderToScreen ? null : writeBuffer); this.q.render(renderer);
  }
}
export const ink = new InkPass();
composer.addPass(ink);
// ---------- v3 look: depth of field (gather blur from the ink pass depth; no extra scene render) ----------
export const DOF = { on: false, focus: 5, aperture: 1.2, maxR: 16 };
export const dof = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, tD: { value: null }, uRes: { value: new THREE.Vector2(W, H) }, uFocus: { value: 5 }, uAp: { value: 1 }, uMax: { value: 0 }, uNear: { value: .05 }, uFar: { value: 6000 } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
  fragmentShader: `uniform sampler2D tDiffuse,tD; uniform vec2 uRes; uniform float uFocus,uAp,uMax,uNear,uFar; varying vec2 vUv;
    float lin(float z){ return uNear * uFar / (uFar - z * (uFar - uNear)); }
    float cocD(float d){ return uMax * clamp(abs(d - uFocus) / max(d, .001) * uAp, 0., 1.); }
    void main(){
      vec4 c0 = texture2D(tDiffuse, vUv); if (uMax < .5) { gl_FragColor = c0; return; }
      float d0 = lin(texture2D(tD, vUv).x); float c = cocD(d0); vec3 acc = c0.rgb; float wsum = 1.;
      for (int i = 0; i < 28; i++) {
        float fi = float(i) + .5; float r = sqrt(fi / 28.) * uMax; float a = fi * 2.39996;
        vec2 uv = vUv + vec2(cos(a), sin(a)) * r / uRes;
        float ds = lin(texture2D(tD, uv).x); float cs = cocD(ds);
        // nearer samples spread with their own blur; farther samples never bleed over a sharper foreground
        float w = ds < d0 ? smoothstep(r - 1.5, r, cs) : smoothstep(r - 1.5, r, min(cs, c));
        acc += texture2D(tDiffuse, uv).rgb * w; wsum += w;
      }
      gl_FragColor = vec4(acc / wsum, c0.a); }`,
});
composer.addPass(dof);
export const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.22, 0.4, 0.97);
composer.addPass(bloom);
composer.addPass(new OutputPass());
// ---------- v3 look: colour grade (display space) ----------
export const GRADE = { gain: 1.1, sat: 1.05, contrast: .2, warm: new THREE.Color('#ffd6a0'), cool: new THREE.Color('#5a4f8f'), split: .05, vignette: .28 };
export const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uGain: { value: 1 }, uSat: { value: 1 }, uCon: { value: 0 }, uWarm: { value: GRADE.warm }, uCool: { value: GRADE.cool }, uSplit: { value: 0 }, uVig: { value: 0 } },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uGain,uSat,uCon,uSplit,uVig; uniform vec3 uWarm,uCool; varying vec2 vUv;
    void main(){ vec3 c = texture2D(tDiffuse, vUv).rgb * uGain;
      float l = dot(c, vec3(.2126,.7152,.0722));
      c = mix(vec3(l), c, uSat);
      c = mix(c, c * c * (3. - 2. * c), uCon);
      l = dot(clamp(c,0.,1.), vec3(.2126,.7152,.0722));
      c = mix(c, c * uCool * 2.2, uSplit * pow(1. - l, 2.));
      c = mix(c, c * uWarm * 1.15, uSplit * pow(l, 2.));
      vec2 q = vUv - .5; q.x *= .62; float v = smoothstep(.25, .75, length(q));
      c *= 1. - uVig * v;
      gl_FragColor = vec4(clamp(c,0.,1.), 1.); }`,
});
composer.addPass(grade);
export function draw() {
  const d = dof.uniforms; d.tD.value = ink.rt.depthTexture; d.uFocus.value = DOF.focus; d.uAp.value = DOF.aperture; d.uMax.value = DOF.on ? DOF.maxR : 0; d.uNear.value = camera.near; d.uFar.value = camera.far;
  const u = grade.uniforms; u.uGain.value = GRADE.gain; u.uSat.value = GRADE.sat; u.uCon.value = GRADE.contrast; u.uSplit.value = GRADE.split; u.uVig.value = GRADE.vignette;
  composer.render();
}

// ---------- lights ----------
export const hemi = new THREE.HemisphereLight(0xa9c8ff, 0x6b5040, 0.6); scene.add(hemi);
export const key = new THREE.DirectionalLight(0xffe4c0, 3.4);
key.position.set(5, 10, 7); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
Object.assign(key.shadow.camera, { left: -32, right: 32, top: 32, bottom: -32, near: 1, far: 200 });
key.shadow.bias = -0.0003; key.shadow.normalBias = 0.02; key.shadow.radius = 4;
scene.add(key); scene.add(key.target);
export function aimSun(target) { key.target.position.copy(target); key.position.copy(target).addScaledVector(sunDir, 90); key.target.updateMatrixWorld(); key.shadow.camera.updateProjectionMatrix(); }
export const flash = new THREE.PointLight(0xffd88a, 0, 20); flash.position.set(0, 3, 2); scene.add(flash);

// ---------- canvas textures ----------
export function canvasTex(w, h, drawFn) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const ctx = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const o = { c, ctx, tex, last: null, draw(...a) { const k = JSON.stringify(a); if (k === o.last) return; o.last = k; ctx.clearRect(0, 0, w, h); drawFn(ctx, w, h, ...a); tex.needsUpdate = true; } };
  o.draw();
  return o;
}
export function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }

// ---------- stage ----------
const gridTex = canvasTex(512, 512, (ctx, w, h) => {
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = '#fff'; ctx.lineWidth = 6; ctx.strokeRect(0, 0, w, h);
  ctx.lineWidth = 2; ctx.globalAlpha = .35;
  ctx.beginPath(); ctx.moveTo(w / 2, 0); ctx.lineTo(w / 2, h); ctx.moveTo(0, h / 2); ctx.lineTo(w, h / 2); ctx.stroke();
});
gridTex.tex.wrapS = gridTex.tex.wrapT = THREE.RepeatWrapping; gridTex.tex.repeat.set(30, 30);
gridTex.tex.colorSpace = THREE.NoColorSpace;
export const floor = new THREE.Mesh(new THREE.PlaneGeometry(90, 90),
  new THREE.MeshStandardMaterial({ color: 0x0b0e1e, roughness: 0.32, metalness: 0.55, emissive: 0x2e5bff, emissiveMap: gridTex.tex, emissiveIntensity: 0.22 }));
floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor); floor.visible = false;
// soft spotlight pool on floor
const pool = new THREE.Mesh(new THREE.CircleGeometry(6, 64), new THREE.MeshBasicMaterial({
  map: canvasTex(256, 256, (ctx, w, h) => { const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); g.addColorStop(0, 'rgba(120,140,255,.18)'); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
pool.rotation.x = -Math.PI / 2; pool.position.y = 0.01;

// ---------- materials ----------
export const M = {
  gold: new THREE.MeshStandardMaterial({ color: 0xffba3c, metalness: 1, roughness: 0.2 }),
  goldGlow: new THREE.MeshStandardMaterial({ color: 0xffba3c, metalness: 0.9, roughness: 0.25, emissive: 0xff9a20, emissiveIntensity: 0.35 }),
  chrome: new THREE.MeshStandardMaterial({ color: 0xdde3f0, metalness: 1, roughness: 0.12 }),
  dark: new THREE.MeshStandardMaterial({ color: 0x14182a, metalness: 0.6, roughness: 0.3 }),
  glass: new THREE.MeshPhysicalMaterial({ color: 0x18245a, metalness: 0.2, roughness: 0.08, transparent: true, opacity: 0.78, clearcoat: 1, clearcoatRoughness: 0.05, depthWrite: false }),
  white: new THREE.MeshStandardMaterial({ color: 0xf3f4fa, roughness: 0.35 }),
  red: new THREE.MeshStandardMaterial({ color: 0xff3b55, roughness: 0.3, metalness: 0.2, emissive: 0xff2040, emissiveIntensity: 0.5 }),
  cyan: new THREE.MeshStandardMaterial({ color: 0x5ee0ff, roughness: 0.25, metalness: 0.3, emissive: 0x2ab8ff, emissiveIntensity: 0.6 }),
  marble: null,
};
M.gold.color.set(0xffba3c);
M.marble = new THREE.MeshStandardMaterial({ roughness: 0.28, metalness: 0.0, map: canvasTex(1024, 1024, (ctx, w, h) => {
  ctx.fillStyle = '#efe9df'; ctx.fillRect(0, 0, w, h);
  const r = rand(5);
  for (let i = 0; i < 26; i++) {
    ctx.strokeStyle = `rgba(${120 + r() * 40},${115 + r() * 30},${110 + r() * 30},${0.12 + r() * 0.25})`; ctx.lineWidth = 1 + r() * 4;
    ctx.beginPath(); let x = r() * w, y = 0; ctx.moveTo(x, y);
    while (y < h) { x += (r() - .5) * 60; y += 20 + r() * 40; ctx.lineTo(x, y); } ctx.stroke();
  }
}).tex });

// ---------- 3D text ----------
let FONT = null;
export async function loadFont() { FONT = await new FontLoader().loadAsync('./node_modules/three/examples/fonts/helvetiker_bold.typeface.json'); }
const geoCache = new Map();
export function textGeo(str, size = 1, depth = 0.3, bevel = true) {
  const k = [str, size, depth, bevel].join('|');
  if (geoCache.has(k)) return geoCache.get(k);
  const g = new TextGeometry(str, { font: FONT, size, depth, curveSegments: 10, bevelEnabled: bevel, bevelThickness: size * 0.04, bevelSize: size * 0.03, bevelSegments: 4 });
  g.center(); g.computeVertexNormals();
  geoCache.set(k, g); return g;
}
export function text3d(str, size = 1, mat = M.gold, depth) {
  const m = new THREE.Mesh(textGeo(str, size, depth ?? size * 0.3), mat);
  m.castShadow = true; return m;
}
export function textWidth(str, size) { const g = textGeo(str, size, size * 0.3); g.computeBoundingBox(); return g.boundingBox.max.x - g.boundingBox.min.x; }

// ---------- shards / particles ----------
export function shards(n, mat, size = 0.12, seed = 1) {
  const geo = new THREE.TetrahedronGeometry(size);
  const im = new THREE.InstancedMesh(geo, mat, n); im.castShadow = true; im.frustumCulled = false;
  const r = rand(seed), data = [];
  for (let i = 0; i < n; i++) {
    const th = r() * Math.PI * 2, ph = Math.acos(2 * r() - 1);
    data.push({ d: new THREE.Vector3(Math.sin(ph) * Math.cos(th), Math.abs(Math.cos(ph)) * 0.8 + 0.2, Math.sin(ph) * Math.sin(th)), sp: 2 + r() * 4, rot: new THREE.Vector3(r() * 9, r() * 9, r() * 9), s: 0.5 + r(), o: new THREE.Vector3((r() - .5), (r() - .5), (r() - .5)) });
  }
  const dm = new THREE.Object3D();
  im.burst = (origin, t, spread = 0.5, grav = 6, life = 1.6) => {
    im.visible = t > 0 && t < life;
    if (!im.visible) return;
    for (let i = 0; i < n; i++) {
      const p = data[i];
      dm.position.set(origin.x + p.o.x * spread + p.d.x * p.sp * t, origin.y + p.o.y * spread + p.d.y * p.sp * t - grav * t * t, origin.z + p.o.z * spread + p.d.z * p.sp * t);
      dm.rotation.set(p.rot.x * t, p.rot.y * t, p.rot.z * t);
      dm.scale.setScalar(p.s * (1 - t / life));
      dm.updateMatrix(); im.setMatrixAt(i, dm.matrix);
    }
    im.instanceMatrix.needsUpdate = true;
  };
  im.visible = false;
  return im;
}

// ---------- Jeremy ----------
function mesh(geo, mat, cast = true) { const m = new THREE.Mesh(geo, mat); m.castShadow = cast; m.receiveShadow = true; return m; }
export function makeJeremy() {
  const skin = new THREE.MeshPhysicalMaterial({ color: 0xf2b48c, roughness: 0.55, sheen: 0.25, sheenColor: 0xffb0a0 });
  const shirt = new THREE.MeshStandardMaterial({ color: 0x3f7cff, roughness: 0.65 });
  const jeans = new THREE.MeshStandardMaterial({ color: 0x2a3456, roughness: 0.75 });
  const hairM = new THREE.MeshStandardMaterial({ color: 0x3b2618, roughness: 0.6 });
  const eyeW = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.15 });
  const pupilM = new THREE.MeshStandardMaterial({ color: 0x111118, roughness: 0.1 });
  const mouthM = new THREE.MeshStandardMaterial({ color: 0x6e1a28, roughness: 0.5 });
  const J = new THREE.Group();
  const body = new THREE.Group(); J.add(body);
  for (const s of [-1, 1]) {
    const leg = mesh(new THREE.CapsuleGeometry(0.14, 0.42, 8, 16), jeans); leg.position.set(s * 0.17, 0.42, 0); body.add(leg);
    const shoe = mesh(new RoundedBoxGeometry(0.3, 0.16, 0.44, 4, 0.07), M.white); shoe.position.set(s * 0.17, 0.08, 0.06); body.add(shoe);
  }
  const torso = mesh(new THREE.CapsuleGeometry(0.42, 0.5, 12, 24), shirt); torso.position.y = 1.15; torso.scale.set(1, 1, 0.82); body.add(torso);
  const arms = [];
  for (const s of [-1, 1]) {
    const piv = new THREE.Group(); piv.position.set(s * 0.46, 1.48, 0); body.add(piv);
    const arm = mesh(new THREE.CapsuleGeometry(0.12, 0.42, 8, 16), shirt); arm.position.y = -0.3; piv.add(arm);
    const hand = mesh(new THREE.SphereGeometry(0.14, 24, 16), skin); hand.position.y = -0.64; piv.add(hand);
    piv.rotation.z = s * 0.18; arms.push(piv);
  }
  const head = new THREE.Group(); head.position.y = 2.08; body.add(head);
  const skull = mesh(new THREE.SphereGeometry(0.5, 48, 32), skin); skull.scale.set(1, 0.96, 0.95); head.add(skull);
  for (const s of [-1, 1]) { const ear = mesh(new THREE.SphereGeometry(0.11, 16, 12), skin); ear.position.set(s * 0.48, 0, 0); ear.scale.z = 0.6; head.add(ear); }
  const nose = mesh(new THREE.SphereGeometry(0.075, 16, 12), skin); nose.position.set(0, -0.06, 0.48); head.add(nose);
  const hair = mesh(new THREE.SphereGeometry(0.53, 48, 24, 0, Math.PI * 2, 0, Math.PI * 0.42), hairM); hair.rotation.x = -0.32; hair.position.y = 0.03; head.add(hair);
  const tuft = mesh(new THREE.SphereGeometry(0.2, 16, 12), hairM); tuft.position.set(0.12, 0.42, 0.22); tuft.scale.set(1.4, 0.6, 1); head.add(tuft);
  const eyes = [], pupils = [], brows = [];
  for (const s of [-1, 1]) {
    const e = new THREE.Group(); e.position.set(s * 0.17, 0.06, 0.4); head.add(e);
    const w = mesh(new THREE.SphereGeometry(0.12, 24, 16), eyeW, false); w.scale.z = 0.6; e.add(w);
    const p = new THREE.Group(); p.position.z = 0.06; e.add(p);
    p.add(mesh(new THREE.SphereGeometry(0.068, 20, 12), pupilM, false));
    const hl = mesh(new THREE.SphereGeometry(0.022, 8, 8), eyeW, false); hl.position.set(-0.025, 0.03, 0.06); p.add(hl);
    eyes.push(e); pupils.push(p);
    const b = mesh(new RoundedBoxGeometry(0.19, 0.045, 0.05, 2, 0.02), hairM, false); b.position.set(s * 0.17, 0.25, 0.44); head.add(b); brows.push(b);
  }
  const smile = mesh(new THREE.TorusGeometry(0.12, 0.028, 8, 24, Math.PI), mouthM, false); smile.rotation.z = Math.PI; smile.position.set(0, -0.17, 0.45); head.add(smile);
  const oMouth = mesh(new THREE.SphereGeometry(0.085, 20, 14), mouthM, false); oMouth.scale.set(0.9, 1.25, 0.5); oMouth.position.set(0, -0.24, 0.44); head.add(oMouth);
  const flat = mesh(new THREE.CapsuleGeometry(0.025, 0.16, 4, 8), mouthM, false); flat.rotation.z = Math.PI / 2; flat.position.set(0, -0.22, 0.46); head.add(flat);
  const sweat = mesh(new THREE.SphereGeometry(0.07, 16, 12), new THREE.MeshPhysicalMaterial({ color: 0x8fd6ff, roughness: 0.05, clearcoat: 1, emissive: 0x2a7fff, emissiveIntensity: 0.3 }), false);
  sweat.scale.y = 1.4; head.add(sweat);
  J.traverse(o => { if (o.isMesh) o.receiveShadow = true; });
  // pose API
  J.pose = ({ expr = 'happy', look = 0, armL = 0.18, armR = 0.18, bob = 0, tilt = 0, sweatK = 0, blink = false, t = 0 } = {}) => {
    body.position.y = bob; head.rotation.z = tilt; head.rotation.y = look * 0.35;
    arms[0].rotation.z = -armL; arms[1].rotation.z = armR;
    smile.visible = expr === 'happy'; oMouth.visible = expr === 'shocked' || expr === 'panic';
    flat.visible = expr === 'confused' || expr === 'sleep' || expr === 'worried';
    flat.rotation.z = Math.PI / 2 + (expr === 'confused' ? 0.25 : 0);
    const eyeS = expr === 'shocked' || expr === 'panic' ? 1.18 : 1;
    const closed = blink || expr === 'sleep';
    eyes.forEach(e => e.scale.set(eyeS, closed ? 0.12 : eyeS, 1));
    pupils.forEach(p => { p.scale.setScalar(expr === 'shocked' || expr === 'panic' ? 0.7 : 1); p.position.x = look * 0.04; p.visible = !closed; });
    const by = { happy: 0.27, shocked: 0.33, panic: 0.33, confused: 0.25, sleep: 0.23, worried: 0.27 }[expr];
    brows.forEach((b, i) => {
      const s = i ? 1 : -1; b.position.y = by;
      b.rotation.z = expr === 'worried' || expr === 'panic' ? s * -0.35 : expr === 'confused' ? (i ? 0.35 : -0.1) : s * 0.08;
      if (expr === 'confused' && i) b.position.y = by + 0.06;
    });
    sweat.visible = sweatK > 0.01;
    sweat.position.set(0.44, 0.2 - (sweatK % 1) * 0.35, 0.28);
  };
  J.traverse(o => { if (o.isMesh) o.castShadow = true; });
  J.pose();
  return J;
}

// ---------- captions (DOM) ----------
const capsEl = document.getElementById('caps');
export function renderCaptions(list, t) {
  // list: [{t0,t1,text,y,size,g:[],r:[],c:[]}]
  let html = '';
  for (const c of list) {
    if (t < c.t0 || t > c.t1 + 0.25) continue;
    const out = 1 - prog(t, c.t1, c.t1 + 0.25);
    const words = c.text.split(' ');
    html += `<div class="cap" style="top:${c.y ?? 1300}px;font-size:${c.size ?? 76}px;opacity:${out}">`;
    words.forEach((w, i) => {
      const s = popS(t, c.t0 + i * 0.06, 0.3); const a = clamp(prog(t, c.t0 + i * 0.06, c.t0 + i * 0.06 + 0.15));
      const bare = w.replace(/[,.?!…:]/g, '');
      const cls = (c.g || []).includes(bare) ? 'g' : (c.r || []).includes(bare) ? 'r' : (c.c || []).includes(bare) ? 'c' : '';
      html += `<span class="w ${cls}" style="transform:scale(${0.6 + 0.4 * s});opacity:${a}">${w}</span>`;
    });
    html += '</div>';
  }
  if (capsEl.innerHTML !== html) capsEl.innerHTML = html;
}
export const ui = {
  fill: document.getElementById('fill'), black: document.getElementById('black'), nosig: document.getElementById('nosig'),
  small: document.getElementById('small'), scan: document.getElementById('scan'),
};
