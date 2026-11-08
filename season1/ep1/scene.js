// Episode 1 — What if ZERO disappeared from math?
import {
  THREE, RoundedBoxGeometry, scene, camera, draw, key, flash, bloom, M, canvasTex, rr, loadFont, text3d, shards,
  makeJeremy, renderCaptions, ui, clamp, prog, eOut, eIn, eInOut, eBack, lerp, rand, popS
} from './engine.js';

await document.fonts.load('80px IDB'); await document.fonts.load('80px IDBo'); await document.fonts.load('40px IM');
await loadFont();

const TOTAL = 59;
const EP_TITLE = 'WHAT IF 0 DISAPPEARED?', EP_NUM = 'EP. 1';
{ const sp = document.querySelectorAll('#bar span'); sp[0].textContent = EP_TITLE; sp[1].textContent = EP_NUM; }
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const look = new THREE.Vector3();
function setCam(p, l, roll = 0) { camera.position.copy(p); look.copy(l); camera.lookAt(look); camera.rotateZ(roll); }
function vlerp(a, b, k) { return a.clone().lerp(b, k); }
function grp(...kids) { const g = new THREE.Group(); kids.forEach(k => g.add(k)); scene.add(g); g.visible = false; return g; }
function rbox(w, h, d, r, mat) { const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 5, r), mat); m.castShadow = true; m.receiveShadow = true; return m; }
function labelPlane(w, h, cw, ch, fn, opts = {}) {
  const ct = canvasTex(cw, ch, fn);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: ct.tex, transparent: true, toneMapped: opts.toneMapped ?? true, depthWrite: opts.depthWrite ?? true }));
  m.ct = ct; return m;
}
const J = makeJeremy(); scene.add(J);
const wood = new THREE.MeshStandardMaterial({ color: 0x6b4426, roughness: 0.6 });
const sparkM = new THREE.MeshStandardMaterial({ color: 0xffd27a, emissive: 0xff8a20, emissiveIntensity: 3, roughness: .4 });

// ---------- background floating symbols ----------
const symM = new THREE.MeshStandardMaterial({ color: 0x1b2148, emissive: 0x3350ff, emissiveIntensity: 0.12, metalness: .5, roughness: .4 });
const bgSyms = new THREE.Group(); scene.add(bgSyms);
{ const r = rand(11); const syms = ['+', '-', 'x', '=', '%', '?', '7', '3', '9', '4', '+', '=', '8', '2'];
  syms.forEach((s, i) => { const m = text3d(s, 0.9 + r() * 0.8, symM); m.castShadow = false;
    m.position.set((r() - .5) * 26, 1 + r() * 11, -10 - r() * 10); m.userData = { sp: (r() - .5) * 0.6, ph: r() * 6 }; bgSyms.add(m); }); }

// =================== SCENES ===================
const S = [];
function def(start, dur, build) { const s = { start, dur, ...build() }; S.push(s); return s; }

// ---- 1. HOOK ----
def(0, 3.5, () => {
  const zero = new THREE.Group(); const segs = []; const N = 16; const arc = Math.PI * 2 / N;
  for (let i = 0; i < N; i++) {
    const m = new THREE.Mesh(new THREE.TorusGeometry(1, 0.34, 24, 10, arc * 1.0), M.gold); m.castShadow = true;
    const piv = new THREE.Group(); piv.rotation.z = i * arc; piv.add(m); zero.add(piv);
    const r = rand(100 + i);
    segs.push({ piv, m, a: (i + .5) * arc, rz: (r() - .5) * 6, rx: (r() - .5) * 6, vz: (r() - .2) * 3, sp: 2.2 + r() * 2.5 });
  }
  zero.scale.set(0.85, 1.2, 1);
  const holder = new THREE.Group(); holder.add(zero); holder.position.set(0, 3.1, 0);
  const sh = shards(70, M.gold, 0.09, 3);
  const g = grp(holder, sh);
  const cracks = new THREE.Mesh(new THREE.TorusGeometry(1, 0.36, 8, 64), new THREE.MeshBasicMaterial({ color: 0xffe2a0, wireframe: true, transparent: true, opacity: 0 }));
  zero.add(cracks);
  return {
    g, caps: [{ t0: .25, t1: 3.4, text: 'What if ZERO disappeared from math?', y: 1290, size: 92, g: ['ZERO'] }],
    update(t) {
      const spin = (1 - eOut(prog(t, 0, 1.6))) * Math.PI * 2.5;
      holder.rotation.y = spin; holder.position.y = 3.1 + Math.sin(t * 2) * 0.05;
      const crack = prog(t, 1.5, 2.0), boom = Math.max(0, t - 2.0);
      cracks.material.opacity = crack * (1 - prog(t, 2.0, 2.1)) * 0.9;
      flash.intensity = crack * 25 + (boom > 0 ? Math.max(0, 60 * (1 - boom / 0.5)) : 0);
      flash.position.set(0, 3.1, 1.5);
      const slow = boom * 0.55; // slow motion
      segs.forEach(s => {
        const j = crack * 0.03 * Math.sin(t * 90 + s.a * 10);
        const out = j + (boom > 0 ? s.sp * slow : 0);
        s.m.position.set(Math.cos(s.a) * out - Math.cos(s.a) * 0, Math.sin(s.a) * out, (boom > 0 ? s.vz * slow : 0));
        // rotate around piece itself
        s.m.rotation.set(s.rx * slow, 0, s.rz * slow * 0.3);
        s.piv.position.y = boom > 0 ? -3.2 * slow * slow : 0;
      });
      sh.burst(V(0, 3.1, 0.2), boom * 0.6, 0.9, 3, 1.6);
      const k = eInOut(prog(t, 0, 3.5));
      setCam(vlerp(V(0, 3.4, 14), V(0, 3.15, 9.2), k), V(0, 3.0, 0), Math.sin(t * .8) * 0.02 + (boom > 0 && boom < .3 ? Math.sin(t * 80) * 0.01 : 0));
    }
  };
});

