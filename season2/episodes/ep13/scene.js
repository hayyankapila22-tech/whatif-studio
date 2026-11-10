// Episode 13 — What if the Roman Empire never collapsed?  (v5.1 premium studio look + AI voiceover; one continuous gallery shot)
// The whole video is timed to the narration (vo.json written by tools/narrate.py from vo_lines.json).
// Facts (checked 2026-11-10):
//  - peak area ~5,000,000 km² in AD 117; population traditionally 55-60 million = one-sixth to one-fourth of humanity (Wikipedia "Roman Empire")
//  - western empire ends 476; eastern (Byzantine) empire falls 1453 (same source) -> 977 years later
//  - more than 400,000 km of roads, over 80,500 km stone-paved (Wikipedia "Roman roads"); Earth's equator 40,075 km -> about twice round
//  - more than 900 million native speakers of Romance languages (Wikipedia "Romance languages")
//  - aeolipile: Heron of Alexandria, 1st century AD, described in Pneumatica; "a curiosity or a toy ... not used for any practical purpose" (Britannica)
//  - Colosseum opened AD 80, 189 x 156 m, 48 m high, ~50,000 spectators; first steam locomotive 1804 (Trevithick); Moon landing 1969.
//  - everything after "imagine it never fell" is labelled SPECULATION on screen and in the voiceover.
import { THREE, RoundedBoxGeometry, scene, camera, clamp, lerp, eOut, eInOut, K, rimLight } from './kit.js';
import { key, hemi, LOOK, GRADE, DOF, draw, renderer, canvasTex, rand } from './engine.js';
import { bootStudio, S, ACCENT, floorScale, shadowFit, orbit, setHUD, tag3, tagsReset, tagsEnd } from './studio.js';
import { makeJeremy2 } from './jeremy2.js';

await bootStudio('WHAT IF ROME NEVER FELL?', 'EP. 13');
const VO = await (await fetch('./vo.json')).json(), LN = VO.lines, total = VO.total;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const $ = id => document.getElementById(id);
floorScale(2);

// ---------------------------------------------------------------- materials
const marbleTex = canvasTex(512, 512, (ctx, w, h) => { const r = rand(8); ctx.fillStyle = '#e9e6e0'; ctx.fillRect(0, 0, w, h);
  for (let i = 0; i < 26; i++) { ctx.strokeStyle = `rgba(120,116,112,${.05 + r() * .12})`; ctx.lineWidth = .6 + r() * 2.2; ctx.beginPath(); let x = r() * w, y = r() * h; ctx.moveTo(x, y); for (let k = 0; k < 9; k++) { x += (r() - .5) * 120; y += (r() - .3) * 90; ctx.lineTo(x, y); } ctx.stroke(); } }).tex;
const marble = new THREE.MeshPhysicalMaterial({ map: marbleTex, roughness: .28, clearcoat: .5, clearcoatRoughness: .3 });
const bronze = new THREE.MeshStandardMaterial({ color: 0xb07a3c, metalness: 1, roughness: .32 });
const gold = new THREE.MeshStandardMaterial({ color: 0xe9b84a, metalness: 1, roughness: .22 });
const darkIron = new THREE.MeshStandardMaterial({ color: 0x23242a, metalness: .85, roughness: .38 });
const romanRed = new THREE.MeshPhysicalMaterial({ color: 0x9c1f24, roughness: .4, clearcoat: .6 });
const shadowAll = g => { g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };
function plinth(w, d, h) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, .03), marble); m.position.y = h / 2; m.castShadow = m.receiveShadow = true; return m; }
const X = { col: 0, globe: 7, train: 14, moon: 21, aeo: 28 };

