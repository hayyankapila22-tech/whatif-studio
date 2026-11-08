// Jeremy's Street — the permanent Season 2 hub set. Street runs along +X; Jeremy walks the north sidewalk (z ≈ 5.6).
import { THREE, RoundedBoxGeometry, canvasTex, rand, M } from './engine.js';

// ---------- procedural PBR texture sets (colour + normal from a height field) ----------
function heightToNormal(hc, strength = 2) {
  const w = hc.width, h = hc.height, src = hc.getContext('2d').getImageData(0, 0, w, h).data;
  const c = document.createElement('canvas'); c.width = w; c.height = h; const ctx = c.getContext('2d'); const img = ctx.createImageData(w, h);
  const H = (x, y) => src[(((y + h) % h) * w + ((x + w) % w)) * 4] / 255;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = (H(x + 1, y) - H(x - 1, y)) * strength, dy = (H(x, y + 1) - H(x, y - 1)) * strength;
    const l = Math.hypot(dx, dy, 1), i = (y * w + x) * 4;
    img.data[i] = (-dx / l * .5 + .5) * 255; img.data[i + 1] = (dy / l * .5 + .5) * 255; img.data[i + 2] = (1 / l * .5 + .5) * 255; img.data[i + 3] = 255;
  }
  ctx.putImageData(img, 0, 0); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.NoColorSpace; return t;
}
function texSet(size, drawColor, drawHeight, rep = [1, 1], strength = 2) {
  const col = canvasTex(size, size, drawColor).tex;
  const hc = document.createElement('canvas'); hc.width = hc.height = size; drawHeight(hc.getContext('2d'), size, size);
  const nor = heightToNormal(hc, strength);
  [col, nor].forEach(t => { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); t.anisotropy = 8; });
  return { map: col, normalMap: nor };
}
const speckle = (ctx, w, h, n, seed, cols, smin = 1, smax = 3) => { const r = rand(seed); for (let i = 0; i < n; i++) { ctx.fillStyle = cols[Math.floor(r() * cols.length)]; const s = smin + r() * (smax - smin); ctx.fillRect(r() * w, r() * h, s, s); } };
const asphalt = texSet(512, (ctx, w, h) => { ctx.fillStyle = '#3a3c42'; ctx.fillRect(0, 0, w, h); speckle(ctx, w, h, 9000, 1, ['#2c2e33', '#4a4c53', '#55575e', '#303238']); ctx.strokeStyle = 'rgba(20,20,24,.5)'; ctx.lineWidth = 2; const r = rand(2); for (let i = 0; i < 6; i++) { ctx.beginPath(); let x = r() * w, y = r() * h; ctx.moveTo(x, y); for (let k = 0; k < 6; k++) { x += (r() - .5) * 60; y += (r() - .5) * 60; ctx.lineTo(x, y); } ctx.stroke(); } },
  (ctx, w, h) => { ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, w, h); speckle(ctx, w, h, 12000, 3, ['#606060', '#a0a0a0', '#909090', '#707070']); }, [3, 12], 3);
const concrete = texSet(512, (ctx, w, h) => { ctx.fillStyle = '#9a968e'; ctx.fillRect(0, 0, w, h); speckle(ctx, w, h, 5000, 4, ['#8d8981', '#a7a39b', '#85817a']); ctx.strokeStyle = '#8f8b84'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 2); ctx.lineTo(w, 2); ctx.moveTo(2, 0); ctx.lineTo(2, h); ctx.stroke(); },
  (ctx, w, h) => { ctx.fillStyle = '#909090'; ctx.fillRect(0, 0, w, h); speckle(ctx, w, h, 6000, 5, ['#888', '#999', '#a0a0a0']); ctx.fillStyle = '#404040'; ctx.fillRect(0, 0, w, 4); ctx.fillRect(0, 0, 4, h); }, [10, 1], 2);