// ---- 2. JEREMY ----
const phoneScreen = (bal, label = 'Available balance', col = '#4ff0a0') => (ctx, w, h) => {
  const g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#16204a'); g.addColorStop(1, '#0a0f24'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = '#fff'; ctx.font = '600 34px IDBo'; ctx.fillText('9:41', 40, 60);
  ctx.fillStyle = '#9aa6d8'; ctx.font = '40px IDBo'; ctx.fillText('Jeremy’s Bank', 40, 170);
  ctx.fillStyle = '#c9d1f5'; ctx.font = '34px IM'; ctx.fillText(label, 40, 300);
  ctx.fillStyle = col; ctx.font = '150px IDB'; ctx.fillText(bal, 32, 450);
  for (let i = 0; i < 4; i++) { rr(ctx, 40, 560 + i * 120, w - 80, 90, 22); ctx.fillStyle = 'rgba(255,255,255,.07)'; ctx.fill();
    ctx.fillStyle = '#c9d1f5'; ctx.font = '30px IM'; ctx.fillText(['Coffee', 'Groceries', 'Paycheck', 'Rent'][i], 70, 615 + i * 120);
    ctx.fillStyle = i == 2 ? '#4ff0a0' : '#ff8a9a'; ctx.textAlign = 'right'; ctx.fillText(['−$4', '−$62', '+$1,000', '−$700'][i], w - 70, 615 + i * 120); ctx.textAlign = 'left'; }
};
function makePhone(screenFn, w = 1.25, h = 2.5) {
  const body = rbox(w, h, 0.12, 0.16, new THREE.MeshPhysicalMaterial({ color: 0x1a1d2a, metalness: 0.8, roughness: 0.2, clearcoat: 1 }));
  const scr = labelPlane(w - 0.1, h - 0.1, 640, 1280, screenFn); scr.position.z = 0.062;
  const g = new THREE.Group(); g.add(body, scr); g.scr = scr; return g;
}
def(3.5, 3.5, () => {
  const phone = makePhone(phoneScreen('$1,050')); phone.position.set(1.35, 2.5, 0.6);
  const g = grp(phone);
  return {
    g, jer: true, caps: [{ t0: .15, t1: 1.6, text: 'Meet Jeremy.', size: 96, g: ['Jeremy'] }, { t0: 1.7, t1: 3.4, text: 'Totally average guy.', size: 90, g: ['average'] }],
    update(t) {
      const s = popS(t, 0, .5); J.scale.setScalar(s); J.position.set(-0.85, 0, 0); J.rotation.y = 0.25;
      J.pose({ expr: 'happy', armR: t < 2.2 ? 2.5 + Math.sin(t * 11) * 0.35 : 0.2, armL: 0.2, look: 0.5, bob: Math.abs(Math.sin(t * 3)) * 0.04, blink: t > 2.6 && t < 2.72 });
      const ps = popS(t, .7, .5); phone.scale.setScalar(ps); phone.rotation.set(0, -0.35 + Math.sin(t) * 0.05, 0.06); phone.position.y = 2.5 + Math.sin(t * 2) * 0.06;
      const a = lerp(-0.35, 0.15, eInOut(t / 3.5));
      setCam(V(Math.sin(a) * 7.6 + 0.2, 2.4, Math.cos(a) * 7.6), V(0.25, 1.75, 0));
    }
  };
});

// ---- 3. PLACE VALUE ----
def(7, 5, () => {
  const xs = [-2.05, -0.69, 0.69, 2.05];
  const digs = ['1', '0', '5', '0'].map((d, i) => { const m = text3d(d, 1.55, M.gold); m.position.set(xs[i], 3.45, 0); return m; });
  const sh1 = shards(40, M.gold, 0.1, 21), sh2 = shards(40, M.gold, 0.1, 22);
  const opts = ['15?', '105?', '150?', '1,050?'].map((o, i) => {
    const tile = rbox(1.7, 0.72, 0.14, 0.2, M.glass);
    const lab = labelPlane(1.7, 0.72, 340, 144, (ctx, w, h) => { ctx.fillStyle = '#7fe6ff'; ctx.font = '78px IDB'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(o, w / 2, h / 2 + 4); }, { toneMapped: false });
    lab.position.z = 0.08; const gg = new THREE.Group(); gg.add(tile, lab);
    gg.position.set(i % 2 ? 0.98 : -0.98, i < 2 ? 1.95 : 1.12, 0.9); return gg;
  });
  const g = grp(...digs, sh1, sh2, ...opts);
  return {
    g, caps: [{ t0: .2, t1: 2.1, text: 'No zero = no place value.', g: ['zero', 'place', 'value'] },
    { t0: 2.25, t1: 3.6, text: 'So which number is it?', y: 1440, c: ['which'] },
    { t0: 3.7, t1: 5, text: 'Babylonians really had this problem.', size: 70, y: 1440, g: ['Babylonians'] }],
    update(t) {
      digs.forEach((d, i) => { d.scale.setScalar(popS(t, i * 0.07, .45)); d.rotation.y = Math.sin(t * 1.5 + i) * 0.12; });
      const shake = prog(t, .8, 1.25);
      [1, 3].forEach(i => { const d = digs[i]; d.visible = t < 1.25; d.material = shake > 0 ? M.goldGlow : M.gold; d.position.x = xs[i] + Math.sin(t * 70 + i) * 0.05 * shake; d.position.y = 3.45 + Math.sin(t * 61) * 0.04 * shake; });
      sh1.burst(V(xs[1], 3.45, 0), t - 1.25, 0.5, 5); sh2.burst(V(xs[3], 3.45, 0), t - 1.25, 0.5, 5);
      const sl = eInOut(prog(t, 1.35, 2.0));
      digs[0].position.x = lerp(xs[0], -0.62, sl); digs[2].position.x = lerp(xs[2], 0.62, sl);
      opts.forEach((o, i) => { const s = popS(t, 2.3 + i * 0.2, .4); o.scale.setScalar(s); o.rotation.y = Math.sin(t * 2 + i) * 0.1; });
      const k = eInOut(t / 5);
      setCam(V(lerp(-0.8, 0.6, k), lerp(3.3, 2.9, k), lerp(10.5, 8.8, k)), V(0, 2.55, 0));
    }
  };
});

// ---- 4. ODOMETER ----
def(12, 3.5, () => {
  const housing = rbox(3.3, 2.0, 0.9, 0.22, new THREE.MeshPhysicalMaterial({ color: 0x252a3c, metalness: 0.9, roughness: 0.25, clearcoat: 1 }));
  const win = rbox(2.7, 1.45, 0.1, 0.08, new THREE.MeshStandardMaterial({ color: 0x05060c, roughness: 0.2 })); win.position.z = 0.43;
  const divider = rbox(0.06, 1.3, 0.12, 0.02, M.chrome); divider.position.z = 0.46;
  const white = new THREE.MeshStandardMaterial({ color: 0xf5f5ff, roughness: .3, emissive: 0xffffff, emissiveIntensity: .15 });
  const digits = ['7', '8', '9'].map(d => { const m = text3d(d, 0.95, white, 0.12); m.position.set(0.66, 0, 0.5); return m; });
  const q = text3d('?', 0.95, M.red, 0.12); q.position.set(-0.66, 0, 0.5);
  const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.13, 20, 14), M.red.clone()); lamp.position.set(1.35, 0.78, 0.5);
  const sp = shards(40, sparkM, 0.05, 41);
  const box = new THREE.Group(); box.add(housing, win, divider, ...digits, q, lamp); box.position.set(0, 2.6, 0);
  const g = grp(box, sp);
  return {
    g, caps: [{ t0: .15, t1: 1.9, text: '7… 8… 9…', size: 110 }, { t0: 2.0, t1: 3.5, text: '10 can’t be written.', size: 86, r: ['10'] },
    { t0: 2.35, t1: 3.5, text: 'Neither can 100 or 1,000.', y: 1410, size: 62, g: ['100', '1000'] }],
    update(t) {
      box.scale.setScalar(popS(t, 0, .4));
      const ticks = [0.0, 0.6, 1.2];
      digits.forEach((d, i) => {
        const tin = prog(t, ticks[i], ticks[i] + 0.22), tout = i < 2 ? prog(t, ticks[i + 1], ticks[i + 1] + 0.22) : 0;
        d.visible = tin > 0 && tout < 1;
        d.position.y = (1 - eOut(tin)) * -0.6 + eIn(tout) * 0.6; d.scale.set(1, Math.max(0.01, eOut(tin) * (1 - tout)), 1);
      });
      const jam = prog(t, 1.8, 2.0);
      if (t > 1.8) { digits[2].position.y = Math.sin(t * 60) * 0.12 * (1 - prog(t, 2.6, 3.2)); }
      q.visible = t > 2.0 && Math.floor(t * 12) % 3 !== 0; q.position.x = -0.66 + (Math.random() - .5) * 0.04;
      lamp.material.emissiveIntensity = t > 1.9 ? (Math.floor(t * 8) % 2 ? 3 : 0.3) : 0.3;
      sp.burst(V(0.66, 2.6, 0.6), t - 2.0, 0.4, 4, 1.2);
      box.rotation.z = jam * Math.sin(t * 50) * 0.01;
      const k = eInOut(t / 3.5);
      setCam(V(lerp(-1.8, 0.5, k), lerp(3.3, 2.8, k), lerp(9.2, 7.0, k)), V(0, 2.4, 0));
    }
  };
});