// ---------------------------------------------------------------- A. Colosseum (1:78 model; real 189 x 156 x 48 m)
function colosseum() {
  const g = new THREE.Group(), a = 94.5, b = 78, N = 80;
  const tex = canvasTex(512, 512, (ctx, w, h) => { const r = rand(3); ctx.fillStyle = '#d9c8a6'; ctx.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 32) for (let x = (y / 32 % 2) * 40; x < w; x += 80) { const v = r() * 22 - 11; ctx.fillStyle = `rgb(${214 + v},${197 + v},${163 + v})`; ctx.fillRect(x + 1, y + 1, 78, 30); }
    for (let i = 0; i < 2500; i++) { ctx.fillStyle = `rgba(90,70,45,${r() * .12})`; ctx.fillRect(r() * w, r() * h, 2 + r() * 3, 2 + r() * 3); } }).tex;
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(.12, .12);
  const stone = new THREE.MeshStandardMaterial({ map: tex, roughness: .85 });
  const bay = (H, hole) => { const W0 = 1, s = new THREE.Shape(); s.moveTo(-W0 / 2, 0); s.lineTo(W0 / 2, 0); s.lineTo(W0 / 2, H); s.lineTo(-W0 / 2, H); s.closePath();
    const p = new THREE.Path(); if (hole === 'arch') { const hw = .31, sp = H * .56; p.moveTo(-hw, .4); p.lineTo(hw, .4); p.lineTo(hw, sp); p.absarc(0, sp, hw, 0, Math.PI, false); p.lineTo(-hw, .4); } else { p.moveTo(-.12, H * .5); p.lineTo(.12, H * .5); p.lineTo(.12, H * .72); p.lineTo(-.12, H * .72); p.closePath(); }
    s.holes.push(p); const e = new THREE.ExtrudeGeometry(s, { depth: 3.2, bevelEnabled: false, curveSegments: 10 }); e.translate(0, 0, -3.2); return e; };
  const levels = [[0, 10.5, 'arch'], [10.5, 10.5, 'arch'], [21, 10.5, 'arch'], [31.5, 16.5, 'win']], dm = new THREE.Object3D();
  for (const [y0, H, kind] of levels) { const im = new THREE.InstancedMesh(bay(H, kind), stone, N);
    for (let i = 0; i < N; i++) { const th = (i + .5) / N * Math.PI * 2, c = Math.cos(th), s = Math.sin(th); const ds = Math.hypot(a * s, b * c) * (Math.PI * 2 / N); const nx = c / a, nz = s / b;
      dm.position.set(a * c, y0, b * s); dm.rotation.set(0, Math.atan2(nx, nz), 0); dm.scale.set(ds * 1.01, 1, 1); dm.updateMatrix(); im.setMatrixAt(i, dm.matrix); }
    g.add(im); }
  const ring = (y, out, inn, th, mat = stone) => { const s = new THREE.Shape(); s.absellipse(0, 0, a + out, b + out, 0, Math.PI * 2); const h = new THREE.Path(); h.absellipse(0, 0, a - inn, b - inn, 0, Math.PI * 2); s.holes.push(h);
    const e = new THREE.ExtrudeGeometry(s, { depth: th, bevelEnabled: false, curveSegments: 96 }); e.rotateX(-Math.PI / 2); const m = new THREE.Mesh(e, mat); m.position.y = y; g.add(m); };
  ring(10.2, .9, 3.4, .9); ring(20.7, .9, 3.4, .9); ring(31.2, .9, 3.4, .9); ring(47.4, 1.1, 3.4, 1.0); ring(-.6, 3, 60, .7);
  const core = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 31, 96, 1, true), new THREE.MeshStandardMaterial({ color: 0x2b2018, roughness: 1, side: THREE.DoubleSide })); core.scale.set(a - 3.6, 1, b - 3.6); core.position.y = 15.5; g.add(core);
  const seatTex = canvasTex(64, 512, (ctx, w, h) => { for (let i = 0; i < 32; i++) { ctx.fillStyle = i % 2 ? '#cdbb98' : '#a8977a'; ctx.fillRect(0, i * 16, w, 16); } }).tex;
  const prof = [[.40, 3], [.44, 5], [.6, 16], [.76, 27], [.92, 38], [.955, 38], [.955, 31]].map(([r, y]) => new THREE.Vector2(r, y));
  const seats = new THREE.Mesh(new THREE.LatheGeometry(prof, 96), new THREE.MeshStandardMaterial({ map: seatTex, roughness: .9, side: THREE.DoubleSide })); seats.scale.set(a, 1, b); g.add(seats);
  const arena = new THREE.Mesh(new THREE.CircleGeometry(1, 64), new THREE.MeshStandardMaterial({ color: 0xd8b98a, roughness: 1 })); arena.rotation.x = -Math.PI / 2; arena.scale.set(a * .41, b * .41, 1); arena.position.y = 3.1; g.add(arena);
  g.scale.setScalar(1 / 78); return shadowAll(g);
}
{ const p = plinth(3.0, 2.6, .55); p.position.x = X.col; scene.add(p); const c = colosseum(); c.position.set(X.col, .56, 0); scene.add(c); }

