// Jeremy v2 — higher-detail, same pose() API as v1.
import { THREE, RoundedBoxGeometry } from './engine.js';

function mesh(geo, mat, cast = true) { const m = new THREE.Mesh(geo, mat); m.castShadow = cast; m.receiveShadow = true; return m; }
export function makeJeremy2() {
  const skin = new THREE.MeshPhysicalMaterial({ color: 0xf1b58e, roughness: .48, sheen: .35, sheenColor: 0xffb7a0, clearcoat: .05 });
  const blushM = new THREE.MeshStandardMaterial({ color: 0xff8c8c, roughness: .6, transparent: true, opacity: .35 });
  const hoodie = new THREE.MeshPhysicalMaterial({ color: 0x2f6dff, roughness: .82, sheen: .6, sheenColor: 0x9ab8ff });
  const hoodieDark = new THREE.MeshStandardMaterial({ color: 0x2457cc, roughness: .85 });
  const jeans = new THREE.MeshStandardMaterial({ color: 0x2b3a5e, roughness: .8 });
  const hairM = new THREE.MeshPhysicalMaterial({ color: 0x3a2417, roughness: .45, clearcoat: .4, clearcoatRoughness: .5 });
  const eyeW = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .1, clearcoat: 1 });
  const irisM = new THREE.MeshStandardMaterial({ color: 0x6b3f1d, roughness: .3 });
  const pupilM = new THREE.MeshStandardMaterial({ color: 0x0b0b10, roughness: .1 });
  const mouthM = new THREE.MeshStandardMaterial({ color: 0x5e1422, roughness: .5 });
  const teethM = new THREE.MeshStandardMaterial({ color: 0xfaf8f2, roughness: .3 });
  const shoeM = new THREE.MeshStandardMaterial({ color: 0xff3d6e, roughness: .5 });
  const soleM = new THREE.MeshStandardMaterial({ color: 0xf6f6f6, roughness: .6 });
  const cordM = new THREE.MeshStandardMaterial({ color: 0xf2f2f2, roughness: .6 });

  const J = new THREE.Group(); const body = new THREE.Group(); J.add(body);
  // legs + sneakers
  for (const s of [-1, 1]) {
    const leg = mesh(new THREE.CapsuleGeometry(.15, .44, 12, 24), jeans); leg.position.set(s * .17, .45, 0); body.add(leg);
    const cuff = mesh(new THREE.CylinderGeometry(.165, .165, .07, 24), jeans); cuff.position.set(s * .17, .2, 0); body.add(cuff);
    const sole = mesh(new RoundedBoxGeometry(.32, .07, .5, 4, .03), soleM); sole.position.set(s * .17, .035, .07); body.add(sole);
    const upper = mesh(new RoundedBoxGeometry(.3, .16, .46, 5, .08), shoeM); upper.position.set(s * .17, .13, .06); body.add(upper);
    const toe = mesh(new THREE.SphereGeometry(.15, 24, 16, 0, 6.3, 0, 1.6), soleM); toe.scale.set(1, .5, 1); toe.position.set(s * .17, .07, .2); body.add(toe);
  }
  // torso: hoodie with pocket, hood, drawstrings, hem
  const torso = mesh(new THREE.CapsuleGeometry(.44, .52, 16, 32), hoodie); torso.position.y = 1.17; torso.scale.set(1, 1, .82); body.add(torso);
  const hem = mesh(new THREE.TorusGeometry(.4, .06, 12, 40), hoodieDark); hem.rotation.x = Math.PI / 2; hem.scale.set(1, .82, 1); hem.position.y = .83; body.add(hem);
  const pocket = mesh(new RoundedBoxGeometry(.5, .2, .06, 4, .04), hoodieDark); pocket.position.set(0, 1.0, .34); pocket.rotation.x = -.18; body.add(pocket);
  const hood = mesh(new THREE.TorusGeometry(.24, .1, 16, 40), hoodieDark); hood.rotation.x = Math.PI / 2 + .35; hood.position.set(0, 1.66, -.08); body.add(hood);
  for (const s of [-1, 1]) { const c = mesh(new THREE.CapsuleGeometry(.015, .2, 4, 8), cordM); c.position.set(s * .08, 1.48, .35); c.rotation.x = -.15; body.add(c); const tip = mesh(new THREE.CylinderGeometry(.022, .022, .05, 8), cordM); tip.position.set(s * .08, 1.35, .37); body.add(tip); }
  const neck = mesh(new THREE.CylinderGeometry(.12, .14, .2, 24), skin); neck.position.y = 1.74; body.add(neck);
  // arms: sleeve + cuff + hand with thumb
  const arms = [];
  for (const s of [-1, 1]) {
    const piv = new THREE.Group(); piv.position.set(s * .47, 1.5, 0); body.add(piv);
    const arm = mesh(new THREE.CapsuleGeometry(.13, .4, 12, 24), hoodie); arm.position.y = -.3; piv.add(arm);
    const cuffA = mesh(new THREE.CylinderGeometry(.115, .115, .08, 20), hoodieDark); cuffA.position.y = -.56; piv.add(cuffA);
    const hand = mesh(new THREE.SphereGeometry(.12, 32, 24), skin); hand.scale.set(1, 1.15, .8); hand.position.y = -.68; piv.add(hand);
    const thumb = mesh(new THREE.CapsuleGeometry(.035, .06, 6, 12), skin); thumb.position.set(-s * .09, -.64, .05); thumb.rotation.z = s * .7; piv.add(thumb);
    piv.rotation.z = s * .18; arms.push(piv);
  }
  // head
  const head = new THREE.Group(); head.position.y = 2.12; body.add(head);
  const skull = mesh(new THREE.SphereGeometry(.5, 64, 48), skin); skull.scale.set(1, .97, .94); head.add(skull);
  const jaw = mesh(new THREE.SphereGeometry(.4, 48, 32), skin); jaw.scale.set(1, .7, .9); jaw.position.set(0, -.18, .06); head.add(jaw);
  for (const s of [-1, 1]) { const ear = mesh(new THREE.SphereGeometry(.11, 24, 16), skin); ear.position.set(s * .48, 0, -.02); ear.scale.set(.55, 1, .8); head.add(ear);
    const bl = mesh(new THREE.SphereGeometry(.08, 20, 12), blushM, false); bl.scale.set(1, .6, .3); bl.position.set(s * .28, -.12, .38); head.add(bl); }
  const nose = mesh(new THREE.SphereGeometry(.07, 24, 16), skin); nose.scale.set(.9, 1, 1.15); nose.position.set(0, -.05, .48); head.add(nose);
  // hair: base cap + clumps for volume
  const cap = mesh(new THREE.SphereGeometry(.53, 64, 32, 0, Math.PI * 2, 0, Math.PI * 0.45), hairM); cap.rotation.x = -.3; cap.position.y = .03; head.add(cap);
  [[.1, .43, .26, 1.5, .6, 1], [-.18, .42, .2, 1.2, .55, 1], [.3, .32, .18, .9, .7, .9], [-.36, .3, .1, .8, .7, 1], [.0, .5, .0, 1.4, .5, 1.3], [.22, .45, -.15, 1.1, .6, 1], [-.22, .45, -.18, 1.1, .6, 1]].forEach(([x, y, z, sx, sy, sz]) => {
    const c = mesh(new THREE.SphereGeometry(.17, 24, 16), hairM); c.position.set(x, y, z); c.scale.set(sx, sy, sz); head.add(c); });
  // eyes with iris, pupil, highlight and eyelids
  const eyes = [], pupils = [], lids = [], brows = [];
  for (const s of [-1, 1]) {
    const e = new THREE.Group(); e.position.set(s * .17, .07, .39); head.add(e);
    const w = mesh(new THREE.SphereGeometry(.12, 32, 24), eyeW, false); w.scale.z = .62; e.add(w);
    const p = new THREE.Group(); p.position.z = .065; e.add(p);
    const iris = mesh(new THREE.SphereGeometry(.072, 24, 16), irisM, false); iris.scale.z = .4; p.add(iris);
    const pup = mesh(new THREE.SphereGeometry(.04, 20, 12), pupilM, false); pup.scale.z = .4; pup.position.z = .012; p.add(pup);
    const hl = mesh(new THREE.SphereGeometry(.018, 10, 8), eyeW, false); hl.position.set(-.025, .03, .03); p.add(hl);
    const lid = mesh(new THREE.SphereGeometry(.128, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), skin, false); lid.scale.z = .66; lid.rotation.x = -.2; e.add(lid);
    eyes.push(e); pupils.push(p); lids.push(lid);
    const b = mesh(new THREE.TorusGeometry(.1, .025, 8, 20, Math.PI * .8), hairM, false); b.rotation.z = Math.PI * .1; b.position.set(s * .17, .24, .44); head.add(b); brows.push(b);
  }
  // mouths
  const smile = new THREE.Group(); { const lip = mesh(new THREE.TorusGeometry(.12, .026, 10, 32, Math.PI), mouthM, false); lip.rotation.z = Math.PI; const fill = mesh(new THREE.CircleGeometry(.11, 32, Math.PI, Math.PI), mouthM, false); const teeth = mesh(new THREE.PlaneGeometry(.16, .035), teethM, false); teeth.position.set(0, -.02, .005); smile.add(lip, fill, teeth); }
  smile.position.set(0, -.2, .44); head.add(smile);
  const oMouth = new THREE.Group(); { const o = mesh(new THREE.SphereGeometry(.085, 24, 16), mouthM, false); o.scale.set(.9, 1.25, .5); const t = mesh(new THREE.SphereGeometry(.05, 16, 8), new THREE.MeshStandardMaterial({ color: 0xd2566a }), false); t.scale.set(1, .5, .4); t.position.set(0, -.06, .02); oMouth.add(o, t); }
  oMouth.position.set(0, -.25, .43); head.add(oMouth);
  const flat = mesh(new THREE.CapsuleGeometry(.024, .15, 4, 10), mouthM, false); flat.rotation.z = Math.PI / 2; flat.position.set(0, -.22, .45); head.add(flat);
  const sweat = mesh(new THREE.SphereGeometry(.07, 20, 14), new THREE.MeshPhysicalMaterial({ color: 0x9fdcff, roughness: .02, clearcoat: 1, transmission: 0, emissive: 0x2a7fff, emissiveIntensity: .25 }), false); sweat.scale.y = 1.4; head.add(sweat);

  J.pose = ({ expr = 'happy', look = 0, armL = 0.18, armR = 0.18, bob = 0, tilt = 0, sweatK = 0, blink = false } = {}) => {
    body.position.y = bob; head.rotation.z = tilt; head.rotation.y = look * 0.35;
    arms[0].rotation.z = -armL; arms[1].rotation.z = armR;
    const shock = expr === 'shocked' || expr === 'panic';
    smile.visible = expr === 'happy'; oMouth.visible = shock; flat.visible = ['confused', 'sleep', 'worried'].includes(expr);
    flat.rotation.z = Math.PI / 2 + (expr === 'confused' ? 0.25 : 0);
    const closed = blink || expr === 'sleep';
    eyes.forEach(e => e.scale.setScalar(shock ? 1.15 : 1));
    lids.forEach(l => { l.rotation.x = closed ? 1.45 : shock ? -.75 : expr === 'worried' ? .15 : -.2; });
    pupils.forEach(p => { p.scale.setScalar(shock ? .75 : 1); p.position.x = look * .035; p.visible = !closed; });
    const by = { happy: .25, shocked: .32, panic: .32, confused: .24, sleep: .22, worried: .26 }[expr];
    brows.forEach((b, i) => { const s = i ? 1 : -1; b.position.y = by; b.rotation.z = Math.PI * .1 + (expr === 'worried' || expr === 'panic' ? s * -.3 : expr === 'confused' ? (i ? .35 : -.05) : 0); if (expr === 'confused' && i) b.position.y = by + .05; });
    sweat.visible = sweatK > .01; sweat.position.set(.44, .2 - (sweatK % 1) * .35, .26);
  };
  J.pose();
  return J;
}