// ---- 5. CHALKBOARD ----
const noise = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); const r = rand(9);
  for (let i = 0; i < 2600; i++) { x.fillStyle = `rgba(0,0,0,${r() * .5})`; x.fillRect(r() * 256, r() * 256, 1 + r() * 2, 1 + r() * 2); } return c; })();
def(15.5, 4, () => {
  const frame = rbox(5.4, 3.4, 0.22, 0.06, wood); frame.position.set(0, 2.75, -0.3);
  const board = labelPlane(5.0, 3.0, 1500, 900, (ctx, w, h, k) => {
    const g = ctx.createRadialGradient(w / 2, h / 2, 50, w / 2, h / 2, w * .7); g.addColorStop(0, '#24453a'); g.addColorStop(1, '#13271f'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.globalAlpha = .07; ctx.fillStyle = '#fff'; for (let i = 0; i < 9; i++) { ctx.beginPath(); ctx.ellipse(200 + i * 160, 300 + (i % 3) * 200, 220, 60, .2, 0, 7); ctx.fill(); } ctx.globalAlpha = 1;
    const line = (txt, x, y, size, col, a0, a1, font = 'IDBo') => {
      const p = clamp((k - a0) / (a1 - a0)); if (p <= 0) return; const n = Math.ceil(txt.length * p);
      ctx.save(); ctx.translate(x, y); ctx.rotate(-0.012); ctx.font = `${size}px ${font}`; ctx.fillStyle = col; ctx.fillText(txt.slice(0, n), 0, 0); ctx.restore();
    };
    line('How do you write 2,026?', 90, 150, 82, 'rgba(245,245,235,.95)', 0.0, 0.5);
    if (k > 0.55) { ctx.font = '82px IDBo'; const zx = 90 + ctx.measureText('How do you write 2,').width + ctx.measureText('0').width / 2; ctx.strokeStyle = 'rgba(255,90,100,.95)'; ctx.lineWidth = 9; ctx.beginPath(); ctx.ellipse(zx, 122, 38, 50, 0, 0, 7 * clamp((k - .55) / .2)); ctx.stroke(); }
    line('→ two thousand twenty-six', 90, 330, 92, 'rgba(255,230,140,.95)', 0.7, 1.7);
    line('→ MMXXVI', 90, 500, 104, 'rgba(255,230,140,.95)', 1.8, 2.3, 'serif');
    line('MMXXVI ÷ VII = ???', 90, 720, 96, 'rgba(245,245,235,.95)', 2.5, 3.0, 'serif');
    if (k > 3.0) { ctx.strokeStyle = 'rgba(255,90,100,.9)'; ctx.lineWidth = 6; ctx.beginPath(); const r = rand(4); let x = 1060, y = 690; ctx.moveTo(x, y);
      const n = Math.floor(clamp((k - 3.0) / 0.6) * 40); for (let i = 0; i < n; i++) { x = 1050 + r() * 380; y = 600 + r() * 220; ctx.lineTo(x, y); } ctx.stroke(); }
    ctx.globalCompositeOperation = 'destination-out'; ctx.globalAlpha = .5; ctx.fillStyle = ctx.createPattern(noise, 'repeat'); ctx.fillRect(0, 0, w, h);
    ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
  });
  board.position.set(0, 2.75, -0.18); board.material.transparent = false;
  const g = grp(frame, board);
  return {
    g, jer: true, caps: [{ t0: .1, t1: 2.3, text: 'Writing 2,026 without zero?', g: ['2026'] }, { t0: 2.5, t1: 4, text: 'Long division? Good luck.', r: ['luck'] }],
    update(t) {
      board.ct.draw(Math.round(t * 30) / 30);
      J.scale.setScalar(0.72); J.position.set(1.55, 0, 2.2); J.rotation.y = -0.5;
      J.pose({ expr: t < 2.5 ? 'confused' : 'worried', look: -0.8, tilt: 0.12, armL: 0.25, armR: t < 2.5 ? 2.2 : 0.3, sweatK: t > 2.8 ? (t - 2.8) * 0.8 : 0 });
      const k = eInOut(t / 4);
      setCam(V(lerp(-0.6, 0.5, k), 2.6, lerp(11.6, 10.6, k)), V(lerp(-0.1, 0.15, k), 2.2, 0));
    }
  };
});

// ---- 6. 5 - 5 = ? ----
def(19.5, 3.5, () => {
  const xs = [-1.95, -0.98, 0, 0.95];
  const row1 = ['5', '-', '5', '='].map((c, i) => { const m = text3d(c, 0.95, M.gold); m.position.set(xs[i], 3.5, 0); return m; });
  const slot = rbox(0.95, 1.25, 0.32, 0.12, M.glass); slot.position.set(1.98, 3.5, 0);
  const slotEdge = new THREE.Mesh(new THREE.BoxGeometry(0.97, 1.27, 0.34), new THREE.MeshBasicMaterial({ color: 0x5ee0ff, wireframe: true, transparent: true, opacity: .35 })); slotEdge.position.copy(slot.position);
  const q = text3d('?', 0.85, M.red); q.position.set(1.98, 3.5, 0);
  const r2 = ['x', '+', '0', '=', 'x'].map((c, i) => { const m = text3d(c, 0.72, c === '0' ? M.gold : M.chrome); m.position.set(-1.7 + i * 0.85, 1.85, 0.4); return m; });
  const sh = shards(40, M.gold, 0.08, 61);
  const g = grp(...row1, slot, slotEdge, q, ...r2, sh);
  return {
    g, caps: [{ t0: .15, t1: 1.9, text: 'There’s no number for nothing.', r: ['nothing'] }, { t0: 2.0, t1: 3.5, text: 'x + 0 = x? Gone.', size: 90, r: ['Gone'] }],
    update(t) {
      row1.forEach((m, i) => { m.scale.setScalar(popS(t, i * .08, .4)); m.rotation.y = Math.sin(t * 1.4 + i) * .12; });
      const ss = popS(t, .35, .4); slot.scale.setScalar(ss); slotEdge.scale.setScalar(ss);
      q.visible = t > .8 && (Math.floor(t * 14) % 4 !== 0); q.position.x = 1.98 + (Math.random() - .5) * .08; q.rotation.y = Math.sin(t * 9) * .4;
      slotEdge.material.opacity = .25 + (t > .8 ? Math.abs(Math.sin(t * 20)) * .5 : 0);
      r2.forEach((m, i) => { m.scale.setScalar(popS(t, 1.2 + i * .07, .35)); });
      r2[2].visible = t < 2.2; if (t > 1.9 && t < 2.2) r2[2].position.x = -1.7 + 2 * .85 + Math.sin(t * 80) * .05;
      sh.burst(V(-1.7 + 2 * .85, 1.85, .4), t - 2.2, .4, 5);
      const a = lerp(-0.22, 0.22, eInOut(t / 3.5));
      setCam(V(Math.sin(a) * 11.2, 2.9, Math.cos(a) * 11.2), V(0, 2.6, 0));
    }
  };
});

// ---- 7. DECIMALS & PERCENT ----
def(23, 4, () => {
  const A = ['0', '.', '5'].map((c, i) => { const m = text3d(c, 0.95, M.gold); m.position.set(-0.75 + i * 0.6, 4.3, 0); return m; });
  A[1].position.x = -0.3; A[2].position.x = 0.25;
  const half = text3d('HALF', 0.85, M.chrome); half.position.set(0, 4.3, 0);
  const B = ['1', '0', '0', '%'].map((c, i) => { const m = text3d(c, 0.95, M.gold); m.position.set(-1.35 + i * 0.85, 2.85, 0); return m; });
  const tagMat = new THREE.MeshStandardMaterial({ color: 0xf6f1e4, roughness: .55 });
  const tag = rbox(2.4, 1.05, 0.06, 0.12, tagMat);
  const tagLab = labelPlane(2.3, 0.95, 460, 190, (ctx, w, h, broken) => {
    ctx.fillStyle = '#1b1d2a'; ctx.font = '120px IDB'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(broken ? '$9. 5' : '$9.05', w / 2 + 20, h / 2 + 6);
    ctx.beginPath(); ctx.arc(46, h / 2, 16, 0, 7); ctx.fillStyle = '#c7c0b0'; ctx.fill();
    if (broken) { ctx.strokeStyle = '#ff3b55'; ctx.lineWidth = 14; ctx.beginPath(); ctx.moveTo(80, 30); ctx.lineTo(w - 30, h - 30); ctx.moveTo(w - 30, 30); ctx.lineTo(80, h - 30); ctx.stroke(); }
  });
  tagLab.position.z = 0.035; const tagG = new THREE.Group(); tagG.add(tag, tagLab); tagG.position.set(0, 1.35, 0);
  const shA = shards(30, M.gold, .07, 71), shB = shards(40, M.gold, .08, 72), shC = shards(25, M.red, .06, 73);
  const g = grp(...A, half, ...B, tagG, shA, shB, shC);
  return {
    g, caps: [{ t0: .1, t1: 1.3, text: '0.5 becomes just HALF.', g: ['HALF'] }, { t0: 1.4, t1: 2.65, text: '100% becomes 1%.', r: ['1%'] }, { t0: 2.75, t1: 4, text: '$9.05? Can’t be written.', r: ['written'] }],
    update(t) {
      A.forEach((m, i) => { m.scale.setScalar(popS(t, i * .05, .35)); m.visible = i === 2 ? t < 0.75 : t < 0.6; });
      shA.burst(V(-0.5, 4.3, 0), t - 0.6, .4, 5);
      half.visible = t > 0.7; half.scale.setScalar(popS(t, .7, .4));
      B.forEach((m, i) => { m.scale.setScalar(popS(t, .9 + i * .05, .35)); });
      [1, 2].forEach(i => B[i].visible = t < 1.75);
      shB.burst(V(-0.1, 2.85, 0), t - 1.75, .7, 5);
      const sl = eInOut(prog(t, 1.85, 2.3));
      B[0].position.x = lerp(-1.35, -0.45, sl); B[3].position.x = lerp(-1.35 + 3 * .85, 0.45, sl);
      if (t > 2.3) B[0].material = B[3].material = M.red; else B[0].material = B[3].material = M.gold;
      tagG.scale.setScalar(popS(t, 2.2, .4)); tagG.rotation.z = Math.sin(t * 2.5) * .06 + (t > 3.0 ? Math.sin(t * 50) * .03 * (1 - prog(t, 3.0, 3.4)) : 0);
      tagLab.ct.draw(t > 3.0);
      shC.burst(V(0.2, 1.35, .2), t - 3.0, .5, 4);
      const k = eInOut(t / 4);
      setCam(V(lerp(0.9, -0.7, k), lerp(3.6, 2.6, k), 10.2), V(0, lerp(3.4, 2.4, k), 0));
    }
  };
});

// ---- 8. NUMBER LINE & GRAPH ----
def(27, 5, () => {
  // number line
  const lineM = M.cyan;
  const halfL = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 4.4, 16), lineM); halfL.rotation.z = Math.PI / 2; halfL.position.x = -2.25; halfL.castShadow = true;
  const halfR = halfL.clone(); halfR.position.x = 2.25;
  const L = new THREE.Group(), R = new THREE.Group(); L.add(halfL); R.add(halfR);
  const white = new THREE.MeshStandardMaterial({ color: 0xeef2ff, roughness: .3, emissive: 0x8899ff, emissiveIntensity: .2 });
  for (let n = -3; n <= 3; n++) {
    if (n === 0) continue;
    const tick = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.4, 8), white); tick.position.x = n * 1.3;
    const lab = text3d(n < 0 ? '-' + (-n) : String(n), 0.38, white, 0.08); lab.position.set(n * 1.3, -0.55, 0);
    (n < 0 ? L : R).add(tick, lab);
  }
  const zTick = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.6, 12), M.goldGlow);
  const zLab = text3d('0', 0.55, M.goldGlow, 0.12); zLab.position.y = -0.65;
  const gap = text3d('?', 0.8, M.red); gap.position.y = 0.05;
  const nl = new THREE.Group(); nl.add(L, R, zTick, zLab, gap); nl.position.set(0, 2.7, 0);
  const shZ = shards(45, M.gold, .08, 81);
  // graph
  const gr = new THREE.Group(); gr.position.set(-1.3, 1.0, 0);
  const ax = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 4.8, 12), M.chrome); ax.rotation.z = Math.PI / 2; ax.position.x = 1.6;
  const ay = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 3.4, 12), M.chrome); ay.position.y = 1.2;
  const axG = new THREE.Group(), ayG = new THREE.Group(); axG.add(ax); ayG.add(ay);
  const orig = new THREE.Mesh(new THREE.SphereGeometry(0.13, 24, 16), M.goldGlow);
  const origLab = labelPlane(1.3, 0.45, 300, 104, (ctx, w, h) => { ctx.fillStyle = '#ffd36a'; ctx.font = '72px IDB'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('(0, 0)', w / 2, h / 2); }, { toneMapped: false });
  origLab.position.set(-0.75, -0.35, 0.1);
  const pts = []; for (let x = -0.35; x <= 5.35; x += 0.05) pts.push(V(x * 0.55, (x * x - 5 * x + 6) * 0.3, 0));
  const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 200, 0.045, 10), new THREE.MeshStandardMaterial({ color: 0x5ee0ff, emissive: 0x30c0ff, emissiveIntensity: 1.2 }));
  const roots = [2, 3].map(x => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.11, 20, 14), M.red); m.position.set(x * 0.55, 0, 0.05); return m; });
  const eq = labelPlane(3.6, 0.8, 900, 200, (ctx, w, h, broken) => {
    rr(ctx, 4, 4, w - 8, h - 8, 40); ctx.fillStyle = 'rgba(15,22,55,.85)'; ctx.fill(); ctx.strokeStyle = 'rgba(94,224,255,.6)'; ctx.lineWidth = 4; ctx.stroke();
    ctx.font = '96px IDB'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#fff'; ctx.fillText('x² − 5x + 6 = ', 60, h / 2 + 4);
    const x0 = 60 + ctx.measureText('x² − 5x + 6 = ').width; ctx.fillStyle = broken ? '#ff3b55' : '#ffc444'; ctx.fillText(broken ? '?' : '0', x0, h / 2 + 4);
  }, { toneMapped: false });
  eq.position.set(1.4, 3.35, 0.3);
  gr.add(axG, ayG, orig, origLab, tube, ...roots, eq);
  const shO = shards(35, M.gold, .07, 82);
  const g = grp(nl, shZ, gr, shO);
  return {
    g, caps: [{ t0: .1, t1: 2.2, text: 'The number line loses its center.', g: ['center'] },
    { t0: 2.35, t1: 3.6, text: 'Graphs lose (0, 0).', c: ['(0', '0)'] }, { t0: 3.7, t1: 5, text: 'Algebra breaks too.', r: ['breaks'] }],
    update(t) {
      const A = t < 2.3;
      nl.visible = A; gr.visible = !A;
      if (A) {
        nl.scale.setScalar(popS(t, 0, .45));
        zTick.visible = zLab.visible = t < 0.85;
        if (t > .6 && t < .85) zLab.position.x = Math.sin(t * 80) * .04;
        shZ.burst(V(0, 2.2, 0), t - 0.85, .5, 5);
        const sp = eOut(prog(t, .9, 1.6)); L.position.x = -sp * 0.9; R.position.x = sp * 0.9; L.rotation.z = sp * 0.04; R.rotation.z = -sp * 0.04;
        gap.visible = t > 1.2; gap.scale.setScalar(popS(t, 1.2, .4)); gap.rotation.y = Math.sin(t * 4) * .5;
        const k = eInOut(t / 2.3);
        setCam(V(lerp(-0.6, 0.4, k), 2.9, lerp(14.2, 13.0, k)), V(0, 2.4, 0));
      } else {
        const u = t - 2.3;
        gr.scale.setScalar(popS(u, 0, .45));
        tube.geometry.setDrawRange(0, Math.floor(tube.geometry.index.count * clamp(u / 0.8)));
        orig.visible = origLab.visible = u < 1.15;
        if (u > .85 && u < 1.15) orig.position.x = Math.sin(u * 90) * .04;
        shO.burst(V(-1.3, 1.0, 0), u - 1.15, .3, 4);
        const d = eOut(prog(u, 1.2, 2.2));
        axG.position.y = -d * 0.45; axG.rotation.z = d * 0.08; ayG.position.x = -d * 0.5; ayG.rotation.z = -d * 0.1;
        roots.forEach((r, i) => { r.visible = u > 1.3 && Math.floor(u * 10 + i) % 2 === 0; r.position.y = -d * 0.45; });
        eq.ct.draw(u > 1.6);
        eq.scale.setScalar(popS(u, .3, .4));
        const a = lerp(-0.25, 0.2, eInOut(u / 2.7));
        setCam(V(Math.sin(a) * 9.4 + 0.3, 2.6, Math.cos(a) * 9.4), V(0.3, 2.2, 0));
      }
    }
  };
});