// ---------------------------------------------------------------- B. Globe with the empire overlay
const GR = .78, GY = 1.55, globe = new THREE.Group(); globe.position.set(X.globe, GY, 0); scene.add(globe);
const ll = (lon, lat, r = GR) => { const ph = (lon + 180) / 180 * Math.PI, la = lat / 180 * Math.PI; return V(-Math.cos(ph) * Math.cos(la) * r, Math.sin(la) * r, Math.sin(ph) * Math.cos(la) * r); };
const TL = new THREE.TextureLoader();
const earthImg = await TL.loadAsync('./assets/planets/earth_atmos_2048.jpg'); earthImg.colorSpace = THREE.SRGBColorSpace; earthImg.anisotropy = 8;
const earthM = new THREE.Mesh(new THREE.SphereGeometry(GR, 128, 96), new THREE.MeshStandardMaterial({ map: earthImg, normalMap: TL.load('./assets/planets/earth_normal_2048.jpg'), roughness: .55, metalness: 0, emissive: 0xffffff, emissiveMap: earthImg, emissiveIntensity: .22 })); earthM.castShadow = true; globe.add(earthM);
const EMPIRE = [[-10, 36], [-10, 44], [-5, 48.8], [-5.5, 50], [-3.5, 54.9], [-1.5, 55], [1.8, 52.8], [4.5, 52.3], [6.5, 51.8], [8.3, 50], [8.5, 48.5], [10.5, 48.8], [13.5, 48.6], [17, 48], [19, 47.7], [19.3, 45.5], [21.5, 44.8], [22, 47.8], [24.5, 48], [26.8, 47], [27.5, 45.4], [29.7, 45.3], [29, 41], [36, 41.2], [40, 41], [44, 41.5], [48, 40], [49.5, 38], [48, 31], [47.8, 30], [44, 31], [39, 32.5], [36, 29.5], [35, 28], [34.5, 25], [33, 23.8], [31.5, 24], [30, 28], [25, 30.5], [20, 30.2], [15, 31], [10, 32.5], [8, 34], [0, 34.5], [-6, 33.5], [-8, 33.5]];
const overlay = (() => { const Wd = 1024, Hd = 512, c = document.createElement('canvas'); c.width = Wd; c.height = Hd; const ctx = c.getContext('2d', { willReadFrequently: true });
  ctx.drawImage(earthImg.image, 0, 0, Wd, Hd); const land = ctx.getImageData(0, 0, Wd, Hd).data;
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, Wd, Hd); ctx.fillStyle = '#fff'; ctx.beginPath(); EMPIRE.forEach(([lo, la], i) => { const x = (lo + 180) / 360 * Wd, y = (90 - la) / 180 * Hd; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.closePath(); ctx.fill();
  const emp = ctx.getImageData(0, 0, Wd, Hd).data, out = new Uint8Array(Wd * Hd * 4), rome = ll(12.5, 41.9, 1);
  for (let y = 0; y < Hd; y++) for (let x = 0; x < Wd; x++) { const i = (y * Wd + x) * 4, o = ((Hd - 1 - y) * Wd + x) * 4; const r = land[i], g2 = land[i + 1], b = land[i + 2];
    const isLand = !(b > r * 1.25 && b > g2 * .98) || (r > 150 && g2 > 150); const lon = x / Wd * 360 - 180, lat = 90 - y / Hd * 180;
    out[o] = emp[i] > 128 ? (lon < 19 ? 128 : 255) : 0; out[o + 1] = isLand ? 255 : 0; out[o + 2] = Math.acos(clamp(ll(lon, lat, 1).dot(rome), -1, 1)) / Math.PI * 255; out[o + 3] = 255; }
  const t = new THREE.DataTexture(out, Wd, Hd); t.magFilter = t.minFilter = THREE.LinearFilter; t.needsUpdate = true;
  const m = new THREE.Mesh(new THREE.SphereGeometry(GR * 1.004, 128, 96), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: { tD: { value: t }, uWest: { value: 1 }, uEast: { value: 1 }, uSpread: { value: 0 }, uPulse: { value: 0 } },
    vertexShader: `varying vec2 vUv; varying vec3 vN; void main(){ vUv = uv; vN = normalize(normalMatrix * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }`,
    fragmentShader: `uniform sampler2D tD; uniform float uWest,uEast,uSpread,uPulse; varying vec2 vUv; varying vec3 vN;
      void main(){ vec4 d = texture2D(tD, vUv); float west = smoothstep(.3,.45,d.r) * (1. - smoothstep(.6,.75,d.r)), east = smoothstep(.75,.9,d.r);
        float sp = uSpread > .001 ? 1. - smoothstep(uSpread - .02, uSpread, d.b) : 0.; float a = d.g * max(max(west * uWest, east * uEast), sp);
        float edge = uSpread > .001 ? (1. - smoothstep(0., .03, abs(d.b - uSpread + .02))) * d.g : 0.;
        vec3 col = mix(vec3(.94,.42,.16), vec3(1.,.82,.5), edge + uPulse * .25); float lit = .55 + .45 * max(dot(vN, normalize(vec3(.3,.6,.7))), 0.);
        gl_FragColor = vec4(col * lit, a * .78 + edge * .5); }` }));
  globe.add(m); return m.material.uniforms; })();
// the paved roads as one line wrapped twice around the planet
const roadPts = []; for (let i = 0; i <= 400; i++) { const s = i / 400; roadPts.push(ll(12.5 + s * 720, 41.9 * (1 - s * 1.2) * Math.cos(s * Math.PI * 2) * .6 + 10 * Math.sin(s * Math.PI * 4), GR * 1.012)); }
const road = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(roadPts), 800, .0045, 8), new THREE.MeshBasicMaterial({ color: 0xfff0d0, toneMapped: false })); globe.add(road);
const roadN = road.geometry.index.count;
{ const st = new THREE.Group(); const base = new THREE.Mesh(new THREE.CylinderGeometry(.34, .4, .07, 64), bronze); base.position.y = .035; const post = new THREE.Mesh(new THREE.CylinderGeometry(.035, .05, GY - GR - .1, 24), bronze); post.position.y = (GY - GR - .1) / 2 + .05;
  const arc = new THREE.Mesh(new THREE.TorusGeometry(GR + .07, .022, 16, 96, Math.PI), bronze); arc.position.y = GY; arc.rotation.set(0, Math.PI / 2, -Math.PI / 2 + .41);
  const cup = new THREE.Mesh(new THREE.SphereGeometry(.07, 24, 16), bronze); cup.position.y = GY - GR - .04; st.add(base, post, arc, cup); st.position.x = X.globe; scene.add(shadowAll(st)); }
const GLOBE_YAW = -2.38;

