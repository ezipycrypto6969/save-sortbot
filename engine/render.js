// node render.js <timeline.json> <out.mp4> [stillsDir]  — renders the stage frame by frame at 30 fps into an H.264 MP4.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
(async () => {
  const [tlPath, out, stills] = process.argv.slice(2);
  const tl = JSON.parse(fs.readFileSync(tlPath, 'utf8'));
  const fps = 30, n = Math.round(tl.dur * fps);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.join(__dirname, 'stage.html'));
  await p.evaluate(t => window.load(t), tl);
  await p.waitForTimeout(200);
  if (stills) {  // one still per scene for a quick visual check
    for (const [i, s] of tl.scenes.entries()) {
      await p.evaluate(t => window.render(t), Math.min(s.end - 0.05, s.start + (s.end - s.start) * 0.8));
      await p.screenshot({ path: path.join(stills, `scene-${i}.png`) });
    }
  }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.render(t), i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
  if (errs.length) { console.error('stage errors:', errs); process.exit(1); }
})();