// ---- 9. CLOCK ----
def(32, 2.5, () => {
  const stand = rbox(2.8, 1.0, 1.4, 0.06, wood); stand.position.set(0.9, 0.5, 0);
  const clockBody = rbox(2.3, 1.25, 0.9, 0.3, new THREE.MeshPhysicalMaterial({ color: 0xe8364e, roughness: .25, clearcoat: 1 }));
  const disp = labelPlane(1.9, 0.8, 600, 250, (ctx, w, h, mode) => {
    ctx.fillStyle = '#0c0306'; rr(ctx, 0, 0, w, h, 30); ctx.fill();
    ctx.font = 'bold 200px monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#ff3044'; ctx.shadowColor = '#ff2040'; ctx.shadowBlur = 25;
    ctx.fillText(['10:05', '1 : 5', '--:--', 'ERR'][mode], w / 2, h / 2 + 10);
  }, { toneMapped: false });
  disp.position.z = 0.46;
  const bells = [-1, 1].map(s => { const b = new THREE.Mesh(new THREE.SphereGeometry(0.33, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2), M.chrome); b.position.set(s * 0.7, 0.68, 0); b.rotation.z = s * -0.4; b.castShadow = true; return b; });
  const clk = new THREE.Group(); clk.add(clockBody, disp, ...bells); clk.position.set(0.9, 1.65, 0.1);
  const g = grp(stand, clk);
  return {
    g, jer: true, caps: [{ t0: .1, t1: 2.4, text: '10:05? Your alarm can’t show it.', size: 72, r: ['can’t'], g: ['10:05'] }],
    update(t) {
      const ring = t > .7;
      disp.ct.draw(t < .7 ? 0 : [1, 2, 3, 2][Math.floor(t * 9) % 4]);
      clk.rotation.z = ring ? Math.sin(t * 70) * 0.05 : 0; clk.position.y = 1.65 + (ring ? Math.abs(Math.sin(t * 35)) * .05 : 0);
      J.scale.setScalar(0.85); J.position.set(-1.35, 0, 0.6); J.rotation.y = 0.35;
      const woke = t > 1.2;
      J.pose({ expr: woke ? 'panic' : 'sleep', armL: woke ? 2.6 : 0.15, armR: woke ? 2.6 : 0.15, bob: woke ? Math.abs(Math.sin(t * 14)) * .1 : Math.sin(t * 2) * .02, tilt: woke ? 0 : 0.2, sweatK: woke ? (t - 1.2) : 0 });
      const k = eInOut(t / 2.5);
      setCam(V(lerp(0.4, -0.1, k), lerp(2.3, 2.1, k), lerp(10.6, 9.4, k)), V(-0.1, 1.55, 0));
    }
  };
});