// ---------------------------------------------------------------- C. Roman steam locomotive (speculation)
const train = new THREE.Group(), wheels = [];
{ const boiler = new THREE.Mesh(new THREE.CylinderGeometry(.2, .2, 1.05, 48), darkIron); boiler.rotation.z = Math.PI / 2; boiler.position.set(.1, .52, 0);
  const smoke = new THREE.Mesh(new THREE.CylinderGeometry(.215, .215, .16, 48), bronze); smoke.rotation.z = Math.PI / 2; smoke.position.set(.7, .52, 0);
  const face = new THREE.Mesh(new THREE.SphereGeometry(.2, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), darkIron); face.rotation.z = -Math.PI / 2; face.scale.y = .35; face.position.set(.78, .52, 0);
  const wreath = new THREE.Mesh(new THREE.TorusGeometry(.105, .018, 12, 48), gold); wreath.rotation.y = Math.PI / 2; wreath.position.set(.855, .52, 0);
  const chim = new THREE.Mesh(new THREE.CylinderGeometry(.075, .05, .26, 32), darkIron); chim.position.set(.62, .84, 0); const chimTop = new THREE.Mesh(new THREE.TorusGeometry(.075, .016, 12, 32), gold); chimTop.rotation.x = Math.PI / 2; chimTop.position.set(.62, .97, 0);
  const dome = new THREE.Mesh(new THREE.SphereGeometry(.09, 32, 24), gold); dome.position.set(.18, .74, 0); dome.scale.y = 1.15;
  const bands = [-.3, .0, .45].map(x => { const b = new THREE.Mesh(new THREE.TorusGeometry(.203, .012, 10, 48), gold); b.rotation.y = Math.PI / 2; b.position.set(x, .52, 0); return b; });
  const cab = new THREE.Mesh(new RoundedBoxGeometry(.46, .56, .5, 4, .03), romanRed); cab.position.set(-.62, .62, 0);
  const roof = new THREE.Mesh(new RoundedBoxGeometry(.56, .05, .58, 3, .02), gold); roof.position.set(-.62, .92, 0);
  const sp = canvasTex(256, 128, (ctx, w, h) => { ctx.fillStyle = '#8f1c21'; ctx.fillRect(0, 0, w, h); ctx.strokeStyle = '#e9b84a'; ctx.lineWidth = 8; ctx.strokeRect(10, 10, w - 20, h - 20); ctx.fillStyle = '#f0c35a'; ctx.font = '700 64px Georgia, serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('SPQR', w / 2, h / 2 + 4); }).tex;
  for (const s of [-1, 1]) { const pl = new THREE.Mesh(new THREE.PlaneGeometry(.34, .17), new THREE.MeshStandardMaterial({ map: sp, roughness: .4, metalness: .3 })); pl.position.set(-.62, .56, s * .252); pl.rotation.y = s > 0 ? 0 : Math.PI; train.add(pl);
    const win = new THREE.Mesh(new THREE.PlaneGeometry(.2, .14), new THREE.MeshStandardMaterial({ color: 0x1a2430, roughness: .1, metalness: .6 })); win.position.set(-.62, .78, s * .252); win.rotation.y = s > 0 ? 0 : Math.PI; train.add(win); }
  const frame = new THREE.Mesh(new RoundedBoxGeometry(1.75, .07, .4, 2, .02), darkIron); frame.position.set(0, .3, 0);
  const cow = new THREE.Mesh(new THREE.CylinderGeometry(.02, .22, .2, 4, 1), bronze); cow.rotation.set(0, Math.PI / 4, -Math.PI / 2); cow.scale.z = 1.6; cow.position.set(.98, .2, 0);
  const wt = canvasTex(256, 256, (ctx, w, h) => { ctx.clearRect(0, 0, w, h); ctx.translate(w / 2, h / 2); ctx.strokeStyle = '#b3812f'; ctx.lineWidth = 14; for (let i = 0; i < 8; i++) { ctx.rotate(Math.PI / 4); ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, 104); ctx.stroke(); } ctx.fillStyle = '#e9b84a'; ctx.beginPath(); ctx.arc(0, 0, 26, 0, 7); ctx.fill(); }).tex;
  for (const [x, r] of [[.5, .17], [.08, .17], [-.34, .17], [-.72, .12]]) for (const s of [-1, 1]) { const w = new THREE.Group(); const rim = new THREE.Mesh(new THREE.TorusGeometry(r - .02, .024, 12, 48), darkIron); const sp2 = new THREE.Mesh(new THREE.CircleGeometry(r - .02, 32), new THREE.MeshStandardMaterial({ map: wt, transparent: true, alphaTest: .4, side: THREE.DoubleSide, metalness: .8, roughness: .3 })); w.add(rim, sp2); w.position.set(x, r, s * .235); w.userData.r = r; wheels.push(w); train.add(w); }
  for (const s of [-1, 1]) { const rod = new THREE.Mesh(new RoundedBoxGeometry(.9, .028, .016, 2, .006), gold); rod.position.set(.08, .17, s * .27); rod.userData.rod = s; train.add(rod); }
  train.add(boiler, smoke, face, wreath, chim, chimTop, dome, ...bands, cab, roof, frame, cow); shadowAll(train); }
const trainBase = new THREE.Group(); { const p = plinth(3.2, 1.0, .5); const railM = new THREE.MeshStandardMaterial({ color: 0x8d9099, metalness: 1, roughness: .25 });
  for (const s of [-1, 1]) { const r = new THREE.Mesh(new THREE.BoxGeometry(3.1, .03, .025), railM); r.position.set(0, .535, s * .235); trainBase.add(r); }
  for (let i = 0; i < 21; i++) { const sl = new THREE.Mesh(new THREE.BoxGeometry(.07, .025, .62), new THREE.MeshStandardMaterial({ color: 0x4a3626, roughness: .9 })); sl.position.set(-1.5 + i * .15, .512, 0); trainBase.add(sl); }
  trainBase.add(p); trainBase.position.x = X.train; scene.add(shadowAll(trainBase)); train.position.set(X.train, .55, 0); scene.add(train); }
// steam puffs (shared)
const puffTex = canvasTex(128, 128, (ctx, w, h) => { const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); g.addColorStop(0, 'rgba(255,255,255,.85)'); g.addColorStop(.6, 'rgba(250,250,250,.35)'); g.addColorStop(1, 'rgba(250,250,250,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }).tex;
const mkPuffs = n => Array.from({ length: n }, () => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTex, transparent: true, depthWrite: false, opacity: 0 })); scene.add(s); return s; });
const trainPuffs = mkPuffs(14), aeoPuffs = mkPuffs(20);