function brickSet(base, mortar, seed, rep) {
  return texSet(512, (ctx, w, h) => { ctx.fillStyle = mortar; ctx.fillRect(0, 0, w, h); const r = rand(seed); const bw = 64, bh = 24;
    for (let y = 0; y < h; y += bh) for (let x = (y / bh % 2) * -bw / 2; x < w; x += bw) { const v = .85 + r() * .3; const c = new THREE.Color(base).multiplyScalar(v); ctx.fillStyle = '#' + c.getHexString(); ctx.fillRect(x + 2, y + 2, bw - 4, bh - 4); }
    speckle(ctx, w, h, 4000, seed + 1, ['rgba(0,0,0,.12)', 'rgba(255,255,255,.08)']); },
  (ctx, w, h) => { ctx.fillStyle = '#303030'; ctx.fillRect(0, 0, w, h); const bw = 64, bh = 24; for (let y = 0; y < h; y += bh) for (let x = (y / bh % 2) * -bw / 2; x < w; x += bw) { ctx.fillStyle = '#b0b0b0'; ctx.fillRect(x + 3, y + 3, bw - 6, bh - 6); } }, rep, 4);
}
const wood = texSet(256, (ctx, w, h) => { ctx.fillStyle = '#8a5a34'; ctx.fillRect(0, 0, w, h); const r = rand(9); for (let y = 0; y < h; y += 2) { ctx.fillStyle = `rgba(${60 + r() * 40},${35 + r() * 20},15,${.2 + r() * .3})`; ctx.fillRect(0, y, w, 1 + r() * 2); } },
  (ctx, w, h) => { ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, w, h); const r = rand(10); for (let y = 0; y < h; y += 2) { ctx.fillStyle = `rgb(${100 + r() * 60},0,0)`; ctx.fillRect(0, y, w, 1); } }, [1, 1], 1.5);

export const MAT = {
  asphalt: new THREE.MeshStandardMaterial({ ...asphalt, roughness: .92, metalness: 0 }),
  concrete: new THREE.MeshStandardMaterial({ ...concrete, roughness: .85 }),
  curb: new THREE.MeshStandardMaterial({ color: 0xa8a49c, roughness: .8 }),
  paint: new THREE.MeshStandardMaterial({ color: 0xf4f4f0, roughness: .6 }),
  yellow: new THREE.MeshStandardMaterial({ color: 0xffc400, roughness: .6 }),
  glass: new THREE.MeshPhysicalMaterial({ color: 0x3f5a78, roughness: .08, metalness: .2, clearcoat: 1, envMapIntensity: .7 }),
  frame: new THREE.MeshStandardMaterial({ color: 0x2b2e36, roughness: .4, metalness: .7 }),
  wood: new THREE.MeshStandardMaterial({ ...wood, roughness: .7 }),
  bark: new THREE.MeshStandardMaterial({ color: 0x5a4130, roughness: .95 }),
  leaf: [0x3f8f3a, 0x4fa244, 0x357c33].map(c => new THREE.MeshStandardMaterial({ color: c, roughness: .8 })),
  metal: new THREE.MeshStandardMaterial({ color: 0x3a3f4a, roughness: .35, metalness: .85 }),
};
const bricks = [brickSet(0xa4553e, '#cfc6b8', 11, [3, 6]), brickSet(0xc9b28a, '#e8e0d0', 12, [3, 6]), brickSet(0x7d4a3a, '#bdb3a4', 13, [3, 6]), brickSet(0xe6dccb, '#f5f0e6', 14, [3, 6])];
const plasterCols = [0xf2e3c6, 0xe7f0f7, 0xf6d9d3, 0xd8eedf];