// ---- 10. MONEY ----
def(34.5, 2.5, () => {
  const vals = ['10', '20', '50', '100'];
  const bills = vals.map((v, i) => {
    const pl = labelPlane(2.3, 1.0, 690, 300, (ctx, w, h, broken) => {
      const g = ctx.createLinearGradient(0, 0, w, h); g.addColorStop(0, '#cfe6c4'); g.addColorStop(1, '#9fc596'); ctx.fillStyle = g; rr(ctx, 0, 0, w, h, 18); ctx.fill();
      ctx.strokeStyle = '#4f7a4a'; ctx.lineWidth = 8; rr(ctx, 14, 14, w - 28, h - 28, 12); ctx.stroke();
      ctx.beginPath(); ctx.ellipse(w / 2, h / 2, 80, 100, 0, 0, 7); ctx.fillStyle = '#86ae7f'; ctx.fill();
      ctx.fillStyle = '#244a2a'; ctx.font = '120px IDB'; ctx.textBaseline = 'middle';
      const s = '$' + (broken ? v.replace(/0/g, '') : v);
      ctx.textAlign = 'left'; ctx.fillText(s, 40, h / 2 + 6); ctx.textAlign = 'right'; ctx.font = '64px IDB'; ctx.fillText(broken ? v.replace(/0/g, '') : v, w - 40, 70);
    });
    pl.material.side = THREE.DoubleSide; pl.material.transparent = false; pl.castShadow = true;
    const holder = new THREE.Group(); holder.add(pl);
    holder.position.set(1.0 + (i - 1.5) * 0.25, 2.9 - i * 0.12 + 0.2, i * 0.06); holder.rotation.z = (1.5 - i) * 0.22;
    return holder;
  });
  const zeros = []; const zm = new THREE.MeshStandardMaterial({ color: 0x2f6a3a, roughness: .4, metalness: .2 });
  bills.forEach((b, i) => { const n = vals[i].split('0').length - 1; for (let k = 0; k < n; k++) { const z = text3d('0', 0.4, zm, .08); z.userData = { i, k }; zeros.push(z); } });
  const g = grp(...bills, ...zeros);
  return {
    g, jer: true, caps: [{ t0: .1, t1: 1.0, text: '$10, $20, $50, $100…', g: ['$10', '$20', '$50', '$100…', '$100'] }, { t0: 1.1, t1: 2.5, text: '…become $1, $2, $5, $1.', r: ['$1', '$2', '$5'] }],
    update(t) {
      bills.forEach((b, i) => { b.scale.setScalar(popS(t, i * .06, .35)); b.children[0].ct.draw(t > 0.85); b.rotation.y = Math.sin(t * 2 + i) * .15; b.position.y = 3.1 - i * 0.12 + Math.sin(t * 2.5 + i) * .05; });
      zeros.forEach(z => { const { i, k } = z.userData; const b = bills[i]; const u = t - 0.85;
        z.visible = u > 0 && u < 1.3; z.position.set(b.position.x - 0.1 + k * 0.3, b.position.y + u * 2.4, b.position.z + 0.3 + u * 1.5); z.rotation.set(u * 5, u * 3 * (k ? 1 : -1), u * 2); });
      J.scale.setScalar(0.85); J.position.set(-1.45, 0, 0.8); J.rotation.y = 0.35;
      J.pose({ expr: t < .9 ? 'happy' : 'shocked', armL: t < .9 ? .2 : 2.4, armR: t < .9 ? .2 : 2.4, look: .6, bob: t > .9 ? Math.abs(Math.sin(t * 12)) * .06 : 0, sweatK: t > 1.4 ? t - 1.4 : 0 });
      const a = lerp(0.2, -0.15, eInOut(t / 2.5));
      setCam(V(Math.sin(a) * 10.4, 2.5, Math.cos(a) * 10.4), V(-0.1, 2.0, 0));
    }
  };
});