// ---------------------------------------------------------------- D. Moon diorama with a Roman standard (speculation)
const moonG = new THREE.Group(); { const mt = TL.load('./assets/planets/moon_1024.jpg'); mt.colorSpace = THREE.SRGBColorSpace; mt.wrapS = mt.wrapT = THREE.RepeatWrapping; mt.repeat.set(.35, .5); mt.offset.set(.3, .25);
  const base = plinth(2.3, 2.3, .5); const geo = new THREE.CircleGeometry(1.05, 96, 0, Math.PI * 2); const r = rand(17), p = geo.attributes.position; const craters = Array.from({ length: 9 }, () => [(r() - .5) * 1.7, (r() - .5) * 1.7, .08 + r() * .2]);
  const g2 = new THREE.PlaneGeometry(2.1, 2.1, 160, 160), q = g2.attributes.position; for (let i = 0; i < q.count; i++) { const x = q.getX(i), y = q.getY(i); let z = .012 * Math.sin(x * 9) * Math.cos(y * 7); for (const [cx, cy, cr] of craters) { const d = Math.hypot(x - cx, y - cy) / cr; if (d < 1.25) z += d < 1 ? -cr * .22 * (1 - d * d) : cr * .08 * (1 - (d - 1) / .25); } const e = Math.max(Math.abs(x), Math.abs(y)); if (e > .98) z *= clamp((1.05 - e) / .07); q.setZ(i, z); }
  g2.computeVertexNormals(); const surf = new THREE.Mesh(g2, new THREE.MeshStandardMaterial({ color: 0xc4c4c9, roughness: 1, bumpMap: mt, bumpScale: 3 })); surf.rotation.x = -Math.PI / 2; surf.position.y = .535;
  const slab = new THREE.Mesh(new RoundedBoxGeometry(2.12, .1, 2.12, 2, .01), new THREE.MeshStandardMaterial({ color: 0x77777c, roughness: 1 })); slab.position.y = .46;
  // vexillum: pole, crossbar, red banner with SPQR, eagle on top
  const st = new THREE.Group(); const pole = new THREE.Mesh(new THREE.CylinderGeometry(.014, .014, 1.05, 16), gold); pole.position.y = .525; const bar = new THREE.Mesh(new THREE.CylinderGeometry(.01, .01, .42, 12), gold); bar.rotation.z = Math.PI / 2; bar.position.y = .92;
  const bt = canvasTex(256, 320, (ctx, w, h) => { ctx.fillStyle = '#9c1f24'; ctx.fillRect(0, 0, w, h); ctx.strokeStyle = '#e9b84a'; ctx.lineWidth = 10; ctx.strokeRect(12, 12, w - 24, h - 24); ctx.fillStyle = '#f0c35a'; ctx.font = '700 74px Georgia, serif'; ctx.textAlign = 'center'; ctx.fillText('SPQR', w / 2, 150); ctx.beginPath(); ctx.arc(w / 2, 225, 34, 0, 7); ctx.lineWidth = 9; ctx.stroke(); for (let i = 0; i < 7; i++) ctx.fillRect(22 + i * 32, h - 14, 20, 14); }).tex;
  const bg = new THREE.PlaneGeometry(.38, .46, 12, 1), bp2 = bg.attributes.position; for (let i = 0; i < bp2.count; i++) bp2.setZ(i, .012 * Math.sin(bp2.getX(i) * 22)); bg.computeVertexNormals();
  const banner = new THREE.Mesh(bg, new THREE.MeshStandardMaterial({ map: bt, side: THREE.DoubleSide, roughness: .7, emissive: 0xffffff, emissiveMap: bt, emissiveIntensity: .25 })); banner.position.set(0, .685, .022);
  const eagle = new THREE.Group(); const body = new THREE.Mesh(new THREE.SphereGeometry(.035, 20, 16), gold); body.scale.set(.9, 1.4, .9); const head = new THREE.Mesh(new THREE.SphereGeometry(.02, 16, 12), gold); head.position.set(.012, .058, 0); const beak = new THREE.Mesh(new THREE.ConeGeometry(.008, .024, 10), gold); beak.rotation.z = -Math.PI / 2; beak.position.set(.036, .056, 0);
  const wsh = new THREE.Shape(); wsh.moveTo(0, 0); wsh.quadraticCurveTo(.06, .1, .15, .09); wsh.lineTo(.125, .06); wsh.lineTo(.135, .035); wsh.lineTo(.1, .025); wsh.lineTo(.105, 0); wsh.lineTo(.07, -.005); wsh.quadraticCurveTo(.03, -.03, 0, -.02); const wgeo = new THREE.ExtrudeGeometry(wsh, { depth: .008, bevelEnabled: false });
  for (const s of [-1, 1]) { const wg = new THREE.Mesh(wgeo, gold); wg.rotation.y = s > 0 ? -Math.PI / 2 : Math.PI / 2; wg.position.set(0, .012, s * .02); if (s < 0) wg.position.z -= 0; eagle.add(wg); }
  const perch = new THREE.Mesh(new THREE.TorusGeometry(.04, .009, 10, 32), gold); perch.rotation.x = Math.PI / 2; perch.position.y = -.05; eagle.add(body, head, beak, perch); eagle.position.y = 1.1; eagle.rotation.y = Math.PI / 2;
  st.add(pole, bar, banner, eagle); st.position.set(.15, .52, .15); st.rotation.y = -.58; st.scale.setScalar(1.2);
  moonG.add(base, slab, surf, st); moonG.position.x = X.moon; scene.add(shadowAll(moonG)); surf.castShadow = false; }

