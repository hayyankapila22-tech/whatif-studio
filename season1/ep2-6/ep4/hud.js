// v2 HUD: slot-machine intro, live rolling counter, stage helpers. Reused by every episode.
import { clamp, prog, eOut, eBack, eInOut } from './engine.js';

const $ = id => document.getElementById(id);
export function setTitle(title, ep) { const sp = document.querySelectorAll('#bar span'); sp[0].textContent = title; sp[1].textContent = ep; }

// ---------- slot machine intro ----------
// items: list of strings that spin past; the LAST one is where it lands.
let reelBuilt = false;
export function intro(t, items, dur = 3.0) {
  const el = $('intro');
  if (t > dur + 0.3) { el.style.opacity = 0; return false; }
  if (!reelBuilt) { $('reelIn').innerHTML = items.map(s => `<div class="ri" style="font-size:${Math.min(84, Math.floor(1520 / s.length))}px">${s}</div>`).join(''); reelBuilt = true; }
  const n = items.length - 1;
  // spin: fast, then decelerate and land at 2.1s with an overshoot
  const p = clamp(t / 2.1);
  const pos = n * (1 - Math.pow(1 - p, 3.2));
  const land = t > 2.1 ? Math.sin((t - 2.1) * 22) * Math.exp(-(t - 2.1) * 9) * 0.12 : 0;
  $('reelIn').style.transform = `translateY(${-(pos - land) * 220}px)`;
  const speed = t < 2.1 ? 3.2 * n * Math.pow(1 - p, 2.2) / 2.1 : 0; // items per second
  $('reelIn').style.filter = `blur(${Math.min(10, speed * 0.6)}px)`;
  const ws = eBack(prog(t, 0, 0.35));
  $('iWhat').style.transform = `scale(${0.6 + 0.4 * ws})`;
  const landPop = t > 2.1 ? 1 + 0.1 * Math.exp(-(t - 2.1) * 6) : 1;
  $('reel').style.transform = `scale(${(0.6 + 0.4 * eBack(prog(t, 0.1, 0.45))) * landPop})`;
  $('reel').style.boxShadow = t > 2.1 ? `0 0 ${50 + 120 * Math.exp(-(t - 2.1) * 4)}px rgba(255,196,68,.9), inset 0 0 40px rgba(0,0,0,.8)` : '';
  el.style.opacity = 1 - prog(t, dur, dur + 0.3);
  $('flash').style.opacity = t > 2.1 && t < 2.35 ? 0.55 * (1 - (t - 2.1) / 0.25) : 0;
  return true;
}
export function introTicks(items) { // times the reel passes each item (for tick SFX)
  const n = items.length - 1, out = [];
  for (let k = 1; k <= n; k++) { const p = 1 - Math.pow(1 - k / n, 1 / 3.2); out.push(p * 2.1); }
  return out;
}

// ---------- live counter ----------
const sevCol = ['#5dff9e', '#b6ff5d', '#ffe45d', '#ffb02e', '#ff7a3d', '#ff3b55'];
export function counter(t, { on, valueAt, fmt, label, sub = '', sev = 0, shake = 0 }) {
  const el = $('counter');
  el.style.opacity = on ? 1 : 0;
  if (!on) return;
  const s = fmt(valueAt(t)), s1 = fmt(valueAt(t - 1 / 30)), s2 = fmt(valueAt(t - 2 / 30));
  const col = sevCol[Math.max(0, Math.min(5, Math.round(sev)))];
  let html = '';
  let diffs = 0; if (s1.length === s.length) for (let i = 0; i < s.length; i++) if (s1[i] !== s[i]) diffs++;
  const roll = diffs <= 2;
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    let off = 0;
    if (roll && /[0-9]/.test(ch)) { if (s1.length === s.length && s1[i] !== ch) off = 0.55; else if (s2.length === s.length && s2[i] !== ch) off = 0.2; }
    html += `<span style="transform:translateY(${off * 100}%);opacity:${1 - off * 0.8};color:${col};text-shadow:0 0 28px ${col}88">${ch === ' ' ? '&nbsp;' : ch}</span>`;
  }
  const v = document.getElementById('cVal'); v.style.fontSize = Math.min(132, Math.floor(1450 / s.length)) + 'px';
  if (v.innerHTML !== html) v.innerHTML = html;
  $('cLabel').textContent = label; $('cSub').textContent = sub;
  const sx = shake ? (Math.sin(t * 97) * shake * 14) : 0, sy = shake ? (Math.cos(t * 83) * shake * 10) : 0;
  el.style.transform = `translateX(calc(-50% + ${sx}px)) translateY(${sy}px)`;
}

// ---------- stages ----------
// stages: [{t, ...}] sorted; returns {i, lt, s} for the current stage
export function stageAt(stages, t) { let i = 0; for (let k = 0; k < stages.length; k++) if (t >= stages[k].t) i = k; return { i, lt: t - stages[i].t, s: stages[i] }; }
// piecewise-linear interpolation over keyframes [[t, v], ...]
export function keyframes(kf, t, ease = x => x) {
  if (t <= kf[0][0]) return kf[0][1];
  for (let k = 1; k < kf.length; k++) if (t <= kf[k][0]) { const [t0, v0] = kf[k - 1], [t1, v1] = kf[k]; return v0 + (v1 - v0) * ease((t - t0) / (t1 - t0)); }
  return kf[kf.length - 1][1];
}
export function flash(a) { $('flash').style.opacity = a; }