// ---- 11. PHONE ----
def(37, 2.5, () => {
  const body = rbox(2.3, 3.9, 0.18, 0.28, new THREE.MeshPhysicalMaterial({ color: 0x1a1d2a, metalness: .8, roughness: .2, clearcoat: 1 }));
  const scr = labelPlane(2.1, 1.1, 640, 335, (ctx, w, h, n, err) => {
    ctx.fillStyle = '#0d1430'; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#fff'; ctx.font = '96px IDBo'; ctx.textAlign = 'center'; ctx.fillText('555-21'.slice(0, n) + (err ? '?' : ''), w / 2, 150);
    if (err) { ctx.fillStyle = '#ff5468'; ctx.font = '44px IDBo'; ctx.fillText('Number can’t be dialed', w / 2, 260); }
  }, { toneMapped: false });
  scr.position.set(0, 1.25, 0.095);
  const keyMat = new THREE.MeshPhysicalMaterial({ color: 0x9da2b4, roughness: .25, clearcoat: 1 });
  const labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'];
  const keys = labels.map((l, i) => {
    const k = rbox(0.56, 0.4, 0.12, 0.08, keyMat);
    const lab = labelPlane(0.5, 0.36, 140, 100, (ctx, w, h) => { ctx.fillStyle = l === '0' ? '#d99a12' : '#1a1d2a'; ctx.font = '76px IDB'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(l, w / 2, h / 2 + 4); });
    lab.position.z = 0.065; const gg = new THREE.Group(); gg.add(k, lab);
    gg.home = V((i % 3 - 1) * 0.68, 0.2 - Math.floor(i / 3) * 0.5, 0.12); gg.position.copy(gg.home); return gg;
  });
  const ph = new THREE.Group(); ph.add(body, scr, ...keys); ph.position.set(0.75, 2.45, 0); ph.rotation.set(-0.12, -0.2, 0);
  const sh = shards(30, keyMat, .07, 111);
  const g = grp(ph, sh);
  return {
    g, jer: true, caps: [{ t0: .1, t1: 1.05, text: 'Any phone number with a 0?', g: ['0'] }, { t0: 1.25, t1: 2.5, text: 'Can’t dial it.', size: 96, r: ['dial'] }],
    update(t) {
      ph.scale.setScalar(popS(t, 0, .4));
      const n = Math.min(6, Math.floor(t / 0.16));
      scr.ct.draw(n, t > 1.1);
      // pressed keys dip
      const seq = ['5', '5', '5', '2', '1'];
      keys.forEach(k => k.position.copy(k.home));
      const idx = Math.floor(t / 0.16); if (idx < seq.length) { const kk = keys[labels.indexOf(seq[idx])]; kk.position.z = 0.06; }
      const z = keys[10]; const u = t - 0.95;
      if (u > 0) { z.position.set(z.home.x + u * 0.8, z.home.y + u * 2.2 - 4 * u * u, z.home.z + u * 1.8); z.rotation.set(u * 6, u * 4, u * 3); } else z.rotation.set(0, 0, 0);
      z.visible = u < 1.0;
      sh.burst(V(0.75, 0.9, 0.4), u - 0.05, .3, 4);
      J.scale.setScalar(0.8); J.position.set(-1.55, 0, 0.9); J.rotation.y = 0.4;
      J.pose({ expr: t < 1.0 ? 'worried' : 'shocked', look: 0.7, armL: .2, armR: t < 1.0 ? 1.3 : 2.5, sweatK: t > 1.2 ? t - 1.2 : 0 });
      const k = eInOut(t / 2.5);
      setCam(V(lerp(-0.4, 0.3, k), lerp(2.7, 2.5, k), lerp(10.8, 9.8, k)), V(-0.2, 2.15, 0));
    }
  };
});

// ---- 12. CALENDAR & THERMOMETER ----
def(39.5, 3, () => {
  const cal = labelPlane(2.6, 2.75, 780, 825, (ctx, w, h, k) => {
    ctx.fillStyle = '#fbfaf6'; ctx.fillRect(0, 0, w, h); ctx.fillStyle = '#e8364e'; ctx.fillRect(0, 0, w, 130);
    ctx.fillStyle = '#fff'; ctx.font = '72px IDB'; ctx.textAlign = 'center'; ctx.fillText('NOVEMBER', w / 2, 92);
    const cw = w / 7, ch = 112;
    for (let d = 1; d <= 30; d++) { const c = (d + 5) % 7, r = Math.floor((d + 5) / 7);
      const x = c * cw + cw / 2, y = 175 + r * ch + 50; const gone = d % 10 === 0;
      if (gone && k > 0) { ctx.globalAlpha = 1; rr(ctx, x - cw / 2 + 6, y - 56, cw - 12, ch - 12, 12); ctx.fillStyle = `rgba(255,59,85,${0.2 * k})`; ctx.fill(); ctx.fillStyle = '#ff3b55'; ctx.font = '60px IDB'; ctx.fillText(k > .5 ? '?' : String(d), x, y + 20); continue; }
      ctx.fillStyle = '#2a2d3d'; ctx.font = '52px IDBo'; ctx.fillText(String(d), x, y + 18); }
  });
  cal.material.transparent = false; cal.material.color.set(0xb8bac4); cal.castShadow = true;
  const binder = rbox(2.7, 0.22, 0.2, 0.08, M.dark); binder.position.y = 1.47;
  const calG = new THREE.Group(); calG.add(cal, binder); calG.position.set(-0.95, 2.6, 0); calG.rotation.y = 0.22;
  const glass = new THREE.Mesh(new THREE.CapsuleGeometry(0.22, 2.9, 8, 24), new THREE.MeshPhysicalMaterial({ color: 0xdff4ff, roughness: .05, transparent: true, opacity: .3, clearcoat: 1, depthWrite: false }));
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.3, 24, 16), M.red); bulb.position.y = -1.55;
  const liquid = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 1, 16), M.red);
  const scale = labelPlane(1.2, 3.2, 300, 800, (ctx, w, h, broken) => {
    ctx.strokeStyle = '#dfe6ff'; ctx.lineWidth = 6; ctx.fillStyle = '#dfe6ff';
    for (let i = 0; i < 9; i++) { const y = 80 + i * 80; ctx.beginPath(); ctx.moveTo(20, y); ctx.lineTo(i === 4 ? 110 : 70, y); ctx.stroke(); }
    ctx.font = '70px IDB'; ctx.fillStyle = broken ? '#ff5468' : '#ffc444'; ctx.fillText(broken ? '?°C' : '0°C', 120, 405);
  }, { toneMapped: false });
  scale.position.set(0.72, 0.3, 0);
  const th = new THREE.Group(); th.add(glass, bulb, liquid, scale); th.position.set(1.55, 2.5, 0.35);
  const g = grp(calG, th);
  return {
    g, caps: [{ t0: .1, t1: 1.5, text: 'The 10th, 20th and 30th? Gone.', size: 70, r: ['Gone'] }, { t0: 1.6, t1: 3, text: '0°C: is it freezing? Nobody knows.', size: 70, c: ['freezing'] }],
    update(t) {
      calG.scale.setScalar(popS(t, 0, .4)); th.scale.setScalar(popS(t, .2, .4));
      cal.ct.draw(Math.round(clamp((t - .5) / .6) * 10) / 10);
      const level = lerp(2.4, 1.85, eInOut(prog(t, .3, 1.6)));
      liquid.scale.y = level; liquid.position.y = -1.5 + level / 2;
      scale.ct.draw(t > 1.8 && Math.floor(t * 8) % 3 !== 0);
      const k = eInOut(t / 3);
      setCam(V(lerp(-0.6, 0.6, k), 2.6, lerp(11.0, 10.4, k)), V(lerp(-0.2, 0.3, k), 2.4, 0));
    }
  };
});