// ---------------------------------------------------------------- E. Hero's aeolipile (real, 1st century AD)
const aeo = new THREE.Group(), ball = new THREE.Group();
{ const ped = plinth(.8, .8, 1.0); const prof = [[0, 0], [.2, 0], [.26, .06], [.28, .16], [.24, .26], [.16, .3], [0, .3]].map(([r, y]) => new THREE.Vector2(r, y));
  const caul = new THREE.Group(); { const bd = new THREE.Mesh(new THREE.SphereGeometry(.27, 48, 32), bronze); bd.scale.y = .62; bd.position.y = .17; const lid = new THREE.Mesh(new THREE.TorusGeometry(.2, .018, 12, 48), gold); lid.rotation.x = Math.PI / 2; lid.position.y = .3; caul.add(bd, lid); } caul.position.y = 1.2;
  const legs = [0, 1, 2].map(i => { const l = new THREE.Mesh(new THREE.CylinderGeometry(.014, .014, .24, 10), darkIron); const a = i * 2.094 + .5; l.position.set(Math.cos(a) * .2, 1.1, Math.sin(a) * .2); l.rotation.set(Math.sin(a) * .25, 0, -Math.cos(a) * .25); return l; });
  const fire = [0, 1, 2, 3].map(i => { const f = new THREE.Mesh(new THREE.ConeGeometry(.05, .14, 12), new THREE.MeshBasicMaterial({ color: i % 2 ? 0xffb347 : 0xff7a1a, toneMapped: false })); f.position.set(Math.cos(i * 1.6) * .06, 1.08, Math.sin(i * 1.6) * .06); f.userData.fire = i; return f; });
  const tray = new THREE.Mesh(new THREE.CylinderGeometry(.16, .14, .03, 32), darkIron); tray.position.y = 1.015;
  const pipes = [-1, 1].map(s => { const g = new THREE.Group(); const up = new THREE.Mesh(new THREE.CylinderGeometry(.016, .016, .3, 12), bronze); up.position.set(s * .19, 1.63, 0); const inn = new THREE.Mesh(new THREE.CylinderGeometry(.016, .016, .08, 12), bronze); inn.rotation.z = Math.PI / 2; inn.position.set(s * .155, 1.78, 0); g.add(up, inn); return g; });
  const sph = new THREE.Mesh(new THREE.SphereGeometry(.125, 48, 32), new THREE.MeshStandardMaterial({ color: 0xc98a45, metalness: 1, roughness: .2 }));
  const band = new THREE.Mesh(new THREE.TorusGeometry(.126, .008, 10, 48), gold); band.rotation.y = Math.PI / 2; ball.add(sph, band);
  for (const s of [-1, 1]) { const n1 = new THREE.Mesh(new THREE.CylinderGeometry(.014, .014, .09, 10), bronze); n1.position.set(0, s * .165, 0); const n2 = new THREE.Mesh(new THREE.CylinderGeometry(.012, .014, .07, 10), bronze); n2.rotation.x = Math.PI / 2; n2.position.set(0, s * .205, s * .03); ball.add(n1, n2); }
  ball.position.y = 1.78; aeo.add(ped, caul, ...legs, ...fire, tray, ...pipes, ball); aeo.position.x = X.aeo; scene.add(shadowAll(aeo)); aeo.userData.fire = fire; fire.forEach(f => f.castShadow = false); }

// ---------------------------------------------------------------- Jeremy at three exhibits
const J1 = K.J, J2 = makeJeremy2(), J3 = makeJeremy2(); [J2, J3].forEach(j => { scene.add(j); rimLight(j); });
const putJ = (J, x, z, ry, pose) => { J.visible = true; J.position.set(x, 0, z); J.rotation.set(0, ry, 0); J.scale.setScalar(.75); J.pose(pose); };

// ---------------------------------------------------------------- timeline (from the voiceover)
const T0 = LN.map(l => l.t0), T1 = LN.map(l => l.t1), endAt = T0[10] + 2.3;
const lineAt = t => { let i = 0; for (let k = 0; k < LN.length; k++) if (t >= T0[k] - .05) i = k; return i; };
const CAM = [ // one per narration line: [target x, y, dist, yaw, pitch]
  [X.col, .8, 10.2, -.62, .34], [X.globe, GY, 7.4, -.5, .16], [X.globe, GY, 6.6, -.44, .14], [X.globe, GY, 6.9, -.5, .16], [X.globe, GY, 7.6, -.55, .16], [X.globe, GY, 8.0, -.6, .16],
  [X.train, .85, 9.8, -.5, .2], [X.moon, 1.0, 8.6, -.58, .28], [X.aeo, 1.5, 5.0, -.5, .14], [X.aeo, 1.66, 3.1, -.4, .1], [X.aeo + .45, 1.2, 8.3, -.5, .16]];
