// Season 2 look test: Jeremy's street, POV, wide, reaction, aerial
import { THREE, scene, camera, draw, setSun, aimSun, makeJeremy, renderCaptions, clamp, lerp, loadFont } from './engine.js';
import { buildStreet, makePOVHands } from './street.js';
import { makeJeremy2 } from './jeremy2.js';
import { setTitle, counter } from './hud.js';
await document.fonts.load('80px IDB'); await document.fonts.load('80px IDBo'); await loadFont();
setTitle('WHAT IF YOUR HAIR KEPT DOUBLING?', 'EP. 7');
setSun(34, 215, 3.5, 1.2);
const street = buildStreet(scene);
const J = makeJeremy2(); scene.add(J);
const hands = makePOVHands(); camera.add(hands); scene.add(camera);
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const pov = document.getElementById('pov');
window.renderAt = (T) => {
  hands.visible = false; J.visible = true; pov.style.opacity = 0;
  const shot = Math.floor(T) % 4;
  if (shot === 0) { // POV walk toward the café
    J.visible = false; hands.visible = true; pov.style.opacity = 1;
    const x = 2 + T * 1.4, bob = Math.sin(T * 9) * .035;
    camera.position.set(x, 1.62 + bob, 5.4); camera.lookAt(x + 8, 1.35, 5.0); hands.right.rotation.z = Math.sin(T * 9) * .03;
  }
  if (shot === 1) { J.position.set(6, .18, 5.6); J.rotation.y = Math.PI / 2; J.scale.setScalar(.75); J.pose({ expr: 'happy', look: .3, armL: .2, armR: .2 }); camera.position.set(12, 2.2, 1.2); camera.lookAt(6.5, 1.4, 6); }
  if (shot === 2) { J.position.set(6, .18, 6.2); J.rotation.y = Math.PI - 0.35; J.scale.setScalar(.75); J.pose({ expr: 'shocked', armL: 2.4, armR: 2.4, look: -.4, sweatK: .3 }); camera.position.set(7.0, 1.5, 3.4); camera.lookAt(6.0, 1.45, 6.2); }
  if (shot === 3) { J.position.set(6, .18, 5.6); J.scale.setScalar(.75); camera.position.set(2, 42, -6); camera.lookAt(12, 0, 5); }
  aimSun(V(camera.position.x, 0, 4));
  counter(T, { on: true, valueAt: () => 0.1 * Math.pow(2, Math.floor(T * 2)), fmt: v => (v < 1000 ? v.toFixed(1) + ' m' : Math.round(v).toLocaleString('en-US') + ' m'), label: 'MINUTE ' + Math.floor(T * 2), sub: 'Jeremy’s hair length', sev: shot + 1 });
  renderCaptions([{ t0: Math.floor(T), t1: Math.floor(T) + .9, text: ['Jeremy grabs his morning coffee…', 'Minute 1: his hair hits his shoulders.', 'Minute 4: it drags on the floor.', 'Minute 10: it’s 100 m long.'][shot], y: 1200, size: 70, g: ['coffee', 'shoulders', 'floor', '100', 'm'] }], T);
  document.getElementById('fill').style.width = (T / 4 * 100) + '%';
  draw();
};
window.READY = true;