// ---- 13. SPORTS ----
def(42.5, 2.5, () => {
  const board = rbox(3.8, 1.9, 0.4, 0.12, M.dark);
  const led = labelPlane(3.5, 1.6, 1050, 480, (ctx, w, h, broken) => {
    ctx.fillStyle = '#050608'; ctx.fillRect(0, 0, w, h);
    ctx.textAlign = 'center'; ctx.fillStyle = '#ffb02e'; ctx.shadowColor = '#ff9a00'; ctx.shadowBlur = 20;
    ctx.font = '64px IDB'; ctx.fillText('HOME', 250, 110); ctx.fillText('AWAY', 800, 110);
    ctx.font = '240px IDB'; ctx.fillText('3', 250, 360); ctx.fillText('–', 525, 340);
    ctx.fillStyle = broken ? '#ff3b55' : '#ffb02e'; ctx.shadowColor = broken ? '#ff2040' : '#ff9a00'; ctx.fillText(broken ? '?' : '0', 800, 360);
    ctx.shadowBlur = 0; ctx.globalAlpha = .25; ctx.fillStyle = '#000'; for (let y = 0; y < h; y += 8) ctx.fillRect(0, y, w, 3);
  }, { toneMapped: false });
  led.position.z = 0.21;
  const posts = [-1, 1].map(s => { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 3.2, 12), M.chrome); p.position.set(s * 1.4, -2.2, -0.1); p.castShadow = true; return p; });
  const sb = new THREE.Group(); sb.add(board, led, ...posts); sb.position.set(0.3, 3.75, -0.6);
  const g = grp(sb);
  return {
    g, jer: true, caps: [{ t0: .15, t1: 2.5, text: 'Final score: 3 to… what?', r: ['what'] }],
    update(t) {
      sb.scale.setScalar(popS(t, 0, .4));
      led.ct.draw(t > .8 && Math.floor(t * 10) % 4 !== 0);
      J.scale.setScalar(0.8); J.position.set(-1.0, 0, 1.4); J.rotation.y = 0.3;
      J.pose({ expr: t < .9 ? 'happy' : 'confused', look: .6, tilt: t > .9 ? 0.18 : 0, armL: t < .9 ? 2.6 : .3, armR: t < .9 ? 2.6 : 1.4, bob: t < .9 ? Math.abs(Math.sin(t * 10)) * .1 : 0 });
      const k = eInOut(t / 2.5);
      setCam(V(lerp(-0.8, 0.3, k), lerp(1.5, 1.9, k), lerp(11.0, 10.0, k)), V(-0.1, 2.4, 0));
    }
  };
});