function camAt(t) { let c = CAM[0].slice(); for (let i = 1; i < CAM.length; i++) { const k = eInOut(clamp((t - (T0[i] - .8)) / 1.3)); if (k <= 0) break; c = c.map((v, j) => lerp(v, CAM[i][j], k)); } return c; }
const HUDS = [['80 AD', 'FACT', 'THE COLOSSEUM', '50,000 seats'], ['117 AD', 'FACT', 'TERRITORY', '5 million km²'], ['117 AD', 'FACT', 'PAVED ROADS', '80,500 km'], ['476 AD', 'FACT', 'THE WESTERN EMPIRE', 'Falls'], ['What if?', 'SPECULATION', 'THE EMPIRE', 'Never falls'],
  ['What if?', 'SPECULATION', 'LATIN LANGUAGES TODAY', '900 million speakers'], ['What if?', 'SPECULATION', 'STEAM POWER', 'Centuries early'], ['What if?', 'SPECULATION', 'FIRST FLAG ON THE MOON', 'Roman?'], ['1st century', 'FACT', "HERO'S STEAM ENGINE", 'Already existed'], ['1st century', 'FACT', 'YEARS AS A TOY', '400'], ['1st century', 'FACT', 'YEARS AS A TOY', '400']];
window.SPEC = { total, reel: 1, ctaAt: endAt, subtle: true, beats: [],
  beds: [{ t0: 0, t1: total, name: 'room', gain: .1 }, { t0: T0[7] - .5, t1: T1[7] + .4, name: 'space', gain: .2 }],
  sfx: [...[1, 6, 7, 8].map(i => ({ t: T0[i] - .85, name: 'glide', gain: .3 })), { t: T0[1] + .1, name: 'swell', gain: .3 }, { t: T0[2] + .2, name: 'riser_soft', gain: 0 }, { t: T0[3] + 1.4, name: 'rumble_low', gain: .55 },
    { t: T0[4], name: 'chime', gain: .28 }, { t: T0[4] + .2, name: 'swell', gain: .32 }, { t: T0[6] + .1, name: 'chuff', gain: .4 }, { t: T0[8] + 1.2, name: 'hiss', gain: .3 }, { t: T0[9], name: 'hiss', gain: .22 }, { t: endAt, name: 'chime', gain: .3 }].filter(e => e.gain > 0) };
$('v5line').style.width = '840px'; $('v5line').style.fontSize = '38px'; $('v5line').style.lineHeight = '1.18';

