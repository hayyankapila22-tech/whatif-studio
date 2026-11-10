// usage: node render.cjs stills t1 t2 ...   |   node render.cjs video start end out.mp4
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const ROOT = __dirname;
const TYPES = { ".exr": "application/octet-stream", '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.otf': 'font/otf', '.ttf': 'font/ttf', '.png': 'image/png', '.jpg': 'image/jpeg', '.exr': 'application/octet-stream' };

(async () => {
  const [mode, ...args] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'error' || m.text().startsWith('[ep]')) console.log('PAGE:', m.text()); });
  page.on('pageerror', e => console.log('PAGEERR:', e.message));
  await page.route('http://app/**', route => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    if (!fs.existsSync(p)) return route.fulfill({ status: 404, body: 'nf' });
    route.fulfill({ status: 200, contentType: TYPES[path.extname(p)] || 'application/octet-stream', body: fs.readFileSync(p) });
  });
  await page.goto('http://app/index.html');
  await page.waitForFunction('window.READY === true', null, { timeout: 120000 });
  if (mode === 'spec') { fs.writeFileSync(path.join(ROOT, 'spec.json'), JSON.stringify(await page.evaluate(() => window.SPEC))); console.log('spec written'); }
  if (mode === 'stills') {
    for (const t of args) {
      const t0 = Date.now();
      await page.evaluate(t => window.renderAt(t), +t);
      await page.screenshot({ path: path.join(ROOT, `still_${t}.jpg`), type: 'jpeg', quality: 90 });
      console.log('still', t, Date.now() - t0, 'ms');
    }
  } else if (mode === 'video') {
    const [start, end, out] = [+args[0], +args[1], args[2]];
    const FPS = 30, n0 = Math.round(start * FPS), n1 = Math.round(end * FPS);
    const tmp = out.replace(/\.mp4$/, '.part.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
    const tStart = Date.now();
    for (let i = n0; i < n1; i++) {
      await page.evaluate(t => window.renderAt(t), i / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if ((i - n0) % 60 === 0) console.log(out, i, ((Date.now() - tStart) / (i - n0 + 1)).toFixed(0), 'ms/frame');
    }
    ff.stdin.end();
    const code = await new Promise(r => ff.on('close', r));
    if (code === 0) fs.renameSync(tmp, out);
    console.log('done', out, code);
  }
  await browser.close();
})();