// ---- 14. TECH COLLAPSE ----
def(45, 4.5, () => {
  const mk = ch => new THREE.MeshBasicMaterial({ map: canvasTex(128, 128, (ctx, w, h) => { ctx.fillStyle = '#6dffb0'; ctx.font = 'bold 110px monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.shadowColor = '#3dff90'; ctx.shadowBlur = 16; ctx.fillText(ch, w / 2, h / 2); }).tex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false });
  const m0 = mk('0'), m1 = mk('1');
  const N = 320, geo = new THREE.PlaneGeometry(0.45, 0.45);
  const i0 = new THREE.InstancedMesh(geo, m0, N), i1 = new THREE.InstancedMesh(geo, m1, N); i0.frustumCulled = i1.frustumCulled = false;
  const r = rand(141); const P = [];
  for (let i = 0; i < N * 2; i++) P.push({ x: Math.round((r() - .5) * 26) * 0.5, y: r() * 14, z: -2 - r() * 18, sp: 1.5 + r() * 3 });
  const dm = new THREE.Object3D();
  const g = grp(i0, i1);
  return {
    g, caps: [{ t0: .1, t1: 1.5, text: 'Computers run on 1s and 0s.', c: ['1s', '0s'] }, { t0: 1.6, t1: 2.4, text: 'Delete the 0s…', size: 96, r: ['0s…', '0s'] },
    { t0: 3.4, t1: 4.5, text: 'Every phone, bank and GPS: OFFLINE.', size: 72, y: 1150, r: ['OFFLINE'] }],
    update(t) {
      for (let i = 0; i < N * 2; i++) { const p = P[i]; dm.position.set(p.x, ((p.y - t * p.sp) % 14 + 14) % 14 - 1, p.z); dm.rotation.set(0, 0, 0); dm.scale.setScalar(1); dm.updateMatrix(); (i < N ? i0 : i1).setMatrixAt(i % N, dm.matrix); }
      i0.instanceMatrix.needsUpdate = i1.instanceMatrix.needsUpdate = true;
      m0.opacity = 1 - prog(t, 1.6, 2.2); m1.opacity = 1;
      const gl = t > 2.2 && t < 3.2; const sh = gl ? (Math.random() - .5) * 0.25 : 0;
      setCam(V(sh, 3.2 + sh, lerp(9, 5, t / 4.5)), V(0, 3.4, -10), gl ? (Math.random() - .5) * .08 : 0);
      ui.scan.style.opacity = gl ? .8 : 0;
      document.querySelector('canvas').style.transform = gl ? `translateX(${(Math.random() - .5) * 40}px)` : '';
      document.querySelector('canvas').style.filter = gl ? `hue-rotate(${Math.random() * 180}deg) saturate(2)` : '';
      ui.black.style.opacity = t > 3.0 ? 1 : 0;
      ui.nosig.style.opacity = t > 3.0 && t < 3.4 ? (Math.floor(t * 20) % 2 ? 1 : .4) : 0;
    }
  };
});

// ---- 15. HISTORY ----
def(49.5, 5.5, () => {
  const colGeo = new THREE.CylinderGeometry(0.34, 0.38, 4.4, 64, 1);
  { const p = colGeo.attributes.position; for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i), a = Math.atan2(z, x), r = Math.hypot(x, z); if (r < 0.01) continue; const k = 1 - 0.04 * Math.max(0, Math.cos(a * 20)); p.setX(i, x * k); p.setZ(i, z * k); } colGeo.computeVertexNormals(); }
  const cols = [-2.9, -1.5, 1.5, 2.9].map(x => { const c = new THREE.Group(); const sh = new THREE.Mesh(colGeo, M.marble); sh.position.y = 2.2; sh.castShadow = sh.receiveShadow = true;
    const cap = rbox(1.0, 0.3, 1.0, 0.04, M.marble); cap.position.y = 4.55; const base = rbox(1.0, 0.25, 1.0, 0.04, M.marble); base.position.y = 0.12; c.add(sh, cap, base); c.position.set(x, 0, -1.6); return c; });
  const tablet = rbox(3.6, 1.15, 0.3, 0.06, M.marble); const mm = text3d('MMXXVI', 0.6, M.gold, 0.1); mm.position.z = 0.2; tablet.add(mm);
  const tabG = new THREE.Group(); tabG.add(tablet); tabG.position.set(0, 3.75, 0);
  const eq = text3d('= 2026', 0.62, M.goldGlow); eq.position.set(0, 2.75, 0.2);
  const card = (l1, l2) => { const gg = new THREE.Group(); const b = rbox(4.2, 0.78, 0.1, 0.18, M.glass);
    const lab = labelPlane(4.2, 0.78, 1100, 204, (ctx, w, h) => { ctx.textBaseline = 'middle'; ctx.fillStyle = '#ffc444'; ctx.font = '84px IDB'; ctx.fillText(l1, 50, h / 2 + 4); const x = 60 + ctx.measureText(l1).width + 30; ctx.fillStyle = '#fff'; ctx.font = '50px IDBo'; ctx.fillText(l2, x, h / 2 + 4); }, { toneMapped: false });
    lab.position.z = 0.06; gg.add(b, lab); return gg; };
  const c1 = card('628 AD', 'Brahmagupta: rules for zero'); c1.position.set(0, 1.8, 0.8);
  const c2 = card('1202', 'Fibonacci brings it to Europe'); c2.position.set(0, 0.92, 0.8);
  const g = grp(...cols, tabG, eq, c1, c2);
  return {
    g, caps: [{ t0: .1, t1: 1.4, text: 'Sound crazy? It actually happened.', y: 330, size: 66, g: ['happened'] },
    { t0: 1.5, t1: 3.9, text: 'The Romans had no zero.', y: 330, size: 74, r: ['no', 'zero'] },
    { t0: 4.0, t1: 5.5, text: 'Zero is one of history’s greatest inventions.', y: 300, size: 64, g: ['greatest', 'inventions'] }],
    update(t) {
      cols.forEach((c, i) => { c.position.y = -4.8 * (1 - eOut(prog(t, i * 0.1, 0.9 + i * 0.1))); });
      tabG.scale.setScalar(popS(t, 0.8, .45)); tabG.rotation.y = Math.sin(t) * .08;
      eq.visible = t > 1.4; eq.scale.setScalar(popS(t, 1.4, .4));
      c1.position.x = lerp(-7, 0, eOut(prog(t, 2.4, 2.9))); c2.position.x = lerp(7, 0, eOut(prog(t, 3.0, 3.5)));
      const k = eInOut(t / 5.5);
      setCam(V(lerp(1.5, -0.8, k), lerp(1.6, 2.6, k), lerp(11.5, 9.8, k)), V(0, 2.4, 0));
    }
  };
});

// ---- 16. CTA ----
def(55, 4, () => {
  const t1 = text3d('WHAT SHOULD', 0.4, M.chrome); t1.position.set(0, 4.75, 0);
  const t2 = text3d('DISAPPEAR NEXT?', 0.4, M.goldGlow); t2.position.set(0, 4.1, 0);
  const cm = [['@mia', 'what if gravity disappeared', '#ff7a8c'], ['@dev.k', 'what if pi was exactly 3', '#5ee0ff'], ['@sam', 'what if the moon vanished', '#ffc444']].map(([u, c, col], i) => {
    const gg = new THREE.Group(); const b = rbox(3.6, 0.78, 0.12, 0.3, new THREE.MeshPhysicalMaterial({ color: 0x1c2350, roughness: .2, clearcoat: 1, transparent: true, opacity: .92 }));
    const lab = labelPlane(3.6, 0.78, 1000, 216, (ctx, w, h) => { ctx.beginPath(); ctx.arc(100, h / 2, 62, 0, 7); ctx.fillStyle = col; ctx.fill();
      ctx.fillStyle = '#a9b2d6'; ctx.font = '44px IDBo'; ctx.fillText(u, 200, 82); ctx.fillStyle = '#fff'; ctx.font = '58px IDBo'; ctx.fillText(c, 200, 160); }, { toneMapped: false });
    lab.position.z = 0.07; gg.add(b, lab); return gg; });
  const g = grp(t1, t2, ...cm);
  return {
    g, jer: true, caps: [{ t0: 1.9, t1: 4, text: 'Comment your idea ↓', size: 82, y: 1400, g: ['idea', '↓'] }],
    update(t) {
      t1.scale.setScalar(popS(t, 0, .4)); t2.scale.setScalar(popS(t, .2, .4));
      t1.rotation.y = Math.sin(t * 1.5) * .08; t2.rotation.y = Math.sin(t * 1.5 + .5) * .08;
      cm.forEach((c, i) => { const p = eOut(prog(t, .6 + i * .3, 1.2 + i * .3)); c.visible = p > 0; c.position.set(-0.45, lerp(-1, 3.05 - i * 0.92, p), 0.6); c.rotation.y = Math.sin(t * 2 + i) * .06; });
      J.scale.setScalar(0.6); J.position.set(1.75, 0, 1.6); J.rotation.y = -0.4;
      J.pose({ expr: 'happy', armR: 2.5 + Math.sin(t * 11) * .3, armL: .2, look: -.5 });
      ui.small.style.top = '1495px'; ui.small.textContent = 'Purely hypothetical · for entertainment'; ui.small.style.opacity = clamp((t - 2.2) / .4);
      const k = eInOut(t / 4);
      setCam(V(lerp(-0.5, 0.3, k), 2.8, lerp(13.0, 12.0, k)), V(0, 2.6, 0));
    }
  };
});

// =================== RENDER ===================
window.renderAt = (T) => {
  ui.black.style.opacity = 0; ui.nosig.style.opacity = 0; ui.scan.style.opacity = 0; ui.small.textContent = '';
  const cv = document.querySelector('canvas'); cv.style.transform = ''; cv.style.filter = '';
  flash.intensity = 0; J.visible = false;
  let caps = [];
  for (const s of S) {
    const on = T >= s.start && T < s.start + s.dur || (s === S[S.length - 1] && T >= s.start);
    s.g.visible = on;
    if (on) { if (s.jer) J.visible = true; s.update(T - s.start); caps = s.caps.map(c => ({ ...c, t0: c.t0 + s.start, t1: c.t1 + s.start })); }
  }
  bgSyms.children.forEach(m => { m.rotation.y = T * m.userData.sp + m.userData.ph; m.position.y += 0; });
  renderCaptions(caps, T);
  ui.fill.style.width = (clamp(T / TOTAL) * 100) + '%';
  draw();
};
window.TOTAL = TOTAL;
window.READY = true;