window.renderAt = (t) => {
  tagsReset();
  const i = lineAt(t), lt = t - T0[i], ld = T1[i] - T0[i];
  // ---- globe state
  const u = overlay; let west = 1, east = 1, spread = 0;
  if (i === 3) west = 1 - eInOut(clamp((lt - 1.3) / 1.3));
  if (i >= 4) { west = t < T0[4] + .5 ? eOut(clamp(lt / .5)) : 1; spread = i === 4 ? .02 + eInOut(clamp((lt - .4) / (ld + .2))) * .45 : .47 + eOut(clamp((t - T0[5]) / 2.2)) * .56; }
  u.uWest.value = west; u.uEast.value = east; u.uSpread.value = spread; u.uPulse.value = .5 + .5 * Math.sin(t * 3);
  globe.rotation.x = .5; globe.rotation.y = GLOBE_YAW + (i >= 5 ? eInOut(clamp((t - T0[5]) / 2.6)) * Math.PI * 2 : 0) + Math.sin(t * .2) * .03;
  const rk = i === 2 ? eInOut(clamp((lt - .3) / 3.2)) : i > 2 ? 1 : 0; road.visible = rk > 0 && i < 4; road.geometry.setDrawRange(0, Math.floor(roadN * rk / 3) * 3); road.material.opacity = 1;
  // ---- train
  const tk = i === 6 ? eOut(clamp(lt / 2.2)) : i > 6 ? 1 : 0; const tx = lerp(-.6, .22, tk); train.position.x = X.train + tx;
  wheels.forEach(w => w.rotation.z = -tx / w.userData.r); train.children.forEach(o => { if (o.userData.rod) { const a = -tx / .17; o.position.set(.08 + Math.cos(a) * .06, .17 + Math.sin(a) * .06, o.userData.rod * .27); } });
  trainPuffs.forEach((s, n) => { const k = ((t * .55 + n / trainPuffs.length) % 1); s.position.set(train.position.x + .62 - k * .7 * (i === 6 ? 1 : .4), 1.55 + k * .55, Math.sin(n * 2.3) * .08 * k); s.scale.setScalar(.12 + k * .4); s.material.opacity = (i >= 6 && i <= 7 ? 1 : 0) * (1 - k) * .75; });
  // ---- aeolipile
  ball.rotation.x = t * 9; aeo.userData.fire.forEach(f => f.scale.y = 1 + .25 * Math.sin(t * 17 + f.userData.fire * 2));
  aeoPuffs.forEach((s, n) => { const k = ((t * .9 + n / aeoPuffs.length) % 1), sgn = n % 2 ? 1 : -1, a = ball.rotation.x - k * 2.2; s.position.set(X.aeo + (n % 3 - 1) * .01, 1.78 + sgn * Math.cos(a) * (.21 + k * .16), sgn * Math.sin(a) * (.21 + k * .16)); s.scale.setScalar(.05 + k * .2); s.material.opacity = (1 - k) * .7; });
  // ---- Jeremys
  putJ(J1, X.col + .75, -1.75, -.55, { expr: 'happy', look: -.4, armL: .25, armR: i === 0 ? 2.2 + Math.sin(t * 7) * .35 : .25, blink: (t % 2.7) < .1 });
  putJ(J2, X.train + 1.35, -1.0, -.6, { expr: i === 6 ? 'shocked' : 'happy', look: -.5, armL: i === 6 ? 2.2 : .25, armR: i === 6 ? 2.2 : .25, blink: (t % 3.1) < .1 });
  putJ(J3, X.aeo + 1.52, .22, -.85, { expr: i >= 10 ? 'confused' : i === 9 ? 'worried' : 'happy', look: -.6, armL: i >= 10 ? 1.3 : .25, armR: i >= 10 ? 1.3 : .25, tilt: i >= 10 ? .12 : 0, blink: (t % 2.3) < .1 });
  // ---- light mood: slightly dimmer and cooler on the Moon beat
  const mk = eInOut(clamp((t - (T0[7] - .6)) / 1)) * (1 - eInOut(clamp((t - (T0[8] - .7)) / 1)));
  renderer.toneMappingExposure = lerp(.4, .36, mk); key.intensity = lerp(1.7, 2.6, mk); hemi.intensity = lerp(.4, .16, mk); scene.environmentIntensity = lerp(.32, .14, mk);
  // ---- camera: one continuous glide along the gallery, drifting slowly inside each beat
  const c = camAt(t), drift = clamp(lt / Math.max(ld, 1));
  const tgt = V(c[0], c[1], 0), dist = c[2] * (1 - .035 * drift);
  orbit(tgt, dist, { yaw: c[3] + .04 * drift + t * .002, pitch: c[4], fov: 34, lookUp: .075 });
  shadowFit(tgt, 4.2); DOF.on = true; DOF.focus = dist; DOF.aperture = .55; DOF.maxR = 9;
  // ---- callout tags
  const A = (t0, t1) => clamp((t - t0) / .35) * clamp((t1 - t) / .3);
  if (i === 0) tag3('COLOSSEUM', 'opened 80 AD · 189 m wide', V(X.col - .7, .6, 1.25), A(T0[0] + .5, T0[1] - .7));
  if (i === 1 || i === 2) tag3('ROMAN EMPIRE', i === 1 ? 'about 1 in 5 humans' : '80,500 km of paved road', globe.localToWorld(ll(14, 60, GR * 1.02)), A(T0[1] + .6, T0[3] - .1));
  if (i === 3) { tag3('WEST', 'falls in 476', globe.localToWorld(ll(2, 47, GR * 1.02)), A(T0[3] + 1.2, T0[4] - .1)); tag3('EAST', 'lasts until 1453', globe.localToWorld(ll(38, 33, GR * 1.02)), A(T0[3] + 3.2, T0[4] - .1)); }
  if (i === 5) tag3('FACT', "900 million speak Latin's descendants", V(X.globe, GY + GR + .12, 0), A(T0[5] + .5, T0[6] - .7));
  if (i === 6) tag3('SPECULATION', 'real steam trains: 1804', V(train.position.x - .62, 1.52, 0), A(T0[6] + .6, T0[7] - .7));
  if (i === 7) tag3('SPECULATION', 'real Moon landing: 1969', V(X.moon - .55, .62, .75), A(T0[7] + .5, T0[8] - .8));
  if (i === 8 || i === 9) tag3('AEOLIPILE', i === 8 ? 'steam spins the sphere' : 'a curiosity, never put to work', V(X.aeo, 2.08, 0), A(T0[8] + 1.6, T0[10] - .2));
  tagsEnd();
  // ---- HUD
  const H = HUDS[i], endK = clamp((t - endAt) / .35), endIn = clamp((t - endAt - .35) / .45);
  let year = H[0]; if (i === 3) year = Math.round(lerp(117, 476, eInOut(clamp(lt / 1.6)))) + ' AD';
  let val = H[3]; if (i === 2) val = Math.round(80500 * eOut(clamp((lt - .2) / 2.4)) / 100) * 100 >= 80500 ? '80,500 km' : (Math.round(80500 * eOut(clamp((lt - .2) / 2.4)) / 100) * 100).toLocaleString('en-US') + ' km';
  if (i >= 9) val = String(Math.round(400 * eOut(clamp((t - T0[9]) / 1.2))));
  const fadeIn = clamp(lt / .25);
  setHUD({ q: 'What if the Roman Empire <b>never collapsed</b>?', qA: clamp((t - .2) / .4) * (1 - endK), l1: 'YEAR', n1: year, l2: 'THIS PART IS', n2: H[1], l3: H[2], val,
    line: i === 0 ? '' : LN[i].show, lineA: fadeIn * clamp((T1[i] + .25 - t) / .2 + (i === 10 ? 9 : 0)), dataA: (1 - endK),
    end: 'Which moment in history<br>would <b>you</b> change? 👇', endA: endIn });
  $('v5n2').style.color = H[1] === 'FACT' ? '#fff' : ACCENT;
  draw();
};
window.READY = true;
