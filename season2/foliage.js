// v4 realism: leaf-card foliage and blade-card grass (alpha-textured, no visible polygons).
import { THREE, canvasTex, rand, INK } from './engine.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

// ---- leaf cluster texture (many small leaves with veins and light/dark variation) ----
function leafCanvas(seed, hue) {
  return canvasTex(512, 512, (ctx, w, h) => {
    ctx.clearRect(0, 0, w, h); const r = rand(seed);
    for (let i = 0; i < 260; i++) {
      const a = r() * Math.PI * 2, d = Math.sqrt(r()) * w * .44, x = w / 2 + Math.cos(a) * d, y = h / 2 + Math.sin(a) * d;
      const L = 18 + r() * 22, W = L * (.42 + r() * .12), rot = r() * Math.PI * 2;
      const li = 22 + r() * 26 + (1 - d / (w * .44)) * 8;
      ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
      ctx.fillStyle = `hsl(${hue + r() * 18 - 9},${48 + r() * 22}%,${li}%)`;
      ctx.beginPath(); ctx.moveTo(-L / 2, 0); ctx.quadraticCurveTo(0, -W, L / 2, 0); ctx.quadraticCurveTo(0, W, -L / 2, 0); ctx.fill();
      ctx.strokeStyle = `hsla(${hue},40%,${li + 14}%,.55)`; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(-L / 2, 0); ctx.lineTo(L / 2, 0); ctx.stroke();
      ctx.restore();
    }
  }).tex;
}
const LEAF = [leafCanvas(11, 105), leafCanvas(12, 95), leafCanvas(13, 115)];
export const leafMats = LEAF.map(t => new THREE.MeshStandardMaterial({ map: t, alphaTest: .45, side: THREE.DoubleSide, roughness: .75, metalness: 0 }));
const inner = [0x2c5a24, 0x34662a, 0x274f22].map(c => new THREE.MeshStandardMaterial({ color: c, roughness: .9 }));
const card = new THREE.PlaneGeometry(1, 1);
export const CARDS = []; // leaf-card meshes: skipped in the depth/normal pass (cheaper, no square artifacts)

/** A leafy crown made of ~cards alpha-textured leaf clusters around a dark inner volume. Returns a Group. */
export function crown(radius = 1.6, seed = 1, k = 0) {
  const g = new THREE.Group(), r = rand(seed * 7 + 3);
  const core = new THREE.Mesh(new THREE.SphereGeometry(radius * .72, 20, 14), inner[k % 3]); core.scale.y = .85; core.castShadow = true; core.receiveShadow = true; g.add(core);
  const n = Math.round(12 + radius * 6), geos = [];
  for (let i = 0; i < n; i++) {
    const th = r() * Math.PI * 2, ph = Math.acos(2 * r() - 1), d = radius * (.55 + r() * .45);
    const p = new THREE.Vector3(Math.sin(ph) * Math.cos(th) * d, Math.cos(ph) * d * .82, Math.sin(ph) * Math.sin(th) * d);
    const gg = card.clone(); const s = radius * (.85 + r() * .6); gg.scale(s, s, s);
    gg.rotateX(r() * Math.PI); gg.rotateY(r() * Math.PI); gg.rotateZ(r() * Math.PI); gg.translate(p.x, p.y, p.z); geos.push(gg);
  }
  const m = new THREE.Mesh(mergeGeometries(geos), leafMats[k % 3]); m.castShadow = false; m.receiveShadow = true; m.userData.noInk = true; g.add(m); CARDS.push(m);
  INK.skip.push(m);
  return g;
}

// ---- grass: crossed alpha cards with drawn blades ----
const grassTex = canvasTex(256, 256, (ctx, w, h) => {
  ctx.clearRect(0, 0, w, h); const r = rand(21);
  for (let i = 0; i < 70; i++) {
    const x = w * (.1 + r() * .8), hh = h * (.45 + r() * .5), bend = (r() - .5) * 60, bw = 3 + r() * 5;
    ctx.fillStyle = `hsl(${85 + r() * 30},${45 + r() * 25}%,${26 + r() * 24}%)`;
    ctx.beginPath(); ctx.moveTo(x - bw, h); ctx.quadraticCurveTo(x + bend * .3, h - hh * .6, x + bend, h - hh); ctx.quadraticCurveTo(x + bend * .3 + 2, h - hh * .6, x + bw, h); ctx.fill();
  }
}).tex;
export const grassMat = new THREE.MeshStandardMaterial({ map: grassTex, alphaTest: .4, side: THREE.DoubleSide, roughness: .85 });
export const grassGeo = (() => { const a = new THREE.PlaneGeometry(.7, .5); a.translate(0, .25, 0); const b = a.clone(); b.rotateY(Math.PI / 2); const c = a.clone(); c.rotateY(Math.PI / 4); return mergeGeometries([a, b, c]); })();