function box(w, h, d, mat, r = 0) { const g = r ? new RoundedBoxGeometry(w, h, d, 3, r) : new THREE.BoxGeometry(w, h, d); const m = new THREE.Mesh(g, mat); m.castShadow = m.receiveShadow = true; return m; }
function signTex(text, bg, fg, w = 1024, h = 220, font = 'IDB') { return canvasTex(w, h, (ctx) => { ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h); ctx.fillStyle = fg; ctx.font = `${h * .55}px ${font}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, w / 2, h / 2 + 6); }).tex; }

// ---------- a building with a detailed facade ----------
function building(x, z, w, d, h, side, style, seed) {
  const g = new THREE.Group(); g.position.set(x, 0, z);
  const r = rand(seed);
  const facadeMat = style < 4 ? new THREE.MeshStandardMaterial({ ...bricks[style], roughness: .9 }) : new THREE.MeshStandardMaterial({ color: plasterCols[style % 4], roughness: .85 });
  const body = box(w, h, d, facadeMat); body.position.y = h / 2; g.add(body);
  const front = side * d / 2; // facade faces the street
  // cornice + roof parapet
  const cornice = box(w + .3, .35, .5, MAT.curb); cornice.position.set(0, h - .2, front + side * .1); g.add(cornice);
  // windows (real recessed glass + frames + sills) on upper floors
  const floors = Math.floor((h - 4.2) / 3.1), cols = Math.max(2, Math.floor(w / 2.3));
  const winGeo = new THREE.BoxGeometry(1.15, 1.6, .08), frameGeo = new THREE.BoxGeometry(1.3, 1.75, .12), sillGeo = new THREE.BoxGeometry(1.45, .12, .3);
  const glassI = new THREE.InstancedMesh(winGeo, MAT.glass, floors * cols), frameI = new THREE.InstancedMesh(frameGeo, MAT.frame, floors * cols), sillI = new THREE.InstancedMesh(sillGeo, MAT.curb, floors * cols);
  const dm = new THREE.Object3D(); let n = 0;
  for (let f = 0; f < floors; f++) for (let c = 0; c < cols; c++) {
    const wx = (c - (cols - 1) / 2) * (w / cols), wy = 5.4 + f * 3.1;
    dm.position.set(wx, wy, front + side * .02); dm.rotation.set(0, 0, 0); dm.updateMatrix(); frameI.setMatrixAt(n, dm.matrix);
    dm.position.set(wx, wy, front + side * .07); dm.updateMatrix(); glassI.setMatrixAt(n, dm.matrix);
    dm.position.set(wx, wy - .92, front + side * .12); dm.updateMatrix(); sillI.setMatrixAt(n, dm.matrix); n++;
  }
  [glassI, frameI, sillI].forEach(m => { m.castShadow = true; m.receiveShadow = true; g.add(m); });
  // ground floor storefront
  const sf = box(w - .4, 3.4, .25, MAT.frame); sf.position.set(0, 1.7, front + side * .05); g.add(sf);
  const sfGlass = box(w - 1.2, 2.6, .1, MAT.glass); sfGlass.position.set(0, 1.55, front + side * .18); g.add(sfGlass);
  return g;
}

// ---------- named shops: CORNER MART and CAFÉ π ----------
function shop(x, z, w, name, colA, colB, seed, cafe) {
  const g = building(x, z, w, 10, cafe ? 9.5 : 12.5, -1, cafe ? 5 : 0, seed);
  const front = -5;
  // striped awning
  const awTex = canvasTex(512, 128, (ctx, W, H) => { for (let i = 0; i < 16; i++) { ctx.fillStyle = i % 2 ? colA : '#ffffff'; ctx.fillRect(i * W / 16, 0, W / 16, H); } }).tex;
  const aw = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, w - .6, 32, 1, true, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ map: awTex, side: THREE.DoubleSide, roughness: .7 }));
  aw.rotation.z = Math.PI / 2; aw.rotation.y = Math.PI; aw.position.set(0, 3.55, front - .2); aw.castShadow = true; g.add(aw);
  // sign board
  const sign = new THREE.Mesh(new RoundedBoxGeometry(w * .7, 1.1, .2, 3, .08), [MAT.frame, MAT.frame, MAT.frame, MAT.frame, new THREE.MeshStandardMaterial({ map: signTex(name, colB, '#ffffff'), emissive: 0xffffff, emissiveMap: signTex(name, colB, '#ffffff'), emissiveIntensity: .35 }), MAT.frame]);
  sign.position.set(0, 4.6, front - .15); sign.rotation.y = Math.PI; sign.castShadow = true; g.add(sign);
  // door
  const door = box(1.4, 2.5, .12, MAT.glass); door.position.set(cafe ? -w * .25 : w * .25, 1.25, front - .22); g.add(door);
  const handle = box(.06, .5, .08, M.chrome); handle.position.set(door.position.x + .5, 1.2, front - .3); g.add(handle);
  if (cafe) { // outdoor tables + umbrella
    for (const tx of [-1.5, 1.8]) { const t = new THREE.Group(); const top = new THREE.Mesh(new THREE.CylinderGeometry(.45, .45, .05, 32), MAT.wood); top.position.y = .75; const leg = new THREE.Mesh(new THREE.CylinderGeometry(.04, .04, .75, 12), MAT.metal); leg.position.y = .37; t.add(top, leg);
      for (const s of [-1, 1]) { const ch = box(.4, .05, .4, MAT.wood); ch.position.set(s * .7, .45, 0); const back = box(.05, .45, .4, MAT.wood); back.position.set(s * .9, .68, 0); t.add(ch, back); }
      t.position.set(tx, 0, front - 1.3); t.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); g.add(t); }
  } else { // produce crates
    for (let i = 0; i < 3; i++) { const cr = box(.7, .45, .5, MAT.wood); cr.position.set(-w * .3 + i * .8, .23, front - .6); g.add(cr);
      const fruit = new THREE.Mesh(new THREE.SphereGeometry(.28, 16, 8, 0, 6.3, 0, 1.6), new THREE.MeshStandardMaterial({ color: [0xff6b2d, 0x9be15d, 0xffd23d][i], roughness: .5 })); fruit.scale.set(1.1, .5, .8); fruit.position.set(cr.position.x, .45, front - .6); g.add(fruit); } }
  return g;
}

// ---------- props ----------
function tree(x, z, s = 1, seed = 1) {
  const g = new THREE.Group(); const r = rand(seed);
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(.12 * s, .2 * s, 3 * s, 16), MAT.bark); trunk.position.y = 1.5 * s; trunk.castShadow = true; g.add(trunk);
  for (let i = 0; i < 9; i++) { const b = new THREE.Mesh(new THREE.SphereGeometry((.9 + r() * .6) * s, 28, 20), MAT.leaf[i % 3]); b.position.set((r() - .5) * 1.6 * s, (3.2 + r() * 1.6) * s, (r() - .5) * 1.6 * s); b.castShadow = true; b.receiveShadow = true;
    const p = b.geometry.attributes.position, ph = r() * 9; for (let k = 0; k < p.count; k++) { const x = p.getX(k), y = p.getY(k), z = p.getZ(k); const f = 1 + .12 * Math.sin(x * 4 + ph) * Math.sin(y * 5 + ph) * Math.sin(z * 4.5); p.setXYZ(k, x * f, y * f, z * f); } b.geometry.computeVertexNormals(); g.add(b); }
  const pit = box(1.3, .06, 1.3, new THREE.MeshStandardMaterial({ color: 0x4a3a2a, roughness: 1 })); pit.position.y = .17; g.add(pit);
  g.position.set(x, 0, z); return g;
}
function lamp(x, z, side) {
  const g = new THREE.Group(); const pole = new THREE.Mesh(new THREE.CylinderGeometry(.07, .1, 5.2, 16), MAT.metal); pole.position.y = 2.6; const arm = new THREE.Mesh(new THREE.CylinderGeometry(.04, .04, 1.2, 8), MAT.metal); arm.rotation.x = Math.PI / 2; arm.position.set(0, 5.1, side * .55);
  const head = box(.35, .14, .6, MAT.metal, .05); head.position.set(0, 5.05, side * 1.1); const bulb = new THREE.Mesh(new THREE.BoxGeometry(.25, .03, .45), new THREE.MeshStandardMaterial({ color: 0xfff6d8, emissive: 0xfff0c0, emissiveIntensity: .8 })); bulb.position.set(0, 4.97, side * 1.1);
  g.add(pole, arm, head, bulb); g.traverse(o => { if (o.isMesh) o.castShadow = true; }); g.position.set(x, 0, z); return g;
}
export function makeCar(color = 0x3a7bff) {
  const g = new THREE.Group();
  const paint = new THREE.MeshPhysicalMaterial({ color, metalness: .6, roughness: .25, clearcoat: 1, clearcoatRoughness: .05 });
  const body = box(4.2, .75, 1.85, paint, .3); body.position.y = .62; const cab = box(2.3, .7, 1.7, MAT.glass, .28); cab.position.set(-.25, 1.25, 0);
  const roof = box(2.0, .08, 1.6, paint, .04); roof.position.set(-.25, 1.62, 0);
  g.add(body, cab, roof);
  const tyre = new THREE.MeshStandardMaterial({ color: 0x15161a, roughness: .8 });
  for (const wx of [-1.35, 1.35]) for (const wz of [-.85, .85]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(.36, .36, .26, 32), tyre); w.rotation.x = Math.PI / 2; w.position.set(wx, .36, wz); const hub = new THREE.Mesh(new THREE.CylinderGeometry(.22, .22, .28, 10), M.chrome); hub.rotation.x = Math.PI / 2; hub.position.copy(w.position); g.add(w, hub); }
  for (const s of [-1, 1]) { const hl = box(.08, .16, .4, new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfff6e0, emissiveIntensity: .6 })); hl.position.set(2.1, .72, s * .6); const tl = box(.08, .14, .4, new THREE.MeshStandardMaterial({ color: 0xff2030, emissive: 0xff1020, emissiveIntensity: .5 })); tl.position.set(-2.1, .75, s * .6); g.add(hl, tl); }
  g.traverse(o => { if (o.isMesh) o.castShadow = true; }); return g;
}
function bench(x, z, rotY) { const g = new THREE.Group(); for (let i = 0; i < 3; i++) { const s = box(1.8, .06, .14, MAT.wood); s.position.set(0, .48, -.18 + i * .18); g.add(s); } for (let i = 0; i < 2; i++) { const s = box(1.8, .14, .05, MAT.wood); s.position.set(0, .7 + i * .2, -.3); g.add(s); } for (const lx of [-.8, .8]) { const l = box(.06, .5, .5, MAT.metal); l.position.set(lx, .25, -.05); g.add(l); } g.position.set(x, 0, z); g.rotation.y = rotY; return g; }

// ---------- assemble the street ----------
export function buildStreet(scene) {
  const S = new THREE.Group(); scene.add(S);
  const L = 220;
  const road = new THREE.Mesh(new THREE.PlaneGeometry(L, 9), MAT.asphalt); road.rotation.x = -Math.PI / 2; road.receiveShadow = true; S.add(road);
  MAT.asphalt.map.repeat.set(L / 6, 2); MAT.asphalt.normalMap.repeat.set(L / 6, 2);
  for (const s of [-1, 1]) { // sidewalks + curbs
    const sw = new THREE.Mesh(new THREE.BoxGeometry(L, .18, 3.4), MAT.concrete); sw.position.set(0, .09, s * 6.2); sw.receiveShadow = true; S.add(sw);
    const curb = new THREE.Mesh(new THREE.BoxGeometry(L, .2, .25), MAT.curb); curb.position.set(0, .1, s * 4.5); curb.receiveShadow = true; S.add(curb);
  }
  MAT.concrete.map.repeat.set(L / 1.7, 2); MAT.concrete.normalMap.repeat.set(L / 1.7, 2);
  // lane markings
  const dash = new THREE.InstancedMesh(new THREE.PlaneGeometry(2.4, .15), MAT.yellow, 60); const dm = new THREE.Object3D();
  for (let i = 0; i < 60; i++) { dm.position.set(-L / 2 + i * 4, .012, 0); dm.rotation.set(-Math.PI / 2, 0, 0); dm.updateMatrix(); dash.setMatrixAt(i, dm.matrix); } S.add(dash);
  // crosswalk at x = 34
  for (let i = 0; i < 8; i++) { const st = new THREE.Mesh(new THREE.PlaneGeometry(3, .55), MAT.paint); st.rotation.x = -Math.PI / 2; st.position.set(34, .013, -3.6 + i * 1.03); st.receiveShadow = true; S.add(st); }
  // north side (Jeremy's side): shops + buildings; south side: buildings
  const north = [[-36, 8, 3], [-26, 10, 1], [-15, 11, 4], [-3, 12, 2], [9, 10, 'mart'], [21, 12, 'cafe'], [44, 11, 6], [56, 12, 1], [68, 10, 3], [80, 12, 2]];
  north.forEach(([x, w, st], i) => { const b = st === 'mart' ? shop(x, 12.9, w, 'CORNER MART', '#e8364e', '#e8364e', 40 + i, false) : st === 'cafe' ? shop(x, 12.9, w, 'CAFÉ π', '#2fb57d', '#1d6b52', 50 + i, true) : building(x, 12.9, w, 10, 10 + (i * 7) % 14, -1, st, 30 + i); S.add(b); });
  const south = [[-34, 12, 5], [-21, 13, 0], [-7, 12, 6], [6, 13, 3], [19, 12, 1], [44, 13, 7], [57, 12, 2], [70, 13, 4], [83, 12, 0]];
  south.forEach(([x, w, st], i) => { S.add(building(x, -12.9, w, 10, 11 + (i * 5) % 16, 1, st, 60 + i)); });
  // trees, lamps, benches
  for (let i = 0; i < 12; i++) { S.add(tree(-38 + i * 11, 7.2, 1, 70 + i)); S.add(tree(-33 + i * 11, -7.2, 1, 90 + i)); }
  for (let i = 0; i < 14; i++) { S.add(lamp(-42 + i * 9, 4.8, -1)); S.add(lamp(-37 + i * 9, -4.8, 1)); }
  S.add(bench(15, 7.4, Math.PI)); S.add(bench(-8, 7.4, Math.PI));
  // parked cars
  const carCols = [0x3a7bff, 0xe8364e, 0xf2f2f2, 0x2a2d35, 0xffc93a, 0x29b48a];
  for (let i = 0; i < 6; i++) { const c = makeCar(carCols[i]); c.position.set(-30 + i * 14, 0, i % 2 ? -3.2 : 3.2); c.rotation.y = i % 2 ? Math.PI : 0; S.add(c); }
  // distant skyline for depth
  const far = new THREE.MeshStandardMaterial({ color: 0x9fb2c8, roughness: 1 }); const r = rand(99);
  for (let i = 0; i < 40; i++) { const h = 20 + r() * 50, w = 8 + r() * 12; const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, w), far); b.position.set(-100 + r() * 260, h / 2, (r() > .5 ? 1 : -1) * (40 + r() * 60)); S.add(b); }
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(2000, 2000), new THREE.MeshStandardMaterial({ color: 0x8a8f86, roughness: 1 })); ground.rotation.x = -Math.PI / 2; ground.position.y = -.02; ground.receiveShadow = true; S.add(ground);
  S.updateMatrixWorld(true);
  return { group: S, martDoor: new THREE.Vector3(11.5, 0, 7.6), cafeDoor: new THREE.Vector3(18, 0, 7.6), walkZ: 5.6 };
}

// ---------- first-person hands holding a coffee cup (POV) ----------
export function makePOVHands(skinColor = 0xf2b48c) {
  const g = new THREE.Group();
  const skin = new THREE.MeshPhysicalMaterial({ color: skinColor, roughness: .5, sheen: .3 });
  const sleeve = new THREE.MeshStandardMaterial({ color: 0x3f7cff, roughness: .7 });
  const cup = new THREE.Group(); const c = new THREE.Mesh(new THREE.CylinderGeometry(.045, .035, .13, 32), M.white); const sl = new THREE.Mesh(new THREE.CylinderGeometry(.047, .04, .05, 32), new THREE.MeshStandardMaterial({ color: 0x1d6b52, roughness: .8 })); sl.position.y = -.005;
  const lid = new THREE.Mesh(new THREE.CylinderGeometry(.049, .049, .015, 32), new THREE.MeshStandardMaterial({ color: 0x222, roughness: .4 })); lid.position.y = .072; cup.add(c, sl, lid);
  const hand = new THREE.Mesh(new THREE.SphereGeometry(.05, 24, 16), skin); hand.scale.set(1.1, .8, 1.3); hand.position.set(.03, -.01, .015);
  const fingers = new THREE.Mesh(new THREE.CapsuleGeometry(.018, .05, 6, 12), skin); fingers.rotation.z = Math.PI / 2; fingers.position.set(-.02, .0, .04);
  const arm = new THREE.Mesh(new THREE.CapsuleGeometry(.045, .3, 8, 16), sleeve); arm.rotation.x = Math.PI / 2.4; arm.position.set(.06, -.08, .19);
  const right = new THREE.Group(); right.add(cup, hand, fingers, arm); right.position.set(.085, -.15, -.46); right.rotation.set(.2, -.3, .05); right.scale.setScalar(.85);
  g.add(right); g.right = right; g.cup = cup; return g;
}
